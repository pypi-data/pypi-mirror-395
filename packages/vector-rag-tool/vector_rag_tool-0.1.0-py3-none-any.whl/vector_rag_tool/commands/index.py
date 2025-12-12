"""Index command for vector-rag-tool.

This module provides the index command that orchestrates file indexing
using the indexer service with progress tracking.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

from pathlib import Path

import click

from vector_rag_tool.core.backend_factory import get_backend
from vector_rag_tool.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


@click.command()
@click.argument("glob_pattern", nargs=-1, required=False)
@click.option(
    "--store",
    "-s",
    "store_name",
    required=False,
    help="Name of the vector store to index into",
)
@click.option(
    "--bucket",
    "-b",
    help="S3 bucket name for remote S3 Vectors storage",
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
    "--dry-run",
    "-n",
    is_flag=True,
    default=True,
    help="Preview what would be indexed without actually indexing (default: enabled)",
)
@click.option(
    "--no-dry-run",
    is_flag=True,
    default=False,
    help="Perform actual indexing (disables --dry-run)",
)
@click.option(
    "--incremental",
    "-i",
    is_flag=True,
    default=True,
    help="Skip unchanged files (default: enabled)",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="Force reindexing of all files, ignoring incremental mode",
)
@click.option(
    "--chunk-size",
    "-c",
    type=int,
    default=1500,
    help="Target chunk size in characters (default: 1500)",
)
@click.option(
    "--chunk-overlap",
    "-o",
    type=int,
    default=200,
    help="Number of characters to overlap between chunks (default: 200)",
)
@click.option(
    "--enable-openai",
    is_flag=True,
    default=False,
    help="Enable OpenAI for image descriptions in documents (requires OPENAI_API_KEY)",
)
@click.option(
    "--openai-model",
    default="gpt-4o",
    help="OpenAI model for image descriptions (default: gpt-4o)",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
def index(
    glob_pattern: tuple[str, ...],
    store_name: str | None,
    bucket: str | None,
    region: str,
    profile: str | None,
    dry_run: bool,
    no_dry_run: bool,
    incremental: bool,
    force: bool,
    chunk_size: int,
    chunk_overlap: int,
    enable_openai: bool,
    openai_model: str,
    verbose: int,
) -> None:
    """Index files matching glob patterns into a vector store.

    Supports text files (py, md, yaml, etc.) and documents (pdf, docx, xlsx, pptx).
    Documents are converted to Markdown using markitdown before indexing.

    Examples:

    \b
        # Preview indexing Python files (dry run)
        vector-rag-tool index "*.py" --store my-store

    \b
        # Actually index Markdown and Python files locally
        vector-rag-tool index "*.md" "*.py" --store my-store --no-dry-run

    \b
        # Index PDF and Word documents
        vector-rag-tool index "docs/**/*.pdf" "docs/**/*.docx" --store my-store --no-dry-run

    \b
        # Index images with OpenAI descriptions (requires OPENAI_API_KEY)
        vector-rag-tool index "images/**/*.png" --store my-store \\
            --enable-openai --no-dry-run

    \b
        # Index files to S3 Vectors with custom profile
        vector-rag-tool index "src/**/*.py" --store my-store \\
            --bucket my-vectors-bucket --profile dev --no-dry-run

    \b
        # Force reindex all files in a directory to S3
        vector-rag-tool index "docs/**/*.md" --store my-store \\
            --bucket my-vectors-bucket --region us-west-2 --force --no-dry-run

    \b
        # Incremental indexing (skip unchanged files)
        vector-rag-tool index "**/*.py" --store my-store --no-dry-run --incremental
    """
    # Show help if missing required arguments
    if not glob_pattern or not store_name:
        click.echo("vector-rag-tool index - Index files into a vector store")
        click.echo("")
        click.echo("Use cases:")
        click.echo('  vector-rag-tool index "**/*.py" --store my-store')
        click.echo('  vector-rag-tool index "**/*.py" "**/*.md" --store my-store --no-dry-run')
        click.echo('  vector-rag-tool index "docs/**/*.pdf" --store my-docs --no-dry-run')
        click.echo('  vector-rag-tool index "**/*.py" --store my-store --force --no-dry-run')
        click.echo("")
        click.echo("Required:")
        click.echo('  GLOB_PATTERN  One or more glob patterns (e.g., "**/*.py")')
        click.echo("  --store/-s    Name of the vector store")
        click.echo("")
        click.echo("Use 'vector-rag-tool index --help' for all options")
        return

    # Setup logging based on verbosity
    setup_logging(verbose)

    # Resolve dry-run flag
    if no_dry_run:
        dry_run = False

    # Resolve incremental flag
    if force:
        incremental = False

    # Log backend choice
    if bucket:
        logger.info(
            "Using S3 Vectors backend: bucket=%s, region=%s, profile=%s",
            bucket,
            region,
            profile,
        )
    else:
        logger.info("Using local FAISS backend")

    logger.info(
        "Indexing files for store: %s (dry-run: %s, incremental: %s)",
        store_name,
        dry_run,
        incremental,
    )

    # Validate glob patterns
    patterns = list(glob_pattern)
    if not patterns:
        raise click.ClickException("At least one glob pattern is required")

    # Convert glob patterns to absolute paths
    for i, pattern in enumerate(patterns):
        path = Path(pattern)
        if not path.is_absolute() and not any(c in pattern for c in "*?[]"):
            # Treat relative paths without wildcards as relative to current directory
            patterns[i] = str(Path.cwd() / path)

    logger.debug("Using glob patterns: %s", patterns)

    # Initialize backend and indexer
    from vector_rag_tool.core.embeddings import OllamaEmbeddings
    from vector_rag_tool.services.indexer import Indexer

    backend = get_backend(bucket=bucket, region=region, profile=profile)
    embeddings = OllamaEmbeddings()
    indexer = Indexer(
        backend=backend,
        embeddings=embeddings,
        chunking_kwargs={"chunk_size": chunk_size, "chunk_overlap": chunk_overlap},
        enable_openai=enable_openai,
        openai_model=openai_model,
    )

    # Check if store exists
    if not backend.store_exists(store_name):
        if dry_run:
            click.echo(f"[DRY RUN] Would create new store: {store_name}")
        else:
            logger.info("Creating new store: %s", store_name)
            backend.create_store(store_name, dimension=embeddings.dimension)
            click.echo(f"Created new store: {store_name}")

    # Perform indexing
    try:
        if dry_run:
            # Preview what would be indexed
            from vector_rag_tool.core.converter import (
                is_markitdown_available,
            )
            from vector_rag_tool.core.converter import (
                requires_openai as file_requires_openai,
            )
            from vector_rag_tool.core.file_detector import (
                detect_files_from_patterns,
                is_native_text_file,
                requires_markitdown,
            )

            click.echo(f"\n[DRY RUN] Preview for store: {store_name}")
            click.echo(f"Glob patterns: {', '.join(patterns)}")
            click.echo(f"Incremental mode: {'enabled' if incremental else 'disabled'}")
            click.echo(f"OpenAI enabled: {enable_openai}")
            click.echo("")

            # Detect files
            file_matches = detect_files_from_patterns(patterns)

            if not file_matches:
                click.echo("No files found matching the patterns")
                return

            # Categorize files
            native_files = []
            document_files = []
            openai_required_files = []

            for file_path, file_type in file_matches:
                if is_native_text_file(file_path):
                    native_files.append((file_path, file_type))
                elif requires_markitdown(file_path):
                    if file_requires_openai(file_path):
                        openai_required_files.append((file_path, file_type))
                    else:
                        document_files.append((file_path, file_type))

            click.echo(f"Found {len(file_matches)} files:")

            if native_files:
                click.echo(f"\n  Text files ({len(native_files)}):")
                for file_path, file_type in native_files[:10]:
                    rel_path = Path(file_path)
                    try:
                        rel_path = rel_path.relative_to(Path.cwd())
                    except ValueError:
                        pass
                    click.echo(f"    • {rel_path} ({file_type})")
                if len(native_files) > 10:
                    click.echo(f"    ... and {len(native_files) - 10} more")

            if document_files:
                click.echo(f"\n  Documents ({len(document_files)}) [markitdown]:")
                if not is_markitdown_available():
                    click.echo("    ⚠️  markitdown not installed.")
                    click.echo("    Install: uv add 'vector-rag-tool[documents]'")
                for file_path, file_type in document_files[:10]:
                    rel_path = Path(file_path)
                    try:
                        rel_path = rel_path.relative_to(Path.cwd())
                    except ValueError:
                        pass
                    click.echo(f"    • {rel_path} ({file_type})")
                if len(document_files) > 10:
                    click.echo(f"    ... and {len(document_files) - 10} more")

            if openai_required_files:
                click.echo(f"\n  Images/Media ({len(openai_required_files)}) [--enable-openai]:")
                if not enable_openai:
                    click.echo("    ⚠️  These files will be SKIPPED without --enable-openai flag")
                for file_path, file_type in openai_required_files[:10]:
                    rel_path = Path(file_path)
                    try:
                        rel_path = rel_path.relative_to(Path.cwd())
                    except ValueError:
                        pass
                    click.echo(f"    • {rel_path} ({file_type})")
                if len(openai_required_files) > 10:
                    click.echo(f"    ... and {len(openai_required_files) - 10} more")

            if incremental:
                click.echo("\n[DRY RUN] With incremental mode, unchanged files would be skipped")

        else:
            # Actual indexing
            results = indexer.index_files(
                store_name=store_name,
                patterns=patterns,
                incremental=incremental,
                show_progress=True,
            )

            # Display results
            click.echo(f"\nIndexing complete for store: {store_name}")
            click.echo(f"Files scanned: {results['files_scanned']}")
            click.echo(f"Files updated: {results['files_updated']}")
            click.echo(f"Files skipped: {results['files_skipped']}")
            click.echo(f"Chunks created: {results['chunks_created']}")
            click.echo(f"Embeddings generated: {results['embeddings_generated']}")

            if results["errors_count"] > 0:
                click.echo(f"\nErrors encountered: {results['errors_count']}")
                for error in results["errors"][:5]:  # Show first 5 errors
                    click.echo(f"  • {error['file']}: {error['error']}")
                if results["errors_count"] > 5:
                    click.echo(f"  ... and {results['errors_count'] - 5} more errors")

            # Store statistics
            stats = indexer.get_indexing_stats(store_name)
            click.echo("\nStore statistics:")
            click.echo(f"  Total vectors: {stats['vector_count']}")
            click.echo(f"  Dimension: {stats['dimension']}")
            if stats.get("last_indexed"):
                click.echo(f"  Last indexed: {stats['last_indexed']}")

    except Exception as e:
        logger.exception("Indexing failed")
        raise click.ClickException(f"Indexing failed: {e}")
