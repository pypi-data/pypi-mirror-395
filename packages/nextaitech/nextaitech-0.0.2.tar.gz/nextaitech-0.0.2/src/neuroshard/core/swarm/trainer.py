"""
Async Trainer - Swarm-Enabled Training Loop

Integrates the swarm components into the training loop:
- Uses ActivationBuffer for async activation handling
- Supports Interleaved 1F1B schedule
- Enables "Don't Stop" soft overflow handling
- Works with DiLoCo-style local gradient accumulation

This replaces the blocking train_step() with an async version that:
1. Never stalls the GPU waiting for network
2. Falls back to local training on network congestion
3. Accumulates gradients for lazy sync

Usage:
    trainer = AsyncSwarmTrainer(node)
    trainer.start()
    
    # Training loop runs in background
    # Trainer pulls data, computes, handles overflow automatically
"""

import asyncio
import logging
import time
import threading
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum

import torch
import torch.nn.functional as F

from neuroshard.core.swarm.buffers import ActivationBuffer, OutboundBuffer, ActivationPacket
from neuroshard.core.swarm.router import SwarmRouter

logger = logging.getLogger(__name__)


class TrainerState(Enum):
    """State of the async trainer."""
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"


@dataclass
class TrainerConfig:
    """Configuration for async trainer."""
    # Micro-batching
    micro_batch_size: int = 4
    num_micro_batches: int = 4  # In-flight at once
    
    # Gradient accumulation
    gradient_accumulation_steps: int = 8
    
    # DiLoCo settings
    diloco_inner_steps: int = 500
    diloco_outer_lr: float = 0.7
    
    # Overflow handling
    soft_overflow_threshold: float = 0.9
    enable_local_fallback: bool = True
    
    # Learning rate
    learning_rate: float = 1e-4
    max_grad_norm: float = 1.0
    
    # Timing
    log_interval: int = 10


@dataclass
class TrainerStats:
    """Training statistics."""
    total_steps: int = 0
    forward_steps: int = 0
    backward_steps: int = 0
    local_only_steps: int = 0
    dropped_steps: int = 0
    
    total_loss: float = 0.0
    loss_count: int = 0
    
    total_tokens: int = 0
    start_time: float = field(default_factory=time.time)
    
    @property
    def avg_loss(self) -> float:
        if self.loss_count == 0:
            return 0.0
        return self.total_loss / self.loss_count
    
    @property
    def tokens_per_second(self) -> float:
        elapsed = time.time() - self.start_time
        if elapsed == 0:
            return 0.0
        return self.total_tokens / elapsed
    
    @property
    def local_only_rate(self) -> float:
        if self.total_steps == 0:
            return 0.0
        return self.local_only_steps / self.total_steps


class AsyncSwarmTrainer:
    """
    Asynchronous trainer with swarm integration.
    
    Features:
    - Non-blocking compute: GPU never waits for network
    - Soft overflow handling: Falls back to local training on congestion
    - Interleaved 1F1B: Overlaps forward and backward passes
    - DiLoCo-compatible: Accumulates gradients for lazy sync
    
    The trainer runs in a background thread with its own event loop,
    continuously processing activations and training.
    """
    
    def __init__(
        self,
        node: Any,  # DynamicNeuroNode
        config: Optional[TrainerConfig] = None,
        inbound: Optional[ActivationBuffer] = None,
        outbound: Optional[OutboundBuffer] = None,
        router: Optional[SwarmRouter] = None,
    ):
        """
        Initialize async trainer.
        
        Args:
            node: The DynamicNeuroNode to train
            config: Training configuration
            inbound: Input activation buffer (creates if None)
            outbound: Output activation buffer (creates if None)
            router: SwarmRouter for peer communication
        """
        self.node = node
        self.config = config or TrainerConfig()
        
        # Get model reference
        self.model = getattr(node, 'model', None)
        self.device = getattr(node, 'device', 'cpu')
        
        # Buffers
        self.inbound = inbound or ActivationBuffer(max_size=100)
        self.outbound = outbound or OutboundBuffer(max_size=50)
        
        # Router
        self.router = router
        
        # State
        self.state = TrainerState.IDLE
        self.stats = TrainerStats()
        
        # Optimizer
        self.optimizer: Optional[torch.optim.Optimizer] = None
        self._setup_optimizer()
        
        # Gradient accumulation
        self._accumulated_steps = 0
        self._accumulated_gradients: Dict[str, torch.Tensor] = {}
        
        # DiLoCo state
        self._diloco_step = 0
        self._initial_weights: Dict[str, torch.Tensor] = {}
        
        # Threading
        self._thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        
        # Pending backwards (for Interleaved 1F1B)
        self._pending_backwards: Dict[int, ActivationPacket] = {}
        
        logger.info(f"AsyncSwarmTrainer initialized")
    
    def _setup_optimizer(self):
        """Setup optimizer for training."""
        if self.model is None:
            return
        
        params = list(self.model.parameters())
        if not params:
            return
        
        self.optimizer = torch.optim.AdamW(
            params,
            lr=self.config.learning_rate,
            betas=(0.9, 0.95),
            weight_decay=0.1,
        )
        
        logger.info(f"Optimizer setup: AdamW lr={self.config.learning_rate}")
    
    # ==================== LIFECYCLE ====================
    
    def start(self):
        """Start the training loop in background thread."""
        if self.state == TrainerState.RUNNING:
            logger.warning("Trainer already running")
            return
        
        self.state = TrainerState.RUNNING
        self.stats = TrainerStats()  # Reset stats
        
        # Save initial weights for DiLoCo
        self._save_initial_weights()
        
        # Start background thread
        self._thread = threading.Thread(
            target=self._run_training_loop,
            daemon=True,
            name="AsyncSwarmTrainer"
        )
        self._thread.start()
        
        logger.info("Async trainer started")
    
    def stop(self):
        """Stop the training loop."""
        if self.state not in (TrainerState.RUNNING, TrainerState.PAUSED):
            return
        
        self.state = TrainerState.STOPPING
        
        # Wait for thread
        if self._thread:
            self._thread.join(timeout=5.0)
        
        self.state = TrainerState.STOPPED
        logger.info("Async trainer stopped")
    
    def pause(self):
        """Pause training (can be resumed)."""
        if self.state == TrainerState.RUNNING:
            self.state = TrainerState.PAUSED
            logger.info("Trainer paused")
    
    def resume(self):
        """Resume paused training."""
        if self.state == TrainerState.PAUSED:
            self.state = TrainerState.RUNNING
            logger.info("Trainer resumed")
    
    # ==================== MAIN LOOP ====================
    
    def _run_training_loop(self):
        """Main training loop running in background thread."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        
        try:
            self._loop.run_until_complete(self._async_training_loop())
        except Exception as e:
            logger.error(f"Training loop error: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self._loop.close()
    
    async def _async_training_loop(self):
        """Async training loop with Interleaved 1F1B schedule."""
        logger.info("Training loop started")
        
        forward_count = 0
        
        while self.state in (TrainerState.RUNNING, TrainerState.PAUSED):
            # Handle pause
            while self.state == TrainerState.PAUSED:
                await asyncio.sleep(0.1)
            
            if self.state != TrainerState.RUNNING:
                break
            
            # Get next activation from buffer
            packet = self.inbound.get(timeout=0.01)
            
            if packet is None:
                # Buffer empty - check if we should generate local data
                if self._should_generate_local_data():
                    packet = await self._generate_local_packet()
                else:
                    await asyncio.sleep(0.001)
                    continue
            
            self.stats.total_steps += 1
            
            # Process packet based on type
            if packet.is_backward:
                await self._process_backward(packet)
            else:
                await self._process_forward(packet)
                forward_count += 1
            
            # Interleaved 1F1B: After warmup, interleave backward passes
            if forward_count > self.config.num_micro_batches:
                if self._pending_backwards:
                    oldest_mb = min(self._pending_backwards.keys())
                    bp = self._pending_backwards.pop(oldest_mb)
                    await self._process_backward(bp)
            
            # Check DiLoCo sync
            if self._should_diloco_sync():
                await self._diloco_outer_step()
            
            # Logging
            if self.stats.total_steps % self.config.log_interval == 0:
                self._log_stats()
        
        logger.info("Training loop ended")
    
    # ==================== FORWARD/BACKWARD ====================
    
    async def _process_forward(self, packet: ActivationPacket):
        """Process forward activation packet."""
        if self.model is None:
            return
        
        # Move to device
        hidden = packet.tensor_data.to(self.device)
        
        # Forward through my layers
        with torch.set_grad_enabled(packet.requires_grad):
            output = self.model.forward_my_layers(hidden)
        
        self.stats.forward_steps += 1
        
        # Check outbound pressure
        pressure = self._check_outbound_pressure()
        
        if pressure == "ok":
            # Normal: send to next peer
            await self._send_activation(output, packet)
        elif pressure == "soft_overflow":
            # Soft overflow: accumulate locally
            await self._handle_soft_overflow(output, packet)
            self.stats.local_only_steps += 1
        else:
            # Hard overflow: drop
            logger.warning(f"Hard overflow at step {self.stats.total_steps}")
            self.stats.dropped_steps += 1
        
        # Save for backward pass
        if packet.requires_grad:
            self._pending_backwards[packet.micro_batch_id] = packet
    
    async def _process_backward(self, packet: ActivationPacket):
        """Process backward pass."""
        if self.model is None or self.optimizer is None:
            return
        
        self.stats.backward_steps += 1
        
        # Get grad output
        grad_output = packet.grad_output
        if grad_output is None:
            return
        
        grad_output = grad_output.to(self.device)
        
        # Backward through my layers
        # Note: In real implementation, we'd need saved activations
        # This is simplified
        
        # Accumulate gradient
        self._accumulated_steps += 1
        
        # Step optimizer if accumulated enough
        if self._accumulated_steps >= self.config.gradient_accumulation_steps:
            self._optimizer_step()
    
    def _optimizer_step(self):
        """Perform optimizer step."""
        if self.optimizer is None:
            return
        
        # Clip gradients
        if self.model:
            torch.nn.utils.clip_grad_norm_(
                self.model.parameters(),
                self.config.max_grad_norm
            )
        
        self.optimizer.step()
        self.optimizer.zero_grad()
        self._accumulated_steps = 0
        
        self._diloco_step += 1
    
    # ==================== OVERFLOW HANDLING ====================
    
    def _check_outbound_pressure(self) -> str:
        """Check outbound buffer pressure."""
        fill_rate = self.outbound.fill_rate
        
        if fill_rate >= 0.99:
            return "hard_overflow"
        elif fill_rate >= self.config.soft_overflow_threshold:
            return "soft_overflow"
        else:
            return "ok"
    
    async def _send_activation(self, output: torch.Tensor, packet: ActivationPacket):
        """Send activation to next peer via outbound buffer."""
        # Determine next layer
        next_layer = packet.target_layer + 1
        if self.model:
            my_max_layer = max(self.model.my_layer_ids) if self.model.my_layer_ids else 0
            next_layer = my_max_layer + 1
        
        outbound_packet = ActivationPacket(
            priority=packet.priority,
            session_id=packet.session_id,
            micro_batch_id=packet.micro_batch_id,
            tensor_data=output.cpu(),
            source_node=getattr(self.node, 'node_id', ''),
            target_layer=next_layer,
            requires_grad=packet.requires_grad,
        )
        
        await self.outbound.put(outbound_packet)
    
    async def _handle_soft_overflow(self, output: torch.Tensor, packet: ActivationPacket):
        """
        Handle soft overflow - accumulate locally instead of sending.
        
        This is the "Don't Stop" mechanism:
        - GPU keeps computing
        - Gradients accumulate locally
        - Activations are discarded (not sent)
        - Will sync later via DiLoCo outer step
        """
        logger.debug(f"Soft overflow: accumulating locally (step {self.stats.total_steps})")
        
        if not packet.requires_grad:
            return
        
        # For training, we'd compute local loss and backward here
        # This is simplified - in real impl we need labels
        
        # Mark as local-only for stats
        # The gradient will be synced in DiLoCo outer step
    
    # ==================== DILOCO ====================
    
    def _save_initial_weights(self):
        """Save initial weights for DiLoCo pseudo-gradient computation."""
        if self.model is None:
            return
        
        self._initial_weights = {
            name: param.data.clone()
            for name, param in self.model.named_parameters()
        }
        self._diloco_step = 0
    
    def _should_diloco_sync(self) -> bool:
        """Check if we should trigger DiLoCo outer sync."""
        return self._diloco_step >= self.config.diloco_inner_steps
    
    async def _diloco_outer_step(self):
        """
        Perform DiLoCo outer optimization step.
        
        1. Compute pseudo-gradient (delta from initial weights)
        2. (In real impl) Gossip to peers and aggregate
        3. Apply outer optimizer update
        4. Reset for next inner loop
        """
        if self.model is None:
            return
        
        logger.info(f"DiLoCo outer step (after {self._diloco_step} inner steps)")
        
        # Compute pseudo-gradients
        pseudo_grads = {}
        for name, param in self.model.named_parameters():
            if name in self._initial_weights:
                delta = self._initial_weights[name] - param.data
                pseudo_grads[name] = delta
        
        # In real implementation: gossip pseudo_grads to peers
        # For now, just apply locally
        
        # Apply outer update (simplified Nesterov)
        with torch.no_grad():
            for name, param in self.model.named_parameters():
                if name in pseudo_grads:
                    param.data.add_(
                        pseudo_grads[name],
                        alpha=self.config.diloco_outer_lr
                    )
        
        # Reset for next inner loop
        self._save_initial_weights()
        
        logger.info("DiLoCo outer step complete")
    
    # ==================== LOCAL DATA ====================
    
    def _should_generate_local_data(self) -> bool:
        """Check if we should generate local training data."""
        # Only if we're a driver node (have embedding)
        if self.model is None:
            return False
        return getattr(self.model, 'has_embedding', False)
    
    async def _generate_local_packet(self) -> Optional[ActivationPacket]:
        """Generate a local training packet from data loader."""
        if not hasattr(self.node, 'genesis_loader'):
            return None
        
        loader = self.node.genesis_loader
        if loader is None or not loader.is_data_ready():
            return None
        
        try:
            input_ids, labels = loader.get_batch(
                batch_size=self.config.micro_batch_size
            )
            
            # Embed
            input_ids = input_ids.to(self.device)
            hidden = self.model.embed(input_ids)
            
            # Create packet
            return ActivationPacket(
                priority=20,  # Training priority
                session_id=f"train_{time.time()}",
                micro_batch_id=self.stats.forward_steps,
                tensor_data=hidden,
                source_node=getattr(self.node, 'node_id', ''),
                target_layer=0,
                requires_grad=True,
            )
        except Exception as e:
            logger.debug(f"Could not generate local packet: {e}")
            return None
    
    # ==================== STATS ====================
    
    def _log_stats(self):
        """Log training statistics."""
        logger.info(
            f"Step {self.stats.total_steps}: "
            f"loss={self.stats.avg_loss:.4f}, "
            f"fwd={self.stats.forward_steps}, "
            f"bwd={self.stats.backward_steps}, "
            f"local_rate={self.stats.local_only_rate:.2%}, "
            f"tok/s={self.stats.tokens_per_second:.1f}"
        )
    
    def get_stats(self) -> Dict[str, Any]:
        """Get training statistics."""
        return {
            'state': self.state.value,
            'total_steps': self.stats.total_steps,
            'forward_steps': self.stats.forward_steps,
            'backward_steps': self.stats.backward_steps,
            'local_only_steps': self.stats.local_only_steps,
            'dropped_steps': self.stats.dropped_steps,
            'avg_loss': self.stats.avg_loss,
            'local_only_rate': self.stats.local_only_rate,
            'tokens_per_second': self.stats.tokens_per_second,
            'diloco_step': self._diloco_step,
            'accumulated_steps': self._accumulated_steps,
        }


# ==================== INTEGRATION HELPERS ====================

def create_swarm_trainer(
    node: Any,  # DynamicNeuroNode
    inbound: Optional[ActivationBuffer] = None,
    outbound: Optional[OutboundBuffer] = None,
    router: Optional[SwarmRouter] = None,
    **config_kwargs,
) -> AsyncSwarmTrainer:
    """
    Factory function to create a swarm-enabled trainer.
    
    Args:
        node: The DynamicNeuroNode to train
        inbound: Input activation buffer
        outbound: Output activation buffer  
        router: SwarmRouter for peer communication
        **config_kwargs: Additional config options
        
    Returns:
        Configured AsyncSwarmTrainer
    """
    config = TrainerConfig(**config_kwargs)
    return AsyncSwarmTrainer(
        node=node,
        config=config,
        inbound=inbound,
        outbound=outbound,
        router=router,
    )

