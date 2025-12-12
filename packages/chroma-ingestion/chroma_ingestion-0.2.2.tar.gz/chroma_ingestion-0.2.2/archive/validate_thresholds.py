#!/usr/bin/env python3
"""Automated threshold validation and drift detection.

This script validates that distance thresholds remain calibrated and detects
when embedding behavior changes significantly (drift detection).

Can be run standalone, in CI/CD, or as a periodic health check.
"""

import json
import sys
from datetime import datetime

from chroma_ingestion.retrieval import CodeRetriever

# Calibrated threshold ranges (from empirical testing Dec 2, 2025)
EXCELLENT_THRESHOLD = 0.8
GOOD_THRESHOLD = 1.0
OKAY_THRESHOLD = 1.2
POOR_THRESHOLD = float("inf")

# Test queries with expected agents and acceptable distance ranges
TEST_QUERIES = [
    {
        "query": "React hooks patterns",
        "expected_agents": ["frontend-architect.prompt.md"],
        "expected_range": (1.0, 1.3),
        "description": "Frontend component patterns",
    },
    {
        "query": "CI/CD pipeline",
        "expected_agents": ["devops-architect.prompt.md", "quality-engineer.prompt.md"],
        "expected_range": (1.0, 1.3),
        "description": "DevOps infrastructure automation",
    },
    {
        "query": "backend architecture system design",
        "expected_agents": ["backend-architect.prompt.md"],
        "expected_range": (0.7, 0.9),
        "description": "Backend design patterns",
    },
    {
        "query": "security patterns",
        "expected_agents": ["security-engineer.prompt.md"],
        "expected_range": (0.9, 1.2),
        "description": "Security best practices",
    },
]


class ThresholdValidator:
    """Validates distance thresholds and detects embedding drift."""

    def __init__(self, collection_name: str = "original_agents"):
        """Initialize validator with collection.

        Args:
            collection_name: Chroma collection to validate
        """
        self.collection_name = collection_name
        self.retriever = CodeRetriever(collection_name)
        self.results = []
        self.drift_detected = False

    def validate_query(self, query_config: dict) -> dict:
        """Validate a single query against expected behavior.

        Args:
            query_config: Query configuration with expected results

        Returns:
            Validation result dictionary
        """
        query = query_config["query"]
        expected_agents = query_config["expected_agents"]
        expected_range = query_config["expected_range"]
        description = query_config["description"]

        # Run query
        results = self.retriever.query(query, n_results=3)

        if not results:
            return {
                "query": query,
                "description": description,
                "status": "ERROR",
                "message": "No results returned",
                "distance": None,
                "agent": None,
            }

        top_result = results[0]
        agent = top_result["metadata"]["filename"]
        distance = top_result["distance"]

        # Check if expected agent found
        agent_found = any(exp in agent for exp in expected_agents)

        # Check if distance within expected range
        in_range = expected_range[0] <= distance <= expected_range[1]

        if not agent_found:
            status = "FAIL"
            message = f"Expected {expected_agents[0]} but got {agent}"
        elif not in_range:
            status = "DRIFT"
            message = f"Distance {distance:.4f} outside expected range {expected_range}"
            self.drift_detected = True
        else:
            status = "PASS"
            message = f"Distance {distance:.4f} within expected range {expected_range}"

        return {
            "query": query,
            "description": description,
            "status": status,
            "message": message,
            "distance": distance,
            "agent": agent,
            "expected_agents": expected_agents,
            "expected_range": expected_range,
            "agent_found": agent_found,
            "distance_in_range": in_range,
        }

    def run_validation(self) -> list[dict]:
        """Run all validation tests.

        Returns:
            List of validation results
        """
        print(f"\n{'='*70}")
        print(f"THRESHOLD VALIDATION: {self.collection_name}")
        print(f"Date: {datetime.now().isoformat()}")
        print(f"{'='*70}\n")

        for i, query_config in enumerate(TEST_QUERIES, 1):
            result = self.validate_query(query_config)
            self.results.append(result)

            # Print result
            status_emoji = {"PASS": "✅", "DRIFT": "⚠️ ", "FAIL": "❌", "ERROR": "💥"}[
                result["status"]
            ]

            print(f"{status_emoji} Test {i}: {result['description']}")
            print(f"   Query: {result['query']}")
            print(f"   Result: {result['agent']} (distance: {result['distance']:.4f})")
            if result["expected_range"]:
                print(f"   Expected range: {result['expected_range']}")
            print(f"   Message: {result['message']}\n")

        return self.results

    def print_summary(self) -> int:
        """Print validation summary and return exit code.

        Returns:
            0 if all tests pass, 1 if drift detected, 2 if tests failed
        """
        passed = sum(1 for r in self.results if r["status"] == "PASS")
        drifts = sum(1 for r in self.results if r["status"] == "DRIFT")
        failed = sum(1 for r in self.results if r["status"] == "FAIL")
        errors = sum(1 for r in self.results if r["status"] == "ERROR")

        total = len(self.results)

        print(f"\n{'='*70}")
        print("SUMMARY")
        print(f"{'='*70}")
        print(f"Total Tests: {total}")
        print(f"  ✅ Passed: {passed}/{total}")
        print(f"  ⚠️  Drift:  {drifts}/{total}")
        print(f"  ❌ Failed: {failed}/{total}")
        print(f"  💥 Error:  {errors}/{total}\n")

        if drifts > 0:
            print("⚠️  DRIFT DETECTED!")
            print("   Embedding behavior has changed from expected ranges.")
            print("   Consider re-running with updated test queries.")
            print("   The collection may need re-ingestion or recalibration.\n")
            return 1

        if failed > 0 or errors > 0:
            print("❌ VALIDATION FAILED!")
            print("   Some tests did not find expected agents.")
            print("   The collection may be corrupted or have stale data.\n")
            return 2

        print("✅ ALL TESTS PASSED!")
        print("   Distance thresholds remain well-calibrated.\n")
        return 0

    def save_results(self, output_file: str = "threshold_validation_results.json"):
        """Save validation results to JSON file.

        Args:
            output_file: Path to output file
        """
        output_data = {
            "timestamp": datetime.now().isoformat(),
            "collection": self.collection_name,
            "tests_passed": sum(1 for r in self.results if r["status"] == "PASS"),
            "tests_total": len(self.results),
            "drift_detected": self.drift_detected,
            "results": self.results,
        }

        with open(output_file, "w") as f:
            json.dump(output_data, f, indent=2)

        print(f"📁 Results saved to: {output_file}\n")

    def generate_report(self) -> str:
        """Generate a markdown report of validation results.

        Returns:
            Markdown formatted report
        """
        report = f"""# Threshold Validation Report

**Date:** {datetime.now().isoformat()}
**Collection:** {self.collection_name}
**Drift Detected:** {'Yes ⚠️' if self.drift_detected else 'No ✅'}

## Results

| Test | Query | Distance | Expected | Status |
|------|-------|----------|----------|--------|
"""
        for result in self.results:
            status_icon = {"PASS": "✅", "DRIFT": "⚠️", "FAIL": "❌", "ERROR": "💥"}[
                result["status"]
            ]

            exp_range = (
                f"{result['expected_range'][0]}-{result['expected_range'][1]}"
                if result["expected_range"]
                else "N/A"
            )

            report += (
                f"| {result['description']} | {result['query']} | "
                f"{result['distance']:.4f} | {exp_range} | {status_icon} |\n"
            )

        report += "\n## Summary\n"
        report += f"- Tests Passed: {sum(1 for r in self.results if r['status'] == 'PASS')}/{len(self.results)}\n"
        report += f"- Drift Detected: {sum(1 for r in self.results if r['status'] == 'DRIFT')}\n"
        report += f"- Tests Failed: {sum(1 for r in self.results if r['status'] == 'FAIL')}\n"

        return report


def main():
    """Run threshold validation from command line."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Validate distance thresholds and detect embedding drift"
    )
    parser.add_argument(
        "--collection",
        default="original_agents",
        help="Chroma collection to validate (default: original_agents)",
    )
    parser.add_argument(
        "--output",
        default="threshold_validation_results.json",
        help="Output file for results (default: threshold_validation_results.json)",
    )
    parser.add_argument(
        "--report",
        action="store_true",
        help="Generate markdown report (saved as validation_report.md)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail on drift detection (exit code 1) instead of just warning",
    )

    args = parser.parse_args()

    # Run validation
    validator = ThresholdValidator(args.collection)
    validator.run_validation()

    # Print summary and get exit code
    exit_code = validator.print_summary()

    # Save results
    validator.save_results(args.output)

    # Generate report if requested
    if args.report:
        report = validator.generate_report()
        report_file = "validation_report.md"
        with open(report_file, "w") as f:
            f.write(report)
        print(f"📋 Report saved to: {report_file}\n")

    # Adjust exit code for strict mode
    if args.strict and validator.drift_detected:
        exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
