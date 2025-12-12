"""Store management commands for vector-rag-tool.

This module provides CLI commands for managing vector stores using either
local FAISS or remote S3 Vectors backend. Supports creating, deleting,
listing, and getting information about stores.

Note: This code was generated with assistance from AI coding tools
and has been reviewed and tested by a human.
"""

import click

from vector_rag_tool.core.backend_factory import get_backend
from vector_rag_tool.logging_config import get_logger, setup_logging

logger = get_logger(__name__)


@click.group(invoke_without_command=True)
@click.pass_context
def store(ctx: click.Context) -> None:
    """Manage vector stores for RAG operations."""
    if ctx.invoked_subcommand is None:
        click.echo("vector-rag-tool store - Manage vector stores")
        click.echo("")
        click.echo("Commands:")
        click.echo("  list     List all stores")
        click.echo("  create   Create a new store")
        click.echo("  delete   Delete a store")
        click.echo("  info     Get store details")
        click.echo("")
        click.echo("Use cases:")
        click.echo("  vector-rag-tool store list")
        click.echo("  vector-rag-tool store list --format json")
        click.echo("  vector-rag-tool store create my-store")
        click.echo("  vector-rag-tool store info my-store")
        click.echo("  vector-rag-tool store delete my-store --force")
        click.echo("")
        click.echo("Use 'vector-rag-tool store <command> --help' for command details")


@store.command("create")
@click.argument("name")
@click.option(
    "--dimension",
    "-d",
    default=768,
    type=int,
    help="Vector dimension (default: 768 for sentence-transformers)",
)
@click.option(
    "--bucket",
    "-b",
    help="S3 bucket name for remote storage. If not provided, uses local FAISS storage",
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
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
def create_store(
    name: str, dimension: int, bucket: str | None, region: str, profile: str | None, verbose: int
) -> None:
    """Create a new vector store.

    Examples:

    \b
        # Create a local store with default 768 dimensions
        vector-rag-tool store create my-store

    \b
        # Create a local store with custom dimensions
        vector-rag-tool store create my-store --dimension 1536

    \b
        # Create a remote store in S3 Vectors
        vector-rag-tool store create my-store --bucket my-vector-bucket

    \b
        # Create a remote store with custom region and profile
        vector-rag-tool store create my-store --bucket my-vector-bucket \\
            --region us-west-2 --profile my-aws-profile
    """
    setup_logging(verbose)

    # Get the appropriate backend based on options
    backend = get_backend(bucket=bucket, region=region, profile=profile)

    try:
        backend_type = "S3 Vectors" if bucket else "local FAISS"
        logger.info("Creating %s store '%s' with dimension %d", backend_type, name, dimension)
        backend.create_store(name, dimension)

        location_info = f" in bucket '{bucket}'" if bucket else ""
        click.echo(
            f"✓ Created {backend_type} store '{name}'{location_info} with dimension {dimension}"
        )
        logger.info("Store '%s' created successfully", name)
    except ValueError as e:
        logger.error("Failed to create store: %s", e)
        click.echo(f"✗ Failed to create store: {e}", err=True)
        raise click.ClickException(str(e))
    except Exception as e:
        logger.error("Unexpected error creating store: %s", e)
        click.echo(f"✗ Unexpected error: {e}", err=True)
        raise click.ClickException(str(e))


@store.command("delete")
@click.argument("name")
@click.option(
    "--bucket",
    "-b",
    help="S3 bucket name for remote storage. If not provided, uses local FAISS storage",
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
    "--force",
    "-f",
    is_flag=True,
    help="Force deletion without confirmation",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
def delete_store(
    name: str, bucket: str | None, region: str, profile: str | None, force: bool, verbose: int
) -> None:
    """Delete a vector store.

    This will permanently remove the store and all its vectors.

    Examples:

    \b
        # Delete local store with confirmation prompt
        vector-rag-tool store delete my-store

    \b
        # Force delete local store without confirmation
        vector-rag-tool store delete my-store --force

    \b
        # Delete remote store in S3 Vectors
        vector-rag-tool store delete my-store --bucket my-vector-bucket

    \b
        # Force delete remote store without confirmation
        vector-rag-tool store delete my-store --bucket my-vector-bucket --force
    """
    setup_logging(verbose)

    # Get the appropriate backend based on options
    backend = get_backend(bucket=bucket, region=region, profile=profile)

    try:
        if not backend.store_exists(name):
            logger.error("Store '%s' does not exist", name)
            click.echo(f"✗ Store '{name}' does not exist", err=True)
            raise click.ClickException(f"Store '{name}' does not exist")

        if not force:
            backend_type = "S3 Vectors" if bucket else "local FAISS"
            if not click.confirm(f"Are you sure you want to delete {backend_type} store '{name}'?"):
                click.echo("Delete operation cancelled")
                return

        backend_type = "S3 Vectors" if bucket else "local FAISS"
        logger.info("Deleting %s store '%s'", backend_type, name)
        backend.delete_store(name)
        click.echo(f"✓ Deleted {backend_type} store '{name}'")
        logger.info("Store '%s' deleted successfully", name)
    except Exception as e:
        logger.error("Error deleting store '%s': %s", name, e)
        click.echo(f"✗ Error deleting store: {e}", err=True)
        raise click.ClickException(str(e))


@store.command("list")
@click.option(
    "--bucket",
    "-b",
    help="S3 bucket name for remote storage. If not provided, uses local FAISS storage",
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
    "--format",
    "output_format",
    type=click.Choice(["table", "json"], case_sensitive=False),
    default="table",
    help="Output format (default: table)",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
def list_stores(
    bucket: str | None, region: str, profile: str | None, output_format: str, verbose: int
) -> None:
    """List all vector stores.

    Examples:

    \b
        # List local stores in table format
        vector-rag-tool store list

    \b
        # List local stores in JSON format
        vector-rag-tool store list --format json

    \b
        # List remote stores in S3 Vectors
        vector-rag-tool store list --bucket my-vector-bucket

    \b
        # List remote stores with custom region and profile
        vector-rag-tool store list --bucket my-vector-bucket \\
            --region us-west-2 --profile my-aws-profile
    """
    setup_logging(verbose)

    # Get the appropriate backend based on options
    backend = get_backend(bucket=bucket, region=region, profile=profile)

    try:
        backend_type = "S3 Vectors" if bucket else "local FAISS"
        logger.debug("Retrieving list of %s stores", backend_type)
        stores = backend.list_stores()

        if not stores:
            click.echo("No stores found")
            return

        logger.debug("Found %d stores: %s", len(stores), stores)

        if output_format.lower() == "json":
            import json

            store_info = []
            for store_name in stores:
                try:
                    info = backend.get_store_info(store_name)
                    store_info.append(info)
                except Exception as e:
                    logger.warning("Could not get info for store '%s': %s", store_name, e)
                    store_info.append({"name": store_name, "error": str(e)})
            click.echo(json.dumps(store_info, indent=2))
        else:
            # Table format
            click.echo("Available stores:")
            for store_name in sorted(stores):
                try:
                    info = backend.get_store_info(store_name)
                    vector_count = info.get("vector_count") or 0
                    dimension = info.get("dimension") or 0
                    size_mb = info.get("index_size_mb")
                    size_str = f"{size_mb:>8.2f}MB" if size_mb is not None else "     N/A"
                    click.echo(
                        f"  {store_name:<20} {vector_count:>8} vectors {dimension:>6}D {size_str}"
                    )
                except Exception as e:
                    logger.warning("Could not get info for store '%s': %s", store_name, e)
                    click.echo(f"  {store_name:<20} (info unavailable)")

        logger.info("Listed %d stores", len(stores))
    except Exception as e:
        logger.error("Error listing stores: %s", e)
        click.echo(f"✗ Error listing stores: {e}", err=True)
        raise click.ClickException(str(e))


@store.command("info")
@click.argument("name")
@click.option(
    "--bucket",
    "-b",
    help="S3 bucket name for remote storage. If not provided, uses local FAISS storage",
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
    "--format",
    "output_format",
    type=click.Choice(["table", "json"], case_sensitive=False),
    default="table",
    help="Output format (default: table)",
)
@click.option(
    "-v",
    "--verbose",
    count=True,
    help="Enable verbose output (use -v for INFO, -vv for DEBUG, -vvv for TRACE)",
)
def store_info(
    name: str,
    bucket: str | None,
    region: str,
    profile: str | None,
    output_format: str,
    verbose: int,
) -> None:
    """Get detailed information about a specific store.

    Examples:

    \b
        # Show local store info in table format
        vector-rag-tool store info my-store

    \b
        # Show local store info in JSON format
        vector-rag-tool store info my-store --format json

    \b
        # Show remote store info in S3 Vectors
        vector-rag-tool store info my-store --bucket my-vector-bucket

    \b
        # Show remote store info with custom region and profile
        vector-rag-tool store info my-store --bucket my-vector-bucket \\
            --region us-west-2 --profile my-aws-profile
    """
    setup_logging(verbose)

    # Get the appropriate backend based on options
    backend = get_backend(bucket=bucket, region=region, profile=profile)

    try:
        backend_type = "S3 Vectors" if bucket else "local FAISS"
        logger.debug("Getting info for %s store '%s'", backend_type, name)
        info = backend.get_store_info(name)

        if output_format.lower() == "json":
            import json

            click.echo(json.dumps(info, indent=2))
        else:
            # Table format
            click.echo(f"Store: {info['name']}")
            click.echo(f"Backend: {info['backend']}")
            click.echo(f"Location: {info['location']}")
            click.echo(f"Dimension: {info['dimension']}")
            click.echo(f"Vector Count: {info['vector_count']}")
            click.echo(f"Metadata Keys: {info['metadata_keys']}")
            click.echo(f"Index Size: {info['index_size_mb']:.2f} MB")

        logger.info("Retrieved info for store '%s'", name)
    except ValueError as e:
        logger.error("Store info error: %s", e)
        click.echo(f"✗ {e}", err=True)
        raise click.ClickException(str(e))
    except Exception as e:
        logger.error("Error getting store info: %s", e)
        click.echo(f"✗ Error getting store info: {e}", err=True)
        raise click.ClickException(str(e))
