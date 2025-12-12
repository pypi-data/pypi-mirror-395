"""
gRPC Implementation for Tensor Parallelism

Implements the actual network communication for:
- Ring all-reduce tensor exchange
- Partial result aggregation
- Tensor shard peer discovery

This module bridges the allreduce.py algorithms with actual gRPC calls.
"""

import torch
import grpc
import logging
import time
import threading
import io
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from concurrent import futures

from protos import neuroshard_pb2
from protos import neuroshard_pb2_grpc
from neuroshard.core.network.connection_pool import get_channel
from neuroshard.core.training.allreduce import AllReduceOp

logger = logging.getLogger(__name__)


def serialize_tensor_for_grpc(tensor: torch.Tensor) -> Tuple[bytes, List[int], str]:
    """
    Serialize a tensor for gRPC transmission.
    
    Returns:
        (data_bytes, shape, dtype_str)
    """
    # Convert to contiguous if needed
    if not tensor.is_contiguous():
        tensor = tensor.contiguous()
    
    # Get shape and dtype
    shape = list(tensor.shape)
    dtype_str = str(tensor.dtype).replace('torch.', '')
    
    # Serialize to bytes
    buffer = io.BytesIO()
    torch.save(tensor, buffer)
    data_bytes = buffer.getvalue()
    
    return data_bytes, shape, dtype_str


def deserialize_tensor_from_grpc(data_bytes: bytes, shape: List[int], dtype_str: str) -> torch.Tensor:
    """
    Deserialize a tensor from gRPC transmission.
    """
    buffer = io.BytesIO(data_bytes)
    tensor = torch.load(buffer)
    
    # Verify shape matches
    if list(tensor.shape) != shape:
        logger.warning(f"Shape mismatch: expected {shape}, got {list(tensor.shape)}")
    
    return tensor


@dataclass
class TensorShardPeer:
    """Information about a tensor shard peer."""
    shard_id: int
    grpc_addr: str
    latency_ms: float = 0.0
    last_seen: float = 0.0


class TensorExchangeClient:
    """
    Client for tensor exchange operations.
    
    Used by RingAllReduce to exchange tensor chunks with peer shards.
    """
    
    def __init__(self, my_shard_id: int, total_shards: int):
        self.my_shard_id = my_shard_id
        self.total_shards = total_shards
        
        # Peer addresses: shard_id -> grpc_addr
        self.peer_addresses: Dict[int, str] = {}
        
        # Connection stats
        self.exchange_count = 0
        self.total_latency_ms = 0.0
        self.failed_exchanges = 0
        
        # Ring topology
        self.next_shard = (my_shard_id + 1) % total_shards
        self.prev_shard = (my_shard_id - 1) % total_shards
    
    def update_peers(self, peer_addresses: Dict[int, str]):
        """Update peer addresses."""
        self.peer_addresses = peer_addresses
        logger.debug(f"Updated tensor shard peers: {peer_addresses}")
    
    def exchange_chunk(
        self,
        send_chunk: torch.Tensor,
        layer_id: int,
        step: int,
        chunk_idx: int,
        operation_id: str,
        reduce_op: AllReduceOp = AllReduceOp.SUM,
        timeout_seconds: float = 5.0
    ) -> Optional[torch.Tensor]:
        """
        Exchange a tensor chunk with ring neighbors.
        
        Sends chunk to next_shard, receives from prev_shard.
        
        Args:
            send_chunk: Tensor to send
            layer_id: Layer being processed
            step: Ring all-reduce step
            chunk_idx: Chunk index
            operation_id: Unique operation ID
            reduce_op: Reduction operation
            timeout_seconds: RPC timeout
            
        Returns:
            Received tensor from prev_shard, or None on failure
        """
        if self.total_shards == 1:
            return None  # Single shard, no exchange needed
        
        # Get peer addresses
        next_addr = self.peer_addresses.get(self.next_shard)
        prev_addr = self.peer_addresses.get(self.prev_shard)
        
        if not next_addr or not prev_addr:
            logger.warning(f"Missing peer addresses: next={next_addr}, prev={prev_addr}")
            return None
        
        start_time = time.time()
        
        try:
            # Serialize tensor
            data_bytes, shape, dtype_str = serialize_tensor_for_grpc(send_chunk)
            
            # Create request
            request = neuroshard_pb2.TensorExchangeRequest(
                operation_id=operation_id,
                layer_id=layer_id,
                step=step,
                chunk_idx=chunk_idx,
                sender_shard_id=self.my_shard_id,
                total_shards=self.total_shards,
                tensor_data=data_bytes,
                tensor_shape=shape,
                dtype=dtype_str,
                reduce_op=reduce_op.value
            )
            
            # Send to next shard (they will respond with their chunk)
            channel = get_channel(next_addr)
            stub = neuroshard_pb2_grpc.NeuroShardServiceStub(channel)
            
            response = stub.TensorExchange(request, timeout=timeout_seconds)
            
            if not response.success:
                logger.warning(f"Tensor exchange failed: {response.error_message}")
                self.failed_exchanges += 1
                return None
            
            # Deserialize received tensor
            recv_tensor = deserialize_tensor_from_grpc(
                response.tensor_data,
                list(response.tensor_shape),
                dtype_str  # Assume same dtype
            )
            
            # Update stats
            latency_ms = (time.time() - start_time) * 1000
            self.exchange_count += 1
            self.total_latency_ms += latency_ms
            
            logger.debug(f"Tensor exchange completed: layer={layer_id}, step={step}, "
                        f"latency={latency_ms:.1f}ms")
            
            return recv_tensor
            
        except grpc.RpcError as e:
            logger.error(f"gRPC error in tensor exchange: {e}")
            self.failed_exchanges += 1
            return None
        except Exception as e:
            logger.error(f"Tensor exchange error: {e}")
            self.failed_exchanges += 1
            return None
    
    def get_stats(self) -> Dict:
        """Get exchange statistics."""
        return {
            "exchange_count": self.exchange_count,
            "failed_exchanges": self.failed_exchanges,
            "avg_latency_ms": (
                self.total_latency_ms / self.exchange_count 
                if self.exchange_count > 0 else 0
            ),
            "success_rate": (
                (self.exchange_count - self.failed_exchanges) / max(1, self.exchange_count)
            )
        }


class TensorExchangeServicer:
    """
    gRPC servicer mixin for tensor exchange operations.
    
    Mix this into the main NeuroShardServiceServicer.
    """
    
    def __init__(self):
        # Pending exchanges: operation_id -> received tensor
        self.pending_exchanges: Dict[str, torch.Tensor] = {}
        self.exchange_lock = threading.Lock()
        
        # My tensor shard info
        self.my_shard_id: int = 0
        self.total_shards: int = 1
        self.my_current_chunks: Dict[str, torch.Tensor] = {}
    
    def set_shard_info(self, shard_id: int, total_shards: int):
        """Set tensor shard information."""
        self.my_shard_id = shard_id
        self.total_shards = total_shards
    
    def set_current_chunk(self, operation_id: str, chunk_idx: int, chunk: torch.Tensor):
        """Set current chunk for exchange (called before receiving)."""
        key = f"{operation_id}:{chunk_idx}"
        self.my_current_chunks[key] = chunk
    
    def TensorExchange(self, request, context):
        """
        Handle tensor exchange request.
        
        This is called by the previous shard in the ring.
        We receive their chunk and respond with our chunk.
        """
        try:
            # Deserialize received tensor
            recv_tensor = deserialize_tensor_from_grpc(
                request.tensor_data,
                list(request.tensor_shape),
                request.dtype
            )
            
            # Store for the all-reduce operation
            key = f"{request.operation_id}:{request.chunk_idx}"
            with self.exchange_lock:
                self.pending_exchanges[key] = recv_tensor
            
            # Get our chunk to send back
            # In ring all-reduce, we send the chunk that the requester needs
            # which is our current chunk at the same index
            our_chunk = self.my_current_chunks.get(key)
            
            if our_chunk is None:
                # We don't have a chunk ready - this can happen if timing is off
                logger.warning(f"No chunk ready for exchange {key}")
                return neuroshard_pb2.TensorExchangeResponse(
                    operation_id=request.operation_id,
                    success=False,
                    error_message="Chunk not ready"
                )
            
            # Serialize our chunk
            data_bytes, shape, dtype_str = serialize_tensor_for_grpc(our_chunk)
            
            return neuroshard_pb2.TensorExchangeResponse(
                operation_id=request.operation_id,
                success=True,
                tensor_data=data_bytes,
                tensor_shape=shape
            )
            
        except Exception as e:
            logger.error(f"TensorExchange error: {e}")
            return neuroshard_pb2.TensorExchangeResponse(
                operation_id=request.operation_id,
                success=False,
                error_message=str(e)
            )
    
    def get_received_chunk(self, operation_id: str, chunk_idx: int) -> Optional[torch.Tensor]:
        """Get a received chunk (called after exchange)."""
        key = f"{operation_id}:{chunk_idx}"
        with self.exchange_lock:
            return self.pending_exchanges.pop(key, None)


class PartialResultAggregator:
    """
    Aggregates partial results from tensor shards.
    
    Used for async all-reduce where shards send partials
    and we combine them.
    """
    
    def __init__(self, total_shards: int):
        self.total_shards = total_shards
        
        # Pending aggregations: operation_id -> {shard_id: tensor}
        self.pending: Dict[str, Dict[int, torch.Tensor]] = {}
        self.lock = threading.Lock()
        
        # Callbacks for completed aggregations
        self.callbacks: Dict[str, callable] = {}
    
    def add_partial(
        self,
        operation_id: str,
        shard_id: int,
        partial_tensor: torch.Tensor,
        reduce_op: AllReduceOp = AllReduceOp.SUM
    ) -> Optional[torch.Tensor]:
        """
        Add a partial result.
        
        Returns combined tensor if all partials received, else None.
        """
        with self.lock:
            if operation_id not in self.pending:
                self.pending[operation_id] = {}
            
            self.pending[operation_id][shard_id] = partial_tensor
            
            # Check if all partials received
            if len(self.pending[operation_id]) == self.total_shards:
                # Combine
                partials = list(self.pending[operation_id].values())
                del self.pending[operation_id]
                
                if reduce_op == AllReduceOp.SUM:
                    combined = torch.stack(partials).sum(dim=0)
                elif reduce_op == AllReduceOp.MEAN:
                    combined = torch.stack(partials).mean(dim=0)
                elif reduce_op == AllReduceOp.MAX:
                    combined = torch.stack(partials).max(dim=0)[0]
                elif reduce_op == AllReduceOp.MIN:
                    combined = torch.stack(partials).min(dim=0)[0]
                else:
                    combined = torch.stack(partials).sum(dim=0)
                
                # Call callback if registered
                if operation_id in self.callbacks:
                    self.callbacks[operation_id](combined)
                    del self.callbacks[operation_id]
                
                return combined
            
            return None
    
    def register_callback(self, operation_id: str, callback: callable):
        """Register callback for when aggregation completes."""
        self.callbacks[operation_id] = callback
    
    def get_pending_count(self, operation_id: str) -> int:
        """Get count of received partials for an operation."""
        with self.lock:
            return len(self.pending.get(operation_id, {}))


class TensorShardDiscovery:
    """
    Discovers tensor shard peers for all-reduce coordination.
    
    Uses DHT and tracker to find peers holding the same layer
    but different tensor shards.
    """
    
    def __init__(self, tracker_url: str, node_token: str = None):
        self.tracker_url = tracker_url
        self.node_token = node_token
        
        # Cache: (model_id, layer_id, total_shards) -> {shard_id: peer_info}
        self.peer_cache: Dict[str, Dict[int, TensorShardPeer]] = {}
        self.cache_ttl = 60  # seconds
        self.cache_timestamps: Dict[str, float] = {}
        
        self.lock = threading.Lock()
    
    def find_shard_peers(
        self,
        model_id: str,
        layer_id: int,
        total_shards: int,
        exclude_shard_id: int = -1
    ) -> Dict[int, TensorShardPeer]:
        """
        Find peers holding tensor shards of a layer.
        
        Args:
            model_id: Model identifier
            layer_id: Layer ID
            total_shards: Total tensor shards
            exclude_shard_id: Our shard ID to exclude
            
        Returns:
            Dict of shard_id -> TensorShardPeer
        """
        cache_key = f"{model_id}:{layer_id}:{total_shards}"
        
        # Check cache
        with self.lock:
            if cache_key in self.peer_cache:
                cache_time = self.cache_timestamps.get(cache_key, 0)
                if time.time() - cache_time < self.cache_ttl:
                    peers = self.peer_cache[cache_key]
                    return {
                        sid: peer for sid, peer in peers.items()
                        if sid != exclude_shard_id
                    }
        
        # Query tracker
        peers = self._query_tracker(model_id, layer_id, total_shards)
        
        # Update cache
        with self.lock:
            self.peer_cache[cache_key] = peers
            self.cache_timestamps[cache_key] = time.time()
        
        return {
            sid: peer for sid, peer in peers.items()
            if sid != exclude_shard_id
        }
    
    def _query_tracker(
        self,
        model_id: str,
        layer_id: int,
        total_shards: int
    ) -> Dict[int, TensorShardPeer]:
        """Query tracker for tensor shard peers."""
        import requests
        
        try:
            resp = requests.get(
                f"{self.tracker_url}/tensor_shards",
                params={
                    "model_id": model_id,
                    "layer_id": layer_id,
                    "total_shards": total_shards
                },
                timeout=5
            )
            
            if resp.status_code != 200:
                logger.warning(f"Tracker query failed: {resp.status_code}")
                return {}
            
            data = resp.json()
            peers = {}
            
            for shard_info in data.get("shards", []):
                shard_id = shard_info.get("shard_id", 0)
                peers[shard_id] = TensorShardPeer(
                    shard_id=shard_id,
                    grpc_addr=shard_info.get("grpc_addr", ""),
                    latency_ms=shard_info.get("latency_ms", 0),
                    last_seen=shard_info.get("last_seen", time.time())
                )
            
            return peers
            
        except Exception as e:
            logger.error(f"Tracker query error: {e}")
            return {}
    
    def announce_shard(
        self,
        model_id: str,
        layer_id: int,
        shard_id: int,
        total_shards: int,
        grpc_addr: str
    ) -> bool:
        """Announce our tensor shard to the tracker."""
        import requests
        
        try:
            resp = requests.post(
                f"{self.tracker_url}/tensor_shards/announce",
                json={
                    "model_id": model_id,
                    "layer_id": layer_id,
                    "shard_id": shard_id,
                    "total_shards": total_shards,
                    "grpc_addr": grpc_addr,
                    "node_token": self.node_token
                },
                timeout=5
            )
            
            return resp.status_code == 200
            
        except Exception as e:
            logger.error(f"Shard announce error: {e}")
            return False

