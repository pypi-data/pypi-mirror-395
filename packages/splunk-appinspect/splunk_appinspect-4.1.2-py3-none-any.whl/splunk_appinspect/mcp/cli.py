import sys
from importlib.util import find_spec

import click

_MCP_AVAILABLE = find_spec("fastmcp") is not None


@click.group()
def mcp_cli(): ...


_short_help = "Start the MCP server."
if not _MCP_AVAILABLE:
    _short_help += " (Requires installation with mcp extra: splunk-appinspect[mcp])"


@mcp_cli.command(
    "mcp-server",
    short_help=_short_help,
)
def start_server():
    """Start the MCP server for AppInspect."""
    try:
        from .server import main as mcp_main
    except ImportError:
        click.echo(
            click.style(
                "Error: The MCP server requires additional dependencies "
                "which are in the optional 'mcp' group.\n"
                "Please install splunk-appinspect[mcp] to use this command.",
                fg="red",
            ),
            err=True,
        )
        sys.exit(1)

    mcp_main()
