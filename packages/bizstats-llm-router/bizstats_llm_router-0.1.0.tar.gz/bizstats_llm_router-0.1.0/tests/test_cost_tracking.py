"""
Tests for cost tracking.

Copyright (c) 2025 Absolut-e Data Com Inc. and BizStats.AI
All rights reserved. Proprietary and confidential.
"""

import pytest
from bizstats_llm_router import (
    CostTrackingConfig,
    CostTracker,
    CostSummary,
    get_cost_tracker,
)


class TestCostTracker:
    """Tests for CostTracker."""

    @pytest.fixture
    def enabled_config(self):
        return CostTrackingConfig(
            enabled=True,
            budget_limit_daily=10.0,
            budget_limit_monthly=100.0,
        )

    @pytest.fixture
    def disabled_config(self):
        return CostTrackingConfig(enabled=False)

    @pytest.mark.asyncio
    async def test_track_disabled(self, disabled_config):
        """Test tracking when disabled."""
        tracker = CostTracker(disabled_config)
        await tracker.track(cost=0.01, provider="openai", model="gpt-4")
        # Should not track anything
        summary = tracker.get_summary()
        assert summary.total_cost == 0

    @pytest.mark.asyncio
    async def test_track_cost(self, enabled_config):
        """Test tracking a cost entry."""
        tracker = CostTracker(enabled_config)
        await tracker.track(
            cost=0.01,
            provider="openai",
            model="gpt-4",
            prompt_tokens=100,
            completion_tokens=50,
        )
        summary = tracker.get_summary()
        assert summary.total_cost == 0.01
        assert summary.total_requests == 1

    @pytest.mark.asyncio
    async def test_track_multiple_costs(self, enabled_config):
        """Test tracking multiple cost entries."""
        tracker = CostTracker(enabled_config)
        await tracker.track(cost=0.01, provider="openai", model="gpt-4")
        await tracker.track(cost=0.02, provider="anthropic", model="claude-3")
        await tracker.track(cost=0.005, provider="openai", model="gpt-3.5")

        summary = tracker.get_summary()
        assert summary.total_cost == 0.035
        assert summary.total_requests == 3
        assert "openai" in summary.by_provider
        assert "anthropic" in summary.by_provider

    @pytest.mark.asyncio
    async def test_track_per_user(self):
        """Test per-user cost tracking."""
        config = CostTrackingConfig(enabled=True, track_per_user=True)
        tracker = CostTracker(config)

        await tracker.track(cost=0.01, provider="openai", user_id="user1")
        await tracker.track(cost=0.02, provider="openai", user_id="user2")
        await tracker.track(cost=0.01, provider="openai", user_id="user1")

        summary = tracker.get_summary()
        assert summary.by_user.get("user1") == 0.02
        assert summary.by_user.get("user2") == 0.02

    @pytest.mark.asyncio
    async def test_daily_cost(self, enabled_config):
        """Test getting daily cost."""
        tracker = CostTracker(enabled_config)
        await tracker.track(cost=0.01, provider="openai")
        await tracker.track(cost=0.02, provider="openai")

        daily = tracker.get_daily_cost()
        assert daily == 0.03

    @pytest.mark.asyncio
    async def test_monthly_cost(self, enabled_config):
        """Test getting monthly cost."""
        tracker = CostTracker(enabled_config)
        await tracker.track(cost=0.05, provider="openai")

        monthly = tracker.get_monthly_cost()
        assert monthly == 0.05

    @pytest.mark.asyncio
    async def test_budget_status(self, enabled_config):
        """Test getting budget status."""
        tracker = CostTracker(enabled_config)
        await tracker.track(cost=2.0, provider="openai")

        status = tracker.get_budget_status()
        assert status["enabled"] is True
        assert status["daily"]["current"] == 2.0
        assert status["daily"]["limit"] == 10.0
        assert status["daily"]["remaining"] == 8.0
        assert status["daily"]["percent_used"] == 20.0

    @pytest.mark.asyncio
    async def test_alert_callback(self, enabled_config):
        """Test budget alert callback."""
        tracker = CostTracker(enabled_config)

        alerts_received = []

        def on_alert(period, current, limit):
            alerts_received.append((period, current, limit))

        tracker.on_alert(on_alert)

        # Track cost that exceeds daily threshold (80% of $10 = $8)
        await tracker.track(cost=9.0, provider="openai")

        assert len(alerts_received) >= 1
        assert alerts_received[0][0] == "daily"

    @pytest.mark.asyncio
    async def test_reset(self, enabled_config):
        """Test resetting tracker."""
        tracker = CostTracker(enabled_config)
        await tracker.track(cost=0.05, provider="openai")

        tracker.reset()

        summary = tracker.get_summary()
        assert summary.total_cost == 0
        assert summary.total_requests == 0


class TestCostSummary:
    """Tests for CostSummary."""

    def test_summary_fields(self):
        """Test summary has all fields."""
        summary = CostSummary(
            total_cost=0.05,
            total_requests=10,
            total_tokens=1000,
            by_provider={"openai": 0.03, "anthropic": 0.02},
            by_model={"gpt-4": 0.03, "claude-3": 0.02},
        )
        assert summary.total_cost == 0.05
        assert summary.total_requests == 10
        assert summary.total_tokens == 1000
        assert len(summary.by_provider) == 2


class TestGetCostTracker:
    """Tests for get_cost_tracker factory function."""

    def test_create_enabled_tracker(self):
        """Test creating enabled tracker."""
        config = CostTrackingConfig(enabled=True)
        tracker = get_cost_tracker(config)
        assert isinstance(tracker, CostTracker)

    def test_create_with_budgets(self):
        """Test creating tracker with budgets."""
        config = CostTrackingConfig(
            enabled=True,
            budget_limit_daily=10.0,
            budget_limit_monthly=200.0,
        )
        tracker = get_cost_tracker(config)
        assert tracker.config.budget_limit_daily == 10.0
        assert tracker.config.budget_limit_monthly == 200.0
