# Contributing to Sonora

Thank you for your interest in contributing to Sonora! We welcome contributions from the community.

## Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/your-username/sonora.git`
3. Install dependencies: `pip install -e .[dev]`
4. Install pre-commit hooks: `pre-commit install`
5. Create a branch for your changes: `git checkout -b feature/your-feature`

## Code Style

We use the following tools for code quality:

- **Black** for code formatting
- **Ruff** for linting
- **MyPy** for type checking

Run these tools before committing:

```bash
black .
ruff check . --fix
mypy sonora
```

## Testing

Add tests for new features and ensure all tests pass:

```bash
pytest
```

Aim for >= 85% test coverage.

## Pull Requests

1. Ensure your code follows the style guidelines
2. Add tests for new functionality
3. Update documentation if needed
4. Write clear commit messages following conventional commits
5. Create a pull request with a descriptive title and description

## Commit Messages

Use conventional commit format:

- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for formatting
- `refactor:` for code refactoring
- `test:` for tests
- `chore:` for maintenance

## Issues

Report bugs and request features using GitHub Issues.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Contact

- Lead Developer: Ramkrishna
- Email: [ramkrishna@code-xon.fun](mailto:ramkrishna@code-xon.fun)