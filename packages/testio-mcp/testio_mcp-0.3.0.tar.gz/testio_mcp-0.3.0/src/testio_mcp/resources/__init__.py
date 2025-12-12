from pathlib import Path

from fastmcp import FastMCP


def register_resources(mcp: FastMCP) -> None:
    """Register MCP resources."""

    @mcp.resource("testio://knowledge/playbook")
    def get_playbook() -> str:
        """Expert heuristics for analyzing TestIO data (patterns, templates)."""
        playbook_path = Path(__file__).parent / "playbook.md"
        return playbook_path.read_text(encoding="utf-8")

    @mcp.resource("testio://knowledge/programmatic-access")
    def get_programmatic_access() -> str:
        """How to discover and use the TestIO REST API via OpenAPI schema."""
        access_path = Path(__file__).parent / "programmatic_access.md"
        return access_path.read_text(encoding="utf-8")
