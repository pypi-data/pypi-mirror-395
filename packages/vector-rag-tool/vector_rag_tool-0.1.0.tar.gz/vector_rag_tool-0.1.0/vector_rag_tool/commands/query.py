"""Query command for vector-rag-tool.

This module provides CLI command for querying vector stores with text input.
Supports JSON output, stdin input, and customizable result display.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import json
import sys
from typing import Any

import click

from vector_rag_tool.core.backend_factory import get_backend
from vector_rag_tool.core.models import SimilarityLevel
from vector_rag_tool.logging_config import get_logger, setup_logging
from vector_rag_tool.services.querier import Querier

logger = get_logger(__name__)


@click.command()
@click.argument("text", required=False)
@click.option(
    "--store",
    "-s",
    required=False,
    help="Name of the vector store to query",
)
@click.option(
    "--top-k",
    "-k",
    default=5,
    type=int,
    help="Number of top results to return (default: 5)",
)
@click.option(
    "--json",
    "output_json",
    is_flag=True,
    help="Output results in JSON format",
)
@click.option(
    "--stdin",
    is_flag=True,
    help="Read query text from stdin",
)
@click.option(
    "--bucket",
    "-b",
    help="S3 bucket name for remote vector storage",
)
@click.option(
    "--region",
    "-r",
    default="eu-central-1",
    help="AWS region for S3 Vectors (default: eu-central-1)",
)
@click.option(
    "--profile",
    "-p",
    help="AWS profile name for authentication",
)
@click.option(
    "--snippet-length",
    "-l",
    type=int,
    default=300,
    help="Max length of content snippets in characters (default: 300)",
)
@click.option(
    "--full",
    "-F",
    is_flag=True,
    help="Return full chunk content instead of snippets",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
def query(
    text: str | None,
    store: str | None,
    top_k: int,
    output_json: bool,
    stdin: bool,
    bucket: str | None,
    region: str,
    profile: str | None,
    snippet_length: int,
    full: bool,
    verbose: int,
) -> None:
    """Query a vector store for relevant document chunks.

    Examples:

    \b
        # Basic query with local FAISS backend
        vector-rag-tool query "machine learning" --store my-store

    \b
        # Get more results
        vector-rag-tool query "deep learning" --store my-store --top-k 10

    \b
        # Query remote S3 Vectors backend
        vector-rag-tool query "neural networks" --store my-store \\
            --bucket my-vector-store --profile dev

    \b
        # Query with custom region
        vector-rag-tool query "transformer models" --store my-store \\
            --bucket my-vector-store --region us-west-2 --profile prod

    \b
        # Output as JSON
        vector-rag-tool query "attention mechanism" --store my-store --json

    \b
        # Read from stdin (pipeable)
        echo "query text" | vector-rag-tool query --store my-store --stdin

    \b
        # Verbose output
        vector-rag-tool query "quantum computing" --store my-store -vv

    \b
    Output Format:
        Returns matching document chunks with:
        - File path and line numbers
        - Relevance score (0-1)
        - Content snippet
        - Metadata (tags, links, etc.)
    """
    # Show help if missing required arguments (and not reading from stdin)
    if not store or (not text and not stdin):
        click.echo("vector-rag-tool query - Search vector store with semantic queries")
        click.echo("")
        click.echo("Use cases:")
        click.echo('  vector-rag-tool query "how does auth work" --store my-store')
        click.echo('  vector-rag-tool query "error handling" --store my-store --top-k 10')
        click.echo('  vector-rag-tool query "database schema" --store my-store --full --json')
        click.echo('  echo "query" | vector-rag-tool query --store my-store --stdin')
        click.echo("")
        click.echo("Required:")
        click.echo("  TEXT        Query text (or use --stdin)")
        click.echo("  --store/-s  Name of the vector store")
        click.echo("")
        click.echo("Use 'vector-rag-tool query --help' for all options")
        return

    setup_logging(verbose)

    # Get query text from stdin if requested
    if stdin:
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
            if not text:
                click.echo("✗ No input received from stdin", err=True)
                raise click.ClickException("Empty stdin input")
        else:
            click.echo("✗ No stdin input available", err=True)
            raise click.ClickException("Cannot read from stdin")

    # Validate query text
    if not text:
        click.echo("✗ Query text is required", err=True)
        raise click.ClickException(
            "Provide query text as argument or use --stdin to read from pipe"
        )

    # Validate top_k
    if top_k < 1:
        click.echo("✗ top-k must be at least 1", err=True)
        raise click.ClickException("Invalid top-k value")

    try:
        logger.info("Querying store '%s' with text: %s", store, text[:100])
        logger.debug("Parameters: top_k=%d, json_output=%s", top_k, output_json)

        # Get backend based on configuration
        backend = get_backend(bucket=bucket, region=region, profile=profile)
        logger.debug(
            "Using backend: %s (bucket=%s, region=%s, profile=%s)",
            type(backend).__name__,
            bucket,
            region,
            profile,
        )

        # Initialize querier with backend
        querier = Querier(backend=backend)

        # Check if store exists
        if not querier.backend.store_exists(store):
            click.echo(f"✗ Store '{store}' does not exist", err=True)
            available_stores = querier.list_stores()
            if available_stores:
                click.echo(f"\nAvailable stores: {', '.join(available_stores)}")
            raise click.ClickException(f"Store '{store}' not found")

        # Perform query
        # Use large snippet_length when --full is requested
        effective_snippet_length = 100000 if full else snippet_length

        result = querier.query(
            store_name=store,
            query_text=text,
            top_k=top_k,
            min_score=0.0,  # Let user see all results
            snippet_length=effective_snippet_length,
        )

        logger.info(
            "Query completed: %d results in %.3f seconds",
            result.total_results,
            result.query_time or 0,
        )

        # Output results
        if output_json:
            _output_json(result, text, store, top_k)
        else:
            _output_text(result, text, store, top_k)

        logger.info("Query results displayed successfully")

    except ValueError as e:
        logger.error("Query validation failed: %s", e)
        click.echo(f"✗ Query failed: {e}", err=True)
        raise click.ClickException(str(e))
    except RuntimeError as e:
        logger.error("Query runtime error: %s", e)
        click.echo(f"✗ Query error: {e}", err=True)
        raise click.ClickException(str(e))
    except Exception as e:
        logger.error("Unexpected query error: %s", e)
        click.echo(f"✗ Unexpected error: {e}", err=True)
        raise click.ClickException(str(e))


def _output_text(result: Any, query: str, store: str, top_k: int) -> None:
    """Output query results in human-readable text format."""
    if not result.chunks:
        click.echo(f"\nNo results found for query: {query!r}")
        click.echo(f"Store: {store}")
        return

    click.echo(f"\nQuery: {query!r}")
    click.echo(f"Store: {store}")
    click.echo(f"Results: {result.total_results}/{top_k}")
    if result.query_time:
        click.echo(f"Time: {result.query_time:.3f}s")
    click.echo()

    for i, (chunk, score) in enumerate(result.get_sorted_chunks(), 1):
        # Get similarity level
        similarity_level = SimilarityLevel.from_score(score)

        # Header with score and similarity level
        click.echo(
            f"{i}. Score: {score:.3f} ({similarity_level.value}: {similarity_level.description()})"
        )

        # File path and line numbers
        metadata = chunk.metadata
        file_path = str(metadata.source_file)
        if metadata.line_start and metadata.line_end:
            click.echo(f"   📄 {file_path}:{metadata.line_start}-{metadata.line_end}")
        else:
            click.echo(f"   📄 {file_path}")

        # Additional metadata
        if metadata.tags:
            click.echo(f"   🏷️  Tags: {', '.join(metadata.tags)}")
        if metadata.links:
            click.echo(f"   🔗 Links: {', '.join(metadata.links)}")

        # Content snippet
        click.echo(f"\n   {chunk.content}")
        click.echo()


def _output_json(result: Any, query: str, store: str, top_k: int) -> None:
    """Output query results in JSON format."""
    output = {
        "query": query,
        "store": store,
        "total_results": result.total_results,
        "requested_results": top_k,
        "query_time": result.query_time,
        "metadata": result.metadata,
        "results": [],
    }

    for chunk, score in result.get_sorted_chunks():
        metadata = chunk.metadata
        similarity_level = SimilarityLevel.from_score(score)

        result_item = {
            "score": score,
            "similarity_level": similarity_level.value,
            "similarity_description": similarity_level.description(),
            "file_path": str(metadata.source_file),
            "line_start": metadata.line_start,
            "line_end": metadata.line_end,
            "chunk_index": metadata.chunk_index,
            "total_chunks": metadata.total_chunks,
            "content": chunk.content,
            "word_count": metadata.word_count,
            "char_count": metadata.char_count,
            "tags": metadata.tags,
            "links": metadata.links,
            "frontmatter": metadata.frontmatter,
        }

        output["results"].append(result_item)

    # Print JSON
    json_output = json.dumps(output, indent=2, ensure_ascii=False)
    click.echo(json_output)
