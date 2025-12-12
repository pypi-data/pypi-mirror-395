"""
Cost Tracking for LLM Router.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.

Provides cost tracking and budget management for LLM usage.
"""

import logging
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from .config import CostTrackingConfig

logger = logging.getLogger(__name__)


@dataclass
class CostEntry:
    """A single cost entry."""

    timestamp: float
    provider: str
    model: str
    prompt_tokens: int
    completion_tokens: int
    cost: float
    user_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class CostSummary:
    """Summary of costs for a period."""

    total_cost: float
    total_requests: int
    total_tokens: int
    by_provider: Dict[str, float] = field(default_factory=dict)
    by_model: Dict[str, float] = field(default_factory=dict)
    by_user: Dict[str, float] = field(default_factory=dict)
    period_start: float = 0
    period_end: float = 0


class CostTracker:
    """Tracks costs for LLM usage."""

    def __init__(self, config: CostTrackingConfig):
        self.config = config
        self._entries: List[CostEntry] = []
        self._daily_costs: Dict[str, float] = {}  # date -> cost
        self._monthly_costs: Dict[str, float] = {}  # month -> cost
        self._alert_callbacks: List[Callable[[str, float, float], None]] = []

    async def track(
        self,
        cost: float,
        provider: str = "",
        model: str = "",
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        user_id: Optional[str] = None,
        **metadata: Any,
    ) -> None:
        """Track a cost entry.

        Args:
            cost: Cost in USD.
            provider: LLM provider name.
            model: Model name.
            prompt_tokens: Number of prompt tokens.
            completion_tokens: Number of completion tokens.
            user_id: Optional user ID for per-user tracking.
            **metadata: Additional metadata.
        """
        if not self.config.enabled:
            return

        entry = CostEntry(
            timestamp=time.time(),
            provider=provider,
            model=model,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            cost=cost,
            user_id=user_id if self.config.track_per_user else None,
            metadata=metadata,
        )

        self._entries.append(entry)

        # Update daily/monthly totals
        now = datetime.now(timezone.utc)
        date_key = now.strftime("%Y-%m-%d")
        month_key = now.strftime("%Y-%m")

        self._daily_costs[date_key] = self._daily_costs.get(date_key, 0) + cost
        self._monthly_costs[month_key] = self._monthly_costs.get(month_key, 0) + cost

        # Check budget alerts
        await self._check_alerts(date_key, month_key)

        # Cleanup old entries (keep last 30 days)
        self._cleanup_old_entries()

    async def _check_alerts(self, date_key: str, month_key: str) -> None:
        """Check if budget alerts should be triggered."""
        # Check daily budget
        if self.config.budget_limit_daily:
            daily_cost = self._daily_costs.get(date_key, 0)
            threshold = self.config.budget_limit_daily * (self.config.alert_threshold_percent / 100)

            if daily_cost >= threshold:
                await self._trigger_alert(
                    "daily",
                    daily_cost,
                    self.config.budget_limit_daily,
                )

        # Check monthly budget
        if self.config.budget_limit_monthly:
            monthly_cost = self._monthly_costs.get(month_key, 0)
            threshold = self.config.budget_limit_monthly * (self.config.alert_threshold_percent / 100)

            if monthly_cost >= threshold:
                await self._trigger_alert(
                    "monthly",
                    monthly_cost,
                    self.config.budget_limit_monthly,
                )

    async def _trigger_alert(
        self,
        period: str,
        current: float,
        limit: float,
    ) -> None:
        """Trigger a budget alert.

        Args:
            period: "daily" or "monthly".
            current: Current cost.
            limit: Budget limit.
        """
        percent = (current / limit) * 100
        logger.warning(
            f"Budget alert: {period} cost ${current:.4f} is {percent:.1f}% of limit ${limit:.2f}"
        )

        for callback in self._alert_callbacks:
            try:
                callback(period, current, limit)
            except Exception as e:
                logger.error(f"Alert callback error: {e}")

    def _cleanup_old_entries(self, days: int = 30) -> None:
        """Remove entries older than specified days."""
        cutoff = time.time() - (days * 24 * 60 * 60)
        self._entries = [e for e in self._entries if e.timestamp >= cutoff]

    def on_alert(self, callback: Callable[[str, float, float], None]) -> None:
        """Register an alert callback.

        Args:
            callback: Function to call with (period, current, limit).
        """
        self._alert_callbacks.append(callback)

    def get_summary(
        self,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
    ) -> CostSummary:
        """Get cost summary for a period.

        Args:
            start_time: Start timestamp (defaults to start of day).
            end_time: End timestamp (defaults to now).

        Returns:
            CostSummary with aggregated data.
        """
        if start_time is None:
            # Default to start of current day
            now = datetime.now(timezone.utc)
            start_time = datetime(
                now.year, now.month, now.day, tzinfo=timezone.utc
            ).timestamp()

        if end_time is None:
            end_time = time.time()

        # Filter entries
        filtered = [
            e for e in self._entries
            if start_time <= e.timestamp <= end_time
        ]

        # Aggregate
        total_cost = sum(e.cost for e in filtered)
        total_tokens = sum(e.prompt_tokens + e.completion_tokens for e in filtered)

        by_provider: Dict[str, float] = {}
        by_model: Dict[str, float] = {}
        by_user: Dict[str, float] = {}

        for entry in filtered:
            by_provider[entry.provider] = by_provider.get(entry.provider, 0) + entry.cost
            by_model[entry.model] = by_model.get(entry.model, 0) + entry.cost
            if entry.user_id:
                by_user[entry.user_id] = by_user.get(entry.user_id, 0) + entry.cost

        return CostSummary(
            total_cost=round(total_cost, 6),
            total_requests=len(filtered),
            total_tokens=total_tokens,
            by_provider={k: round(v, 6) for k, v in by_provider.items()},
            by_model={k: round(v, 6) for k, v in by_model.items()},
            by_user={k: round(v, 6) for k, v in by_user.items()},
            period_start=start_time,
            period_end=end_time,
        )

    def get_daily_cost(self, date: Optional[str] = None) -> float:
        """Get cost for a specific day.

        Args:
            date: Date string (YYYY-MM-DD). Defaults to today.

        Returns:
            Total cost for the day.
        """
        if date is None:
            date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        return self._daily_costs.get(date, 0)

    def get_monthly_cost(self, month: Optional[str] = None) -> float:
        """Get cost for a specific month.

        Args:
            month: Month string (YYYY-MM). Defaults to current month.

        Returns:
            Total cost for the month.
        """
        if month is None:
            month = datetime.now(timezone.utc).strftime("%Y-%m")
        return self._monthly_costs.get(month, 0)

    def get_budget_status(self) -> Dict[str, Any]:
        """Get current budget status.

        Returns:
            Dictionary with budget information.
        """
        now = datetime.now(timezone.utc)
        date_key = now.strftime("%Y-%m-%d")
        month_key = now.strftime("%Y-%m")

        daily_cost = self._daily_costs.get(date_key, 0)
        monthly_cost = self._monthly_costs.get(month_key, 0)

        status = {
            "enabled": self.config.enabled,
            "daily": {
                "current": round(daily_cost, 6),
                "limit": self.config.budget_limit_daily,
                "remaining": (
                    round(self.config.budget_limit_daily - daily_cost, 6)
                    if self.config.budget_limit_daily
                    else None
                ),
                "percent_used": (
                    round(daily_cost / self.config.budget_limit_daily * 100, 1)
                    if self.config.budget_limit_daily
                    else None
                ),
            },
            "monthly": {
                "current": round(monthly_cost, 6),
                "limit": self.config.budget_limit_monthly,
                "remaining": (
                    round(self.config.budget_limit_monthly - monthly_cost, 6)
                    if self.config.budget_limit_monthly
                    else None
                ),
                "percent_used": (
                    round(monthly_cost / self.config.budget_limit_monthly * 100, 1)
                    if self.config.budget_limit_monthly
                    else None
                ),
            },
            "total_entries": len(self._entries),
        }

        return status

    def reset(self) -> None:
        """Reset all tracking data."""
        self._entries.clear()
        self._daily_costs.clear()
        self._monthly_costs.clear()


def get_cost_tracker(config: CostTrackingConfig) -> CostTracker:
    """Create a cost tracker instance.

    Args:
        config: Cost tracking configuration.

    Returns:
        Configured CostTracker instance.
    """
    return CostTracker(config)
