"""Tests for Portfolio CLI commands.

Tests for nthlayer portfolio command.
"""

import os
import tempfile
from pathlib import Path


class TestPortfolioCommand:
    """Tests for nthlayer portfolio command."""

    def test_portfolio_discovers_services(self):
        """Test that portfolio discovers services with SLOs."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            # Create services directory with SLO resources
            services_dir = tmpdir / "services"
            services_dir.mkdir()

            (services_dir / "payment-api.yaml").write_text("""
service:
  name: payment-api
  team: payments
  tier: critical
  type: api

resources:
  - kind: SLO
    name: availability
    spec:
      objective: 99.95
      window: 30d
""")

            (services_dir / "search-api.yaml").write_text("""
service:
  name: search-api
  team: search
  tier: standard
  type: api

resources:
  - kind: SLO
    name: availability
    spec:
      objective: 99.5
      window: 30d
""")

            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                from nthlayer.cli.portfolio import _discover_services_with_slos

                services = _discover_services_with_slos()
                assert len(services) == 2
                names = {s["name"] for s in services}
                assert "payment-api" in names
                assert "search-api" in names
            finally:
                os.chdir(old_cwd)

    def test_portfolio_calculates_health(self):
        """Test that portfolio calculates health correctly."""
        from nthlayer.cli.portfolio import _calculate_portfolio_health

        results = [
            {
                "name": "service-a",
                "tier": "critical",
                "team": "team-a",
                "slos": [
                    {
                        "name": "availability",
                        "objective": 99.9,
                        "status": "HEALTHY",
                        "healthy": True,
                        "burned_minutes": 10,
                        "percent_consumed": 20,
                    },
                    {
                        "name": "latency",
                        "objective": 99.0,
                        "status": "WARNING",
                        "healthy": False,
                        "burned_minutes": 300,
                        "percent_consumed": 60,
                    },
                ],
            },
            {
                "name": "service-b",
                "tier": "standard",
                "team": "team-b",
                "slos": [
                    {
                        "name": "availability",
                        "objective": 99.5,
                        "status": "HEALTHY",
                        "healthy": True,
                        "burned_minutes": 5,
                        "percent_consumed": 10,
                    },
                ],
            },
        ]

        portfolio = _calculate_portfolio_health(results)

        assert portfolio["total_services"] == 2
        assert portfolio["total_slos"] == 3
        assert portfolio["healthy_slos"] == 2
        assert portfolio["health_percent"] == (2 / 3) * 100

    def test_portfolio_groups_by_tier(self):
        """Test that portfolio groups services by tier."""
        from nthlayer.cli.portfolio import _calculate_portfolio_health

        results = [
            {
                "name": "critical-svc",
                "tier": "critical",
                "team": "team",
                "slos": [{"name": "slo", "status": "HEALTHY", "healthy": True}],
            },
            {
                "name": "standard-svc",
                "tier": "standard",
                "team": "team",
                "slos": [{"name": "slo", "status": "HEALTHY", "healthy": True}],
            },
            {
                "name": "low-svc",
                "tier": "low",
                "team": "team",
                "slos": [{"name": "slo", "status": "WARNING", "healthy": False}],
            },
        ]

        portfolio = _calculate_portfolio_health(results)

        assert "critical" in portfolio["by_tier"]
        assert "standard" in portfolio["by_tier"]
        assert "low" in portfolio["by_tier"]
        assert portfolio["by_tier"]["critical"]["healthy"] == 1
        assert portfolio["by_tier"]["low"]["healthy"] == 0

    def test_portfolio_generates_insights(self):
        """Test that portfolio generates actionable insights."""
        from nthlayer.cli.portfolio import _generate_insights

        results = [
            {
                "name": "exhausted-svc",
                "tier": "critical",
                "slos": [
                    {"name": "slo", "status": "EXHAUSTED", "percent_consumed": 150},
                ],
            },
            {
                "name": "healthy-svc",
                "tier": "standard",
                "slos": [
                    {"name": "slo", "status": "HEALTHY", "percent_consumed": 10},
                ],
            },
        ]

        insights = _generate_insights(results, {})

        assert len(insights) >= 1
        exhausted_insight = next(
            (i for i in insights if "exhausted" in i["message"].lower()), None
        )
        assert exhausted_insight is not None
        assert exhausted_insight["type"] == "critical"

    def test_portfolio_command_skip_collect(self):
        """Test portfolio command with --skip-collect."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)

            services_dir = tmpdir / "services"
            services_dir.mkdir()

            (services_dir / "test-service.yaml").write_text("""
service:
  name: test-service
  team: test
  tier: critical
  type: api

resources:
  - kind: SLO
    name: availability
    spec:
      objective: 99.9
      window: 30d
""")

            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                from nthlayer.cli.portfolio import portfolio_command

                result = portfolio_command(skip_collect=True)
                assert result == 0
            finally:
                os.chdir(old_cwd)

    def test_portfolio_handles_empty_services(self):
        """Test portfolio handles no services gracefully."""
        with tempfile.TemporaryDirectory() as tmpdir:
            old_cwd = os.getcwd()
            try:
                os.chdir(tmpdir)
                from nthlayer.cli.portfolio import portfolio_command

                result = portfolio_command(skip_collect=True)
                assert result == 0
            finally:
                os.chdir(old_cwd)


class TestWindowParsing:
    """Tests for window parsing in portfolio."""

    def test_parse_days(self):
        """Test parsing day windows."""
        from nthlayer.cli.portfolio import _parse_window_minutes

        assert _parse_window_minutes("30d") == 30 * 24 * 60
        assert _parse_window_minutes("7d") == 7 * 24 * 60

    def test_parse_hours(self):
        """Test parsing hour windows."""
        from nthlayer.cli.portfolio import _parse_window_minutes

        assert _parse_window_minutes("24h") == 24 * 60

    def test_parse_weeks(self):
        """Test parsing week windows."""
        from nthlayer.cli.portfolio import _parse_window_minutes

        assert _parse_window_minutes("1w") == 7 * 24 * 60
