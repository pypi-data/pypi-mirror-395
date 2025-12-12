# neuroshard/core/training/__init__.py
"""
Training coordination components for NeuroShard.

- distributed: TrainingCoordinator, FederatedDataManager, GenesisDataLoader
- production: ProductionTrainer
- allreduce: AllReduceManager, AllReduceOp
- checkpoint: CheckpointShardManager
"""

__all__ = [
    'TrainingCoordinator',
    'FederatedDataManager',
    'GenesisDataLoader',
    'ProductionTrainer',
    'AllReduceManager',
    'AllReduceOp',
    'CheckpointShardManager',
]

def __getattr__(name):
    """Lazy loading of submodules."""
    if name in ('TrainingCoordinator', 'FederatedDataManager', 'GenesisDataLoader', 'GradientContribution'):
        from neuroshard.core.training import distributed
        return getattr(distributed, name)
    elif name == 'ProductionTrainer':
        from neuroshard.core.training.production import ProductionTrainer
        return ProductionTrainer
    elif name in ('AllReduceManager', 'AllReduceOp'):
        from neuroshard.core.training import allreduce
        return getattr(allreduce, name)
    elif name == 'CheckpointShardManager':
        from neuroshard.core.training.checkpoint import CheckpointShardManager
        return CheckpointShardManager
    raise AttributeError(f"module 'neuroshard.core.training' has no attribute '{name}'")
