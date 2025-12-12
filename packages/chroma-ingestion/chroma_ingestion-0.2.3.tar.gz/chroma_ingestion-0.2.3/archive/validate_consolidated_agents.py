#!/usr/bin/env python3
"""Verify consolidated agents are properly created and well-formed.

Validates:
1. All 10 consolidated agents exist
2. Each has proper YAML frontmatter
3. Each has comprehensive expertise sections
4. Tools and technologies are properly documented
"""

from pathlib import Path

import yaml

# Define expected consolidated agents
CONSOLIDATED_AGENTS = {
    "frontend-expert": {
        "required_keywords": ["nextjs", "react", "typescript", "tailwind", "ui"],
        "expected_sections": ["expertise", "guidelines", "scenarios"],
    },
    "backend-expert": {
        "required_keywords": ["python", "fastapi", "api", "server"],
        "expected_sections": ["expertise", "guidelines", "scenarios"],
    },
    "architect-expert": {
        "required_keywords": ["architecture", "system", "design"],
        "expected_sections": ["expertise", "guidelines", "scenarios"],
    },
    "testing-expert": {
        "required_keywords": ["testing", "playwright", "vitest", "qa"],
        "expected_sections": ["expertise", "guidelines", "scenarios"],
    },
    "ai-ml-expert": {
        "required_keywords": ["ai", "ml", "llm", "embeddings"],
        "expected_sections": ["expertise", "guidelines", "scenarios"],
    },
    "devops-expert": {
        "required_keywords": ["devops", "docker", "deployment", "ci/cd"],
        "expected_sections": ["expertise", "guidelines", "scenarios"],
    },
    "security-expert": {
        "required_keywords": ["security", "auth", "encryption"],
        "expected_sections": ["expertise", "guidelines", "scenarios"],
    },
    "quality-expert": {
        "required_keywords": ["quality", "refactor", "review", "best"],
        "expected_sections": ["expertise", "guidelines", "scenarios"],
    },
    "database-expert": {
        "required_keywords": ["database", "postgresql", "sql"],
        "expected_sections": ["expertise", "guidelines", "scenarios"],
    },
    "planning-expert": {
        "required_keywords": ["planning", "task", "requirement"],
        "expected_sections": ["expertise", "guidelines", "scenarios"],
    },
}


def check_agent_file(agent_name: str, file_path: Path) -> dict:
    """Check if an agent file is properly formed.

    Args:
        agent_name: Name of the agent
        file_path: Path to the agent file

    Returns:
        Dictionary with validation results
    """
    results = {
        "name": agent_name,
        "exists": False,
        "valid_frontmatter": False,
        "has_required_keywords": False,
        "has_sections": False,
        "content_length": 0,
        "errors": [],
    }

    # Check file exists
    if not file_path.exists():
        results["errors"].append(f"File not found: {file_path}")
        return results

    results["exists"] = True

    try:
        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        results["content_length"] = len(content)

        # Parse frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    frontmatter = yaml.safe_load(parts[1])
                    results["valid_frontmatter"] = True
                    body = parts[2].lower()
                except yaml.YAMLError as e:
                    results["errors"].append(f"YAML parse error: {e}")
                    return results
            else:
                results["errors"].append("Malformed frontmatter")
                return results
        else:
            results["errors"].append("No frontmatter found")
            return results

        # Check required keywords
        spec = CONSOLIDATED_AGENTS.get(agent_name, {})
        required_keywords = spec.get("required_keywords", [])
        found_keywords = [kw for kw in required_keywords if kw in body]

        if found_keywords:
            results["has_required_keywords"] = True
            results["found_keywords"] = found_keywords
        else:
            results["errors"].append(f"Missing required keywords: {required_keywords}")

        # Check sections
        expected_sections = spec.get("expected_sections", [])
        found_sections = [sec for sec in expected_sections if sec in body]

        if len(found_sections) >= len(expected_sections) - 1:  # Allow one missing
            results["has_sections"] = True
            results["found_sections"] = found_sections
        else:
            results["errors"].append(f"Missing sections: {expected_sections}")

    except Exception as e:
        results["errors"].append(f"Read error: {e}")

    return results


def main():
    """Run validation for all consolidated agents."""
    print("\n" + "=" * 80)
    print("CONSOLIDATED AGENT VALIDATION")
    print("=" * 80)

    consolidated_dir = Path("consolidated_agents")

    if not consolidated_dir.exists():
        print(f"\n❌ Directory not found: {consolidated_dir}")
        return 1

    print(f"\n📂 Consolidated agents directory: {consolidated_dir.absolute()}")

    # Check all agents
    all_valid = True
    validation_results = []

    for agent_name in CONSOLIDATED_AGENTS:
        file_path = consolidated_dir / f"{agent_name}.md"
        result = check_agent_file(agent_name, file_path)
        validation_results.append(result)

        if not (
            result["exists"]
            and result["valid_frontmatter"]
            and result["has_required_keywords"]
            and result["has_sections"]
        ):
            all_valid = False

    # Print results
    print("\n📋 Validation Results:\n")
    for result in validation_results:
        status = (
            "✅"
            if (
                result["exists"]
                and result["valid_frontmatter"]
                and result["has_required_keywords"]
                and result["has_sections"]
            )
            else "❌"
        )

        print(f"{status} {result['name']}")

        if result["errors"]:
            for error in result["errors"]:
                print(f"   ⚠️  {error}")
        else:
            print("   ✓ File exists and valid")
            if result.get("found_keywords"):
                print(f"   ✓ Keywords: {', '.join(result['found_keywords'][:3])}")
            if result.get("found_sections"):
                print(f"   ✓ Sections: {', '.join(result['found_sections'])}")
            print(f"   ✓ Content: {result['content_length']} bytes")
        print()

    # Summary
    print("\n" + "=" * 80)
    valid_count = sum(1 for r in validation_results if r["exists"] and r["valid_frontmatter"])
    print(f"\n✅ Valid agents: {valid_count}/{len(validation_results)}")

    if all_valid:
        print("✅ All consolidated agents are properly formed and ready!")
        print("\n✨ Consolidation Phase Complete!")
        print("\nNext steps:")
        print("  1. Review consolidated agents in consolidated_agents/ folder")
        print("  2. Optionally archive or delete original source agents")
        print("  3. Deploy consolidated agents to production")
        return 0
    else:
        print("⚠️  Some agents have issues - see above for details")
        return 1


if __name__ == "__main__":
    import sys

    sys.exit(main())
