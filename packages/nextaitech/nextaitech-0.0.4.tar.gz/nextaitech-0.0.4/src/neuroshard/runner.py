"""
NeuroShard Node Runner

This is the main entry point for running a NeuroShard node.
The node participates in:
1. Training NeuroLLM (our own model, trained from scratch by the network)
2. Inference (generating text using the collective model)
3. Earning NEURO tokens through Proof of Neural Work

TRULY DECENTRALIZED:
- No fixed model phases
- Model size grows with network capacity
- Each node contributes based on available memory
- More memory = more layers = more NEURO rewards
"""

import argparse
import uvicorn
import threading
import torch  # Imported early for API endpoints
import time
import requests
import logging
import logging.handlers  # For RotatingFileHandler
import sys
import os
import socket
import uuid
import hashlib
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List

from neuroshard.core.model.dynamic import DynamicNeuroNode, create_dynamic_node
from neuroshard.core.model.tokenizer import get_neuro_tokenizer
from neuroshard.core.network.p2p import P2PManager

# Swarm Architecture Imports (Phase 4)
try:
    from neuroshard.core.swarm.factory import (
        SwarmEnabledDynamicNode,
        SwarmNodeConfig,
        create_swarm_node,
    )
    SWARM_AVAILABLE = True
except ImportError:
    SWARM_AVAILABLE = False
from neuroshard.core.economics.constants import (
    is_valid_stake_amount,
    is_valid_stake_duration,
    VALIDATOR_MIN_STAKE,
)
from neuroshard.ui.app import STATE, templates
from neuroshard.utils.serialization import deserialize_tensor, serialize_tensor
from neuroshard.grpc_server import start_grpc_background
from neuroshard.version import __version__

# Safe print for Windows frozen GUI mode (where stdout may be None)
_original_print = print

def _safe_print(*args, **kwargs):
    """Print that works even when stdout is None (Windows GUI)."""
    try:
        if sys.stdout is not None:
            _original_print(*args, **kwargs)
    except (AttributeError, OSError, ValueError):
        pass  # Silently ignore - logging will capture it

# Override print globally in this module
print = _safe_print

# Global shutdown flag for clean exit from GUI
_SHUTDOWN_REQUESTED = threading.Event()
_UVICORN_SERVER = None  # Global reference to uvicorn server for shutdown

def request_shutdown():
    """Request graceful shutdown of the node. Called from GUI when stopping."""
    global _UVICORN_SERVER, NEURO_NODE, P2P
    logger.info("[NODE] Shutdown requested...")
    _SHUTDOWN_REQUESTED.set()
    
    # Stop gRPC server first (releases port)
    try:
        from neuroshard.grpc_server import stop_grpc
        stop_grpc(timeout=3.0)
    except Exception as e:
        logger.error(f"[NODE] gRPC shutdown error: {e}")
    
    # Stop swarm components if enabled
    if NEURO_NODE and hasattr(NEURO_NODE, 'stop_swarm_sync'):
        try:
            logger.info("[NODE] Stopping swarm components...")
            NEURO_NODE.stop_swarm_sync()
            logger.info("[NODE] Swarm components stopped.")
        except Exception as e:
            logger.error(f"[NODE] Swarm shutdown error: {e}")
    
    # Save checkpoint before shutting down
    if NEURO_NODE:
        try:
            logger.info("[NODE] Saving checkpoint before shutdown...")
            NEURO_NODE._save_checkpoint()
            logger.info("[NODE] Checkpoint saved.")
        except Exception as e:
            logger.error(f"[NODE] Failed to save checkpoint: {e}")
        
        # CRITICAL: Free memory by deleting model and data
        try:
            logger.info("[NODE] Freeing memory...")
            
            # Clear genesis data
            if hasattr(NEURO_NODE, 'genesis_loader') and NEURO_NODE.genesis_loader:
                NEURO_NODE.genesis_loader.loaded_shards.clear()
                NEURO_NODE.genesis_loader._prefetch_ready.clear()
                NEURO_NODE.genesis_loader.current_dataset = None
            
            # Get base node (for SwarmEnabledDynamicNode) or use directly
            base = getattr(NEURO_NODE, 'base_node', NEURO_NODE)
            
            # Delete optimizer (holds 2x model params in memory for Adam)
            if hasattr(base, 'optimizer') and base.optimizer is not None:
                del base.optimizer
            
            # Delete model
            if hasattr(base, 'model') and base.model is not None:
                del base.model
            
            # Force garbage collection
            import gc
            gc.collect()
            
            # Clear GPU cache if applicable
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                logger.info("[NODE] Cleared CUDA cache")
            elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                torch.mps.empty_cache()
                logger.info("[NODE] Cleared MPS cache")
            
            logger.info("[NODE] Memory freed")
        except Exception as e:
            logger.error(f"[NODE] Memory cleanup error: {e}")
    
    # Stop P2P manager (stops background threads)
    if P2P:
        try:
            P2P.stop()
        except Exception as e:
            logger.error(f"[NODE] P2P stop error: {e}")
    
    # Stop uvicorn server
    if _UVICORN_SERVER:
        _UVICORN_SERVER.should_exit = True
        
        # FORCE EXIT: If uvicorn doesn't stop in 3 seconds, force kill
        def force_exit():
            import time, os
            time.sleep(3.0)
            if _UVICORN_SERVER and _UVICORN_SERVER.started:
                logger.warning("[NODE] Forcing exit...")
                os._exit(0)  # Force exit without cleanup
        
        t = threading.Thread(target=force_exit, daemon=True)
        t.start()
    
    # Reset globals so next run starts fresh
    NEURO_NODE = None
    P2P = None
    _UVICORN_SERVER = None

# Configure Logging - ensure all loggers use our format
# Clear any existing handlers first to prevent duplicates
root_logger = logging.getLogger()
root_logger.handlers = []  # Clear existing handlers
root_logger.setLevel(logging.INFO)

# --- In-memory log buffer for dashboard ---
from collections import deque
from datetime import datetime

# Circular buffer to store recent logs (max 500 entries)
_LOG_BUFFER = deque(maxlen=500)
_LOG_BUFFER_LOCK = threading.Lock()

class MemoryLogHandler(logging.Handler):
    """Custom handler that stores logs in memory for dashboard API."""
    
    def emit(self, record):
        try:
            msg = self.format(record)
            timestamp = datetime.fromtimestamp(record.created).strftime('%H:%M:%S')
            
            # Determine log type for filtering
            log_type = 'info'
            msg_lower = msg.lower()
            if 'neuro' in msg_lower and ('earned' in msg_lower or 'reward' in msg_lower or '+' in msg):
                log_type = 'neuro'
            elif 'error' in msg_lower or record.levelno >= logging.ERROR:
                log_type = 'error'
            elif 'training' in msg_lower or 'diloco' in msg_lower or 'gradient' in msg_lower or 'batch' in msg_lower:
                log_type = 'training'
            elif record.levelno >= logging.WARNING:
                log_type = 'warning'
            
            with _LOG_BUFFER_LOCK:
                _LOG_BUFFER.append({
                    'timestamp': timestamp,
                    'message': msg,
                    'type': log_type,
                    'level': record.levelname,
                })
        except Exception:
            pass  # Never fail logging

# Windows GUI apps (frozen) may have None stdout/stderr
# Create a safe handler that won't crash
def _create_safe_handler():
    """Create a logging handler that works even when stdout is None (Windows GUI)."""
    # Check if stdout is usable
    if sys.stdout is not None and hasattr(sys.stdout, 'write'):
        try:
            # Test if it's actually writable
            sys.stdout.write('')
            sys.stdout.flush()
            return logging.StreamHandler(sys.stdout)
        except (AttributeError, OSError, ValueError):
            pass
    
    # Fallback: log to file in .neuroshard directory
    log_dir = os.path.join(os.path.expanduser("~"), ".neuroshard")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "node.log")
    
    # Rotate logs - keep last 5MB
    return logging.handlers.RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=2, encoding='utf-8')

handler = _create_safe_handler()
handler.setFormatter(logging.Formatter('[NODE] %(message)s'))
root_logger.addHandler(handler)

# Add memory handler for dashboard logs API
memory_handler = MemoryLogHandler()
memory_handler.setFormatter(logging.Formatter('%(message)s'))
memory_handler.setLevel(logging.INFO)
root_logger.addHandler(memory_handler)

# Also configure neuroshard module loggers explicitly
for module in ['neuroshard.core.p2p', 'neuroshard.core.ledger', 'neuroshard.core.dynamic_model',
               'neuroshard.core.distributed_training', 'neuroshard.core.dht_service']:
    module_logger = logging.getLogger(module)
    module_logger.setLevel(logging.INFO)
    module_logger.propagate = True  # Propagate to root logger

# Create logger for this module
logger = logging.getLogger(__name__)

# --- Main API App ---
node_app = FastAPI(title="NeuroShard Node", version=__version__)
# Serve dashboard at root
from fastapi.responses import HTMLResponse

@node_app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    """Serve the main dashboard at root."""
    return templates.TemplateResponse("index.html", {"request": request})

# Shared State
NEURO_NODE: Optional[DynamicNeuroNode] = None
P2P: Optional[P2PManager] = None
SESSION_TIMESTAMPS = {}

def get_app():
    return node_app


class InferenceRequest(BaseModel):
    tensor_data: str
    request_id: str
    session_id: Optional[str] = None
    sender_reputation: float = 100.0


class TextGenerationRequest(BaseModel):
    prompt: str
    max_new_tokens: int = 50
    temperature: float = 1.0
    top_k: int = 50
    top_p: float = 0.9


class TrainingDataRequest(BaseModel):
    text: str
    apply_dp: bool = True  # Apply differential privacy


# ==================== INFERENCE ENDPOINTS ====================

@node_app.post("/generate_text")
async def generate_text(req: TextGenerationRequest):
    """
    Generate text using NeuroLLM.
    
    Note: Early in the network's life, output will be mostly random.
    As more users train the model, quality will improve!
    """
    if not NEURO_NODE:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    try:
        generated = NEURO_NODE.generate(
            prompt=req.prompt,
            max_new_tokens=req.max_new_tokens,
            temperature=req.temperature,
        )
        
        STATE["processed_count"] = STATE.get("processed_count", 0) + 1
        STATE["token_count"] = NEURO_NODE.total_tokens_processed
        
        return {
            "text": generated,
            "my_layers": NEURO_NODE.my_layer_ids,
            "total_training_rounds": NEURO_NODE.total_training_rounds,
            "note": "Quality improves as more users train the model!"
        }
        
    except Exception as e:
        return {"error": str(e)}


@node_app.post("/forward")
async def forward(req: InferenceRequest):
    """Forward pass for distributed inference pipeline."""
    if not NEURO_NODE:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    try:
        STATE["processed_count"] = STATE.get("processed_count", 0) + 1
        
        if req.session_id:
            SESSION_TIMESTAMPS[req.session_id] = time.time()
        
        # Deserialize input
        input_tensor = deserialize_tensor(req.tensor_data)
        
        # Forward through NeuroLLM
        output = NEURO_NODE.forward(input_tensor, session_id=req.session_id)
        
        # Update token count
        STATE["token_count"] = NEURO_NODE.total_tokens_processed
        
        # Return result (NeuroLLM is always a full model, no pipeline needed)
        return {"result": serialize_tensor(output)}
        
    except Exception as e:
        return {"error": str(e)}


# ==================== TRAINING ENDPOINTS ====================

@node_app.post("/contribute_data")
async def contribute_training_data(req: TrainingDataRequest):
    """
    Contribute training data to help train NeuroLLM.
    
    Your data is processed locally with differential privacy.
    You earn NEURO tokens for contributing!
    """
    if not NEURO_NODE:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    if not NEURO_NODE.enable_training:
        raise HTTPException(status_code=400, detail="Training not enabled on this node")
    
    try:
        tokens_added = NEURO_NODE.contribute_training_data(req.text, apply_dp=req.apply_dp)
        
        data_stats = NEURO_NODE.data_manager.get_stats() if NEURO_NODE.data_manager else {}
        
        return {
            "success": True,
            "message": "Data added to training buffer",
            "tokens_added": tokens_added or 0,
            "buffer_size": data_stats.get("buffer_size", 0),
            "total_tokens": data_stats.get("total_tokens", 0),
        }
        
    except Exception as e:
        return {"error": str(e)}


@node_app.post("/train_step")
async def trigger_train_step():
    """Manually trigger a training step (for testing)."""
    if not NEURO_NODE:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    loss = NEURO_NODE.train_step()
    
    if loss is None:
        return {"success": False, "message": "Not enough training data in buffer"}
    
    return {
        "success": True,
        "loss": loss,
        "total_training_rounds": NEURO_NODE.total_training_rounds
    }


@node_app.get("/training_status")
async def get_training_status():
    """Get current training status."""
    if not NEURO_NODE:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    return {
        "training_enabled": NEURO_NODE.enable_training,
        "total_training_rounds": NEURO_NODE.total_training_rounds,
        "current_loss": NEURO_NODE.current_loss,
        "training_contributions": NEURO_NODE.training_contribution_count,
        "data_buffer": NEURO_NODE.data_manager.get_stats() if NEURO_NODE.data_manager else None,
        "my_layers": NEURO_NODE.my_layer_ids,
    }


# ==================== STATS & PONW ENDPOINTS ====================

@node_app.get("/api/stats")
async def get_api_stats():
    """Endpoint for GUI to fetch local node stats."""
    import math
    import asyncio
    import os
    
    # Yield to event loop to ensure responsiveness
    await asyncio.sleep(0)
    
    # Get actual system resource usage
    system_stats = {}
    try:
        import psutil
        # CPU usage (system-wide percentage)
        system_stats["cpu_percent"] = psutil.cpu_percent(interval=None)  # Non-blocking
        
        # Memory usage (system-wide)
        mem = psutil.virtual_memory()
        system_stats["ram_used_gb"] = round(mem.used / (1024**3), 2)
        system_stats["ram_total_gb"] = round(mem.total / (1024**3), 2)
        system_stats["ram_percent"] = mem.percent
        
        # Process-specific memory
        process = psutil.Process(os.getpid())
        system_stats["process_ram_mb"] = round(process.memory_info().rss / (1024**2), 1)
    except Exception:
        pass
    
    # Start with basic stats from STATE
    stats = {
        "peer_count": STATE.get("peer_count", 0),
        "processed_count": STATE.get("processed_count", 0),
        "training_status": STATE.get("training_status", "idle"),
        # Actual system resource usage
        "system": system_stats,
        # Resource throttle info
        "throttle": {
            "cpu_ratio": STATE.get("throttle_cpu_ratio", 1.0),
            "ram_ratio": STATE.get("throttle_ram_ratio", 1.0),
            "effective": STATE.get("throttle_effective", 1.0),
            "interval_seconds": STATE.get("throttle_interval", 2.0),
            "max_steps_per_min": STATE.get("throttle_max_steps", 30),
        },
    }
    
    if NEURO_NODE:
        # Run get_stats in executor to not block event loop
        loop = asyncio.get_event_loop()
        node_stats = await loop.run_in_executor(None, NEURO_NODE.get_stats)
        
        # Handle infinity values (not JSON serializable)
        current_loss = node_stats.get("current_loss", float('inf'))
        if math.isinf(current_loss) or math.isnan(current_loss):
            current_loss = None  # Use None for JSON compatibility
        
        # Determine role string for display
        has_embedding = node_stats.get("has_embedding", False)
        has_lm_head = node_stats.get("has_lm_head", False)
        if has_embedding and has_lm_head:
            role = "Full Node (Driver + Validator)"
        elif has_embedding:
            role = "Driver"
        elif has_lm_head:
            role = "Validator"
        else:
            role = "Worker"
        
        stats.update({
            # My contribution
            "my_layers": node_stats.get("my_layers", []),
            "my_params_m": node_stats.get("my_params", 0) / 1e6,
            "has_embedding": has_embedding,
            "has_lm_head": has_lm_head,
            "role": role,
            "available_memory_mb": node_stats.get("available_memory_mb", 0),
            "reward_multiplier": node_stats.get("reward_multiplier", 1.0),
            
            # Network stats
            "network_layers": node_stats.get("network_layers", 0),
            "network_params_m": node_stats.get("network_params", 0) / 1e6,
            "network_nodes": node_stats.get("network_nodes", 0),
            "contribution_ratio": node_stats.get("contribution_ratio", 0),
            
            # Training stats - use CUMULATIVE values from NEURO_NODE, not delta from STATE
            "training_enabled": NEURO_NODE.enable_training,
            "training_rounds": node_stats.get("total_training_rounds", 0),
            "token_count": node_stats.get("total_tokens_processed", 0),  # Cumulative tokens
            "current_loss": current_loss,
            "data_buffer_size": node_stats.get("data_buffer_size", 0),
            
            # Data shard stats (if Driver)
            "shard_stats": node_stats.get("shard_stats", {}),
            
            # Device info
            "device": NEURO_NODE.device,
            
            # Instance info (for multi-node support)
            "instance_id": getattr(NEURO_NODE, 'instance_id', None),
        })
        
        # Add DiLoCo progress
        diloco = NEURO_NODE.get_diloco_progress()
        if diloco.get("enabled", False):
            stats["diloco"] = {
                "inner_step": diloco.get("inner_step_count", 0),
                "inner_total": diloco.get("inner_steps_total", 500),
                "progress": diloco.get("progress", 0.0),
                "outer_step": diloco.get("outer_step_count", 0),
            }
    else:
        # Node not ready yet
        stats["token_count"] = 0
        stats["training_rounds"] = 0
    
    # Add version
    stats["version"] = __version__
    
    return stats


@node_app.get("/api/market")
async def get_market_stats():
    """
    Get real-time inference market statistics.
    
    Returns current price, supply, demand, utilization.
    """
    if not P2P or not P2P.ledger:
        raise HTTPException(status_code=503, detail="Ledger not available")
    
    return P2P.ledger.get_inference_market_stats()


@node_app.post("/api/market/register")
async def register_inference_capacity(
    tokens_per_second: int,
    min_price: float = 0.0
):
    """
    Register this node's inference capacity with the market.
    
    Nodes should call this when idle/available to serve inference.
    Call withdraw endpoint when switching to training.
    """
    if not P2P or not P2P.ledger:
        raise HTTPException(status_code=503, detail="Ledger not available")
    
    P2P.ledger.register_inference_capacity(
        tokens_per_second=tokens_per_second,
        min_price=min_price
    )
    
    return {"status": "registered", "tokens_per_second": tokens_per_second, "min_price": min_price}


@node_app.post("/api/market/withdraw")
async def withdraw_inference_capacity():
    """
    Withdraw this node from inference market.
    
    Call this when switching to training.
    """
    if not P2P or not P2P.ledger:
        raise HTTPException(status_code=503, detail="Ledger not available")
    
    P2P.ledger.withdraw_inference_capacity()
    
    return {"status": "withdrawn"}


# ==================== DISTRIBUTED INFERENCE MARKETPLACE ====================

class MarketplaceSubmitRequest(BaseModel):
    """User submits inference request to marketplace."""
    prompt: str
    max_tokens: int = 100
    max_price: float = 1.0
    driver_node_id: Optional[str] = None  # Optional: specify driver, else round-robin


class DriverPromptRequest(BaseModel):
    """User sends encrypted prompt directly to driver."""
    encrypted_prompt: str
    user_id: str


@node_app.post("/api/market/submit")
async def submit_marketplace_request(req: MarketplaceSubmitRequest):
    """
    Submit inference request to marketplace (USER API).
    
    Flow:
    1. User submits request with prompt
    2. Marketplace locks price, assigns driver
    3. User sends encrypted prompt to driver
    4. Driver processes, returns result
    
    Returns:
        request_id, locked_price, driver_node_id
    """
    if not NEURO_NODE or not P2P or not P2P.ledger:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    if not hasattr(P2P.ledger, 'inference_market'):
        raise HTTPException(status_code=503, detail="Marketplace not available")
    
    market = P2P.ledger.inference_market
    
    # Choose driver (round-robin if not specified)
    driver_node_id = req.driver_node_id
    
    if not driver_node_id:
        # Find a driver node from layer pool
        if NEURO_NODE.layer_pool:
            route = NEURO_NODE.layer_pool.get_pipeline_route()
            if route and len(route) > 0:
                # First layer should be embedding (driver)
                driver_node_id = route[0][1].split(':')[0] if ':' in route[0][1] else NEURO_NODE.node_id
            else:
                # Fallback to this node if it's a driver
                if NEURO_NODE.model.has_embedding:
                    driver_node_id = NEURO_NODE.node_id
                else:
                    raise HTTPException(status_code=503, detail="No driver nodes available")
        else:
            # Single node mode
            driver_node_id = NEURO_NODE.node_id
    
    # Sign request with node's ECDSA key (authorizes payment)
    from neuroshard.core.crypto.ecdsa import sign_message
    signature_payload = f"{NEURO_NODE.node_id}:{driver_node_id}:{req.max_tokens}:{req.max_price}"
    user_signature = sign_message(signature_payload, NEURO_NODE.node_token)
    
    # Submit to marketplace (without prompt - privacy!)
    success, request_id, locked_price = market.submit_request(
        user_id=NEURO_NODE.node_id,  # For testing, use node ID as user ID
        driver_node_id=driver_node_id,
        tokens_requested=req.max_tokens,
        max_price=req.max_price,
        user_signature=user_signature,
        priority=0
    )
    
    if not success:
        raise HTTPException(status_code=400, detail="Request rejected (price too high or market full)")
    
    # Encrypt prompt for driver
    from neuroshard.core.network.encrypted_channel import PromptEncryption
    encrypted_prompt = PromptEncryption.encrypt_prompt(req.prompt, request_id)
    
    # If we are the driver, add to our own queue
    if driver_node_id == NEURO_NODE.node_id and hasattr(NEURO_NODE, 'prompt_queue'):
        from neuroshard.core.network.encrypted_channel import EncryptedPrompt
        import time
        
        NEURO_NODE.prompt_queue.add_prompt(EncryptedPrompt(
            request_id=request_id,
            encrypted_data=encrypted_prompt,
            timestamp=time.time(),
            user_id=NEURO_NODE.node_id
        ))
        logger.info(f"[API] ✓ Added encrypted prompt to local driver queue")
    
    return {
        "request_id": request_id,
        "locked_price": locked_price,
        "driver_node_id": driver_node_id,
        "encrypted_prompt": encrypted_prompt,  # User should send this to driver
        "instructions": f"POST encrypted_prompt to /api/driver/prompt/{request_id} on driver node"
    }


@node_app.post("/api/driver/prompt/{request_id}")
async def submit_encrypted_prompt(request_id: str, req: DriverPromptRequest):
    """
    User sends encrypted prompt to driver node (PRIVACY CHANNEL).
    
    This endpoint is called on the DRIVER node, not the marketplace.
    Prompt is encrypted - only driver can decrypt it.
    """
    if not NEURO_NODE or not NEURO_NODE.model.has_embedding:
        raise HTTPException(status_code=403, detail="This node is not a driver")
    
    if not hasattr(NEURO_NODE, 'prompt_queue'):
        raise HTTPException(status_code=503, detail="Driver not initialized")
    
    # Add to prompt queue
    from neuroshard.core.network.encrypted_channel import EncryptedPrompt
    import time
    
    prompt = EncryptedPrompt(
        request_id=request_id,
        encrypted_data=req.encrypted_prompt,
        timestamp=time.time(),
        user_id=req.user_id
    )
    
    success = NEURO_NODE.prompt_queue.add_prompt(prompt)
    
    if not success:
        raise HTTPException(status_code=503, detail="Prompt queue full")
    
    return {
        "status": "success",
        "message": f"Encrypted prompt queued for request {request_id[:8]}...",
        "queue_position": len(NEURO_NODE.prompt_queue.prompts)
    }


@node_app.get("/api/market/request/{request_id}")
async def get_request_status(request_id: str):
    """
    Get status of inference request.
    
    Returns:
        status, progress, eta, result (if completed)
    """
    if not NEURO_NODE or not P2P or not P2P.ledger:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    if not hasattr(P2P.ledger, 'inference_market'):
        raise HTTPException(status_code=503, detail="Marketplace not available")
    
    market = P2P.ledger.inference_market
    request = market.get_request(request_id)
    
    if not request:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # Get result from marketplace storage
    result_text = market.get_result(request_id)
    
    return {
        "request_id": request_id,
        "status": request.status,
        "locked_price": request.locked_price,
        "tokens_requested": request.tokens_requested,
        "driver_node_id": request.driver_node_id,
        "pipeline_session_id": request.pipeline_session_id,
        "result": result_text,
        "completed": request.status == "completed" and result_text is not None
    }


@node_app.get("/api/ponw")
async def get_ponw_proof():
    """
    Get Proof of Neural Work for this node.
    
    This proves the node actually contributed compute for training/inference.
    Used for NEURO token rewards.
    """
    if not NEURO_NODE:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    return NEURO_NODE.get_ponw_proof()


@node_app.get("/api/neuro")
async def get_neuro_balance():
    """
    Get NEURO token balance and account info for this node.
    
    Returns:
    - balance: Current spendable balance
    - total_earned: Lifetime earnings from PoNW
    - total_spent: Lifetime spending
    - stake: Currently staked amount
    - stake_multiplier: Reward multiplier from staking
    """
    if not P2P or not P2P.ledger:
        raise HTTPException(status_code=503, detail="Ledger not available")
    
    # Use NEUROLedger API (no fallbacks)
    account_info = P2P.ledger.get_account_info()
    burn_stats = P2P.ledger.get_burn_stats()
    
    # Get node IDs
    wallet_id = P2P.ledger.node_id if P2P.ledger else None
    node_id = P2P.node_id if P2P else None
    
    return {
        "balance": round(account_info.get("balance", 0.0), 6),
        "total_earned": round(account_info.get("total_earned", 0.0), 6),
        "total_spent": round(account_info.get("total_spent", 0.0), 6),
        "stake": round(account_info.get("stake", 0.0), 2),
        "stake_multiplier": round(account_info.get("stake_multiplier", 1.0), 2),
        "proof_count": account_info.get("proof_count", 0),
        "wallet_id": wallet_id,
        "node_id": node_id,
        "network": {
            "total_burned": round(burn_stats.get("total_burned", 0.0), 6),
            "circulating_supply": round(burn_stats.get("circulating_supply", 0.0), 6),
            "burn_rate": "5%"
        }
    }


# ==================== STAKING ENDPOINTS ====================

class StakeRequest(BaseModel):
    amount: float
    duration_days: int = 30


@node_app.post("/api/stake")
async def stake_neuro(req: StakeRequest):
    """
    Stake NEURO tokens for reward multiplier.
    
    Staking provides:
    - 10% bonus per 1000 NEURO staked (diminishing returns)
    - Tokens locked for specified duration
    
    Example: Stake 2000 NEURO for 30 days = ~1.16x multiplier on all rewards
    """
    if not P2P or not P2P.ledger:
        raise HTTPException(status_code=503, detail="Ledger not available")
    
    # Validate using centralized economics
    is_valid, error = is_valid_stake_amount(req.amount)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    is_valid, error = is_valid_stake_duration(req.duration_days)
    if not is_valid:
        raise HTTPException(status_code=400, detail=error)
    
    success, message = P2P.ledger.stake(req.amount, req.duration_days)
    
    if success:
        account = P2P.ledger.get_account_info()
        return {
            "success": True,
            "message": message,
            "new_stake": account.get("stake", 0.0),
            "new_multiplier": account.get("stake_multiplier", 1.0),
            "locked_until": account.get("stake_locked_until", 0.0)
        }
    else:
        raise HTTPException(status_code=400, detail=message)


@node_app.post("/api/unstake")
async def unstake_neuro():
    """
    Unstake NEURO tokens (if lock period expired).
    
    Returns staked tokens to balance.
    """
    if not P2P or not P2P.ledger:
        raise HTTPException(status_code=503, detail="Ledger not available")
    
    success, amount, message = P2P.ledger.unstake()
    
    if success:
        return {
            "success": True,
            "message": message,
            "amount_unstaked": amount
        }
    else:
        raise HTTPException(status_code=400, detail=message)


@node_app.get("/api/stake/info")
async def get_stake_info():
    """Get current staking information."""
    if not P2P or not P2P.ledger:
        raise HTTPException(status_code=503, detail="Ledger not available")
    
    account = P2P.ledger.get_account_info()
    
    return {
        "stake": account.get("stake", 0.0),
        "stake_multiplier": account.get("stake_multiplier", 1.0),
        "stake_locked_until": account.get("stake_locked_until", 0.0),
        "balance": account.get("balance", 0.0),
        "staking_info": {
            "bonus_per_1000": "10% (diminishing)",
            "min_lock_days": 1,
            "max_lock_days": 365,
            "validator_min_stake": VALIDATOR_MIN_STAKE
        }
    }


class ThrottleUpdateRequest(BaseModel):
    cpu_threads: Optional[int] = None
    memory_mb: Optional[int] = None


@node_app.post("/api/throttle")
async def update_throttle(req: ThrottleUpdateRequest):
    """
    Update training throttle settings while node is running.
    
    This allows the GUI to change CPU/RAM limits without restarting.
    Changes take effect within 5 seconds.
    """
    updated = {}
    
    if req.cpu_threads is not None:
        STATE["config_cpu_threads"] = req.cpu_threads
        updated["cpu_threads"] = req.cpu_threads
    
    if req.memory_mb is not None:
        STATE["config_memory_mb"] = req.memory_mb
        updated["memory_mb"] = req.memory_mb
    
    return {
        "success": True,
        "updated": updated,
        "message": "Throttle settings updated. Changes take effect within 5 seconds.",
        "current_throttle": {
            "cpu_ratio": STATE.get("throttle_cpu_ratio", 1.0),
            "ram_ratio": STATE.get("throttle_ram_ratio", 1.0),
            "effective": STATE.get("throttle_effective", 1.0),
        }
    }


@node_app.get("/api/validator/info")
async def get_validator_info():
    """
    Get validator eligibility and status.
    
    Validators require:
    - Minimum 100 NEURO staked
    - LM Head layer assignment (last layer)
    
    Validators earn:
    - 30% bonus on rewards (up from 20%)
    - 0.001 NEURO per proof validated
    """
    if not P2P or not P2P.ledger:
        raise HTTPException(status_code=503, detail="Ledger not available")
    
    validator_info = P2P.ledger.get_validator_info()
    
    # Add role info from node
    if NEURO_NODE:
        validator_info["has_lm_head"] = NEURO_NODE.model.has_lm_head if NEURO_NODE.model else False
        validator_info["is_active_validator"] = (
            validator_info["is_eligible_validator"] and 
            validator_info.get("has_lm_head", False)
        )
    
    return validator_info


# ==================== SWARM ENDPOINTS ====================

@node_app.get("/api/swarm")
async def get_swarm_status():
    """
    Get Swarm architecture status.
    
    Returns buffer fill rates, heartbeat peers, routing stats.
    """
    if not NEURO_NODE:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    # Get swarm status from node
    swarm_status = NEURO_NODE.get_swarm_status()
    
    return swarm_status


@node_app.get("/api/diloco")
async def get_diloco_progress():
    """
    Get DiLoCo training progress.
    
    Returns inner step count, sync progress, outer step count.
    """
    if not NEURO_NODE:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    return NEURO_NODE.get_diloco_progress()


@node_app.get("/api/model_info")
async def get_model_info():
    """Get information about the NeuroLLM model."""
    if not NEURO_NODE:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    stats = NEURO_NODE.get_stats()
    
    # Get architecture info
    arch_info = {}
    if NEURO_NODE.layer_pool and NEURO_NODE.layer_pool.current_architecture:
        arch = NEURO_NODE.layer_pool.current_architecture
        arch_info = {
            "hidden_dim": arch.hidden_dim,
            "num_layers": arch.num_layers,
            "num_heads": arch.num_heads,
            "vocab_size": arch.vocab_size,
            "architecture_version": NEURO_NODE.layer_pool.architecture_version,
            "total_params": arch.estimate_params(),
        }
    
    return {
        "model_name": "NeuroLLM",
        "description": "The People's Language Model - trained from scratch by the network",
        "architecture": arch_info,  # NEW: Show current architecture
        "my_layers": stats.get("my_layers", []),
        "my_params": stats.get("my_params", 0),
        "network_layers": stats.get("network_layers", 0),
        "network_nodes": stats.get("network_nodes", 0),
        "total_training_rounds": NEURO_NODE.total_training_rounds,
        "current_loss": NEURO_NODE.current_loss,
        "note": "This model is trained collaboratively. Quality improves as more users contribute!"
    }


@node_app.get("/api/network")
async def get_network_info():
    """Get network capacity and layer distribution."""
    if not NEURO_NODE or not NEURO_NODE.layer_pool:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    capacity = NEURO_NODE.layer_pool.get_network_capacity()
    
    return {
        "total_nodes": capacity.total_nodes,
        "total_memory_mb": capacity.total_memory_mb,
        "max_possible_layers": capacity.max_layers,
        "current_layers": capacity.assigned_layers,
        "layer_coverage": capacity.layer_coverage,
        "my_contribution": NEURO_NODE.model.get_my_contribution() if NEURO_NODE.model else {},
    }


@node_app.get("/api/logs")
async def get_logs(since: Optional[int] = None, limit: int = 100):
    """
    Get recent logs from the node.
    
    Args:
        since: Return logs after this index (for polling)
        limit: Maximum number of logs to return (default 100)
    
    Returns:
        List of log entries with timestamp, message, type, and level
    """
    with _LOG_BUFFER_LOCK:
        logs = list(_LOG_BUFFER)
    
    # If since is provided, filter to only newer logs
    if since is not None and since >= 0:
        logs = logs[since:]
    
    # Limit results
    if len(logs) > limit:
        logs = logs[-limit:]
    
    return {
        "logs": logs,
        "total": len(_LOG_BUFFER),
        "next_index": len(_LOG_BUFFER),  # Client can use this for next poll
    }


@node_app.post("/api/shutdown")
async def shutdown_node():
    """
    Gracefully shutdown the node.
    
    Saves checkpoint and stops all components cleanly.
    """
    import asyncio
    
    logger.info("[NODE] Shutdown requested via API")
    
    # Schedule shutdown in background (after response is sent)
    async def delayed_shutdown():
        await asyncio.sleep(1.0)  # Give time for response to be sent
        request_shutdown()
    
    asyncio.create_task(delayed_shutdown())
    
    return {
        "status": "shutting_down",
        "message": "Node will shutdown in 1 second. Checkpoint will be saved."
    }


@node_app.get("/api/checkpoint/info")
async def get_checkpoint_info():
    """Get checkpoint info for P2P sync."""
    if not NEURO_NODE:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    return NEURO_NODE.get_checkpoint_info()


@node_app.get("/api/checkpoint/download")
async def download_checkpoint():
    """Download checkpoint (for P2P sync via HTTP fallback)."""
    import io
    import zlib
    from fastapi.responses import Response
    
    if not NEURO_NODE or not NEURO_NODE.model:
        raise HTTPException(status_code=503, detail="Node not ready")
    
    try:
        # Serialize checkpoint for my layers only
        buffer = io.BytesIO()
        
        # Collect layer state dicts
        layer_states = {
            layer_id: layer.state_dict()
            for layer_id, layer in NEURO_NODE.model.my_layers.items()
        }
        
        checkpoint = {
            "layer_ids": NEURO_NODE.my_layer_ids,
            "layers": layer_states,
            "has_embedding": NEURO_NODE.model.has_embedding,
            "has_lm_head": NEURO_NODE.model.has_lm_head,
            "version": NEURO_NODE.total_training_rounds,
        }
        
        if NEURO_NODE.model.embedding:
            checkpoint["embedding"] = NEURO_NODE.model.embedding.state_dict()
        if NEURO_NODE.model.lm_head:
            checkpoint["lm_head"] = NEURO_NODE.model.lm_head.state_dict()
        if NEURO_NODE.model.final_norm:
            checkpoint["final_norm"] = NEURO_NODE.model.final_norm.state_dict()
        
        torch.save(checkpoint, buffer)
        
        # Compress
        raw_data = buffer.getvalue()
        compressed = zlib.compress(raw_data, level=6)
        
        return Response(
            content=compressed,
            media_type="application/octet-stream",
            headers={
                "X-Checkpoint-Version": str(checkpoint["version"]),
                "X-Layer-IDs": ",".join(map(str, NEURO_NODE.my_layer_ids)),
                "X-Original-Size": str(len(raw_data)),
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== UTILITY FUNCTIONS ====================

def get_public_ip():
    """Attempt to get the public IP address of this node."""
    try:
        services = [
            'https://api.ipify.org',
            'https://ifconfig.me/ip',
            'https://icanhazip.com'
        ]
        for service in services:
            try:
                return requests.get(service, timeout=3).text.strip()
            except:
                continue
    except Exception:
        pass
    return None


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


def run_node(
    port: int,
    tracker: str = "https://neuroshard.com/api/tracker",
    node_token: Optional[str] = None,
    announce_ip: str = None,
    announce_port: int = None,
    enable_training: bool = True,
    available_memory_mb: Optional[float] = None,
    max_storage_mb: float = 100.0,
    max_cpu_threads: Optional[int] = None,
    diloco_inner_steps: int = 500,
):
    """
    Start a NeuroShard node.
    
    TRULY DECENTRALIZED:
    - No fixed phases or model sizes
    - Node contributes based on available memory
    - More memory = more layers = more NEURO rewards
    
    MULTI-NODE SUPPORT:
    - Same token on multiple machines/ports is now supported
    - Each instance gets unique network identity (for layers)
    - Earnings accumulate to the same NEURO wallet
    
    Args:
        port: HTTP port
        tracker: Tracker URL for peer discovery
        node_token: Authentication token
        enable_training: Whether to participate in training
        available_memory_mb: Override memory detection (for testing)
        max_storage_mb: Maximum disk space for training data shards
        max_cpu_threads: Maximum CPU threads to use for training
    """
    global NEURO_NODE, P2P
    
    # CRITICAL: Clear shutdown flag from previous run (for GUI restart support)
    _SHUTDOWN_REQUESTED.clear()
    
    # Reset STATE for fresh start (important for GUI restart)
    STATE.clear()
    STATE.update({
        "shard_range": "Unknown",
        "peer_count": 0,
        "processed_count": 0,
        "training_updates": 0,
        "token_count": 0,
        "training_batches": 0,
        "assigned_layers": [],
        "has_embedding": False,
        "has_lm_head": False,
    })
    
    logger.info(f"Starting NeuroShard Node {__version__} on Port {port}")
    
    # Multi-node detection and info
    from neuroshard.utils.hardware import get_instance_id, get_machine_id
    instance_id = get_instance_id(port)
    machine_id = get_machine_id()
    
    logger.info(f"Machine ID: {machine_id}")
    logger.info(f"Instance ID: {instance_id} (machine:port unique)")
    
    if node_token:
        wallet_id = hashlib.sha256(node_token.encode()).hexdigest()[:16]
        logger.info(f"Wallet ID: {wallet_id}... (NEURO earnings go here)")
        logger.info("=" * 50)
        logger.info("MULTI-NODE INFO:")
        logger.info("  Same token on multiple machines? Each gets unique assignment")
        logger.info("=" * 50)
    logger.info(f"Dashboard available at http://localhost:{port}/")
    logger.info(f"Max training data storage: {max_storage_mb}MB")
    
    # Thread configuration
    # Note: For GUI mode, this is already set in gui_runner.py wrapper
    # For CLI mode, we do our best here (may fail if torch already initialized)
    if max_cpu_threads:
        logger.info(f"Limiting CPU threads to: {max_cpu_threads}")
        
        # Set environment variables (these always work)
        import os
        os.environ['OMP_NUM_THREADS'] = str(max_cpu_threads)
        os.environ['MKL_NUM_THREADS'] = str(max_cpu_threads)
        os.environ['OPENBLAS_NUM_THREADS'] = str(max_cpu_threads)
        
        # Try to set PyTorch threads (may fail if already set)
        try:
            torch.set_num_threads(max_cpu_threads)
            torch.set_num_interop_threads(max(1, max_cpu_threads // 2))
        except RuntimeError:
            # Already configured (likely by GUI wrapper or torch initialized)
            pass
        
        # Lower process priority (to not hog system resources)
        try:
            if sys.platform == 'win32':
                # Windows: Use SetPriorityClass
                import ctypes
                kernel32 = ctypes.windll.kernel32
                BELOW_NORMAL_PRIORITY_CLASS = 0x00004000
                kernel32.SetPriorityClass(kernel32.GetCurrentProcess(), BELOW_NORMAL_PRIORITY_CLASS)
                logger.info("Process priority lowered (Windows BELOW_NORMAL)")
            elif hasattr(os, 'nice'):
                # Unix/Mac: Use nice
                os.nice(10)
                logger.info("Process priority lowered (nice=10)")
        except Exception:
            pass
    
    if node_token:
        logger.info(f"Authenticated with Token: {node_token[:8]}...")
    
    # 1. Create SwarmEnabledNode (this IS the standard architecture)
    token_for_id = node_token or str(uuid.uuid4())
    
    logger.info(f"Initializing NeuroShard Node (training={enable_training}, DiLoCo steps={diloco_inner_steps})...")
    
    # Create swarm config
    swarm_config = SwarmNodeConfig(
        diloco_inner_steps=diloco_inner_steps,
    )
    
    NEURO_NODE = create_swarm_node(
        node_token=token_for_id,
        port=port,
        tracker_url=tracker,
        config=swarm_config,
        available_memory_mb=available_memory_mb,
        enable_training=enable_training,
        max_storage_mb=max_storage_mb,
        max_cpu_threads=max_cpu_threads,
    )
    
    STATE["diloco_inner_steps"] = diloco_inner_steps
    
    logger.info(f"NeuroLLM loaded: {NEURO_NODE.model.get_num_params() / 1e6:.1f}M parameters")
    logger.info(f"Assigned layers: {NEURO_NODE.my_layer_ids}")
    logger.info(f"Embedding: {NEURO_NODE.model.has_embedding}, LM Head: {NEURO_NODE.model.has_lm_head}")
    logger.info(f"DiLoCo: inner_steps={diloco_inner_steps}")
    
    # EARLY NETWORK WARNING
    num_layers = len(NEURO_NODE.my_layer_ids)
    if num_layers > 50:
        logger.warning("⚠️  EARLY NETWORK NOTICE ⚠️")
        logger.warning(f"You're holding {num_layers} layers because the network is small.")
        logger.warning("This is TEMPORARY - as more nodes join, the model will be sharded.")
    
    # Show initial memory usage
    try:
        import psutil
        process = psutil.Process()
        process_mem_mb = process.memory_info().rss / (1024 * 1024)
        logger.info(f"Current memory usage: {process_mem_mb:.0f}MB / {available_memory_mb or '?'}MB allocated")
    except Exception:
        pass
    
    # 2. Setup networking
    from neuroshard.core.network.nat import NATTraverser
    nat = NATTraverser()
    
    ip_addr = announce_ip or nat.discover_public_ip() or get_public_ip() or get_local_ip()
    
    # UPnP mapping
    nat.attempt_upnp_mapping(port, "TCP", "NeuroShard HTTP")
    nat.attempt_upnp_mapping(port + 1000, "TCP", "NeuroShard gRPC")
    
    final_announce_port = announce_port or port
    logger.info(f"Announcing as: {ip_addr}:{final_announce_port}")
    
    my_url = f"http://{ip_addr}:{final_announce_port}"
    
    # For dynamic model, shard_range is just a marker
    shard_range = f"dynamic-{len(NEURO_NODE.my_layer_ids)}-layers"
    STATE["shard_range"] = shard_range
    
    # Set node role info for PoNW reward calculation
    STATE["assigned_layers"] = NEURO_NODE.my_layer_ids
    STATE["has_embedding"] = NEURO_NODE.model.has_embedding
    STATE["has_lm_head"] = NEURO_NODE.model.has_lm_head
    
    # 3. Initialize P2P
    P2P = P2PManager(my_url, shard_range, tracker, node_token=node_token)
    P2P.state_ref = STATE
    
    # 4. Connect P2P to NeuroNode
    NEURO_NODE.connect_p2p(P2P)
    logger.info(f"Connected to P2P network for distributed training")
    
    # 4b. Start Swarm components
    if hasattr(NEURO_NODE, 'start_swarm_sync'):
        logger.info("[SWARM] Starting swarm components...")
        NEURO_NODE.start_swarm_sync()
        logger.info("[SWARM] Swarm components started")
    
    # 5. Start gRPC Server
    start_grpc_background(port, NEURO_NODE, P2P, None)
    
    # 5. Background tasks (runs every 1 second)
    def background_tasks():
        # CONTINUOUS TRAINING with USER-DEFINED THROTTLING
        # Respects user's CPU AND RAM limits to allow background operation without hogging resources
        # Settings are re-read each iteration so changes take effect immediately!
        
        import psutil
        
        # Store initial limits (can be updated via API)
        STATE["config_cpu_threads"] = max_cpu_threads
        STATE["config_memory_mb"] = available_memory_mb
        
        total_cpu_cores = psutil.cpu_count() or 4
        total_ram_mb = psutil.virtual_memory().total / (1024 * 1024)
        last_throttle_log = 0
        
        def calculate_throttle():
            """Calculate throttle settings from current config (allows live updates)."""
            # Read current config (can be updated via API while running)
            user_cpu_limit = STATE.get("config_cpu_threads") or total_cpu_cores
            user_ram_limit = STATE.get("config_memory_mb") or (total_ram_mb * 0.7)
            
            cpu_ratio = min(1.0, user_cpu_limit / total_cpu_cores)
            ram_ratio = min(1.0, user_ram_limit / total_ram_mb)
            resource_ratio = min(cpu_ratio, ram_ratio)
            
            base_interval = 2
            interval = max(base_interval, base_interval / max(0.1, resource_ratio))
            max_steps = max(5, int(30 * resource_ratio))
            
            # Store for API access
            STATE["throttle_cpu_ratio"] = cpu_ratio
            STATE["throttle_ram_ratio"] = ram_ratio
            STATE["throttle_effective"] = resource_ratio
            STATE["throttle_interval"] = interval
            STATE["throttle_max_steps"] = max_steps
            
            return interval, max_steps, resource_ratio
        
        # Initial calculation and log
        min_interval_between_steps, max_steps_per_minute, resource_ratio = calculate_throttle()
        logger.info(f"[NODE] Training throttle: effective={resource_ratio*100:.0f}%, "
              f"interval={min_interval_between_steps:.1f}s, max={max_steps_per_minute} steps/min")
        
        last_train_complete = 0
        # BUGFIX: Initialize to current values (may be >0 if loaded from checkpoint)
        last_tokens = NEURO_NODE.total_tokens_processed if NEURO_NODE else 0
        last_training_rounds = NEURO_NODE.total_training_rounds if NEURO_NODE else 0
        training_in_progress = False
        consecutive_data_not_ready = 0
        steps_this_minute = 0
        training_step_count = 0  # Track total steps for logging
        minute_start = time.time()
        last_memory_report = 0  # For periodic memory usage logging
        
        while not _SHUTDOWN_REQUESTED.is_set():
            now = time.time()
            
            # Reset per-minute counter
            if now - minute_start >= 60:
                steps_this_minute = 0
                minute_start = now
            
            # RE-CALCULATE THROTTLE periodically (allows live config changes)
            # Only recalculate every 5 seconds to avoid overhead
            if now - last_throttle_log >= 5:
                new_interval, new_max_steps, new_ratio = calculate_throttle()
                # Log only if changed significantly
                if abs(new_ratio - resource_ratio) > 0.05:
                    logger.info(f"[NODE] Throttle updated: {new_ratio*100:.0f}% "
                          f"(interval={new_interval:.1f}s, max={new_max_steps}/min)")
                min_interval_between_steps = new_interval
                max_steps_per_minute = new_max_steps
                resource_ratio = new_ratio
                last_throttle_log = now
            
            # Update peer count
            STATE["peer_count"] = len(P2P.known_peers)
            
            # PERIODIC MEMORY REPORT (every 60 seconds)
            if now - last_memory_report >= 60:
                try:
                    import os
                    process = psutil.Process(os.getpid())
                    process_mem_mb = process.memory_info().rss / (1024 * 1024)
                    memory_limit = STATE.get("config_memory_mb") or available_memory_mb
                    system_mem = psutil.virtual_memory()
                    
                    logger.info(f"[NODE] Memory: process={process_mem_mb:.0f}MB / {memory_limit or '?'}MB limit, "
                          f"system={system_mem.percent:.0f}% ({system_mem.used/(1024**3):.1f}GB / {system_mem.total/(1024**3):.1f}GB)")
                    
                    # Show component breakdown if training
                    if hasattr(NEURO_NODE, 'genesis_loader') and NEURO_NODE.genesis_loader:
                        loader = NEURO_NODE.genesis_loader
                        num_loaded = len(loader.loaded_shards)
                        num_prefetched = len(loader._prefetch_ready)
                        logger.info(f"[NODE] Genesis cache: {num_loaded} loaded + {num_prefetched} prefetched shards")
                    
                    last_memory_report = now
                except Exception:
                    pass
            
            # Update token count and training batches from node
            current_tokens = NEURO_NODE.total_tokens_processed
            current_training = NEURO_NODE.total_training_rounds
                
            # Add DELTA to STATE counters (for PoNW proof calculation)
            # NOTE: last_tokens/last_training_rounds are initialized to current values
            # at startup to handle checkpoint loading correctly
            STATE["token_count"] = STATE.get("token_count", 0) + (current_tokens - last_tokens)
            STATE["training_batches"] = STATE.get("training_batches", 0) + (current_training - last_training_rounds)
            
            last_tokens = current_tokens
            last_training_rounds = current_training
            
            # Store totals for display
            STATE["total_tokens_processed"] = current_tokens
            STATE["total_training_rounds"] = current_training
        
            # Session cleanup
            to_remove = [sid for sid, ts in SESSION_TIMESTAMPS.items() if now - ts > 300]
            for sid in to_remove:
                del SESSION_TIMESTAMPS[sid]
            
            # Marketplace cleanup (every 60 seconds)
            if int(now) % 60 == 0:
                market = P2P.ledger.inference_market
                # Cleanup stale claims
                stale = market.cleanup_stale_claims()
                if stale > 0:
                    logger.info(f"[MARKET] Cleaned up {stale} stale claims")
                # Cleanup old results
                market.cleanup_old_results()
            
            # CONTINUOUS TRAINING with smart throttling:
            # 1. Training must be enabled
            # 2. NEURO_NODE must exist  
            # 3. No training currently in progress
            # 4. Minimum interval since last step (for system responsiveness)
            # 5. Haven't exceeded max steps per minute (optional throttle)
            should_train = (
                enable_training and 
                not training_in_progress and
                (now - last_train_complete) >= min_interval_between_steps and
                steps_this_minute < max_steps_per_minute
            )
            
            if should_train:
                # ENFORCE MEMORY LIMIT: Check if node is using too much RAM
                try:
                    import os
                    process = psutil.Process(os.getpid())
                    process_mem_mb = process.memory_info().rss / (1024 * 1024)
                    memory_limit = STATE.get("config_memory_mb") or available_memory_mb
                    
                    if memory_limit and process_mem_mb > memory_limit * 1.2:  # 20% over limit
                        logger.warning(f"[NODE] Memory limit exceeded: using {process_mem_mb:.0f}MB / {memory_limit}MB limit")
                        logger.info(f"[NODE] Clearing caches to reduce memory...")
                        
                        # Clear loaded shards (keep only current one)
                        if hasattr(NEURO_NODE, 'genesis_loader') and NEURO_NODE.genesis_loader:
                            loader = NEURO_NODE.genesis_loader
                            current_shard = loader.assigned_shard_ids[loader.current_shard_idx % len(loader.assigned_shard_ids)] if loader.assigned_shard_ids else None
                            
                            # Clear all but current shard
                            shards_to_remove = [sid for sid in loader.loaded_shards.keys() if sid != current_shard]
                            for sid in shards_to_remove:
                                del loader.loaded_shards[sid]
                            loader._prefetch_ready.clear()
                            
                            logger.info(f"[NODE] Cleared {len(shards_to_remove)} cached shards")
                        
                        # Force garbage collection
                        import gc
                        gc.collect()
                        
                        # Clear GPU cache
                        if NEURO_NODE.device == "cuda":
                            torch.cuda.empty_cache()
                        elif NEURO_NODE.device == "mps":
                            torch.mps.empty_cache()
                        
                        # Skip this training step
                        time.sleep(2)
                        continue
                except Exception:
                    pass
                
                # Check if data is ready (non-blocking)
                data_ready = False
                if hasattr(NEURO_NODE, 'genesis_loader') and NEURO_NODE.genesis_loader:
                    data_ready = NEURO_NODE.genesis_loader.is_data_ready()
                    # Show shard download status periodically
                    if not data_ready and consecutive_data_not_ready % 5 == 0:
                        stats = NEURO_NODE.genesis_loader.get_stats()
                        logger.info(f"[GENESIS] Status: assigned={stats.get('assigned_shards', 0)} shards, "
                              f"loaded={stats.get('loaded_shards', 0)}, "
                              f"prefetching={stats.get('prefetch_in_progress', 0)}")
                    elif data_ready and training_step_count == 0:
                        logger.info(f"[GENESIS] Data ready! Starting first training step...")
                        training_step_count = 1  # Prevent repeat message
                else:
                    # No genesis loader yet - first training step will create it
                    data_ready = True
                
                if data_ready or consecutive_data_not_ready > 3:
                    training_in_progress = True
                    consecutive_data_not_ready = 0
                    step_start = time.time()
                    
                    STATE["training_status"] = "running"
                    
                    try:
                        loss = NEURO_NODE.train_step()
                        step_duration = time.time() - step_start
                        
                        if loss is not None:
                            steps_this_minute += 1
                            training_step_count += 1
                            # Log every step with timing info
                            logger.info(f"[NODE] Training step #{NEURO_NODE.total_training_rounds}: "
                                  f"loss={loss:.4f} ({step_duration:.1f}s)")
                            STATE["training_status"] = "idle"
                            STATE["last_loss"] = loss
                        else:
                            # train_step returned None - log why
                            logger.info(f"[NODE] Training step returned None (took {step_duration:.1f}s)")
                            STATE["training_status"] = "waiting_for_data"
                            
                    except RuntimeError as e:
                        error_msg = str(e).lower()
                        if "not ready" in error_msg:
                            if consecutive_data_not_ready == 0:
                                logger.info(f"[NODE] Waiting for Genesis data to download...")
                                if hasattr(NEURO_NODE, 'genesis_loader') and NEURO_NODE.genesis_loader:
                                    stats = NEURO_NODE.genesis_loader.get_stats()
                                    logger.info(f"[GENESIS] Downloading shard... "
                                          f"(assigned: {stats.get('assigned_shards', '?')}, "
                                          f"loaded: {stats.get('loaded_shards', 0)}, "
                                          f"prefetching: {stats.get('prefetch_in_progress', 0)})")
                            STATE["training_status"] = "loading_data"
                            consecutive_data_not_ready += 1
                        elif "genesis loader init failed" in error_msg or "manifest" in error_msg:
                            # Genesis loader initialization error - show details
                            logger.error(f"[GENESIS] ERROR: {e}")
                            STATE["training_status"] = "genesis_error"
                            # Don't spam - wait before retrying
                            time.sleep(10)
                        else:
                            logger.error(f"[NODE] Training error: {e}")
                            STATE["training_status"] = "error"
                    except Exception as e:
                        logger.error(f"[NODE] Training error: {e}")
                        STATE["training_status"] = "error"
                    
                    training_in_progress = False
                    last_train_complete = time.time()
                else:
                    consecutive_data_not_ready += 1
                    if consecutive_data_not_ready == 1:
                        logger.info(f"[NODE] Waiting for training data to load...")
            
            # Heartbeat for layers (only every 10 seconds to reduce overhead)
            if int(now) % 10 == 0 and NEURO_NODE.layer_pool:
                NEURO_NODE.layer_pool.heartbeat(NEURO_NODE.node_id, NEURO_NODE.my_layer_ids)
                
                # Cleanup stale layer assignments (every 60 seconds)
                if int(now) % 60 == 0:
                    removed = NEURO_NODE.layer_pool.cleanup_stale_assignments()
                    if removed > 0:
                        logger.info(f"[LAYER_POOL] Cleaned up {removed} stale layer assignments")
            
            # RESOURCE-AWARE SLEEP: Adjust based on system load
            # This ensures we're a good citizen when running in the background
            try:
                current_cpu = psutil.cpu_percent(interval=None)  # Non-blocking
                current_mem = psutil.virtual_memory().percent
                
                # If system is under heavy load (not from us), back off
                if current_cpu > 90 or current_mem > 90:
                    time.sleep(5)  # Back off significantly if system is stressed
                    continue
                    
                # Dynamic sleep based on activity and user's CPU setting
                if training_in_progress:
                    time.sleep(0.1)  # Fast loop during active training
                elif 'data_ready' in dir() and data_ready:
                    # Ready to train - use interval based on CPU ratio
                    time.sleep(min_interval_between_steps * 0.5)
                else:
                    time.sleep(1)  # Slower loop when idle/waiting
            except:
                time.sleep(1)  # Fallback if psutil fails
    
    threading.Thread(target=background_tasks, daemon=True).start()
    
    # DRIVER WORKER LOOP: Poll marketplace AND process requests
    def driver_worker_loop():
        """
        PRODUCTION-READY Driver Worker Loop
        
        1. Polls marketplace for pending requests
        2. Claims requests assigned to this driver
        3. Waits for encrypted prompt from user
        4. Processes inference through distributed pipeline
        5. Submits PoNW proof for rewards
        """
        import time
        
        # Check if this node is a driver
        is_driver = NEURO_NODE and NEURO_NODE.model.has_embedding
        
        if not is_driver:
            logger.info("[DRIVER] Not a driver node - skipping marketplace worker loop")
            return
        
        logger.info("[DRIVER] Starting PRODUCTION marketplace worker loop...")
        logger.info(f"[DRIVER] Will poll for requests assigned to: {NEURO_NODE.node_id[:16]}...")
        
        # Import encrypted prompt handling
        from neuroshard.core.network.encrypted_channel import PromptEncryption, PromptQueue
        
        prompt_queue = PromptQueue()
        
        # Store in node for API access
        NEURO_NODE.prompt_queue = prompt_queue
        
        last_claim_attempt = 0
        processing_requests = {}  # request_id -> asyncio.Task
        
        def process_request(request_id: str):
            """Process a single inference request using existing distributed inference."""
            try:
                # Get marketplace request for parameters
                market = P2P.ledger.inference_market
                
                market_request = market.get_request(request_id)
                if not market_request:
                    logger.warning(f"[DRIVER] ✗ Request {request_id[:8]}... not found in marketplace")
                    return
                
                # Get encrypted prompt
                encrypted_prompt = prompt_queue.get_prompt(request_id)
                
                if not encrypted_prompt:
                    logger.warning(f"[DRIVER] ✗ No prompt found for {request_id[:8]}...")
                    return
                
                # Decrypt prompt
                try:
                    prompt_text = PromptEncryption.decrypt_prompt(
                        encrypted_prompt.encrypted_data,
                        request_id
                    )
                    logger.info(f"[DRIVER] ✓ Decrypted prompt: '{prompt_text[:50]}...'")
                except Exception as e:
                    logger.error(f"[DRIVER] ✗ Failed to decrypt prompt: {e}")
                    return
                
                # Process using EXISTING distributed inference
                try:
                    output = NEURO_NODE.generate(
                        prompt=prompt_text,
                        max_new_tokens=market_request.tokens_requested,
                        temperature=0.8
                    )
                    
                    logger.info(f"[DRIVER] ✓ Generated: '{output[:100]}...'")
                    logger.info(f"[DRIVER] ✓ Request {request_id[:8]}... completed")
                    processing_requests[request_id] = "completed"
                    
                    # Store result in marketplace
                    market.store_result(request_id, output)
                    
                except Exception as e:
                    logger.error(f"[DRIVER] ✗ Generation failed: {e}")
                    import traceback
                    traceback.print_exc()
                    processing_requests[request_id] = "failed"
                    
            except Exception as e:
                logger.error(f"[DRIVER] ✗ Error processing {request_id[:8]}...: {e}")
                import traceback
                logger.error(traceback.format_exc())
                processing_requests[request_id] = "failed"
        
        while not _SHUTDOWN_REQUESTED.is_set():
            now = time.time()
            
            # STEP 1: Poll marketplace for new requests (every 5 seconds)
            if now - last_claim_attempt >= 5:
                try:
                    market = P2P.ledger.inference_market
                    
                    # Try to claim a request
                    request = market.claim_request(NEURO_NODE.node_id)
                    
                    if request:
                        logger.info(f"[DRIVER] ✓ Claimed request {request.request_id[:8]}... "
                              f"({request.tokens_requested} tokens @ {request.locked_price:.6f} NEURO/1M)")
                        
                        # Start pipeline session
                        market.start_pipeline_session(
                            request_id=request.request_id,
                            session_id=request.pipeline_session_id,
                            driver_node_id=NEURO_NODE.node_id
                        )
                        
                        # Check if we already have the prompt
                        if prompt_queue.has_prompt(request.request_id):
                            logger.info(f"[DRIVER] ✓ Prompt already received, processing immediately")
                            # Process immediately
                            process_request(request.request_id)
                        else:
                            logger.info(f"[DRIVER] Waiting for encrypted prompt from user...")
                            logger.info(f"[DRIVER] User should POST to /api/driver/prompt/{request.request_id[:8]}...")
                            processing_requests[request.request_id] = None  # Mark as waiting
                                    
                except Exception as e:
                    if "not found" not in str(e).lower():
                        logger.error(f"[DRIVER] Marketplace poll error: {e}")
                
                last_claim_attempt = now
            
            # STEP 2: Check for prompts that arrived for waiting requests
            for request_id in list(processing_requests.keys()):
                if processing_requests[request_id] is None:  # Waiting for prompt
                    if prompt_queue.has_prompt(request_id):
                        logger.info(f"[DRIVER] ✓ Prompt received for {request_id[:8]}..., starting processing")
                        # Process (uses existing distributed inference)
                        process_request(request_id)
                        processing_requests[request_id] = "processing"  # Mark as processing
            
            # STEP 3: Cleanup finished requests
            for request_id in list(processing_requests.keys()):
                if processing_requests[request_id] == "completed":
                    del processing_requests[request_id]
            
            # STEP 4: Cleanup old prompts
            prompt_queue.cleanup_old_prompts()
            
            time.sleep(1)  # Fast loop for responsiveness
    
    # Start driver worker loop if this is a driver node
    if NEURO_NODE and NEURO_NODE.model.has_embedding:
        threading.Thread(target=driver_worker_loop, daemon=True).start()
    
    # 6. Run HTTP Server
    logger.info("=" * 50)
    logger.info("NeuroShard Node Ready!")
    logger.info(f"   My Layers: {NEURO_NODE.my_layer_ids}")
    logger.info(f"   My Params: {NEURO_NODE.model.get_num_params() / 1e6:.1f}M")
    logger.info(f"   Embedding: {NEURO_NODE.model.has_embedding}")
    logger.info(f"   LM Head: {NEURO_NODE.model.has_lm_head}")
    logger.info(f"   Training: {'Enabled' if enable_training else 'Disabled'}")
    logger.info(f"   DiLoCo: sync every {diloco_inner_steps} steps")
    logger.info("=" * 50)
    logger.info("TRULY DECENTRALIZED: Model grows with network capacity!")
    logger.info("=" * 50)
    
    # Custom log config: disable access logs and customize startup messages
    # Handle Windows GUI mode where stdout may be None
    if sys.stdout is not None and hasattr(sys.stdout, 'write'):
        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {"format": "[NODE] %(message)s"},
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.StreamHandler",
                    "stream": "ext://sys.stdout",
                },
            },
            "loggers": {
                # Suppress uvicorn's default startup messages (including "Press CTRL+C")
                "uvicorn": {"handlers": ["default"], "level": "WARNING", "propagate": False},
                "uvicorn.error": {"handlers": ["default"], "level": "WARNING", "propagate": False},
                "uvicorn.access": {"handlers": [], "level": "CRITICAL", "propagate": False},
            },
        }
    else:
        # Fallback to file logging when stdout is unavailable (Windows frozen GUI)
        log_dir = os.path.join(os.path.expanduser("~"), ".neuroshard")
        log_file = os.path.join(log_dir, "uvicorn.log")
        log_config = {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {
                "default": {"format": "[NODE] %(message)s"},
            },
            "handlers": {
                "default": {
                    "formatter": "default",
                    "class": "logging.handlers.RotatingFileHandler",
                    "filename": log_file,
                    "maxBytes": 5*1024*1024,
                    "backupCount": 2,
                    "encoding": "utf-8",
                },
            },
            "loggers": {
                # Suppress uvicorn's default startup messages
                "uvicorn": {"handlers": ["default"], "level": "WARNING", "propagate": False},
                "uvicorn.error": {"handlers": ["default"], "level": "WARNING", "propagate": False},
                "uvicorn.access": {"handlers": [], "level": "CRITICAL", "propagate": False},
            },
        }
    
    # Use Server object so we can stop it from outside (GUI shutdown)
    global _UVICORN_SERVER
    config = uvicorn.Config(node_app, host="0.0.0.0", port=port, log_config=log_config)
    _UVICORN_SERVER = uvicorn.Server(config)
    
    # Print our own clean startup message (without "Press CTRL+C")
    logger.info(f"[NODE] HTTP server started on port {port}")
    
    _UVICORN_SERVER.run()


def main():
    parser = argparse.ArgumentParser(description="NeuroShard Node Runner - Truly Decentralized LLM")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--tracker", type=str, default="https://neuroshard.com/api/tracker")
    parser.add_argument("--token", type=str, default=None, 
                       help="Node Token OR 12-word mnemonic phrase for wallet access")
    parser.add_argument("--announce-ip", type=str, default=None, help="Force IP address to announce")
    parser.add_argument("--announce-port", type=int, default=None, help="Force port to announce")
    parser.add_argument("--no-training", action="store_true", help="Disable training (inference only)")
    parser.add_argument("--memory", type=int, default=None, 
                       help="Override detected memory (MB) - for testing")
    parser.add_argument("--max-storage", type=int, default=100,
                       help="Max disk space for training data (MB)")
    parser.add_argument("--cpu-threads", type=int, default=None,
                       help="Max CPU threads to use")
    parser.add_argument("--diloco-steps", type=int, default=500,
                       help="DiLoCo inner steps before gradient sync (default: 500)")
    
    args = parser.parse_args()
    
    # Handle mnemonic input: If token is 12 words, convert to token
    node_token = args.token
    if node_token:
        words = node_token.strip().split()
        if len(words) == 12:
            # It's a BIP39 mnemonic - derive token from it
            try:
                from mnemonic import Mnemonic
                mnemo = Mnemonic("english")
                if mnemo.check(node_token):
                    # Convert mnemonic to deterministic token
                    seed = mnemo.to_seed(node_token, passphrase="")
                    node_token = seed[:32].hex()  # Use first 32 bytes as token
                    logger.info("✅ Wallet recovered from mnemonic")
                else:
                    logger.warning("⚠️  Invalid mnemonic phrase - treating as raw token")
            except ImportError:
                logger.warning("⚠️  'mnemonic' package not installed - treating as raw token")
            except Exception as e:
                logger.warning(f"⚠️  Mnemonic error: {e} - treating as raw token")
    
    run_node(
        port=args.port,
        tracker=args.tracker,
        node_token=node_token,
        announce_ip=args.announce_ip,
        announce_port=args.announce_port,
        enable_training=not args.no_training,
        available_memory_mb=args.memory,
        max_storage_mb=args.max_storage,
        max_cpu_threads=args.cpu_threads,
        diloco_inner_steps=args.diloco_steps,
    )


if __name__ == "__main__":
    main()
