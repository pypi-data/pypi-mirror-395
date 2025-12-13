"""Configuration handling for DocuSync."""

from pydantic import BaseModel, Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Repository(BaseModel):
    """Repository configuration."""

    github_path: str = Field(..., min_length=1, pattern=r"^[\w.-]+/[\w.-]+$")
    docs_path: str = Field(..., min_length=1)
    display_name: str = Field(..., min_length=1)
    position: int = Field(..., ge=0)
    description: str

    @property
    def clone_url(self) -> str:
        """Get the GitHub SSH clone URL."""
        return f"git@github.com:{self.github_path}.git"

    @property
    def repo_name(self) -> str:
        """Get the repository name from the path."""
        return self.github_path.split("/")[-1]


class PathsConfig(BaseModel):
    """Paths configuration."""

    temp_dir: str = Field(..., min_length=1)
    docs_dir: str = Field(..., min_length=1)


class GitConfig(BaseModel):
    """Git configuration."""

    clone_depth: int = Field(..., ge=1)
    default_branches: list[str] = Field(..., min_length=1)


class Config(BaseSettings):
    """Main configuration for DocuSync.

    Uses Pydantic Settings to automatically load from JSON files.
    """

    model_config = SettingsConfigDict(
        extra="forbid",
    )

    repositories: list[Repository] = Field(..., min_length=1)
    paths: PathsConfig
    git: GitConfig

    @model_validator(mode="after")
    def validate_unique_positions(self) -> "Config":
        """Validate that repository positions are unique.

        :returns: Self after validation
        :raises ValueError: If duplicate positions found
        """
        positions = [repo.position for repo in self.repositories]
        if len(positions) != len(set(positions)):
            raise ValueError("Duplicate position values found in repositories")
        return self

    @property
    def sorted_repositories(self) -> list[Repository]:
        """Get repositories sorted by position."""
        return sorted(self.repositories, key=lambda r: r.position)
