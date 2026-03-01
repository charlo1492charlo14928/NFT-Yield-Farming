# -*- coding: utf-8 -*-
"""
NFT Yield Farming — portfolio management and PnL tracking.
Tracks wallet positions across farming pools, calculates realized/unrealized
gains, and provides portfolio-level analytics.
"""
import time
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class TransactionType(Enum):
    STAKE = "stake"
    UNSTAKE = "unstake"
    HARVEST = "harvest"
    COMPOUND = "compound"


@dataclass
class Transaction:
    tx_type: TransactionType
    position_id: str
    amount: float
    token_symbol: str
    price_at_tx_usd: float = 0.0
    timestamp: float = field(default_factory=time.time)
    tx_hash: Optional[str] = None
    gas_cost_bnb: float = 0.0

    @property
    def value_usd(self) -> float:
        return self.amount * self.price_at_tx_usd


@dataclass
class PortfolioSnapshot:
    timestamp: float
    total_value_usd: float
    total_staked_lp: float
    unrealized_pnl_usd: float
    realized_pnl_usd: float
    active_positions: int


class Portfolio:
    """Track farming positions and compute portfolio-level PnL."""

    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
        self._transactions: list[Transaction] = []
        self._snapshots: list[PortfolioSnapshot] = []
        self._cost_basis: dict[str, float] = {}

    def record_stake(self, position_id: str, lp_amount: float,
                     price_usd: float, tx_hash: Optional[str] = None,
                     gas_bnb: float = 0.0) -> Transaction:
        """Record an LP token staking transaction."""
        tx = Transaction(
            tx_type=TransactionType.STAKE,
            position_id=position_id,
            amount=lp_amount,
            token_symbol="LP",
            price_at_tx_usd=price_usd,
            tx_hash=tx_hash,
            gas_cost_bnb=gas_bnb,
        )
        self._transactions.append(tx)
        self._cost_basis[position_id] = self._cost_basis.get(position_id, 0.0) + tx.value_usd
        return tx

    def record_unstake(self, position_id: str, lp_amount: float,
                       price_usd: float, tx_hash: Optional[str] = None,
                       gas_bnb: float = 0.0) -> Transaction:
        """Record an LP unstaking transaction."""
        tx = Transaction(
            tx_type=TransactionType.UNSTAKE,
            position_id=position_id,
            amount=lp_amount,
            token_symbol="LP",
            price_at_tx_usd=price_usd,
            tx_hash=tx_hash,
            gas_cost_bnb=gas_bnb,
        )
        self._transactions.append(tx)
        return tx

    def record_harvest(self, position_id: str, reward_amount: float,
                       reward_symbol: str, price_usd: float,
                       tx_hash: Optional[str] = None,
                       gas_bnb: float = 0.0) -> Transaction:
        """Record a yield harvest event."""
        tx = Transaction(
            tx_type=TransactionType.HARVEST,
            position_id=position_id,
            amount=reward_amount,
            token_symbol=reward_symbol,
            price_at_tx_usd=price_usd,
            tx_hash=tx_hash,
            gas_cost_bnb=gas_bnb,
        )
        self._transactions.append(tx)
        return tx

    def realized_pnl(self) -> float:
        """Sum of all realized gains from unstaking and harvesting."""
        harvests = sum(
            t.value_usd for t in self._transactions
            if t.tx_type in (TransactionType.HARVEST, TransactionType.COMPOUND)
        )
        unstake_value = sum(
            t.value_usd for t in self._transactions
            if t.tx_type == TransactionType.UNSTAKE
        )
        stake_cost = sum(
            t.value_usd for t in self._transactions
            if t.tx_type == TransactionType.STAKE
        )
        gas_costs = sum(t.gas_cost_bnb for t in self._transactions)
        return round(harvests + unstake_value - stake_cost - gas_costs, 4)

    def total_invested(self) -> float:
        """Total USD value deposited into farming positions."""
        return sum(
            t.value_usd for t in self._transactions
            if t.tx_type == TransactionType.STAKE
        )

    def total_harvested(self) -> float:
        """Total USD value from harvested rewards."""
        return sum(
            t.value_usd for t in self._transactions
            if t.tx_type == TransactionType.HARVEST
        )

    def total_gas_spent(self) -> float:
        """Total gas costs in BNB across all transactions."""
        return sum(t.gas_cost_bnb for t in self._transactions)

    def roi_percent(self) -> Optional[float]:
        """Return on investment as a percentage."""
        invested = self.total_invested()
        if invested == 0:
            return None
        return round((self.realized_pnl() / invested) * 100, 2)

    def take_snapshot(self, current_staked_lp: float,
                      current_lp_price_usd: float,
                      active_positions: int) -> PortfolioSnapshot:
        """Capture current portfolio state for historical tracking."""
        total_value = current_staked_lp * current_lp_price_usd + self.total_harvested()
        snap = PortfolioSnapshot(
            timestamp=time.time(),
            total_value_usd=round(total_value, 4),
            total_staked_lp=current_staked_lp,
            unrealized_pnl_usd=round(total_value - self.total_invested(), 4),
            realized_pnl_usd=self.realized_pnl(),
            active_positions=active_positions,
        )
        self._snapshots.append(snap)
        return snap

    def transaction_count(self) -> dict:
        counts: dict[str, int] = {}
        for t in self._transactions:
            key = t.tx_type.value
            counts[key] = counts.get(key, 0) + 1
        return counts

    @property
    def transactions(self) -> list[Transaction]:
        return list(self._transactions)

    @property
    def snapshots(self) -> list[PortfolioSnapshot]:
        return list(self._snapshots)

    def summary(self) -> dict:
        return {
            "wallet": self.wallet_address,
            "total_invested_usd": round(self.total_invested(), 4),
            "total_harvested_usd": round(self.total_harvested(), 4),
            "realized_pnl_usd": self.realized_pnl(),
            "roi_percent": self.roi_percent(),
            "total_gas_bnb": round(self.total_gas_spent(), 6),
            "transactions": self.transaction_count(),
            "snapshots_recorded": len(self._snapshots),
        }
