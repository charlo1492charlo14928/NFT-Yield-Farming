# -*- coding: utf-8 -*-
"""
NFT Yield Farming — staking, unstaking, and yield calculation engine.
Manages LP token staking positions, pending rewards, and harvest operations
against the BSC yield farming smart contract.
"""
import time
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class StakeStatus(Enum):
    ACTIVE = "active"
    PENDING = "pending"
    UNSTAKED = "unstaked"
    HARVESTED = "harvested"


@dataclass
class StakePosition:
    position_id: str
    nft_token_id: str
    collection_address: str
    lp_amount: float
    staked_at: float
    pool_share_pct: float = 0.0
    pending_reward: float = 0.0
    status: StakeStatus = StakeStatus.ACTIVE
    last_harvest_ts: float = 0.0

    @property
    def duration_hours(self) -> float:
        return round((time.time() - self.staked_at) / 3600, 2)


@dataclass
class PoolInfo:
    pool_address: str
    total_staked: float
    reward_per_block: float
    block_time_seconds: float = 3.0
    total_participants: int = 0
    governance_token: str = "GOV"


class YieldCalculator:
    """Compute expected yield for LP staking positions."""

    def __init__(self, pool: PoolInfo):
        self._pool = pool

    def estimate_apr(self, lp_amount: float, token_price_usd: float = 1.0) -> float:
        """Estimate annualized percentage return for a given LP stake."""
        if self._pool.total_staked <= 0 or lp_amount <= 0:
            return 0.0
        share = lp_amount / (self._pool.total_staked + lp_amount)
        blocks_per_year = (365.25 * 24 * 3600) / self._pool.block_time_seconds
        annual_reward = share * self._pool.reward_per_block * blocks_per_year
        annual_value = annual_reward * token_price_usd
        stake_value = lp_amount * token_price_usd
        if stake_value == 0:
            return 0.0
        return round((annual_value / stake_value) * 100, 2)

    def pending_reward(self, position: StakePosition) -> float:
        """Calculate pending reward tokens since last harvest."""
        if self._pool.total_staked <= 0:
            return 0.0
        share = position.lp_amount / self._pool.total_staked
        elapsed = time.time() - max(position.last_harvest_ts, position.staked_at)
        blocks_elapsed = elapsed / self._pool.block_time_seconds
        reward = share * self._pool.reward_per_block * blocks_elapsed
        return round(reward, 8)

    def compound_projection(self, lp_amount: float, days: int,
                            compounds_per_day: int = 1) -> float:
        """Project compounded yield over a number of days."""
        if self._pool.total_staked <= 0 or lp_amount <= 0:
            return lp_amount
        share = lp_amount / self._pool.total_staked
        blocks_per_period = (24 * 3600 / compounds_per_day) / self._pool.block_time_seconds
        reward_per_period = share * self._pool.reward_per_block * blocks_per_period
        total_periods = days * compounds_per_day
        balance = lp_amount
        for _ in range(total_periods):
            balance += reward_per_period
            share = balance / (self._pool.total_staked + balance - lp_amount)
            reward_per_period = share * self._pool.reward_per_block * blocks_per_period
        return round(balance, 8)


class FarmingManager:
    """Manage staking positions and harvest operations."""

    def __init__(self):
        self._positions: dict[str, StakePosition] = {}
        self._harvest_history: list[dict] = []

    def stake(self, nft_token_id: str, collection_address: str,
              lp_amount: float) -> StakePosition:
        """Create a new staking position."""
        pos_id = f"pos_{nft_token_id}_{int(time.time())}"
        position = StakePosition(
            position_id=pos_id,
            nft_token_id=nft_token_id,
            collection_address=collection_address,
            lp_amount=lp_amount,
            staked_at=time.time(),
            status=StakeStatus.ACTIVE,
        )
        self._positions[pos_id] = position
        return position

    def unstake(self, position_id: str) -> Optional[StakePosition]:
        """Unstake a position and mark it inactive."""
        pos = self._positions.get(position_id)
        if pos and pos.status == StakeStatus.ACTIVE:
            pos.status = StakeStatus.UNSTAKED
            return pos
        return None

    def harvest(self, position_id: str, reward_amount: float) -> Optional[dict]:
        """Record a harvest event for a position."""
        pos = self._positions.get(position_id)
        if pos and pos.status == StakeStatus.ACTIVE:
            record = {
                "position_id": position_id,
                "reward": reward_amount,
                "harvested_at": time.time(),
                "token": "GOV",
            }
            pos.last_harvest_ts = time.time()
            pos.pending_reward = 0.0
            self._harvest_history.append(record)
            return record
        return None

    def active_positions(self) -> list[StakePosition]:
        return [p for p in self._positions.values() if p.status == StakeStatus.ACTIVE]

    def total_staked(self) -> float:
        return sum(p.lp_amount for p in self.active_positions())

    def total_harvested(self) -> float:
        return sum(h["reward"] for h in self._harvest_history)

    @property
    def harvest_history(self) -> list[dict]:
        return list(self._harvest_history)
