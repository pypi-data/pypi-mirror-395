"""Utility functions for DocuSync."""

from functools import wraps
from pathlib import Path
from typing import Callable, ParamSpec, TypeVar

import click

from docusync.exceptions import ConfigurationError, DocuSyncError
from docusync.logger import USER_LOG


P = ParamSpec("P")
T = TypeVar("T")


def handle_errors(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator to handle common errors in CLI commands.

    :param func: Function to wrap
    :returns: Wrapped function
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            USER_LOG.error(f"Configuration file not found: {e}")
            raise click.Abort()
        except ConfigurationError as e:
            USER_LOG.error(f"Configuration error: {e}")
            raise click.Abort()
        except DocuSyncError as e:
            USER_LOG.error(f"Sync failed: {e}")
            raise click.Abort()
        except Exception as e:
            USER_LOG.error(f"Unexpected error: {e}")
            # Show traceback in verbose mode
            ctx = click.get_current_context()
            if ctx.params.get("verbose", False):
                raise
            raise click.Abort()

    return wrapper


def load_config(func: Callable[P, T]) -> Callable[P, T]:
    """Decorator to automatically load configuration from file.

    Replaces 'config_path' parameter with loaded 'config' object.

    :param func: Function to wrap
    :returns: Wrapped function
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        from docusync.config import Config

        config_path = kwargs.pop("config_path")

        if not isinstance(config_path, Path):
            if isinstance(config_path, str):
                config_path = Path(config_path)
            else:
                raise ValueError(
                    "config_path must be a Path, or string. "
                    f"Got type: {type(config_path)}"
                )

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}"
            )

        config = Config.model_validate_json(
            config_path.read_text(encoding="utf-8")
        )
        kwargs["config"] = config

        return func(*args, **kwargs)

    return wrapper
