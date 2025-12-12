"""Nox automation for code quality and testing."""

import nox

nox.options.default_venv_backend = "uv"
nox.options.reuse_existing_virtualenvs = True


@nox.session
def lint(session: nox.Session) -> None:
    """Run linters (ruff check)."""
    session.install("ruff")
    session.run("ruff", "check", "src", "tests")


@nox.session
def fmt(session: nox.Session) -> None:
    """Format code with ruff."""
    session.install("ruff")
    session.run("ruff", "format", "src", "tests")
    session.run("ruff", "check", "--fix", "src", "tests")


@nox.session
def type_check(session: nox.Session) -> None:
    """Run mypy type checking."""
    session.install(".", "mypy")
    session.run("mypy", "src")


@nox.session
def test(session: nox.Session) -> None:
    """Run pytest."""
    session.install(".[dev]")
    session.run(
        "pytest",
        "-v",
        "--cov=chroma_ingestion",
        "--cov-report=term-missing",
        *session.posargs,
    )


@nox.session
def docs(session: nox.Session) -> None:
    """Build documentation."""
    session.install(".[dev]")
    session.run("mkdocs", "build")
