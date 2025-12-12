"""
NEURO Token Economics - Centralized Configuration

This module defines ALL economic constants for the NeuroShard network.
All values are documented and should be referenced from here, not hardcoded elsewhere.

=============================================================================
DESIGN PRINCIPLES
=============================================================================

1. TRAINING DOMINATES: Training rewards are the highest to incentivize 
   actual model improvement over passive participation.

2. WORK BEFORE STAKE: Base rewards come from actual work (compute).
   Staking only provides a multiplier, not base rewards.

3. DIMINISHING RETURNS: Stake multipliers use logarithmic scaling to
   prevent rich-get-richer dynamics.

4. DEFLATIONARY: 5% of all spending is burned, creating scarcity.

5. SECURITY: Multiple caps and limits prevent economic attacks.

=============================================================================
"""

# =============================================================================
# REWARD RATES
# =============================================================================

# UPTIME REWARD (minimal - discourages idle farming)
# Goal: Minimal passive income, forces users to train for real rewards
UPTIME_REWARD_PER_MINUTE = 0.0001   # 0.0001 NEURO per minute
                                     # ~0.14 NEURO/day idle (80% reduction)

# TRAINING REWARD (dominant - this is the core value!)
# Goal: Strong incentive for active training, covers electricity + profit
TRAINING_REWARD_PER_BATCH = 0.0005  # 0.0005 NEURO per training batch
                                     # 60 batches/min = 0.03 NEURO/min = ~43 NEURO/day
                                     # Training earns 300x more than idle!

# DATA SERVING REWARD (for nodes serving training shards)
DATA_REWARD_PER_SAMPLE = 0.00001    # 0.00001 NEURO per data sample served

# INFERENCE REWARD (PURE MARKET-BASED PRICING)
# Goal: Let supply/demand discover the true price
# No artificial caps - market determines value based on model quality via demand
# Quality is implicit: stupid model = no demand = low price, good model = high demand = high price

# Dynamic Market Parameters
INFERENCE_MARKET_PRICE_SMOOTHING = 0.8    # EMA smoothing (higher = smoother price changes)
INFERENCE_MARKET_CAPACITY_TIMEOUT = 60    # Seconds before stale capacity expires
INFERENCE_MARKET_TARGET_RESPONSE_TIME = 60  # Target seconds to serve requests
INFERENCE_MARKET_BASE_PRICE = 0.0001      # Starting price (bootstrap with worthless model)

# =============================================================================
# ROLE DISTRIBUTION (for inference rewards)
# =============================================================================

# Role shares for inference (must sum to 1.0)
DRIVER_SHARE = 0.15                 # 15% - Tokenization, embedding, request routing
WORKER_SHARE = 0.70                 # 70% - Heavy computation (split by layers)
VALIDATOR_SHARE = 0.15              # 15% - Output projection, loss calc, response

# Role bonuses (multipliers on base rewards)
DRIVER_BONUS = 1.2                  # 20% bonus for being entry point
VALIDATOR_BONUS = 1.3               # 30% bonus for being exit point + proof validation
WORKER_LAYER_BONUS = 0.05           # 5% bonus per layer held (Increased to incentivize storage)
MAX_LAYER_BONUS = 1.0               # Cap layer bonus at 100% (Allow full nodes to earn 2x)

# Training bonus (extra incentive for training participation)
TRAINING_BONUS = 1.1                # 10% bonus when actively training (Lowered as base reward covers it)

# =============================================================================
# STAKING ECONOMICS
# =============================================================================

# Stake multiplier formula: 1.0 + STAKING_BASE_BONUS * log2(1 + stake / STAKING_UNIT)
STAKING_BASE_BONUS = 0.1            # Base 10% bonus coefficient
STAKING_UNIT = 1000.0               # Staking calculated per 1000 NEURO
STAKING_DIMINISHING = True          # Use logarithmic diminishing returns

# Staking limits
MIN_STAKE_AMOUNT = 1.0              # Minimum stake amount (1 NEURO)
MAX_STAKE_AMOUNT = 10_000_000.0     # Maximum stake amount (10M NEURO)
MIN_STAKE_DURATION_DAYS = 1         # Minimum lock period (1 day)
MAX_STAKE_DURATION_DAYS = 365       # Maximum lock period (1 year)

# =============================================================================
# VALIDATOR REQUIREMENTS
# =============================================================================

VALIDATOR_MIN_STAKE = 100.0         # Minimum stake to be a Validator (100 NEURO)
VALIDATOR_MIN_MEMORY_MB = 2000      # Minimum memory for Validator (2GB)

# Validation rewards
VALIDATION_FEE_PER_PROOF = 0.001    # 0.001 NEURO per proof validated
VALIDATION_CONSENSUS_THRESHOLD = 0.66  # 66% stake-weighted agreement required

# Validator selection
VALIDATOR_ROTATION_ENABLED = True   # Enable random validator selection
VALIDATOR_SELECTION_RANDOMNESS = 0.3  # 30% randomness in selection

# Remote proof security (limits impact of fake stake claims)
REMOTE_STAKE_MULTIPLIER_CAP = 1.5   # Max multiplier for remote proofs

# =============================================================================
# FEE BURN (Deflationary Mechanism)
# =============================================================================

FEE_BURN_RATE = 0.05                # 5% of spending fees are burned
BURN_ADDRESS = "BURN_0x0000000000000000000000000000000000000000"

# =============================================================================
# ANTI-CHEAT LIMITS
# =============================================================================

MAX_UPTIME_PER_PROOF = 120          # Max 2 minutes per proof (prevents inflation)
MAX_TOKENS_PER_MINUTE = 1_000_000   # Max 1M tokens/minute (modern GPUs can do this)
MAX_PROOFS_PER_HOUR = 120           # Max 2 proofs per minute sustained
PROOF_FRESHNESS_WINDOW = 300        # Proofs valid for 5 minutes

# =============================================================================
# SLASHING
# =============================================================================

SLASH_AMOUNT = 10.0                 # NEURO slashed for fraud
WHISTLEBLOWER_REWARD_RATE = 0.5     # 50% of slash goes to reporter
VALIDATOR_SLASH_MULTIPLIER = 2.0    # Validators slashed 2x for bad validation

# =============================================================================
# SUPPLY LIMITS
# =============================================================================

# There is NO hard cap on total supply - NEURO is minted through PoNW
# However, deflationary mechanics (burn) and diminishing rewards create scarcity
MAX_REWARD_PER_PROOF = 100.0        # Cap on single proof reward (sanity check)
MAX_DAILY_MINT_PER_NODE = 10_000.0  # Cap on daily minting per node

# =============================================================================
# GENESIS
# =============================================================================

GENESIS_SUPPLY = 0.0                # Zero pre-mine - all NEURO is earned
GENESIS_SIGNATURE = "GENESIS_BLOCK"

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

import math


def calculate_stake_multiplier(stake: float) -> float:
    """
    Calculate stake multiplier with diminishing returns.
    
    Formula: 1.0 + STAKING_BASE_BONUS * log2(1 + stake / STAKING_UNIT)
    
    Examples:
    - 0 NEURO = 1.00x
    - 1,000 NEURO = 1.10x
    - 2,000 NEURO = 1.16x
    - 10,000 NEURO = 1.35x
    - 100,000 NEURO = 1.66x
    """
    if stake <= 0:
        return 1.0
    
    if STAKING_DIMINISHING:
        return 1.0 + STAKING_BASE_BONUS * math.log2(1 + stake / STAKING_UNIT)
    else:
        # Linear (legacy)
        return 1.0 + (STAKING_BASE_BONUS * (stake / STAKING_UNIT))


def calculate_layer_bonus(layers_held: int) -> float:
    """
    Calculate layer bonus for workers.
    
    Formula: min(MAX_LAYER_BONUS, layers_held * WORKER_LAYER_BONUS)
    """
    return min(MAX_LAYER_BONUS, layers_held * WORKER_LAYER_BONUS)


def calculate_burn_amount(spend_amount: float) -> float:
    """Calculate the burn amount for a transaction."""
    return spend_amount * FEE_BURN_RATE


def is_valid_stake_amount(amount: float) -> tuple:
    """
    Validate a stake amount.
    
    Returns: (is_valid, error_message)
    """
    if amount < MIN_STAKE_AMOUNT:
        return False, f"Minimum stake is {MIN_STAKE_AMOUNT} NEURO"
    if amount > MAX_STAKE_AMOUNT:
        return False, f"Maximum stake is {MAX_STAKE_AMOUNT:,.0f} NEURO"
    return True, ""


def is_valid_stake_duration(days: int) -> tuple:
    """
    Validate a stake duration.
    
    Returns: (is_valid, error_message)
    """
    if days < MIN_STAKE_DURATION_DAYS:
        return False, f"Minimum lock period is {MIN_STAKE_DURATION_DAYS} day(s)"
    if days > MAX_STAKE_DURATION_DAYS:
        return False, f"Maximum lock period is {MAX_STAKE_DURATION_DAYS} days"
    return True, ""


def is_eligible_validator(stake: float, memory_mb: float = None) -> tuple:
    """
    Check if a node is eligible to be a validator.
    
    Returns: (is_eligible, reason)
    """
    if stake < VALIDATOR_MIN_STAKE:
        return False, f"Insufficient stake: {stake:.2f} < {VALIDATOR_MIN_STAKE} NEURO"
    
    if memory_mb is not None and memory_mb < VALIDATOR_MIN_MEMORY_MB:
        return False, f"Insufficient memory: {memory_mb:.0f}MB < {VALIDATOR_MIN_MEMORY_MB}MB"
    
    return True, f"Eligible with {stake:.2f} NEURO staked"


# =============================================================================
# SUMMARY TABLE (for reference)
# =============================================================================
"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                        NEURO ECONOMICS SUMMARY (v2)                            ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ EARNING NEURO                                                                  ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ Activity          │ Rate                    │ Daily (Active)                   ║
║───────────────────┼─────────────────────────┼──────────────────────────────────║
║ Training          │ 0.0005 NEURO/batch      │ ~43 NEURO (60 batch/min)         ║
║ Inference         │ DYNAMIC (0.01-1.0)      │ Market-based (supply/demand)     ║
║ Data Serving      │ 0.00001 NEURO/sample    │ Variable                         ║
║ Uptime (idle)     │ 0.0001 NEURO/min        │ ~0.14 NEURO                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ REALISTIC DAILY EARNINGS (with bonuses)                                       ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ Idle node         │ ~0.14 NEURO/day         │ Just uptime (unprofitable)       ║
║ Light training    │ ~10-20 NEURO/day        │ Few hours active (Raspberry Pi)  ║
║ Active trainer    │ ~40-60 NEURO/day        │ 24/7 training (Gaming PC)        ║
║ Power user        │ ~200-350 NEURO/day      │ 24/7 + GPU + staking (Server)    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ MULTIPLIERS                                                                    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ Staking           │ log2(1 + stake/1000)    │ 1.10x @ 1K, 1.66x @ 100K        ║
║ Training Bonus    │ +10%                    │ When actively training           ║
║ Driver Bonus      │ +20%                    │ Holding Layer 0                  ║
║ Validator Bonus   │ +30%                    │ Holding Last Layer + 100 stake   ║
║ Layer Bonus       │ +5% per layer           │ Max 100%                         ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ REQUIREMENTS                                                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ Validator         │ 100 NEURO stake         │ + 2GB memory                     ║
║ Stake Min/Max     │ 1 / 10,000,000 NEURO    │                                  ║
║ Lock Period       │ 1 - 365 days            │                                  ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ FEES & BURNS                                                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║ Transaction Fee   │ 5% burned               │ Deflationary                     ║
║ Fraud Slash       │ 10 NEURO                │ 50% to reporter, 50% burned      ║
║ Validator Slash   │ 20 NEURO (2x)           │ 100% burned                      ║
╚═══════════════════════════════════════════════════════════════════════════════╝
"""

