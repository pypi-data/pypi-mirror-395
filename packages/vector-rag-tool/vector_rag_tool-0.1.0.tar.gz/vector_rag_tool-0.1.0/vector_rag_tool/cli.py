"""CLI entry point for vector-rag-tool.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from vector_rag_tool.commands.index import index
from vector_rag_tool.commands.query import query
from vector_rag_tool.commands.store import store
from vector_rag_tool.completion import completion_command
from vector_rag_tool.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


@click.group(invoke_without_command=True)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
@click.version_option(version="0.1.0")
@click.pass_context
def main(ctx: click.Context, verbose: int) -> None:
    """RAG tool with local FAISS and remote S3 Vectors backends."""
    # Setup logging based on verbosity count
    setup_logging(verbose)

    # If no subcommand is provided, show workflow guide
    if ctx.invoked_subcommand is None:
        click.echo("vector-rag-tool - Local RAG with Ollama embeddings and FAISS vector search")
        click.echo("")
        click.echo("Workflow:")
        click.echo("  1. Create store:  vector-rag-tool store create my-store")
        click.echo(
            '  2. Index files:   vector-rag-tool index "**/*.py" --store my-store --no-dry-run'
        )
        click.echo(
            '  3. Query:         vector-rag-tool query "how does auth work" --store my-store'
        )
        click.echo("")
        click.echo("Agent workflow (JSON output):")
        click.echo('  vector-rag-tool query "error handling" --store my-store --full --json')
        click.echo("")
        click.echo("Use --help for all commands and options")


# Add subcommands
main.add_command(completion_command)
main.add_command(index)
main.add_command(query)
main.add_command(store)


if __name__ == "__main__":
    main()
