"""
CLI commands for SLO Portfolio management.

Commands:
    nthlayer portfolio          - Show org-wide reliability portfolio
    nthlayer portfolio --details - Show detailed breakdown
"""

from __future__ import annotations

import argparse
import asyncio
import os
from collections import defaultdict
from pathlib import Path
from typing import Any

from nthlayer.specs.parser import parse_service_file


def portfolio_command(
    prometheus_url: str | None = None,
    details: bool = False,
    skip_collect: bool = False,
) -> int:
    """Show org-wide reliability portfolio."""
    prom_url = prometheus_url or os.environ.get(
        "NTHLAYER_PROMETHEUS_URL", "http://localhost:9090"
    )

    print()
    print("=" * 70)
    print("  NthLayer Reliability Portfolio")
    print("=" * 70)
    print()

    # Discover all services with SLOs
    services = _discover_services_with_slos()

    if not services:
        print("No services with SLOs found in services/ or examples/services/")
        print()
        print("Define SLOs in your service.yaml files:")
        print("  resources:")
        print("    - kind: SLO")
        print("      name: availability")
        print("      spec:")
        print("        objective: 99.95")
        return 0

    # Collect metrics for all services (unless skipped)
    if skip_collect:
        results = _create_placeholder_results(services)
    else:
        print(f"Collecting metrics from {prom_url}...")
        print()
        try:
            results = asyncio.run(_collect_all_metrics(services, prom_url))
        except Exception as e:
            print(f"Error collecting metrics: {e}")
            print("Using placeholder data. Run with --skip-collect to see structure.")
            results = _create_placeholder_results(services)

    # Calculate portfolio health
    portfolio = _calculate_portfolio_health(results)

    # Display portfolio
    _print_portfolio(portfolio, details)

    return 0


def _discover_services_with_slos() -> list[dict[str, Any]]:
    """Discover all services that have SLO resources defined."""
    search_paths = [Path("services"), Path("examples/services")]
    services = []

    for search_path in search_paths:
        if not search_path.exists():
            continue

        for service_file in search_path.glob("*.yaml"):
            try:
                context, resources = parse_service_file(str(service_file))
                slo_resources = [r for r in resources if r.kind == "SLO"]

                if slo_resources:
                    services.append({
                        "name": context.name,
                        "tier": context.tier or "standard",
                        "team": context.team,
                        "file": str(service_file),
                        "slos": slo_resources,
                        "context": context,
                    })
            except Exception:
                continue

    return services


async def _collect_all_metrics(
    services: list[dict[str, Any]],
    prometheus_url: str,
) -> list[dict[str, Any]]:
    """Collect metrics for all services."""
    from nthlayer.providers.prometheus import PrometheusProvider, PrometheusProviderError

    provider = PrometheusProvider(prometheus_url)
    results = []

    for service in services:
        service_results = {
            "name": service["name"],
            "tier": service["tier"],
            "team": service["team"],
            "slos": [],
        }

        for slo in service["slos"]:
            spec = slo.spec or {}
            objective = spec.get("objective", 99.9)
            window = spec.get("window", "30d")
            indicator = spec.get("indicator", {})

            window_minutes = _parse_window_minutes(window)
            error_budget_percent = (100 - objective) / 100
            total_budget_minutes = window_minutes * error_budget_percent

            slo_result = {
                "name": slo.name,
                "objective": objective,
                "window": window,
                "total_budget_minutes": total_budget_minutes,
                "current_sli": None,
                "burned_minutes": None,
                "percent_consumed": None,
                "status": "UNKNOWN",
                "healthy": False,
            }

            query = indicator.get("query")
            if query:
                query = query.replace("${service}", service["name"])
                query = query.replace("$service", service["name"])

                try:
                    sli_value = await provider.get_sli_value(query)

                    if sli_value > 0:
                        slo_result["current_sli"] = sli_value * 100
                        error_rate = 1.0 - sli_value
                        burned_minutes = window_minutes * error_rate
                        slo_result["burned_minutes"] = burned_minutes
                        slo_result["percent_consumed"] = (
                            burned_minutes / total_budget_minutes
                        ) * 100

                        if slo_result["percent_consumed"] >= 100:
                            slo_result["status"] = "EXHAUSTED"
                        elif slo_result["percent_consumed"] >= 80:
                            slo_result["status"] = "CRITICAL"
                        elif slo_result["percent_consumed"] >= 50:
                            slo_result["status"] = "WARNING"
                        else:
                            slo_result["status"] = "HEALTHY"

                        slo_result["healthy"] = slo_result["current_sli"] >= objective
                    else:
                        slo_result["status"] = "NO_DATA"
                except PrometheusProviderError:
                    slo_result["status"] = "ERROR"
            else:
                slo_result["status"] = "NO_QUERY"

            service_results["slos"].append(slo_result)

        results.append(service_results)

    return results


def _create_placeholder_results(services: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Create placeholder results when Prometheus is unavailable."""
    results = []

    for service in services:
        service_results = {
            "name": service["name"],
            "tier": service["tier"],
            "team": service["team"],
            "slos": [],
        }

        for slo in service["slos"]:
            spec = slo.spec or {}
            objective = spec.get("objective", 99.9)
            window = spec.get("window", "30d")

            window_minutes = _parse_window_minutes(window)
            error_budget_percent = (100 - objective) / 100
            total_budget_minutes = window_minutes * error_budget_percent

            slo_result = {
                "name": slo.name,
                "objective": objective,
                "window": window,
                "total_budget_minutes": total_budget_minutes,
                "current_sli": None,
                "burned_minutes": None,
                "percent_consumed": None,
                "status": "NO_DATA",
                "healthy": False,
            }

            service_results["slos"].append(slo_result)

        results.append(service_results)

    return results


def _calculate_portfolio_health(
    results: list[dict[str, Any]],
) -> dict[str, Any]:
    """Calculate overall portfolio health metrics."""
    portfolio = {
        "total_services": len(results),
        "total_slos": 0,
        "healthy_slos": 0,
        "by_tier": defaultdict(lambda: {"services": [], "healthy": 0, "total": 0}),
        "by_status": defaultdict(int),
        "top_burners": [],
        "insights": [],
        "services": results,
    }

    all_slos_with_burn = []

    for service in results:
        tier = service["tier"]
        portfolio["by_tier"][tier]["services"].append(service["name"])

        for slo in service["slos"]:
            portfolio["total_slos"] += 1
            portfolio["by_status"][slo["status"]] += 1

            if slo["healthy"]:
                portfolio["healthy_slos"] += 1
                portfolio["by_tier"][tier]["healthy"] += 1

            portfolio["by_tier"][tier]["total"] += 1

            if slo.get("burned_minutes") is not None:
                all_slos_with_burn.append({
                    "service": service["name"],
                    "slo": slo["name"],
                    "burned_minutes": slo["burned_minutes"],
                    "percent_consumed": slo["percent_consumed"],
                    "status": slo["status"],
                })

    # Sort by burn and get top 5
    all_slos_with_burn.sort(key=lambda x: x["burned_minutes"], reverse=True)
    portfolio["top_burners"] = all_slos_with_burn[:5]

    # Calculate health percentage
    if portfolio["total_slos"] > 0:
        portfolio["health_percent"] = (
            portfolio["healthy_slos"] / portfolio["total_slos"]
        ) * 100
    else:
        portfolio["health_percent"] = 0

    # Generate insights
    portfolio["insights"] = _generate_insights(results, portfolio)

    return portfolio


def _generate_insights(
    results: list[dict[str, Any]],
    portfolio: dict[str, Any],
) -> list[dict[str, str]]:
    """Generate actionable insights from portfolio data."""
    insights = []

    for service in results:
        for slo in service["slos"]:
            # Insight: SLO exhausted
            if slo["status"] == "EXHAUSTED":
                svc_slo = f"{service['name']}/{slo['name']}"
                insights.append({
                    "type": "critical",
                    "icon": "!",
                    "message": f"{svc_slo} budget exhausted - needs immediate attention",
                })

            # Insight: SLO critical
            elif slo["status"] == "CRITICAL":
                svc_slo = f"{service['name']}/{slo['name']}"
                pct = slo["percent_consumed"]
                insights.append({
                    "type": "warning",
                    "icon": "!",
                    "message": f"{svc_slo} at {pct:.0f}% - needs reliability investment",
                })

            # Insight: SLO healthy with margin (potential tier promotion)
            elif slo["status"] == "HEALTHY" and slo.get("percent_consumed", 100) < 20:
                if service["tier"] != "critical":
                    insights.append({
                        "type": "info",
                        "icon": "*",
                        "message": f"{service['name']} exceeds SLO - consider tier promotion",
                    })

    # Limit insights
    return insights[:10]


def _print_portfolio(portfolio: dict[str, Any], details: bool) -> None:
    """Print formatted portfolio output."""
    # Overall health
    health = portfolio["health_percent"]
    healthy = portfolio["healthy_slos"]
    total = portfolio["total_slos"]

    print(f"Overall Health: {health:.0f}% ({healthy}/{total} SLOs meeting target)")
    print()

    # By tier breakdown
    print("By Tier:")
    tier_order = ["critical", "standard", "low"]

    for tier in tier_order:
        if tier not in portfolio["by_tier"]:
            continue

        tier_data = portfolio["by_tier"][tier]
        tier_healthy = tier_data["healthy"]
        tier_total = tier_data["total"]
        tier_pct = (tier_healthy / tier_total * 100) if tier_total > 0 else 0

        print(f"  {tier.capitalize()}: {tier_healthy}/{tier_total} healthy ({tier_pct:.0f}%)")

        if details:
            # Show services in this tier
            for service in portfolio["services"]:
                if service["tier"] == tier:
                    for slo in service["slos"]:
                        status_icon = {
                            "HEALTHY": "[OK]",
                            "WARNING": "[! ]",
                            "CRITICAL": "[!!]",
                            "EXHAUSTED": "[X ]",
                            "NO_DATA": "[? ]",
                            "ERROR": "[E ]",
                        }.get(slo["status"], "[? ]")

                        if slo["current_sli"] is not None:
                            print(
                                f"    {status_icon} {service['name']}/{slo['name']}: "
                                f"{slo['current_sli']:.2f}% (target {slo['objective']}%)"
                            )
                        else:
                            print(
                                f"    {status_icon} {service['name']}/{slo['name']}: "
                                f"no data (target {slo['objective']}%)"
                            )

    print()

    # Top burners
    if portfolio["top_burners"]:
        print("Top Budget Burners:")
        for burner in portfolio["top_burners"][:5]:
            burned_hrs = burner["burned_minutes"] / 60
            print(
                f"  {burner['service']}/{burner['slo']}: "
                f"{burned_hrs:.1f}h burned ({burner['percent_consumed']:.0f}%)"
            )
        print()

    # Insights
    if portfolio["insights"]:
        print("Insights:")
        for insight in portfolio["insights"]:
            print(f"  {insight['icon']} {insight['message']}")
        print()

    # Summary
    print("-" * 70)
    print(f"Services: {portfolio['total_services']} | SLOs: {portfolio['total_slos']}")
    print()
    print("Run 'nthlayer portfolio --details' for full breakdown")
    print()


def _parse_window_minutes(window: str) -> float:
    """Parse window string like '30d' into minutes."""
    if window.endswith("d"):
        days = int(window[:-1])
        return days * 24 * 60
    elif window.endswith("h"):
        hours = int(window[:-1])
        return hours * 60
    elif window.endswith("w"):
        weeks = int(window[:-1])
        return weeks * 7 * 24 * 60
    else:
        return 30 * 24 * 60


def register_portfolio_parser(subparsers: argparse._SubParsersAction) -> None:
    """Register portfolio subcommand parser."""
    portfolio_parser = subparsers.add_parser(
        "portfolio", help="Show org-wide reliability portfolio"
    )
    portfolio_parser.add_argument(
        "--details", action="store_true", help="Show detailed breakdown"
    )
    portfolio_parser.add_argument(
        "--prometheus-url",
        help="Prometheus server URL (or set NTHLAYER_PROMETHEUS_URL)",
    )
    portfolio_parser.add_argument(
        "--skip-collect",
        action="store_true",
        help="Skip Prometheus collection (show structure only)",
    )


def handle_portfolio_command(args: argparse.Namespace) -> int:
    """Handle portfolio command."""
    return portfolio_command(
        prometheus_url=getattr(args, "prometheus_url", None),
        details=getattr(args, "details", False),
        skip_collect=getattr(args, "skip_collect", False),
    )
