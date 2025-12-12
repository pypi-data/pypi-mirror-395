"""
All-Reduce Communication for Tensor Parallelism

This module implements distributed all-reduce operations for combining
partial results from tensor-sharded layers across multiple nodes.

Algorithms:
1. Naive All-Reduce: Each node sends to all others (O(N²) messages)
2. Ring All-Reduce: Efficient ring topology (O(N) messages)
3. Tree All-Reduce: Hierarchical reduction (O(log N) latency)

For NeuroShard, we use Ring All-Reduce as the default due to its
balance of efficiency and simplicity.
"""

import torch
import threading
import queue
import time
import logging
from typing import Dict, List, Optional, Tuple, Callable
from dataclasses import dataclass
from enum import Enum
import hashlib

logger = logging.getLogger(__name__)


class AllReduceOp(Enum):
    """Reduction operations."""
    SUM = "sum"
    MEAN = "mean"
    MAX = "max"
    MIN = "min"


@dataclass
class AllReduceRequest:
    """Request to participate in an all-reduce operation."""
    operation_id: str
    layer_id: int
    shard_id: int
    total_shards: int
    tensor_data: bytes  # Serialized tensor
    op: AllReduceOp = AllReduceOp.SUM
    timestamp: float = 0.0


@dataclass
class AllReduceResult:
    """Result of an all-reduce operation."""
    operation_id: str
    success: bool
    reduced_tensor: Optional[torch.Tensor] = None
    error: Optional[str] = None
    latency_ms: float = 0.0


class RingAllReduce:
    """
    Ring All-Reduce implementation.
    
    In ring all-reduce:
    1. Nodes are arranged in a logical ring
    2. Each node sends to next, receives from previous
    3. After N-1 steps, all nodes have the reduced result
    
    This is bandwidth-optimal: each node sends/receives exactly
    (N-1)/N of the data in total.
    """
    
    def __init__(self, 
                 my_shard_id: int,
                 total_shards: int,
                 peer_addresses: Dict[int, str]):
        """
        Initialize ring all-reduce.
        
        Args:
            my_shard_id: Our shard ID (position in ring)
            total_shards: Total number of shards
            peer_addresses: Map of shard_id -> grpc_address
        """
        self.my_shard_id = my_shard_id
        self.total_shards = total_shards
        self.peer_addresses = peer_addresses
        
        # Ring topology
        self.next_shard = (my_shard_id + 1) % total_shards
        self.prev_shard = (my_shard_id - 1) % total_shards
        
        # Pending operations
        self.pending_ops: Dict[str, Dict] = {}
        self.lock = threading.Lock()
        
        # Buffers for partial results
        self.recv_buffers: Dict[str, List[torch.Tensor]] = {}
        
        logger.info(f"RingAllReduce initialized: shard {my_shard_id}/{total_shards}, "
                   f"ring: {self.prev_shard} <- {my_shard_id} -> {self.next_shard}")
    
    def _generate_op_id(self, layer_id: int, step: int) -> str:
        """Generate unique operation ID."""
        return f"allreduce_L{layer_id}_S{step}_{int(time.time()*1000)}"
    
    async def reduce_scatter(self, 
                             tensor: torch.Tensor, 
                             layer_id: int,
                             op: AllReduceOp = AllReduceOp.SUM) -> torch.Tensor:
        """
        Reduce-scatter phase of ring all-reduce.
        
        Splits tensor into chunks, each node reduces one chunk.
        After N-1 steps, each node has the fully reduced version of one chunk.
        """
        # Split tensor into N chunks
        chunks = torch.chunk(tensor, self.total_shards, dim=-1)
        chunks = list(chunks)  # Make mutable
        
        # N-1 iterations
        for step in range(self.total_shards - 1):
            # Chunk index we're sending (rotates each step)
            send_idx = (self.my_shard_id - step) % self.total_shards
            recv_idx = (self.my_shard_id - step - 1) % self.total_shards
            
            # Send our chunk to next node
            send_chunk = chunks[send_idx]
            
            # Receive chunk from previous node (simulated for now)
            # In real implementation, this would be async gRPC
            recv_chunk = await self._exchange_chunk(
                send_chunk, 
                layer_id, 
                step,
                send_idx
            )
            
            # Reduce received chunk with our chunk
            if recv_chunk is not None:
                if op == AllReduceOp.SUM:
                    chunks[recv_idx] = chunks[recv_idx] + recv_chunk
                elif op == AllReduceOp.MEAN:
                    chunks[recv_idx] = (chunks[recv_idx] + recv_chunk) / 2
                elif op == AllReduceOp.MAX:
                    chunks[recv_idx] = torch.max(chunks[recv_idx], recv_chunk)
                elif op == AllReduceOp.MIN:
                    chunks[recv_idx] = torch.min(chunks[recv_idx], recv_chunk)
        
        return chunks
    
    async def all_gather(self, 
                         chunks: List[torch.Tensor],
                         layer_id: int) -> torch.Tensor:
        """
        All-gather phase of ring all-reduce.
        
        After reduce-scatter, each node has one fully reduced chunk.
        All-gather distributes these chunks to all nodes.
        """
        # N-1 iterations
        for step in range(self.total_shards - 1):
            # Chunk index we're sending
            send_idx = (self.my_shard_id - step + 1) % self.total_shards
            recv_idx = (self.my_shard_id - step) % self.total_shards
            
            # Send our reduced chunk to next node
            send_chunk = chunks[send_idx]
            
            # Receive reduced chunk from previous node
            recv_chunk = await self._exchange_chunk(
                send_chunk,
                layer_id,
                step + self.total_shards,  # Offset step to avoid collision
                send_idx
            )
            
            # Replace our chunk with received (already reduced)
            if recv_chunk is not None:
                chunks[recv_idx] = recv_chunk
        
        # Concatenate all chunks
        return torch.cat(chunks, dim=-1)
    
    async def all_reduce(self,
                         tensor: torch.Tensor,
                         layer_id: int,
                         op: AllReduceOp = AllReduceOp.SUM) -> torch.Tensor:
        """
        Full ring all-reduce operation.
        
        Combines reduce-scatter and all-gather phases.
        
        Args:
            tensor: Local tensor to reduce
            layer_id: Layer ID (for operation tracking)
            op: Reduction operation
        
        Returns:
            Fully reduced tensor (same on all nodes)
        """
        start_time = time.time()
        
        # Phase 1: Reduce-scatter
        chunks = await self.reduce_scatter(tensor, layer_id, op)
        
        # Phase 2: All-gather
        result = await self.all_gather(chunks, layer_id)
        
        latency_ms = (time.time() - start_time) * 1000
        logger.debug(f"All-reduce completed for layer {layer_id} in {latency_ms:.2f}ms")
        
        return result
    
    async def _exchange_chunk(self, 
                              send_chunk: torch.Tensor,
                              layer_id: int,
                              step: int,
                              chunk_idx: int) -> Optional[torch.Tensor]:
        """
        Exchange a chunk with ring neighbors.
        
        Uses gRPC to:
        1. Serialize send_chunk
        2. Send to next_shard via gRPC
        3. Receive from prev_shard via gRPC (in response)
        4. Deserialize and return
        """
        if self.total_shards == 1:
            return None  # Single node, no exchange needed
        
        # Check if we have a gRPC client
        if not hasattr(self, '_grpc_client') or self._grpc_client is None:
            logger.debug(f"No gRPC client for tensor exchange, using local-only mode")
            return None
        
        try:
            # Generate operation ID
            op_id = self._generate_op_id(layer_id, step)
            
            # Use the gRPC client for actual exchange
            recv_chunk = self._grpc_client.exchange_chunk(
                send_chunk=send_chunk,
                layer_id=layer_id,
                step=step,
                chunk_idx=chunk_idx,
                operation_id=op_id,
                timeout_seconds=5.0
            )
            
            return recv_chunk
            
        except Exception as e:
            logger.error(f"Chunk exchange failed: {e}")
            return None
    
    def set_grpc_client(self, client):
        """Set the gRPC client for tensor exchange."""
        self._grpc_client = client
        logger.info(f"RingAllReduce gRPC client configured")


class AllReduceCoordinator:
    """
    High-level coordinator for all-reduce operations.
    
    Manages multiple concurrent all-reduce operations and
    handles fault tolerance.
    """
    
    def __init__(self,
                 my_shard_id: int,
                 total_shards: int,
                 peer_addresses: Dict[int, str] = None,
                 timeout_ms: float = 5000):
        """
        Initialize all-reduce coordinator.
        
        Args:
            my_shard_id: Our shard ID
            total_shards: Total shards
            peer_addresses: Map of shard_id -> address
            timeout_ms: Timeout for operations
        """
        self.my_shard_id = my_shard_id
        self.total_shards = total_shards
        self.peer_addresses = peer_addresses or {}
        self.timeout_ms = timeout_ms
        
        # Ring all-reduce implementation
        self.ring = RingAllReduce(my_shard_id, total_shards, self.peer_addresses)
        
        # Operation tracking
        self.active_ops: Dict[str, threading.Event] = {}
        self.results: Dict[str, AllReduceResult] = {}
        self.lock = threading.Lock()
        
        # Statistics
        self.stats = {
            "total_ops": 0,
            "successful_ops": 0,
            "failed_ops": 0,
            "total_latency_ms": 0.0
        }
    
    def update_peers(self, peer_addresses: Dict[int, str]):
        """Update peer addresses (e.g., after peer discovery)."""
        self.peer_addresses = peer_addresses
        self.ring.peer_addresses = peer_addresses
    
    async def all_reduce(self,
                         tensor: torch.Tensor,
                         layer_id: int,
                         op: AllReduceOp = AllReduceOp.SUM,
                         operation_id: str = None) -> AllReduceResult:
        """
        Perform all-reduce operation.
        
        Args:
            tensor: Tensor to reduce
            layer_id: Layer ID
            op: Reduction operation
            operation_id: Optional custom operation ID
        
        Returns:
            AllReduceResult with reduced tensor or error
        """
        op_id = operation_id or f"ar_{layer_id}_{int(time.time()*1000)}"
        start_time = time.time()
        
        try:
            with self.lock:
                self.stats["total_ops"] += 1
            
            # Perform ring all-reduce
            if self.total_shards == 1:
                # Single shard - no reduction needed
                reduced = tensor
            else:
                reduced = await self.ring.all_reduce(tensor, layer_id, op)
            
            latency_ms = (time.time() - start_time) * 1000
            
            with self.lock:
                self.stats["successful_ops"] += 1
                self.stats["total_latency_ms"] += latency_ms
            
            return AllReduceResult(
                operation_id=op_id,
                success=True,
                reduced_tensor=reduced,
                latency_ms=latency_ms
            )
            
        except Exception as e:
            latency_ms = (time.time() - start_time) * 1000
            
            with self.lock:
                self.stats["failed_ops"] += 1
            
            logger.error(f"All-reduce failed for layer {layer_id}: {e}")
            
            return AllReduceResult(
                operation_id=op_id,
                success=False,
                error=str(e),
                latency_ms=latency_ms
            )
    
    def get_stats(self) -> Dict:
        """Get all-reduce statistics."""
        with self.lock:
            avg_latency = (
                self.stats["total_latency_ms"] / self.stats["successful_ops"]
                if self.stats["successful_ops"] > 0 else 0
            )
            return {
                **self.stats,
                "avg_latency_ms": avg_latency,
                "success_rate": (
                    self.stats["successful_ops"] / self.stats["total_ops"]
                    if self.stats["total_ops"] > 0 else 1.0
                )
            }


# Synchronous wrapper for use in forward pass
def sync_all_reduce(tensor: torch.Tensor,
                    coordinator: AllReduceCoordinator,
                    layer_id: int,
                    op: AllReduceOp = AllReduceOp.SUM) -> torch.Tensor:
    """
    Synchronous all-reduce for use in model forward pass.
    
    This is a blocking call that waits for all shards to complete.
    """
    import asyncio
    
    # Get or create event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    # Run async all-reduce
    result = loop.run_until_complete(
        coordinator.all_reduce(tensor, layer_id, op)
    )
    
    if result.success:
        return result.reduced_tensor
    else:
        raise RuntimeError(f"All-reduce failed: {result.error}")

