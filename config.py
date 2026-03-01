# -*- coding: utf-8 -*-
"""
NFT Yield Farming — configuration management.
Handles network selection, RPC endpoints, contract addresses, and staking parameters.
"""
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional


_BASE_DIR = Path(__file__).resolve().parent
_CONFIG_FILE = _BASE_DIR / "farming_config.json"


BSC_MAINNET_RPC = "https://bsc-dataseed1.binance.org"
BSC_TESTNET_RPC = "https://data-seed-prebsc-1-s1.binance.org:8545"

DEFAULT_GAS_LIMIT = 300000
DEFAULT_GAS_PRICE_GWEI = 5
DEFAULT_SLIPPAGE_PCT = 0.5
DEFAULT_POLL_INTERVAL = 15


@dataclass
class FarmingConfig:
    network: str = "bsc-testnet"
    rpc_url: str = BSC_TESTNET_RPC
    chain_id: int = 97
    gas_limit: int = DEFAULT_GAS_LIMIT
    gas_price_gwei: int = DEFAULT_GAS_PRICE_GWEI
    slippage_percent: float = DEFAULT_SLIPPAGE_PCT
    poll_interval_seconds: int = DEFAULT_POLL_INTERVAL
    governance_token_symbol: str = "GOV"
    lp_token_address: Optional[str] = None
    farm_contract_address: Optional[str] = None
    nft_pool_address: Optional[str] = None
    wallet_address: Optional[str] = None
    auto_compound: bool = False
    min_harvest_threshold: float = 1.0
    max_positions: int = 10
    explorer_url: str = "https://testnet.bscscan.com"
    trusted_collections: list = field(default_factory=list)

    def switch_to_mainnet(self) -> None:
        self.network = "bsc-mainnet"
        self.rpc_url = BSC_MAINNET_RPC
        self.chain_id = 56
        self.explorer_url = "https://bscscan.com"

    def switch_to_testnet(self) -> None:
        self.network = "bsc-testnet"
        self.rpc_url = BSC_TESTNET_RPC
        self.chain_id = 97
        self.explorer_url = "https://testnet.bscscan.com"


def load_config() -> FarmingConfig:
    """Load farming configuration from disk or create defaults."""
    if not _CONFIG_FILE.exists():
        cfg = FarmingConfig()
        save_config(cfg)
        return cfg

    with open(_CONFIG_FILE, "r", encoding="utf-8") as fp:
        raw = json.load(fp)

    cfg = FarmingConfig()
    for k, v in raw.items():
        if hasattr(cfg, k):
            setattr(cfg, k, v)
    return cfg


def save_config(cfg: FarmingConfig) -> None:
    """Persist configuration to disk."""
    with open(_CONFIG_FILE, "w", encoding="utf-8") as fp:
        json.dump(asdict(cfg), fp, indent=2, ensure_ascii=False)


def reset_config() -> FarmingConfig:
    """Reset to default configuration."""
    cfg = FarmingConfig()
    save_config(cfg)
    return cfg
