#!/usr/bin/env python3
"""
Agent Configuration and Usability Testing

Tests consolidated agents for:
- Configuration validity (YAML, required fields)
- Content quality and completeness
- Field presence and structure
- Tool integration documentation
- Real-world usability scenarios
"""

import json
import sys
from datetime import datetime
from pathlib import Path

import yaml


def load_agent(filepath):
    """Load and parse an agent markdown file."""
    with open(filepath) as f:
        content = f.read()

    # Parse YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter_str = parts[1]
            markdown_content = parts[2]
            frontmatter = yaml.safe_load(frontmatter_str)
            return frontmatter, markdown_content

    return None, content


def validate_agent(agent_name, filepath):
    """Validate a single agent file."""
    results = {
        "agent": agent_name,
        "filepath": str(filepath),
        "checks": {},
        "metrics": {},
        "issues": [],
    }

    # Load agent
    try:
        frontmatter, content = load_agent(filepath)
        results["checks"]["file_loads"] = True
    except Exception as e:
        results["checks"]["file_loads"] = False
        results["issues"].append(f"Failed to load file: {e}")
        return results

    # Check frontmatter
    required_frontmatter = ["name", "description", "model", "tools"]
    frontmatter = frontmatter or {}

    results["checks"]["has_frontmatter"] = bool(frontmatter)
    results["checks"]["has_name"] = "name" in frontmatter
    results["checks"]["has_description"] = "description" in frontmatter
    results["checks"]["has_model"] = "model" in frontmatter
    results["checks"]["has_tools"] = "tools" in frontmatter

    for field in required_frontmatter:
        if field not in frontmatter:
            results["issues"].append(f"Missing required field: {field}")

    # Check content sections
    content_lower = content.lower()
    sections = {
        "role": "your role" in content_lower,
        "expertise": "expertise" in content_lower,
        "guidelines": "guidelines" in content_lower,
        "tools": "tools" in content_lower or "mcp" in content_lower,
        "scenarios": "scenario" in content_lower,
    }

    for section, exists in sections.items():
        results["checks"][f"has_{section}_section"] = exists
        if not exists:
            results["issues"].append(f"Missing content section: {section}")

    # Metrics
    results["metrics"]["file_size_bytes"] = len(open(filepath).read())
    results["metrics"]["content_length"] = len(content)
    results["metrics"]["frontmatter_fields"] = len(frontmatter) if frontmatter else 0

    # Tool validation
    if "tools" in frontmatter:
        tools = frontmatter["tools"]
        results["metrics"]["tool_count"] = len(tools) if isinstance(tools, list) else 1
        results["checks"]["has_mcp_tools"] = any("mcp" in str(t).lower() for t in tools)

    # Overall status
    all_checks_passed = all(results["checks"].values())
    results["overall_status"] = "PASS" if all_checks_passed else "FAIL"

    return results


def test_agent_scenarios(agent_name, frontmatter, content):
    """Test agent for real-world usability scenarios."""
    scenarios = []

    # Scenario 1: Can identify agent purpose
    if "description" in frontmatter:
        desc = frontmatter.get("description", "")
        scenarios.append(
            {
                "name": "Agent Purpose Clear",
                "status": "PASS" if len(desc) > 20 else "FAIL",
                "detail": desc[:100],
            }
        )

    # Scenario 2: Has concrete expertise areas
    expertise_match = "expertise" in content.lower()
    scenarios.append(
        {
            "name": "Expertise Documented",
            "status": "PASS" if expertise_match else "FAIL",
            "detail": "Expertise section present" if expertise_match else "No expertise section",
        }
    )

    # Scenario 3: Has actionable guidelines
    guidelines_match = "guidelines" in content.lower()
    scenarios.append(
        {
            "name": "Guidelines Provided",
            "status": "PASS" if guidelines_match else "FAIL",
            "detail": "Guidelines section present" if guidelines_match else "No guidelines section",
        }
    )

    # Scenario 4: Integrates with tools
    if "tools" in frontmatter:
        tools = frontmatter.get("tools", [])
        tool_integration = len(tools) > 3
        scenarios.append(
            {
                "name": "Tool Integration",
                "status": "PASS" if tool_integration else "FAIL",
                "detail": f"{len(tools)} tools configured",
            }
        )

    # Scenario 5: Can handle common tasks
    keywords = ["task", "scenario", "example", "pattern"]
    has_examples = any(kw in content.lower() for kw in keywords)
    scenarios.append(
        {
            "name": "Example Scenarios",
            "status": "PASS" if has_examples else "WARN",
            "detail": (
                "Scenario examples documented" if has_examples else "Limited scenario documentation"
            ),
        }
    )

    return scenarios


def main():
    """Run comprehensive agent validation."""

    print("\n" + "=" * 80)
    print("🤖 CONSOLIDATED AGENTS - CONFIGURATION & USABILITY VALIDATION")
    print("=" * 80)
    print(f"Timestamp: {datetime.now().isoformat()}\n")

    # Find all agent files
    agent_dir = Path("consolidated_agents")
    agent_files = list(agent_dir.glob("*.md"))
    agent_files = [f for f in agent_files if f.name != "CONSOLIDATION_ARCHIVE.md"]
    agent_files.sort()

    print(f"📁 Found {len(agent_files)} consolidated agents\n")

    # Validate each agent
    all_results = []
    total_checks = 0
    passed_checks = 0

    print("🧪 VALIDATION RESULTS")
    print("-" * 80)

    for filepath in agent_files:
        agent_name = filepath.stem
        results = validate_agent(agent_name, filepath)

        # Test scenarios
        if results["checks"]["file_loads"]:
            frontmatter, content = load_agent(filepath)
            frontmatter = frontmatter or {}
            scenarios = test_agent_scenarios(agent_name, frontmatter, content)
            results["scenarios"] = scenarios
        else:
            results["scenarios"] = []

        all_results.append(results)

        # Count checks
        for check, passed in results["checks"].items():
            total_checks += 1
            if passed:
                passed_checks += 1

        # Print summary
        status_symbol = "✅" if results["overall_status"] == "PASS" else "⚠️"
        print(f"\n{status_symbol} {agent_name}")
        print(f"   File: {filepath.name}")
        print(f"   Size: {results['metrics']['file_size_bytes']} bytes")
        print(f"   Status: {results['overall_status']}")

        if results["issues"]:
            for issue in results["issues"]:
                print(f"   ⚠️  {issue}")

        # Print scenario results
        for scenario in results["scenarios"]:
            symbol = (
                "✅"
                if scenario["status"] == "PASS"
                else "⚠️"
                if scenario["status"] == "WARN"
                else "❌"
            )
            print(f"   {symbol} {scenario['name']}: {scenario['detail']}")

    # Summary statistics
    print("\n" + "=" * 80)
    print("📊 VALIDATION SUMMARY")
    print("=" * 80)

    passed_agents = sum(1 for r in all_results if r["overall_status"] == "PASS")
    total_agents = len(all_results)

    print(f"\n✅ Agents Passing All Checks: {passed_agents}/{total_agents}")
    print(f"✅ Configuration Checks Passed: {passed_checks}/{total_checks}")
    print(f"📈 Success Rate: {passed_checks / total_checks * 100:.1f}%")

    # Detailed metrics
    print("\n📋 Agent Metrics:")
    total_size = sum(r["metrics"]["file_size_bytes"] for r in all_results)
    avg_size = total_size / len(all_results) if all_results else 0
    avg_tools = (
        sum(r["metrics"].get("tool_count", 0) for r in all_results) / len(all_results)
        if all_results
        else 0
    )

    print(f"   Total size: {total_size:,} bytes")
    print(f"   Average size: {avg_size:,.0f} bytes per agent")
    print(f"   Average tools per agent: {avg_tools:.1f}")

    # Scenario results
    print("\n🎯 Scenario Results:")
    all_scenarios = {}
    for result in all_results:
        for scenario in result.get("scenarios", []):
            if scenario["name"] not in all_scenarios:
                all_scenarios[scenario["name"]] = {"PASS": 0, "FAIL": 0, "WARN": 0}
            all_scenarios[scenario["name"]][scenario["status"]] += 1

    for scenario_name, counts in all_scenarios.items():
        total_scenario = counts["PASS"] + counts["FAIL"] + counts["WARN"]
        pass_rate = counts["PASS"] / total_scenario * 100 if total_scenario > 0 else 0
        print(f"   {scenario_name}: {counts['PASS']}/{total_scenario} passed ({pass_rate:.0f}%)")

    # Quality assessment
    print("\n" + "=" * 80)
    print("🎯 QUALITY ASSESSMENT")
    print("=" * 80)

    if passed_agents == total_agents:
        assessment = "🎉 EXCELLENT - All agents fully validated and ready for production"
    elif passed_agents >= total_agents * 0.9:
        assessment = "✅ VERY GOOD - Minor issues in some agents, generally production-ready"
    elif passed_agents >= total_agents * 0.8:
        assessment = "⚠️  ACCEPTABLE - Some agents need review, can be deployed with monitoring"
    else:
        assessment = "❌ NEEDS WORK - Significant issues requiring attention before production"

    print(f"\n{assessment}")

    # Deployment recommendation
    print("\n" + "=" * 80)
    print("🚀 DEPLOYMENT RECOMMENDATION")
    print("=" * 80)

    if passed_agents == total_agents:
        recommendation = "✅ READY FOR IMMEDIATE PRODUCTION DEPLOYMENT"
    else:
        recommendation = f"⚠️  STAGED DEPLOYMENT RECOMMENDED - Test in staging first, {total_agents - passed_agents} agent(s) need review"

    print(f"\n{recommendation}\n")

    # Save results
    results_file = "validation_report.json"
    with open(results_file, "w") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "summary": {
                    "total_agents": total_agents,
                    "agents_passed": passed_agents,
                    "configuration_checks_passed": passed_checks,
                    "total_checks": total_checks,
                    "success_rate_percent": passed_checks / total_checks * 100,
                },
                "agents": all_results,
                "scenarios": all_scenarios,
            },
            f,
            indent=2,
        )

    print(f"📄 Full report saved to: {results_file}\n")

    return 0 if passed_agents == total_agents else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Error during validation: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
