# Contributing to ytdl

Thank you for your interest in contributing to ytdl! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Development Setup](#development-setup)
- [Workflow](#workflow)
- [Version Management](#version-management)
- [Release Process](#release-process)
- [GitHub Secrets Setup](#github-secrets-setup)
- [Code Style](#code-style)

## Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/abd3lraouf/ytdl.git
   cd ytdl
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install in development mode**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Install pre-commit hooks (optional)**
   ```bash
   pip install pre-commit
   pre-commit install
   ```

## Workflow

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, well-documented code
   - Follow the existing code style
   - Add comments for complex logic

3. **Test your changes**
   ```bash
   # Test installation
   pip install -e .
   ytdl --version

   # Test import
   python -c "import ytdl"

   # Format code
   black ytdl.py

   # Type check (optional)
   mypy ytdl.py --ignore-missing-imports
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   ```

   Use conventional commit messages:
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `chore:` - Maintenance tasks
   - `refactor:` - Code refactoring
   - `test:` - Adding tests

5. **Push and create a pull request**
   ```bash
   git push origin feature/your-feature-name
   ```

## Version Management

This project uses **automated versioning** with `setuptools_scm`:

- Versions are automatically derived from Git tags
- Format: `MAJOR.MINOR.PATCH` (Semantic Versioning)
- Development versions include commit information

### How It Works

1. **Tagged commits** become releases (e.g., `v1.2.3`)
2. **Commits after a tag** get dev versions (e.g., `1.2.4.dev1+g1234567`)
3. **No manual version editing** in files

## Release Process

### Automated Release (Recommended)

Use the GitHub Actions workflow to bump version and create a release:

1. Go to **Actions** → **Bump Version**
2. Click **Run workflow**
3. Select version bump type:
   - `patch` - Bug fixes (1.0.0 → 1.0.1)
   - `minor` - New features (1.0.0 → 1.1.0)
   - `major` - Breaking changes (1.0.0 → 2.0.0)
4. Check **Create as pre-release** if needed
5. Click **Run workflow**

The workflow will:
- Calculate the next version
- Create and push a git tag
- Generate changelog from commits
- Create a GitHub release
- Trigger PyPI publishing automatically

### Manual Release

If you prefer manual releases:

1. **Create a tag**
   ```bash
   git tag -a v1.2.3 -m "Release version 1.2.3"
   git push origin v1.2.3
   ```

2. **Create GitHub release**
   - Go to **Releases** → **Draft a new release**
   - Select the tag you created
   - Write release notes
   - Publish release

3. **PyPI publishing happens automatically** via GitHub Actions

## GitHub Secrets Setup

To enable automated PyPI publishing, add your PyPI API token to GitHub Secrets:

### Step 1: Get PyPI API Token

1. Go to https://pypi.org/manage/account/token/
2. Click **Add API token**
3. Token name: `ytdl-github-actions`
4. Scope: Select **Entire account** or **Project: ytdl-interactive**
5. Click **Add token**
6. **Copy the token** (starts with `pypi-...`)

### Step 2: Add to GitHub Secrets

1. Go to your repository on GitHub
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI token
6. Click **Add secret**

### Step 3: Verify Setup

The secret is now available to GitHub Actions workflows as:
```yaml
${{ secrets.PYPI_API_TOKEN }}
```

## Code Style

- Follow **PEP 8** style guidelines
- Use **black** for code formatting:
  ```bash
  black ytdl.py
  ```
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to functions and classes
- Comment complex logic

## Testing

While we don't have automated tests yet, please manually test:

1. **Basic download**
   ```bash
   ytdl https://www.youtube.com/watch?v=dQw4w9WgXcQ
   ```

2. **Playlist download**
   ```bash
   ytdl "https://www.youtube.com/playlist?list=PLxxxxxx"
   ```

3. **Advanced options** - Test each menu option

4. **Edge cases**
   - Invalid URLs
   - Network errors
   - Non-existent videos

## CI/CD Workflows

The project includes several automated workflows:

### 1. CI Workflow
- **Triggers**: Push to main/develop, Pull requests
- **Actions**: Linting, type checking, build verification
- **Runs on**: Ubuntu, macOS, Windows
- **Python versions**: 3.9, 3.10, 3.11, 3.12

### 2. Publish Workflow
- **Triggers**: New releases
- **Actions**: Build package, verify, publish to PyPI
- **Requirements**: `PYPI_API_TOKEN` secret

### 3. Bump Version Workflow
- **Triggers**: Manual (workflow_dispatch)
- **Actions**: Calculate version, tag, create release
- **Options**: patch/minor/major, pre-release

### 4. Release Drafter
- **Triggers**: Push to main
- **Actions**: Auto-generate release notes
- **Uses**: PR labels for categorization

## Questions?

- Open an issue: https://github.com/abd3lraouf/ytdl/issues
- Discussions: https://github.com/abd3lraouf/ytdl/discussions

Thank you for contributing! 🎉
