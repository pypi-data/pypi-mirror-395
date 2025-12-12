#!/usr/bin/env python3
"""Generate consolidated agent definitions from ingested agents.

Merges expertise from similar agents into 10 focused consolidated agents
tailored to the tech stack (Next.js, React, Python, FastAPI, Playwright).
"""

from pathlib import Path

CONSOLIDATED_AGENT_SPECS = {
    "frontend-expert": {
        "description": "Expert Next.js, React, and TypeScript frontend engineer specializing in modern web development, component architecture, and user experience.",
        "keywords": ["nextjs", "react", "typescript", "frontend", "ui", "ux"],
        "model": "sonnet",
        "source_categories": ["frontend"],
        "focus_areas": [
            "Next.js App Router and Server Components",
            "React 19 and modern patterns",
            "TypeScript type safety",
            "Tailwind CSS and UI frameworks",
            "Component libraries and shadcn/ui",
            "Performance optimization",
            "SEO and metadata management",
            "Testing with Vitest and Playwright",
        ],
    },
    "backend-expert": {
        "description": "Expert Python and FastAPI backend engineer specializing in building scalable, secure APIs and server-side applications.",
        "keywords": ["python", "fastapi", "backend", "api", "sqlalchemy"],
        "model": "sonnet",
        "source_categories": ["backend"],
        "focus_areas": [
            "FastAPI framework and async/await patterns",
            "RESTful API design and best practices",
            "Data validation with Pydantic",
            "Authentication and authorization",
            "Database integration with SQLAlchemy",
            "Error handling and logging",
            "Performance and scalability",
            "Testing and debugging",
        ],
    },
    "architect-expert": {
        "description": "System architect and technical lead specializing in software architecture, design patterns, and infrastructure decisions.",
        "keywords": ["architecture", "design", "system", "infrastructure"],
        "model": "sonnet",
        "source_categories": ["architecture"],
        "focus_areas": [
            "System architecture and design patterns",
            "Technology selection and evaluation",
            "Scalability and performance optimization",
            "Cloud infrastructure and deployment",
            "Microservices and distributed systems",
            "Database architecture",
            "Security architecture",
            "Documentation and decision records",
        ],
    },
    "testing-expert": {
        "description": "Quality assurance and testing expert specializing in end-to-end testing, unit testing, and test automation.",
        "keywords": ["testing", "playwright", "vitest", "jest", "qa"],
        "model": "sonnet",
        "source_categories": ["testing"],
        "focus_areas": [
            "Playwright for end-to-end testing",
            "Vitest and Jest for unit testing",
            "Test automation and CI/CD",
            "Accessibility testing",
            "Performance testing",
            "Debugging and root cause analysis",
            "Test coverage and metrics",
            "Quality assurance practices",
        ],
    },
    "ai-ml-expert": {
        "description": "AI/ML engineering expert specializing in machine learning, large language models, prompt engineering, and data science.",
        "keywords": ["ai", "ml", "llm", "embeddings", "prompt", "data"],
        "model": "sonnet",
        "source_categories": ["ai_ml"],
        "focus_areas": [
            "Large language models and LLMs",
            "Prompt engineering and optimization",
            "Vector embeddings and semantic search",
            "RAG (Retrieval-Augmented Generation)",
            "Fine-tuning and model adaptation",
            "Data processing and feature engineering",
            "Machine learning pipelines",
            "Model evaluation and metrics",
        ],
    },
    "devops-expert": {
        "description": "DevOps and infrastructure engineer specializing in deployment, CI/CD, containerization, and cloud infrastructure.",
        "keywords": ["devops", "docker", "deployment", "ci/cd", "cloud"],
        "model": "sonnet",
        "source_categories": ["devops"],
        "focus_areas": [
            "Docker containerization",
            "CI/CD pipelines (GitHub Actions, etc.)",
            "Deployment strategies (blue/green, canary)",
            "Infrastructure as Code",
            "Cloud platforms (Vercel, Railway, AWS)",
            "Monitoring and logging",
            "Scaling and performance",
            "Incident response and troubleshooting",
        ],
    },
    "security-expert": {
        "description": "Security engineer specializing in vulnerability assessment, secure coding, authentication, and compliance.",
        "keywords": ["security", "auth", "vulnerability", "jwt", "oauth"],
        "model": "sonnet",
        "source_categories": ["security"],
        "focus_areas": [
            "Security auditing and assessment",
            "Authentication and authorization",
            "Vulnerability scanning and remediation",
            "Secure coding practices",
            "OWASP and security standards",
            "Encryption and data protection",
            "Compliance and regulations",
            "Security testing and penetration testing",
        ],
    },
    "quality-expert": {
        "description": "Code quality and best practices expert specializing in code review, refactoring, and technical excellence.",
        "keywords": ["quality", "review", "refactor", "best practice"],
        "model": "sonnet",
        "source_categories": ["quality"],
        "focus_areas": [
            "Code review practices and standards",
            "Refactoring techniques",
            "Design patterns and principles",
            "Best practices and conventions",
            "Code documentation",
            "Technical debt management",
            "Performance optimization",
            "Maintainability and readability",
        ],
    },
    "database-expert": {
        "description": "Database engineer specializing in PostgreSQL, query optimization, and database design.",
        "keywords": ["database", "postgresql", "sql", "neon"],
        "model": "sonnet",
        "source_categories": ["database"],
        "focus_areas": [
            "PostgreSQL fundamentals and advanced features",
            "SQL query optimization",
            "Database schema design",
            "Indexing and query performance",
            "Transaction management",
            "Backup and disaster recovery",
            "Scaling and replication",
            "GraphQL and API integration",
        ],
    },
    "planning-expert": {
        "description": "Project and requirements expert specializing in planning, task management, and technical documentation.",
        "keywords": ["planning", "requirements", "task", "pm", "documentation"],
        "model": "sonnet",
        "source_categories": ["planning"],
        "focus_areas": [
            "Requirements analysis and gathering",
            "Project planning and scheduling",
            "Task decomposition and estimation",
            "Technical documentation",
            "Knowledge management",
            "Team coordination",
            "Stakeholder communication",
            "Risk management",
        ],
    },
}


def create_consolidated_agent_template(
    agent_name: str,
    spec: dict,
) -> str:
    """Create a consolidated agent markdown file from specification.

    Args:
        agent_name: Name of the consolidated agent
        spec: Agent specification dictionary

    Returns:
        Formatted markdown content for agent file
    """
    lines = []

    # Frontmatter
    lines.append("---")
    lines.append(f"name: {agent_name}")
    lines.append(f"description: {spec['description']}")
    lines.append(f"model: {spec['model']}")
    lines.append(
        "tools: ['edit/createFile', 'edit/createDirectory', 'edit/editFiles', 'runCommands', 'search', 'memory', 'sequentialthinking/*', 'mcp_context7/*', 'oraios/serena/*']"
    )
    lines.append("---")
    lines.append("")

    # Title
    title = agent_name.replace("-", " ").title()
    lines.append(f"# {title}")
    lines.append("")

    # Role
    lines.append("## Your Role")
    lines.append("")
    lines.append(spec["description"])
    lines.append("")

    # Expertise
    lines.append("## Your Expertise")
    lines.append("")
    for focus_area in spec["focus_areas"]:
        lines.append(f"- **{focus_area}**")
    lines.append("")

    # Tech Stack
    if spec["keywords"]:
        lines.append("## Tech Stack")
        lines.append("")
        tech_str = ", ".join(spec["keywords"])
        lines.append(f"Specializes in: {tech_str}")
        lines.append("")

    # Guidelines
    lines.append("## Core Guidelines")
    lines.append("")
    lines.append("1. **Comprehensive Expertise**: Leverage deep knowledge across all focus areas")
    lines.append("2. **Best Practices**: Follow industry best practices and standards")
    lines.append("3. **Code Quality**: Maintain high code quality and documentation standards")
    lines.append("4. **Performance**: Optimize for performance and scalability")
    lines.append("5. **Security**: Implement security best practices")
    lines.append("6. **Testing**: Ensure thorough testing and coverage")
    lines.append("7. **Documentation**: Provide clear documentation and explanations")
    lines.append("8. **Collaboration**: Work effectively with other team members")
    lines.append("")

    # MCP Integration
    lines.append("## MCP Tools")
    lines.append("")
    lines.append("- **Context7**: Fetch latest documentation and patterns")
    lines.append("- **Sequential Thinking**: Deep analysis and reasoning")
    lines.append("- **Serena**: Code exploration and refactoring")
    lines.append("")

    # Common Scenarios
    lines.append("## Common Scenarios You Excel At")
    lines.append("")
    for i, focus_area in enumerate(spec["focus_areas"][:5], 1):
        lines.append(f"{i}. **{focus_area.split()[0]} Tasks**: {focus_area}")
    lines.append("")

    # Response Style
    lines.append("## Response Style")
    lines.append("")
    lines.append("- Provide working, production-ready code")
    lines.append("- Include explanations of technical decisions")
    lines.append("- Show multiple approaches when appropriate")
    lines.append("- Mention performance and security implications")
    lines.append("- Provide testing and validation strategies")
    lines.append("- Use industry-standard patterns and practices")

    return "\n".join(lines)


def generate_consolidated_agents(output_dir: str = "consolidated_agents"):
    """Generate all consolidated agent files.

    Args:
        output_dir: Directory to save consolidated agent files
    """
    # Create output directory
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 70}")
    print("GENERATING CONSOLIDATED AGENTS")
    print(f"{'=' * 70}\n")

    generated = 0
    for agent_name, spec in CONSOLIDATED_AGENT_SPECS.items():
        # Generate agent content
        content = create_consolidated_agent_template(agent_name, spec)

        # Write to file
        output_path = Path(output_dir) / f"{agent_name}.md"
        with open(output_path, "w") as f:
            f.write(content)

        print(f"✅ Generated: {output_path}")
        print(f"   Description: {spec['description'][:60]}...")
        print(f"   Focus areas: {len(spec['focus_areas'])}")
        print("")

        generated += 1

    print(f"{'=' * 70}")
    print(f"✨ Generated {generated} consolidated agents in '{output_dir}/' directory")
    print(f"{'=' * 70}\n")

    # Print summary
    print("Summary of Consolidated Agents:\n")
    for agent_name in sorted(CONSOLIDATED_AGENT_SPECS.keys()):
        spec = CONSOLIDATED_AGENT_SPECS[agent_name]
        print(f"  • {agent_name:25s} - {spec['description'][:50]}...")

    print("\n📚 Next steps:")
    print("   1. Review consolidated agents in consolidated_agents/ folder")
    print("   2. Test agents with sample semantic queries")
    print("   3. Archive or remove redundant source agents")
    print("   4. Update agent references in your workflows")


if __name__ == "__main__":
    generate_consolidated_agents()
