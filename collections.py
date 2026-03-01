# -*- coding: utf-8 -*-
"""
NFT Yield Farming — collection discovery and floor price tracking.
Monitors NFT collections eligible for yield farming pools,
tracks floor prices, and identifies high-yield opportunities.
"""
import time
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class CollectionTier(Enum):
    BLUE_CHIP = "blue_chip"
    MID_CAP = "mid_cap"
    MICRO_CAP = "micro_cap"
    UNKNOWN = "unknown"


@dataclass
class PriceSnapshot:
    price_bnb: float
    price_usd: float
    timestamp: float = field(default_factory=time.time)
    source: str = "aggregator"


@dataclass
class NFTCollection:
    contract_address: str
    name: str
    symbol: str
    total_supply: int = 0
    holders: int = 0
    floor_price_bnb: float = 0.0
    floor_price_usd: float = 0.0
    volume_24h_bnb: float = 0.0
    tier: CollectionTier = CollectionTier.UNKNOWN
    farming_eligible: bool = False
    pool_apy: Optional[float] = None
    verified: bool = False
    price_history: list[PriceSnapshot] = field(default_factory=list)
    last_updated: float = field(default_factory=time.time)

    @property
    def market_cap_bnb(self) -> float:
        return self.floor_price_bnb * self.total_supply

    def record_price(self, bnb: float, usd: float, source: str = "aggregator") -> None:
        snap = PriceSnapshot(price_bnb=bnb, price_usd=usd, source=source)
        self.price_history.append(snap)
        self.floor_price_bnb = bnb
        self.floor_price_usd = usd
        self.last_updated = time.time()

    def price_change_pct(self, window_seconds: int = 86400) -> Optional[float]:
        """Calculate price change percentage over a time window."""
        if len(self.price_history) < 2:
            return None
        cutoff = time.time() - window_seconds
        older = [s for s in self.price_history if s.timestamp <= cutoff]
        if not older:
            older = [self.price_history[0]]
        baseline = older[-1].price_bnb
        if baseline == 0:
            return None
        current = self.price_history[-1].price_bnb
        return round(((current - baseline) / baseline) * 100, 2)


class CollectionRegistry:
    """Registry of NFT collections with discovery and tracking capabilities."""

    def __init__(self):
        self._collections: dict[str, NFTCollection] = {}

    def register(self, collection: NFTCollection) -> None:
        self._collections[collection.contract_address.lower()] = collection

    def get(self, contract_address: str) -> Optional[NFTCollection]:
        return self._collections.get(contract_address.lower())

    def remove(self, contract_address: str) -> bool:
        key = contract_address.lower()
        if key in self._collections:
            del self._collections[key]
            return True
        return False

    def all_collections(self) -> list[NFTCollection]:
        return list(self._collections.values())

    def farming_eligible(self) -> list[NFTCollection]:
        return [c for c in self._collections.values() if c.farming_eligible]

    def by_tier(self, tier: CollectionTier) -> list[NFTCollection]:
        return [c for c in self._collections.values() if c.tier == tier]

    def top_by_volume(self, limit: int = 10) -> list[NFTCollection]:
        sorted_cols = sorted(
            self._collections.values(),
            key=lambda c: c.volume_24h_bnb,
            reverse=True,
        )
        return sorted_cols[:limit]

    def top_by_apy(self, limit: int = 10) -> list[NFTCollection]:
        eligible = [c for c in self._collections.values()
                    if c.pool_apy is not None]
        sorted_cols = sorted(eligible, key=lambda c: c.pool_apy, reverse=True)
        return sorted_cols[:limit]

    def search(self, query: str) -> list[NFTCollection]:
        q = query.lower()
        return [
            c for c in self._collections.values()
            if q in c.name.lower() or q in c.symbol.lower()
               or q in c.contract_address.lower()
        ]

    def classify_tier(self, collection: NFTCollection) -> CollectionTier:
        """Classify collection tier based on market cap and holder count."""
        mcap = collection.market_cap_bnb
        if mcap >= 10000 and collection.holders >= 5000:
            return CollectionTier.BLUE_CHIP
        if mcap >= 1000 and collection.holders >= 500:
            return CollectionTier.MID_CAP
        if mcap > 0:
            return CollectionTier.MICRO_CAP
        return CollectionTier.UNKNOWN

    def update_tiers(self) -> None:
        """Re-classify all registered collections."""
        for col in self._collections.values():
            col.tier = self.classify_tier(col)

    def summary(self) -> dict:
        total = len(self._collections)
        eligible = len(self.farming_eligible())
        total_volume = sum(c.volume_24h_bnb for c in self._collections.values())
        return {
            "total_collections": total,
            "farming_eligible": eligible,
            "total_24h_volume_bnb": round(total_volume, 4),
            "blue_chip": len(self.by_tier(CollectionTier.BLUE_CHIP)),
            "mid_cap": len(self.by_tier(CollectionTier.MID_CAP)),
            "micro_cap": len(self.by_tier(CollectionTier.MICRO_CAP)),
        }
