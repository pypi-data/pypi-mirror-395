# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-12-07

### Added

- Initial release of DocuSync
- Click-based CLI with multiple commands:
  - `docusync sync` - Sync all repositories
  - `docusync sync-one` - Sync a single repository
  - `docusync list` - List configured repositories
  - `docusync init` - Initialize configuration file
  - `docusync fix` - Fix common Markdown/MDX issues
- **MD/MDX Fixer** - Automatically fix common Markdown/MDX issues
  - Fixes invalid JSX tag names (tags starting with numbers)
  - Converts HTML comments to JSX comments in MDX context
  - Fixes unclosed void elements (br, hr, img, etc.)
  - Converts HTML attributes to JSX (class → className, for → htmlFor)
  - Fixes self-closing tag spacing
  - Fixes malformed numeric HTML entities
  - Supports both single files and directories (recursive and non-recursive)
  - `--dry-run` flag to preview changes without applying them
- `--fix-md` flag for `docusync sync` and `docusync sync-one` commands
  - Automatically runs the MD fixer after syncing documentation
  - Helps prevent Docusaurus build failures due to MDX syntax errors
- JSON-based configuration system
- Support for syncing documentation from multiple GitHub repositories
- Configurable repository ordering with position field
- Rich console output with progress indicators
- Verbose mode for debugging
- Shallow git cloning with configurable depth
- Automatic cleanup of temporary directories
- Type hints throughout the codebase
- Automatic creation of `_category_.json` files for Docusaurus
  - Files are generated in each synced documentation directory
  - Uses `display_name`, `position`, and `description` from configuration
  - Follows Docusaurus category format with `generated-index` link type
  - Enables automatic index page generation in Docusaurus
