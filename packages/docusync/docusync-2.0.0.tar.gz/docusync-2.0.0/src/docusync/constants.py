"""Constants for DocuSync."""

# Default configuration file name
DEFAULT_CONFIG_FILE = "docusync.json"

# Default paths
DEFAULT_TEMP_DIR = ".temp-repos"
DEFAULT_DOCS_DIR = "docs"

# Git defaults
DEFAULT_CLONE_DEPTH = 1
DEFAULT_BRANCHES = ["main", "master"]

# Git command timeout in seconds
GIT_COMMAND_TIMEOUT = 300

EXAMPLE_CONFIG = """{
  "repositories": [
    {
      "github_path": "acme-corp/api-gateway",
      "docs_path": "docs",
      "display_name": "API Gateway",
      "position": 1,
      "description": "Central API gateway documentation"
    },
    {
      "github_path": "acme-corp/user-service",
      "docs_path": "documentation",
      "display_name": "User Service",
      "position": 2,
      "description": "User management and authentication service"
    },
    {
      "github_path": "acme-corp/payment-processor",
      "docs_path": "docs",
      "display_name": "Payment Processor",
      "position": 3,
      "description": "Payment processing and billing documentation"
    }
  ],
  "paths": {
    "temp_dir": ".temp-repos",
    "docs_dir": "docs"
  },
  "git": {
    "clone_depth": 1,
    "default_branches": ["main", "master"]
  }
}
"""

LOG_COLORS = {
    "DEBUG": "dim",
    "INFO": "cyan",
    "SUCCESS": "green",
    "WARNING": "yellow",
    "ERROR": "red",
}
