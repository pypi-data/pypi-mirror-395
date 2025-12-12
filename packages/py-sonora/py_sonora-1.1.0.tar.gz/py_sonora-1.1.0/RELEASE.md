# Release Process

This document outlines the steps for releasing a new version of Sonora.

## Prerequisites

- All tests pass
- Code is properly formatted and linted
- Documentation is up to date
- CHANGELOG.md is updated with the new version
- Version in `pyproject.toml` is updated

## Steps

### 1. Prepare Release

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md with new version and date
3. Commit changes: `git commit -m "chore: prepare release vX.Y.Z"`

### 2. Create Git Tag

```bash
git tag -a vX.Y.Z -m "Release vX.Y.Z"
git push origin vX.Y.Z
```

### 3. GitHub Actions

The `publish.yml` workflow will automatically:
- Build the package
- Publish to PyPI
- Create a GitHub release

### 4. Post-Release

1. Update documentation site if needed
2. Announce the release on Discord/social media
3. Monitor for issues

## Version Numbering

Sonora follows [Semantic Versioning](https://semver.org/):

- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality additions
- **PATCH** version for backwards-compatible bug fixes

## Security Releases

For security releases:
1. Follow the security disclosure process in SECURITY.md
2. Use a PATCH version bump
3. Include security advisory in the release notes