# Contributing to DocFind

Thank you for your interest in contributing to DocFind! This document provides guidelines and instructions for contributing.

## Development Setup

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then clone your fork
git clone https://github.com/CihanMertDeniz/docfind.git
cd docfind

# Add upstream remote
git remote add upstream https://github.com/CihanMertDeniz/docfind.git
```

### 2. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix/macOS:
source venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### 3. Create a Branch

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create a feature branch
git checkout -b feature/your-feature-name
```

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=docfind --cov-report=html

# Run specific test file
pytest docfind/tests/test_indexer.py

# Run GUI tests (requires display server)
pytest docfind/tests/test_gui_smoke.py
```

### Code Style

We follow PEP 8 with some modifications:

```bash
# Format code with black
black docfind/

# Sort imports with isort
isort docfind/

# Lint with flake8
flake8 docfind/ --max-line-length=120
```

### Type Checking

```bash
# Run mypy for type checking
mypy docfind/
```

## Contribution Guidelines

### Code Standards

- **Type hints**: All functions should have type annotations
- **Docstrings**: Use Google-style docstrings for all public functions/classes
- **Logging**: Use `logging` module instead of `print()`
- **Error handling**: Catch specific exceptions, provide helpful error messages
- **Tests**: Add tests for new features and bug fixes

### Example Code

```python
def process_document(file_path: Path, max_size: int = 1024) -> tuple[str, bool]:
    """
    Process a document and extract text.

    Args:
        file_path: Path to the document file
        max_size: Maximum file size in bytes

    Returns:
        Tuple of (extracted_text, success)

    Raises:
        ValueError: If file_path doesn't exist
        IOError: If file cannot be read
    """
    if not file_path.exists():
        raise ValueError(f"File not found: {file_path}")

    try:
        # Implementation
        text = extract_text(file_path)
        return text, True
    except Exception as e:
        logger.error(f"Failed to process {file_path}: {e}")
        return "", False
```

### Commit Messages

Use clear, descriptive commit messages:

```
feat: Add support for RTF document extraction
fix: Resolve database locking issue on Windows
docs: Update installation instructions
test: Add tests for hex extractor
refactor: Simplify search query builder
```

Prefixes:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or changes
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `chore`: Maintenance tasks

## Pull Request Process

### 1. Prepare Your Changes

```bash
# Ensure tests pass
pytest

# Format code
black docfind/
isort docfind/

# Commit changes
git add .
git commit -m "feat: Your descriptive message"

# Push to your fork
git push origin feature/your-feature-name
```

### 2. Create Pull Request

1. Go to your fork on GitHub
2. Click "Pull Request"
3. Select your feature branch
4. Fill in the PR template:
   - Clear title
   - Description of changes
   - Related issues (if any)
   - Testing performed

### 3. PR Review

- Address reviewer feedback
- Keep commits clean and organized
- Update documentation if needed
- Ensure CI passes

### 4. Merge

Once approved:
- Squash commits if requested
- PR will be merged by maintainers

## What to Contribute

### Good First Issues

Look for issues labeled `good first issue`:
- Documentation improvements
- Small bug fixes
- Test coverage improvements
- Code comments and docstrings

### Feature Ideas

Before implementing major features:
1. Check existing issues/PRs
2. Open an issue to discuss the feature
3. Wait for maintainer feedback
4. Implement after approval

### Bug Reports

When reporting bugs:
- Use the issue template
- Provide minimal reproduction steps
- Include error messages and logs
- Specify OS, Python version, DocFind version

### Documentation

- Fix typos and clarify instructions
- Add examples and use cases
- Improve API documentation
- Write tutorials

## Project Structure

```
docfind/
├── docfind/
│   ├── __init__.py
│   ├── cli.py           # Command-line interface
│   ├── gui.py           # PyQt5 GUI
│   ├── db.py            # Database management
│   ├── indexer.py       # Document indexing
│   ├── search.py        # Search engine
│   ├── hex_extractor.py # Binary text extraction
│   ├── utils.py         # Utilities
│   ├── ui/              # GUI components
│   ├── resources/       # UI resources
│   └── tests/           # Test suite
├── .github/
│   └── workflows/       # CI/CD workflows
├── README.md
├── pyproject.toml       # Project configuration
└── requirements.txt     # Dependencies
```

## Testing Guidelines

### Unit Tests

- Test individual functions in isolation
- Use fixtures for setup/teardown
- Mock external dependencies
- Aim for >80% coverage

### Integration Tests

- Test component interactions
- Use temporary files/databases
- Clean up resources

### GUI Tests

- Use pytest-qt for GUI testing
- Mock long-running operations
- Test signal/slot connections

## Release Process

Maintainers only:

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create git tag: `git tag v1.0.0`
4. Push tag: `git push origin v1.0.0`
5. Create GitHub release
6. CI automatically publishes to PyPI

## Getting Help

- **Questions**: Open a discussion on GitHub
- **Bugs**: Open an issue
- **Chat**: Join our Discord (if available)
- **Email**: Contact maintainers

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on the code, not the person

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to DocFind! 🎉
