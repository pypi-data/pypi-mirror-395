"""Documentation synchronization logic."""

from pathlib import Path

from docusync.config import Config, Repository
from docusync.exceptions import DocuSyncError, FileOperationError
from docusync.file_operations import FileManager
from docusync.git_operations import GitManager
from docusync.logger import USER_LOG
from docusync.md_fixer import MarkdownFixer


class RepositorySyncer:
    """Handles syncing a single repository (Single Responsibility)."""

    def __init__(
        self,
        config: Config,
        git_manager: GitManager,
        file_manager: FileManager,
    ) -> None:
        self.config = config
        self.git_manager = git_manager
        self.file_manager = file_manager
        self.temp_dir = Path(config.paths.temp_dir)
        self.docs_dir = Path(config.paths.docs_dir)

    def sync(self, repo: Repository) -> None:
        """Sync a single repository.

        :param repo: Repository configuration
        :raises DocuSyncError: If sync fails
        """
        USER_LOG.section(f"{repo.display_name} (position: {repo.position})")
        USER_LOG.info(repo.description)

        try:
            repo_path = self._clone_repository(repo)
            self._copy_documentation(repo, repo_path)
            self._create_category_file(repo)
            USER_LOG.success(f"Successfully synced {repo.display_name}")
        except DocuSyncError:
            raise
        except Exception as e:
            raise DocuSyncError(
                f"Unexpected error syncing {repo.display_name}: {e}"
            ) from e

    def _clone_repository(self, repo: Repository) -> Path:
        """Clone repository to temp directory.

        :param repo: Repository configuration
        :returns: Path to cloned repository
        """
        repo_path = self.temp_dir / repo.repo_name

        # Remove existing directory if present
        if repo_path.exists():
            self.file_manager.remove_directory(repo_path)

        # Clone repository
        self.git_manager.clone_repository(
            clone_url=repo.clone_url,
            destination=repo_path,
            depth=self.config.git.clone_depth,
        )

        return repo_path

    def _copy_documentation(self, repo: Repository, repo_path: Path) -> None:
        """Copy documentation from repository to docs directory.

        :param repo: Repository configuration
        :param repo_path: Path to cloned repository
        :raises FileOperationError: If source docs don't exist or copy fails
        """
        source_docs = repo_path / repo.docs_path
        target_docs = self.docs_dir / repo.repo_name

        if not source_docs.exists():
            raise FileOperationError(
                f"Documentation path not found in {repo.display_name}: "
                f"{source_docs}"
            )

        self.file_manager.copy_directory(source_docs, target_docs)

    def _create_category_file(self, repo: Repository) -> None:
        """Create _category_.json file for Docusaurus.

        :param repo: Repository configuration
        """
        target_docs = self.docs_dir / repo.repo_name
        self.file_manager.create_category_file(
            directory=target_docs,
            label=repo.display_name,
            position=repo.position,
            description=repo.description,
        )


class DocuSync:
    """Main orchestrator for documentation synchronization (Facade pattern)."""

    def __init__(self, config: Config, verbose: bool = False) -> None:
        self.config = config
        USER_LOG.verbose = verbose
        self.git_manager = GitManager()
        self.file_manager = FileManager()
        self.md_fixer = MarkdownFixer()
        self.syncer = RepositorySyncer(
            config=config,
            git_manager=self.git_manager,
            file_manager=self.file_manager,
        )
        self.temp_dir = Path(config.paths.temp_dir)
        self.docs_dir = Path(config.paths.docs_dir)

    def sync_all(self, cleanup: bool = True, fix_md: bool = False) -> None:
        """Sync all repositories.

        :param cleanup: Whether to cleanup temp directory after sync
        :param fix_md: Whether to fix common MDX/Markdown issues after sync
        """
        total_repos = len(self.config.repositories)

        USER_LOG.header(
            "DocuSync - Documentation Synchronization",
            f"Syncing {total_repos} repositories",
        )

        # Setup directories
        self._setup_directories()

        # Sync each repository
        for idx, repo in enumerate(self.config.sorted_repositories, 1):
            USER_LOG.step(idx, total_repos, repo.display_name)
            self.syncer.sync(repo)

        # Fix markdown files if requested
        if fix_md:
            self._fix_markdown_files()

        # Cleanup
        if cleanup:
            self._cleanup()

        USER_LOG.newline()
        USER_LOG.success("Documentation sync completed successfully!")

    def sync_one(self, repository_name: str, fix_md: bool = False) -> None:
        """Sync a single repository by name.

        :param repository_name: Name of the repository to sync
        :param fix_md: Whether to fix common MDX/Markdown issues after sync
        :raises DocuSyncError: If repository not found
        """
        repo = self._find_repository(repository_name)

        USER_LOG.header(
            "DocuSync - Single Repository Sync",
            f"Syncing {repo.display_name}",
        )

        self._setup_directories()
        self.syncer.sync(repo)

        # Fix markdown files if requested
        if fix_md:
            target_dir = self.docs_dir / repo.repo_name
            if target_dir.exists():
                USER_LOG.newline()
                USER_LOG.section("Fixing Markdown Files")
                self.md_fixer.fix_directory(target_dir, dry_run=False)

        self._cleanup()

        USER_LOG.newline()
        USER_LOG.success(f"Successfully synced {repo.display_name}!")

    def list_repositories(self) -> None:
        """Display all configured repositories."""
        USER_LOG.table_repositories(self.config.sorted_repositories)

    def _setup_directories(self) -> None:
        """Ensure required directories exist."""
        self.file_manager.ensure_directory(self.temp_dir)
        self.file_manager.ensure_directory(self.docs_dir)

    def _cleanup(self) -> None:
        """Remove temporary directory."""
        if self.temp_dir.exists():
            USER_LOG.info(f"Cleaning up temporary directory: {self.temp_dir}")
            self.file_manager.remove_directory(self.temp_dir)

    def _fix_markdown_files(self) -> None:
        """Fix common MDX/Markdown issues in all synced documentation."""
        if not self.docs_dir.exists():
            return

        USER_LOG.newline()
        USER_LOG.section("Fixing Markdown Files")
        fixed_count = self.md_fixer.fix_directory(
            self.docs_dir, dry_run=False, recursive=True
        )

        if fixed_count > 0:
            USER_LOG.success(f"Fixed {fixed_count} markdown file(s)")
        else:
            USER_LOG.info("No issues found in markdown files")

    def _find_repository(self, repository_name: str) -> Repository:
        """Find repository by name.

        :param repository_name: Repository name to find
        :returns: Repository object
        :raises DocuSyncError: If repository not found
        """
        repo = next(
            (
                r
                for r in self.config.repositories
                if r.repo_name == repository_name
            ),
            None,
        )

        if not repo:
            raise DocuSyncError(
                f"Repository '{repository_name}' not found in configuration"
            )

        return repo
