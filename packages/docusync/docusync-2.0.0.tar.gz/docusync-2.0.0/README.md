<div align="center">

# 📚 DocuSync

**Effortlessly sync documentation from multiple repositories into your Docusaurus site**

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Configuration](#-configuration)

</div>

---

## 🎯 Overview

**DocuSync** is a powerful CLI tool designed specifically for **Docusaurus** projects that need to aggregate documentation from multiple GitHub repositories. It automatically clones, organizes, and generates the proper category structure for your multi-repository documentation setup.

Perfect for:
- 🏢 **Microservices architectures** - Centralize docs from multiple services
- 📦 **Monorepo projects** - Sync docs from different packages
- 🔧 **SDK ecosystems** - Aggregate documentation from multiple SDKs
- 🌐 **Multi-team projects** - Combine docs from different teams

## ✨ Features

- 🚀 **Fast & Efficient** - Shallow cloning with configurable depth
- 🎨 **Docusaurus Integration** - Auto-generates `_category_.json` files
- 📋 **Multi-Repository Support** - Sync from unlimited GitHub repositories
- 🔧 **Flexible Configuration** - JSON-based configuration with validation
- 📊 **Beautiful Output** - Rich console interface with progress indicators
- 🧹 **Clean & Safe** - Automatic cleanup of temporary files
- ✅ **Type-Safe** - Built with Pydantic for robust configuration
- 🎯 **Selective Sync** - Sync all repos or just one
- 🔨 **MD/MDX Fixer** - Automatically fix common Markdown/MDX issues that cause Docusaurus build failures

## 📦 Installation

### Using uv (Recommended)

```bash
uv add docusync
```

### Using pip

```bash
pip install docusync
```

### For Development

```bash
git clone https://github.com/Roman505050/docusync.git
cd docusync
uv sync --all-groups
```

## 🚀 Quick Start

1. **Initialize configuration**
```bash
docusync init
```

2. **Edit `docusync.json`** with your repositories

3. **Sync your documentation**
```bash
docusync sync
```

4. **Run Docusaurus**
```bash
npm run start
```

That's it! Your documentation is now synced and ready to go! 🎉

## 📖 Usage

### Sync All Repositories

```bash
docusync sync
```

**With verbose output:**
```bash
docusync sync -v
```

**Keep temporary files for debugging:**
```bash
docusync sync --no-cleanup
```

**Automatically fix MD/MDX issues after sync:**
```bash
docusync sync --fix-md
```

### Sync Single Repository

```bash
docusync sync-one <repository-name>
```

**Example:**
```bash
docusync sync-one api-gateway
```

**With automatic MD/MDX fixing:**
```bash
docusync sync-one api-gateway --fix-md
```

### Fix Markdown/MDX Files

Fix common MDX/Markdown issues that cause Docusaurus build failures:

```bash
# Fix all .md files in a directory
docusync fix docs/

# Fix a single file
docusync fix docs/my-file.md

# Preview changes without applying them
docusync fix docs/ --dry-run

# Fix only files in the target directory (non-recursive)
docusync fix docs/ --no-recursive
```

**What the fixer fixes:**
- ❌ Invalid JSX tag names (e.g., `<1something>` → `&lt;1something&gt;`)
- ❌ HTML comments in MDX context (e.g., `<!-- comment -->` → `{/* comment */}`)
- ❌ Unclosed void elements (e.g., `<br>` → `<br />`)
- ❌ Invalid HTML attributes (e.g., `class=` → `className=`, `for=` → `htmlFor=`)
- ❌ Self-closing tag spacing (e.g., `<tag/>` → `<tag />`)
- ❌ Malformed numeric entities (e.g., `&#123` → `&#123;`)

### List Configured Repositories

```bash
docusync list
```

### Initialize Configuration

```bash
docusync init
```

**With custom config path:**
```bash
docusync init -c custom-config.json
```

## ⚙️ Configuration

### Basic Configuration

Create a `docusync.json` file in your Docusaurus project root:

```json
{
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
```

### Configuration Options

#### `repositories` (required)

Array of repositories to sync:

| Field | Type | Description |
|-------|------|-------------|
| `github_path` | `string` | GitHub repository path (`owner/repo`) |
| `docs_path` | `string` | Path to documentation within the repository |
| `display_name` | `string` | Display name for the category |
| `position` | `integer` | Sidebar position (must be unique) |
| `description` | `string` | Category description for Docusaurus |

#### `paths` (required)

| Field | Type | Description |
|-------|------|-------------|
| `temp_dir` | `string` | Directory for temporary clones (auto-deleted) |
| `docs_dir` | `string` | Target directory for documentation |

#### `git` (required)

| Field | Type | Description |
|-------|------|-------------|
| `clone_depth` | `integer` | Git clone depth (1 for shallow clone) |
| `default_branches` | `array` | Default branches to try cloning |

## 🎨 Docusaurus Integration

### Automatic `_category_.json` Generation

DocuSync automatically creates `_category_.json` files in each synced documentation directory, following the Docusaurus category format:

```json
{
  "label": "API Gateway",
  "position": 1,
  "link": {
    "type": "generated-index",
    "description": "Central API gateway documentation"
  }
}
```

This enables Docusaurus to:
- ✅ Automatically generate index pages for each category
- ✅ Properly order documentation in the sidebar
- ✅ Display category descriptions on index pages
- ✅ Create a beautiful, organized documentation structure

### Project Structure After Sync

```
your-docusaurus-project/
├── docusaurus.config.js
├── docusync.json
├── docs/
│   ├── api-gateway/
│   │   ├── _category_.json      # Auto-generated ✨
│   │   ├── intro.md
│   │   ├── getting-started.md
│   │   └── api-reference.md
│   ├── user-service/
│   │   ├── _category_.json      # Auto-generated ✨
│   │   ├── overview.md
│   │   └── configuration.md
│   └── payment-processor/
│       ├── _category_.json      # Auto-generated ✨
│       ├── setup.md
│       └── webhooks.md
└── .temp-repos/                 # Cleaned up after sync
```

## 🔍 Real-World Example

Here's a complete workflow for a microservices documentation setup:

```bash
# 1. Initialize your Docusaurus project
npx create-docusaurus@latest my-docs classic

# 2. Navigate to your project
cd my-docs

# 3. Initialize DocuSync
docusync init

# 4. Configure your repositories in docusync.json
cat > docusync.json << 'EOF'
{
  "repositories": [
    {
      "github_path": "your-org/auth-service",
      "docs_path": "docs",
      "display_name": "Authentication Service",
      "position": 1,
      "description": "User authentication and authorization"
    },
    {
      "github_path": "your-org/billing-service",
      "docs_path": "docs",
      "display_name": "Billing Service",
      "position": 2,
      "description": "Payment processing and billing management"
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
EOF

# 5. Sync documentation
docusync sync -v

# 6. Start Docusaurus
npm run start
```

## 🛠️ Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/Roman505050/docusync.git
cd docusync

# Install dependencies
uv sync --all-groups
```

### Code Quality

```bash
# Format code
uv run black src/
uv run isort src/

# Lint
uv run flake8 src/

# Type check
uv run mypy src/
```

### Running Tests

```bash
# Run all tests
uv run pytest

# With coverage
uv run pytest --cov=docusync --cov-report=html
```

## 📋 Requirements

- **Python** 3.12 or higher
- **Git** with SSH access to GitHub repositories
- **Docusaurus** 2.x or higher (for the target project)

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🔧 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. ✅ Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎉 Open a Pull Request

Please make sure to:
- Add tests for new features
- Update documentation as needed
- Follow the existing code style
- Run linters before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Click](https://click.palletsprojects.com/) - Beautiful CLI framework
- [Rich](https://github.com/Textualize/rich) - Rich text and formatting in the terminal
- [Pydantic](https://docs.pydantic.dev/) - Data validation using Python type hints
- [Docusaurus](https://docusaurus.io/) - The documentation framework this tool was built for

## 📧 Support

- 🐛 **Bug Reports**: [Open an issue](https://github.com/Roman505050/docusync/issues)
- 💡 **Feature Requests**: [Open an issue](https://github.com/Roman505050/docusync/issues)
- 📖 **Documentation**: [Read the docs](https://github.com/Roman505050/docusync#readme)

## 🌟 Show Your Support

If you find DocuSync helpful, please consider giving it a ⭐️ on GitHub!

---

<div align="center">

Made with ❤️ for the Docusaurus community

[Report Bug](https://github.com/Roman505050/docusync/issues) • [Request Feature](https://github.com/Roman505050/docusync/issues)

</div>
