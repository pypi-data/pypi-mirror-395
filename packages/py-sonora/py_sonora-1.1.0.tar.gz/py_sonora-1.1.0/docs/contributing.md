# Contributing

Thank you for your interest in contributing to Sonora! We welcome contributions from the community.

## Ways to Contribute

- 🐛 **Bug Reports**: Found a bug? [Open an issue](https://github.com/code-xon/sonora/issues/new?template=bug_report.md)
- 💡 **Feature Requests**: Have an idea? [Open an issue](https://github.com/code-xon/sonora/issues/new)
- 📖 **Documentation**: Help improve our docs
- 🧪 **Testing**: Write tests or report test failures
- 💻 **Code**: Submit pull requests with fixes or features

## Development Setup

### Prerequisites

- Python 3.11+
- Git
- Docker (for testing with Lavalink)

### Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/your-username/sonora.git
   cd sonora
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -e .[dev]
   ```

4. **Install Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

5. **Run Tests**
   ```bash
   pytest
   ```

## Development Workflow

### 1. Choose an Issue

- Check [open issues](https://github.com/code-xon/sonora/issues) for something to work on
- Comment on the issue to indicate you're working on it
- For new features, discuss the design first

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

### 3. Make Changes

- Follow the [code style](#code-style) guidelines
- Write tests for new functionality
- Update documentation if needed
- Run the test suite: `pytest`

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add your feature description"
```

Use [conventional commits](https://conventionalcommits.org/):

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for formatting
- `refactor:` for code refactoring
- `test:` for tests
- `chore:` for maintenance

### 5. Push and Create PR

```bash
git push origin your-branch-name
```

Then create a pull request on GitHub.

## Code Style

### Python Style

We use several tools to maintain code quality:

- **Black** for code formatting (88 character line length)
- **Ruff** for linting and import sorting
- **MyPy** for type checking (strict mode)

Run all tools:

```bash
black .
ruff check . --fix
mypy sonora
```

### Commit Messages

Follow conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Examples:
```
feat(player): add volume normalization
fix(queue): handle empty queue edge case
docs(api): update filter examples
```

### Naming Conventions

- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/Methods**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

## Testing

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=sonora --cov-report=html

# Run specific test
pytest tests/test_player.py::TestPlayer::test_play

# Run tests matching pattern
pytest -k "test_volume"
```

### Writing Tests

- Use `pytest` and `pytest-asyncio` for async tests
- Place tests in `tests/` directory
- Name test files `test_*.py`
- Use descriptive test names: `test_should_do_something`

Example:
```python
import pytest
from sonora import SonoraClient

class TestSonoraClient:
    @pytest.mark.asyncio
    async def test_initialization(self):
        client = SonoraClient([])
        assert client is not None
        assert not client._running
```

### Test Coverage

Aim for ≥85% test coverage. Check coverage:

```bash
pytest --cov=sonora --cov-report=term-missing
```

## Documentation

### Building Docs

```bash
pip install mkdocs mkdocstrings[python]
mkdocs serve  # Serve locally
mkdocs build  # Build for production
```

### Writing Docs

- Use Markdown in `docs/` directory
- Follow existing structure and style
- Include code examples with syntax highlighting
- Update `mkdocs.yml` navigation if adding new pages

## Pull Request Process

### Before Submitting

- ✅ All tests pass
- ✅ Code follows style guidelines
- ✅ Documentation updated
- ✅ Commit messages are clear
- ✅ Branch is up to date with main

### PR Template

Use the PR template with:

- Clear title describing the change
- Description of what was changed and why
- Screenshots/videos for UI changes
- Test results
- Breaking changes noted

### Review Process

1. **Automated Checks**: CI runs tests, linting, and type checking
2. **Code Review**: Maintainers review code quality and design
3. **Testing**: Additional testing may be requested
4. **Approval**: PR approved and merged

## Issue Reporting

### Bug Reports

Use the bug report template with:

- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (Python version, OS, etc.)
- Error messages/logs

### Feature Requests

- Describe the problem you're trying to solve
- Explain your proposed solution
- Consider alternative approaches
- Discuss potential impact

## Community Guidelines

### Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help newcomers learn
- Maintain professional communication

### Getting Help

- **Documentation**: Check [docs](https://code-xon.github.io/sonora/)
- **Issues**: Search existing issues first
- **Discord**: Join our [community server](https://discord.gg/sonora)
- **Discussions**: Use GitHub Discussions for questions

## Recognition

Contributors are recognized in:

- CHANGELOG.md for significant contributions
- GitHub repository contributors list
- Release notes

Thank you for contributing to Sonora! 🎵