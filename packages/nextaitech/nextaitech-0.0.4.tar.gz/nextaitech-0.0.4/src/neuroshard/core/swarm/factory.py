"""
Swarm Node Factory - Creates and configures SwarmEnabledNodes

This is THE architecture for NeuroShard. Every node runs the full swarm stack:
- SwarmRouter for fault-tolerant multipath routing
- ActivationBuffer for async compute decoupling
- SwarmHeartbeatService for capacity advertisement
- DiLoCoTrainer for lazy gradient sync
- SpeculativeCheckpointer for fast crash recovery
- RobustAggregator for Byzantine-tolerant gradient aggregation

There are NO toggles, NO fallbacks, NO backward compatibility modes.
Swarm IS the architecture.

Usage:
    from neuroshard.core.swarm import create_swarm_node, SwarmNodeConfig
    
    config = SwarmNodeConfig(
        diloco_inner_steps=500,
        checkpoint_interval=120,
    )
    
    swarm_node = create_swarm_node(
        node_token=token,
        port=port,
        tracker_url=tracker,
        config=config,
    )
"""

import asyncio
import logging
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Any

import torch

from neuroshard.core.model.dynamic import (
    DynamicNeuroNode, 
    create_dynamic_node,
    DynamicNeuroLLM,
)

logger = logging.getLogger(__name__)


@dataclass
class SwarmNodeConfig:
    """
    Configuration for SwarmEnabledNode.
    
    All values have sensible defaults but can be customized.
    """
    
    # Buffer Sizes
    inbound_buffer_size: int = 100
    outbound_buffer_size: int = 50
    soft_overflow_threshold: float = 0.9
    hard_overflow_threshold: float = 0.99
    
    # Routing
    ack_timeout_ms: int = 200
    k_candidates: int = 3
    
    # Heartbeat
    heartbeat_interval: float = 5.0
    heartbeat_port: int = 9999
    
    # DiLoCo
    diloco_inner_steps: int = 500
    diloco_outer_lr: float = 0.7
    diloco_outer_momentum: float = 0.9
    
    # Checkpointing
    checkpoint_interval: int = 120  # 2 minutes
    max_checkpoints: int = 5
    checkpoint_dir: Optional[str] = None  # Default: ~/.neuroshard/checkpoints
    
    # Aggregation
    aggregation_method: str = "trimmed_mean"  # "mean", "median", "trimmed_mean", "krum"
    krum_f: int = 0  # Byzantine workers for Krum
    trimmed_mean_beta: float = 0.1  # Trim fraction
    
    # Gradient Validation
    cosine_threshold: float = 0.5
    magnitude_ratio_threshold: float = 10.0
    
    # Compute Engine
    num_micro_batches: int = 4
    
    def get_checkpoint_dir(self) -> Path:
        """Get checkpoint directory, creating if needed."""
        if self.checkpoint_dir:
            path = Path(self.checkpoint_dir)
        else:
            path = Path.home() / ".neuroshard" / "checkpoints"
        path.mkdir(parents=True, exist_ok=True)
        return path


class SwarmComponents:
    """
    Container for all swarm components.
    
    Provides unified lifecycle management for:
    - SwarmRouter (multipath routing)
    - ActivationBuffer/OutboundBuffer (async compute)
    - SwarmHeartbeatService (capacity advertisement)
    - ComputeEngine (GPU worker)
    - DiLoCoTrainer (lazy gradient sync)
    - SpeculativeCheckpointer (crash recovery)
    - RobustAggregator (Byzantine-tolerant aggregation)
    """
    
    def __init__(self):
        # Core components
        self.swarm_router = None
        self.inbound_buffer = None
        self.outbound_buffer = None
        self.heartbeat_service = None
        self.compute_engine = None
        
        # Training components
        self.diloco_trainer = None
        self.outer_optimizer = None
        self.speculative_checkpointer = None
        self.robust_aggregator = None
        self.gradient_validator = None
        
        # State
        self.running = False
        self._tasks: List[asyncio.Task] = []
        
    async def start_async(self):
        """Start all async components."""
        self.running = True
        
        if self.swarm_router:
            await self.swarm_router.start()
            logger.info("[SWARM] SwarmRouter started")
        
        if self.compute_engine:
            task = asyncio.create_task(self.compute_engine.run())
            self._tasks.append(task)
            logger.info("[SWARM] ComputeEngine started")
    
    def start_sync(self):
        """Start all synchronous components (threads)."""
        if self.heartbeat_service:
            self.heartbeat_service.start()
            logger.info("[SWARM] HeartbeatService started")
        
        if self.speculative_checkpointer:
            self.speculative_checkpointer.start()
            logger.info("[SWARM] SpeculativeCheckpointer started")
    
    async def stop_async(self):
        """Stop all async components."""
        self.running = False
        
        for task in self._tasks:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
        self._tasks.clear()
        
        if self.swarm_router:
            await self.swarm_router.stop()
        
        if self.compute_engine:
            self.compute_engine.running = False
    
    def stop_sync(self):
        """Stop all synchronous components."""
        if self.heartbeat_service:
            self.heartbeat_service.stop()
        
        if self.speculative_checkpointer:
            self.speculative_checkpointer.stop()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get combined stats from all components."""
        stats = {"running": self.running}
        
        if self.inbound_buffer:
            stats["inbound_buffer"] = self.inbound_buffer.get_stats()
        
        if self.outbound_buffer:
            stats["outbound_buffer"] = self.outbound_buffer.get_stats()
        
        if self.swarm_router:
            stats["router"] = self.swarm_router.get_stats()
        
        if self.heartbeat_service:
            stats["heartbeat"] = self.heartbeat_service.get_stats()
        
        if self.compute_engine:
            stats["compute"] = self.compute_engine.get_stats()
        
        if self.diloco_trainer:
            stats["diloco"] = {
                "inner_step_count": self.diloco_trainer.stats.inner_step_count,
                "inner_steps_total": self.diloco_trainer.config.inner_steps,
                "outer_step_count": self.diloco_trainer.stats.outer_step_count,
            }
        
        return stats


class SwarmEnabledDynamicNode:
    """
    A DynamicNeuroNode with full swarm capabilities.
    
    This is THE node type for NeuroShard. Every node runs:
    - Fault-tolerant multipath routing (SwarmRouter)
    - Async activation buffering (ActivationBuffer, OutboundBuffer)
    - Capacity-aware peer selection (SwarmHeartbeatService)
    - Decoupled GPU compute (ComputeEngine)
    - DiLoCo lazy gradient sync (DiLoCoTrainer)
    - Speculative checkpointing (SpeculativeCheckpointer)
    - Byzantine-tolerant aggregation (RobustAggregator)
    
    There are NO toggles. This IS the architecture.
    """
    
    def __init__(
        self,
        base_node: DynamicNeuroNode,
        config: SwarmNodeConfig,
        p2p_manager: Optional[Any] = None,
    ):
        """
        Initialize SwarmEnabledDynamicNode.
        
        Args:
            base_node: The DynamicNeuroNode to enhance (REQUIRED)
            config: SwarmNodeConfig with settings (REQUIRED)
            p2p_manager: Optional P2P manager (uses base_node.p2p_manager if not provided)
        """
        self.base_node = base_node
        self.config = config
        self.p2p_manager = p2p_manager or base_node.p2p_manager
        
        # Expose base node properties directly
        self.node_id = base_node.node_id
        self.node_token = base_node.node_token
        self.model = base_node.model
        self.my_layer_ids = base_node.my_layer_ids
        self.layer_pool = base_node.layer_pool
        self.enable_training = base_node.enable_training
        self.device = base_node.device
        self.available_memory_mb = base_node.available_memory_mb
        
        # Training state - sync from base node (may have been loaded from checkpoint)
        self._total_training_rounds = base_node.total_training_rounds
        self._current_loss = base_node.current_loss if base_node.current_loss != float('inf') else float('inf')
        
        # Initialize swarm components
        self.swarm = SwarmComponents()
        self._init_swarm_components()
        
        logger.info(f"[SWARM] SwarmEnabledNode initialized for {self.node_id[:16]}...")
        logger.info(f"[SWARM]   - DiLoCo: inner_steps={config.diloco_inner_steps}")
        logger.info(f"[SWARM]   - Checkpointing: interval={config.checkpoint_interval}s")
        logger.info(f"[SWARM]   - Heartbeat: interval={config.heartbeat_interval}s")
        
        # Restore pending state from checkpoint (DiLoCo, optimizer)
        # This must happen AFTER swarm components are initialized
        if hasattr(base_node, '_restore_pending_state'):
            base_node._restore_pending_state()
        
        # Also make swarm accessible from base_node for checkpoint saving
        base_node.swarm = self.swarm
    
    # ==================== PROPERTIES ====================
    # Expose training state for runner/dashboard access
    
    @property
    def total_training_rounds(self) -> int:
        """Total training rounds completed (used by runner for PoNW proofs)."""
        return self._total_training_rounds
    
    @total_training_rounds.setter
    def total_training_rounds(self, value: int):
        self._total_training_rounds = value
    
    @property
    def current_loss(self) -> float:
        """Current training loss (used by dashboard)."""
        return self._current_loss
    
    @current_loss.setter
    def current_loss(self, value: float):
        self._current_loss = value
    
    @property
    def total_tokens_processed(self) -> int:
        """Total tokens processed (delegate to base node)."""
        return self.base_node.total_tokens_processed
    
    @total_tokens_processed.setter
    def total_tokens_processed(self, value: int):
        self.base_node.total_tokens_processed = value
    
    def _init_swarm_components(self):
        """Initialize all swarm components."""
        from neuroshard.core.swarm.buffers import ActivationBuffer, OutboundBuffer
        from neuroshard.core.swarm.router import SwarmRouter
        from neuroshard.core.swarm.heartbeat import SwarmHeartbeatService
        from neuroshard.core.swarm.compute import ComputeEngine
        
        # Create buffers
        self.swarm.inbound_buffer = ActivationBuffer(
            max_size=self.config.inbound_buffer_size
        )
        self.swarm.outbound_buffer = OutboundBuffer(
            max_size=self.config.outbound_buffer_size,
            soft_overflow_threshold=self.config.soft_overflow_threshold,
            hard_overflow_threshold=self.config.hard_overflow_threshold,
        )
        
        # Create router
        dht = self.p2p_manager.dht if self.p2p_manager else None
        self.swarm.swarm_router = SwarmRouter(dht_protocol=dht)
        self.swarm.swarm_router.K_CANDIDATES = self.config.k_candidates
        self.swarm.swarm_router.ACK_TIMEOUT_MS = self.config.ack_timeout_ms
        
        # Create heartbeat service
        self.swarm.heartbeat_service = SwarmHeartbeatService(
            node_id=self.node_id,
            udp_port=self.config.heartbeat_port,
        )
        self.swarm.heartbeat_service.HEARTBEAT_INTERVAL = self.config.heartbeat_interval
        self.swarm.heartbeat_service.set_capacity_callback(self._get_capacity_bitmask)
        self.swarm.heartbeat_service.set_peer_update_callback(
            self.swarm.swarm_router.update_peer_from_heartbeat
        )
        
        # Create compute engine
        self.swarm.compute_engine = ComputeEngine(
            model=self.model,
            inbound=self.swarm.inbound_buffer,
            outbound=self.swarm.outbound_buffer,
            diloco_trainer=None,  # Set after DiLoCo init
            num_micro_batches=self.config.num_micro_batches,
        )
        
        # Initialize training components if training is enabled
        if self.enable_training:
            self._init_diloco()
            self._init_checkpointer()
    
    def _init_diloco(self):
        """Initialize DiLoCo trainer and related components."""
        from neuroshard.core.swarm.diloco import DiLoCoTrainer, OuterOptimizer, DiLoCoConfig
        from neuroshard.core.swarm.aggregation import (
            RobustAggregator, 
            GradientValidator,
            AggregationConfig, 
            AggregationStrategy,
            ValidationConfig,
        )
        
        # Create outer optimizer
        self.swarm.outer_optimizer = OuterOptimizer(
            lr=self.config.diloco_outer_lr,
            momentum=self.config.diloco_outer_momentum,
        )
        
        # Create DiLoCo trainer
        diloco_config = DiLoCoConfig(
            inner_steps=self.config.diloco_inner_steps,
            outer_lr=self.config.diloco_outer_lr,
            outer_momentum=self.config.diloco_outer_momentum,
        )
        
        self.swarm.diloco_trainer = DiLoCoTrainer(
            model=self.model,
            config=diloco_config,
            inner_optimizer=self.base_node.optimizer,
        )
        
        # Connect to compute engine
        self.swarm.compute_engine.diloco = self.swarm.diloco_trainer
        
        # Create gradient validator
        validation_config = ValidationConfig(
            min_cosine_similarity=self.config.cosine_threshold,
            max_magnitude_ratio=self.config.magnitude_ratio_threshold,
        )
        self.swarm.gradient_validator = GradientValidator(config=validation_config)
        
        # Create robust aggregator
        strategy_map = {
            "mean": AggregationStrategy.MEAN,
            "median": AggregationStrategy.MEDIAN,
            "trimmed_mean": AggregationStrategy.TRIMMED_MEAN,
            "krum": AggregationStrategy.KRUM,
        }
        strategy = strategy_map.get(self.config.aggregation_method, AggregationStrategy.TRIMMED_MEAN)
        
        agg_config = AggregationConfig(
            strategy=strategy,
            num_byzantine=self.config.krum_f,
            trim_fraction=self.config.trimmed_mean_beta,
        )
        
        self.swarm.robust_aggregator = RobustAggregator(
            aggregation_config=agg_config,
            validation_config=validation_config,
        )
    
    def _init_checkpointer(self):
        """Initialize speculative checkpointer."""
        from neuroshard.core.swarm.checkpoint import SpeculativeCheckpointer, CheckpointConfig
        
        checkpoint_config = CheckpointConfig(
            checkpoint_dir=str(self.config.get_checkpoint_dir()),
            snapshot_interval=float(self.config.checkpoint_interval),
            max_hot_snapshots=self.config.max_checkpoints,
        )
        
        self.swarm.speculative_checkpointer = SpeculativeCheckpointer(
            model=self.model,
            optimizer=self.base_node.optimizer,
            config=checkpoint_config,
            diloco_trainer=self.swarm.diloco_trainer,
            p2p_manager=self.p2p_manager,
        )
    
    def _get_capacity_bitmask(self):
        """Get current capacity for heartbeat broadcast."""
        from neuroshard.core.swarm.heartbeat import CapacityBitmask
        
        # Get memory info
        available_mb = 0
        gpu_util = 0.0
        
        if torch.cuda.is_available():
            try:
                free, total = torch.cuda.mem_get_info()
                available_mb = free // (1024 * 1024)
            except:
                pass
        else:
            available_mb = self.available_memory_mb
        
        # Determine layer range
        layer_range = (0, 0)
        if self.my_layer_ids:
            layer_range = (min(self.my_layer_ids), max(self.my_layer_ids) + 1)
        
        # Get buffer status
        queue_depth = len(self.swarm.inbound_buffer) if self.swarm.inbound_buffer else 0
        is_backpressured = self.swarm.inbound_buffer.is_backpressured if self.swarm.inbound_buffer else False
        
        return CapacityBitmask(
            node_id=self.node_id,
            timestamp=time.time(),
            available_memory_mb=available_mb,
            queue_depth=queue_depth,
            layer_range=layer_range,
            gpu_utilization=gpu_util,
            network_saturation=0.0,
            is_training=self.enable_training,
            is_accepting_inference=True,
            is_accepting_activations=not is_backpressured,
            grpc_addr=self.base_node.grpc_addr,
        )
    
    # ==================== LIFECYCLE ====================
    
    def start(self):
        """Start all swarm components."""
        self.swarm.start_sync()
        logger.info("[SWARM] Node started")
    
    def stop(self):
        """Stop all swarm components."""
        self.swarm.stop_sync()
        logger.info("[SWARM] Node stopped")
    
    async def start_async(self):
        """Start async swarm components."""
        await self.swarm.start_async()
    
    async def stop_async(self):
        """Stop async swarm components."""
        await self.swarm.stop_async()
    
    # ==================== BUFFER ACCESS ====================
    
    def receive_activation(self, packet: 'ActivationPacket') -> bool:
        """
        Receive an activation packet from a peer.
        
        Called by gRPC handler when SwarmForward is received.
        """
        return self.swarm.inbound_buffer.put_nowait(packet)
    
    def get_buffer_status(self) -> Dict[str, Any]:
        """Get status of inbound and outbound buffers."""
        return {
            'inbound': self.swarm.inbound_buffer.get_stats(),
            'outbound': self.swarm.outbound_buffer.get_stats(),
        }
    
    # ==================== ROUTING ====================
    
    def get_swarm_route(self) -> Dict[int, List['PeerCandidate']]:
        """
        Get swarm route with K candidates per layer.
        
        Returns dict of layer_id -> list of K candidates.
        """
        from neuroshard.core.swarm.router import PeerCandidate
        
        route: Dict[int, List[PeerCandidate]] = {}
        num_layers = self.layer_pool.current_num_layers if self.layer_pool else 12
        
        for layer_id in range(num_layers):
            candidates = self.swarm.swarm_router.get_candidates(layer_id)
            if candidates:
                route[layer_id] = candidates
        
        return route
    
    # ==================== TRAINING ====================
    
    def train_step(self) -> Optional[float]:
        """
        Execute a training step with DiLoCo lazy gradient sync.
        
        Returns loss value or None if no data available.
        """
        if not self.enable_training:
            return None
        
        diloco = self.swarm.diloco_trainer
        
        # Get training data
        batch = self.base_node._get_training_batch()
        if batch is None:
            return None
        
        input_ids, labels = batch
        
        # Forward pass
        self.model.train()
        outputs = self.model.forward_my_layers(
            self.model.embed(input_ids.to(self.device))
        )
        
        # Compute loss
        if self.model.has_lm_head:
            logits = self.model.compute_logits(outputs)
            loss = torch.nn.functional.cross_entropy(
                logits.view(-1, logits.size(-1)),
                labels.view(-1).to(self.device)
            )
        else:
            loss = outputs.norm()  # Worker nodes use activation norm
        
        # DiLoCo inner step (no communication)
        diloco.inner_step(loss)
        self._current_loss = loss.item()
        self._total_training_rounds += 1
        
        # Check if outer sync needed
        if diloco.should_sync():
            self._do_diloco_sync()
        
        return self._current_loss
    
    def _do_diloco_sync(self):
        """Execute DiLoCo outer synchronization."""
        diloco = self.swarm.diloco_trainer
        
        # Compute pseudo-gradient
        pseudo_grad = diloco.compute_pseudo_gradient()
        
        # In a real implementation, this would:
        # 1. Gossip pseudo_grad to peers
        # 2. Aggregate received pseudo-grads using robust_aggregator
        # 3. Apply aggregated update via outer_optimizer
        
        # For now, apply local update
        diloco.apply_outer_update(pseudo_grad)
        
        logger.info(
            f"[SWARM] DiLoCo outer sync #{diloco.stats.outer_step_count} "
            f"(inner_steps={diloco.config.inner_steps})"
        )
    
    # ==================== STATS ====================
    
    def get_stats(self) -> Dict[str, Any]:
        """Get combined stats from base node and swarm components."""
        stats = self.base_node.get_stats()
        
        # Override with swarm node's actual training values (these are updated
        # in train_step() but base_node's values are only synced on checkpoint)
        stats["total_training_rounds"] = self._total_training_rounds
        stats["current_loss"] = self._current_loss
        
        stats["swarm"] = self.swarm.get_stats()
        return stats
    
    def get_swarm_status(self) -> Dict[str, Any]:
        """Get detailed swarm status."""
        return self.swarm.get_stats()
    
    def get_diloco_progress(self) -> Dict[str, Any]:
        """Get DiLoCo training progress."""
        if not self.swarm.diloco_trainer:
            return {"enabled": False}
        
        diloco = self.swarm.diloco_trainer
        return {
            "enabled": True,
            "inner_step_count": diloco.stats.inner_step_count,
            "inner_steps_total": diloco.config.inner_steps,
            "progress": diloco.stats.inner_step_count / diloco.config.inner_steps,
            "outer_step_count": diloco.stats.outer_step_count,
        }
    
    # ==================== DELEGATION ====================
    
    @property
    def grpc_addr(self):
        """Get gRPC address."""
        return self.base_node.grpc_addr
    
    @property
    def data_manager(self):
        """Get data manager."""
        return self.base_node.data_manager
    
    @property
    def genesis_loader(self):
        """Get genesis loader."""
        return self.base_node.genesis_loader
    
    @property
    def optimizer(self):
        """Get optimizer."""
        return self.base_node.optimizer
    
    def forward(self, input_ids: torch.Tensor, **kwargs):
        """Forward pass - delegates to base node."""
        return self.base_node.forward(input_ids, **kwargs)
    
    def _save_checkpoint(self):
        """
        Save checkpoint with swarm state.
        
        Syncs the swarm node's training counters to base node before saving.
        """
        # Sync training state to base node before saving
        self.base_node.total_training_rounds = self._total_training_rounds
        self.base_node.current_loss = self._current_loss
        
        # Delegate to base node's checkpoint saving
        return self.base_node._save_checkpoint()
    
    def __getattr__(self, name):
        """Delegate unknown attributes to base node."""
        return getattr(self.base_node, name)


# ==================== FACTORY ====================

def create_swarm_node(
    node_token: str,
    port: int,
    tracker_url: str,
    config: SwarmNodeConfig,
    available_memory_mb: Optional[int] = None,
    enable_training: bool = False,
    max_storage_mb: int = 10000,
    max_cpu_threads: int = 4,
    p2p_manager: Optional[Any] = None,
) -> SwarmEnabledDynamicNode:
    """
    Factory function to create a SwarmEnabledDynamicNode.
    
    This is the main entry point for creating nodes.
    
    Args:
        node_token: Authentication token for the node
        port: HTTP port for the node
        tracker_url: URL of the tracker server
        config: SwarmNodeConfig with settings (REQUIRED)
        available_memory_mb: Override memory detection
        enable_training: Whether to enable training
        max_storage_mb: Max disk space for data shards
        max_cpu_threads: Max CPU threads to use
        p2p_manager: Optional P2P manager (created if not provided)
    
    Returns:
        SwarmEnabledDynamicNode ready for use
    """
    # Create base DynamicNeuroNode
    base_node = create_dynamic_node(
        node_token=node_token,
        port=port,
        tracker_url=tracker_url,
        available_memory_mb=available_memory_mb,
        enable_training=enable_training,
        max_storage_mb=max_storage_mb,
        max_cpu_threads=max_cpu_threads,
    )
    
    # Wrap with swarm capabilities
    return SwarmEnabledDynamicNode(
        base_node=base_node,
        config=config,
        p2p_manager=p2p_manager,
    )
