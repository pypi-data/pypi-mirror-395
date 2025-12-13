"""CLI commands for DocuSync."""

from pathlib import Path

import click

from docusync import __version__
from docusync.config import Config
from docusync.constants import DEFAULT_CONFIG_FILE, EXAMPLE_CONFIG
from docusync.logger import USER_LOG
from docusync.md_fixer import MarkdownFixer
from docusync.sync import DocuSync
from docusync.utils import handle_errors, load_config


@click.group()
@click.version_option(version=__version__, prog_name="docusync")
def cli() -> None:
    """DocuSync - Sync documentation from multiple repositories.

    A CLI tool for pulling documentation from different repositories
    for Docusaurus sites based on a configuration file.
    """


@cli.command()
@click.option(
    "-c",
    "--config",
    "config_path",
    type=click.Path(exists=True, path_type=Path),
    default=DEFAULT_CONFIG_FILE,
    help=f"Path to configuration file (default: {DEFAULT_CONFIG_FILE})",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enable verbose output",
)
@click.option(
    "--no-cleanup",
    is_flag=True,
    help="Don't cleanup temporary directory after sync",
)
@click.option(
    "--fix-md",
    is_flag=True,
    help="Automatically fix common MDX/Markdown issues after sync",
)
@load_config
@handle_errors
def sync(
    config: Config, verbose: bool, no_cleanup: bool, fix_md: bool
) -> None:
    """Sync documentation from all configured repositories."""
    syncer = DocuSync(config, verbose=verbose)
    syncer.sync_all(cleanup=not no_cleanup, fix_md=fix_md)


@cli.command()
@click.option(
    "-c",
    "--config",
    "config_path",
    type=click.Path(exists=True, path_type=Path),
    default=DEFAULT_CONFIG_FILE,
    help=f"Path to configuration file (default: {DEFAULT_CONFIG_FILE})",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enable verbose output",
)
@click.option(
    "--fix-md",
    is_flag=True,
    help="Automatically fix common MDX/Markdown issues after sync",
)
@click.argument("repository_name", required=False)
@load_config
@handle_errors
def sync_one(
    config: Config, verbose: bool, fix_md: bool, repository_name: str | None
) -> None:
    """Sync documentation from a single repository.

    If REPOSITORY_NAME is provided, syncs only that repository.
    Otherwise, shows a list of available repositories.
    """
    USER_LOG.verbose = verbose

    if not repository_name:
        USER_LOG.warning("Please specify a repository name:")
        USER_LOG.newline()

        for repo in config.sorted_repositories:
            USER_LOG.info(f"  • {repo.repo_name} - {repo.display_name}")
        return

    syncer = DocuSync(config, verbose=verbose)
    syncer.sync_one(repository_name, fix_md=fix_md)


@cli.command()
@click.option(
    "-c",
    "--config",
    "config_path",
    type=click.Path(exists=True, path_type=Path),
    default=DEFAULT_CONFIG_FILE,
    help=f"Path to configuration file (default: {DEFAULT_CONFIG_FILE})",
)
@load_config
@handle_errors
def list(config: Config) -> None:
    """List all configured repositories."""
    syncer = DocuSync(config)
    syncer.list_repositories()


@cli.command()
@click.option(
    "-c",
    "--config",
    "config_path",
    type=click.Path(path_type=Path),
    default=DEFAULT_CONFIG_FILE,
    help=f"Path to configuration file (default: {DEFAULT_CONFIG_FILE})",
)
def init(config_path: Path) -> None:
    """Initialize a new docusync.json configuration file."""
    if config_path.exists():
        if not click.confirm(
            f"{config_path} already exists. Overwrite?", default=False
        ):
            USER_LOG.warning("Aborted.")
            return

    with open(config_path, "w", encoding="utf-8") as f:
        f.write(EXAMPLE_CONFIG)

    USER_LOG.success(f"Created configuration file: {config_path}")
    USER_LOG.info("Edit this file to configure your repositories.")


@cli.command()
@click.argument(
    "target",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be fixed without making changes",
)
@click.option(
    "--no-recursive",
    is_flag=True,
    help="Don't scan subdirectories (only for directories)",
)
@handle_errors
def fix(target: Path, dry_run: bool, no_recursive: bool) -> None:
    """Fix common MDX/Markdown issues in files or directories.

    TARGET can be a single .md file or a directory containing .md files.

    This command fixes common issues that cause Docusaurus build failures:
    - Invalid JSX tag names (starting with numbers)
    - HTML comments (converts to JSX comments)
    - Unclosed void elements (br, hr, img, etc.)
    - Invalid HTML attributes (class -> className, for -> htmlFor)
    - Self-closing tag spacing
    - Malformed numeric entities

    Use --dry-run to preview changes without applying them.
    """
    fixer = MarkdownFixer()

    if dry_run:
        USER_LOG.header("MD Fixer - Dry Run Mode", "No changes will be made")
    else:
        USER_LOG.header("MD Fixer", "Fixing Markdown/MDX files")

    if target.is_file():
        if not target.suffix == ".md":
            USER_LOG.error(f"Not a markdown file: {target}")
            return

        if fixer.fix_file(target, dry_run=dry_run):
            USER_LOG.newline()
            USER_LOG.success("File processed!")
        else:
            USER_LOG.newline()
            USER_LOG.info("No issues found.")
    else:
        fixed_count = fixer.fix_directory(
            target, dry_run=dry_run, recursive=not no_recursive
        )

        USER_LOG.newline()
        if fixed_count > 0:
            action = "would be fixed" if dry_run else "fixed"
            USER_LOG.success(f"{fixed_count} file(s) {action}!")
        else:
            USER_LOG.info("No issues found.")


if __name__ == "__main__":
    cli()
