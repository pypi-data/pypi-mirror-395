# Contributing to Gushwork RAG Python SDK

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to the project.

## Development Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/gushwork/gw-rag.git
   cd gw-rag/sdk/python
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install development dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

## Code Style

We follow Python best practices and PEP 8 guidelines:

### Formatting

- Use **Black** for code formatting
- Line length: 100 characters
- Use **isort** for import sorting

```bash
# Format code
black gushwork_rag/

# Sort imports
isort gushwork_rag/
```

### Type Hints

- Use type hints for all function parameters and return values
- Use `typing` module for complex types
- Run **mypy** for type checking

```bash
mypy gushwork_rag/
```

### Linting

- Use **flake8** for linting
- Fix all linting errors before committing

```bash
flake8 gushwork_rag/
```

## Testing

We use **pytest** for testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=gushwork_rag

# Run specific test file
pytest tests/test_client.py
```

### Writing Tests

- Write tests for all new features
- Maintain or improve code coverage
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern

## Pull Request Process

1. **Fork the repository** and create your branch from `main`

2. **Make your changes**
   - Write clear, concise commit messages
   - Follow the code style guidelines
   - Add tests for new features
   - Update documentation as needed

3. **Run the checks**
   ```bash
   # Format code
   black gushwork_rag/
   isort gushwork_rag/
   
   # Run tests
   pytest
   
   # Type check
   mypy gushwork_rag/
   
   # Lint
   flake8 gushwork_rag/
   ```

4. **Update documentation**
   - Update README.md if adding new features
   - Add docstrings to new functions/classes
   - Update examples if needed

5. **Submit the Pull Request**
   - Provide a clear description of the changes
   - Reference any related issues
   - Wait for review and address feedback

## Commit Messages

Follow conventional commit format:

```
type(scope): subject

body

footer
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(chat): add support for streaming responses

Add streaming support to chat client with new stream() method.
Includes progress indicators and proper error handling.

Closes #123

---

fix(files): handle empty file uploads correctly

Previously, empty files would cause an error. Now they're handled gracefully
with proper error messages.
```

## Project Structure

```
sdk/python/
├── gushwork_rag/          # Main package
│   ├── __init__.py        # Package exports
│   ├── client.py          # Main client class
│   ├── http_client.py     # HTTP client
│   ├── models.py          # Data models
│   ├── exceptions.py      # Exception classes
│   └── clients/           # Sub-clients
│       ├── __init__.py
│       ├── auth.py
│       ├── chat.py
│       ├── files.py
│       └── namespaces.py
├── examples/              # Example scripts
├── tests/                 # Test files
├── setup.py              # Package setup
├── pyproject.toml        # Project configuration
└── README.md             # Documentation
```

## Adding New Features

### Adding a New Client

1. Create a new file in `gushwork_rag/clients/`
2. Implement the client class with proper type hints
3. Add docstrings for all public methods
4. Export from `gushwork_rag/clients/__init__.py`
5. Add property to main `GushworkRAG` class
6. Write tests
7. Add examples
8. Update documentation

### Adding New Models

1. Add to `gushwork_rag/models.py`
2. Use `@dataclass` decorator
3. Add `from_dict()` class method if needed
4. Export from `gushwork_rag/__init__.py`
5. Add type hints
6. Document all fields

### Adding New Exceptions

1. Add to `gushwork_rag/exceptions.py`
2. Inherit from `GushworkError`
3. Export from `gushwork_rag/__init__.py`
4. Update error handling in HTTP client

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int) -> str:
    """Short description.

    Longer description if needed.

    Args:
        param1: Description of param1
        param2: Description of param2

    Returns:
        Description of return value

    Raises:
        ValueError: When something goes wrong

    Example:
        >>> function_name("test", 42)
        'result'
    """
```

### README Updates

When adding features, update:
- Feature list
- Usage examples
- API reference
- Comparison table (if applicable)

## Release Process

1. Update version in:
   - `setup.py`
   - `pyproject.toml`
   - `gushwork_rag/__init__.py`

2. Update `CHANGELOG.md`

3. Create release commit:
   ```bash
   git commit -m "chore: release v0.2.0"
   ```

4. Tag the release:
   ```bash
   git tag v0.2.0
   git push origin v0.2.0
   ```

5. Build and publish:
   ```bash
   python setup.py sdist bdist_wheel
   twine upload dist/*
   ```

## Questions?

If you have questions:
- Open an issue for discussion
- Check existing issues and PRs
- Reach out to maintainers

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Give constructive feedback
- Focus on what's best for the project

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

