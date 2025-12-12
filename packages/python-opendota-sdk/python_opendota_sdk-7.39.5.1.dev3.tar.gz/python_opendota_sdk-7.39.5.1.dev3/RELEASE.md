# Release Process

This document outlines the release process for python-opendota.

## Version Strategy

This library follows the OpenDota API versioning to maintain compatibility tracking. The version number directly corresponds to the OpenDota API version it supports.

- Current OpenDota API version: **26.0.0**
- Current library version: **26.0.0**

## Release Workflow

### 1. Pre-release Checklist

Before creating a release:

- [ ] All tests pass locally: `uv run pytest`
- [ ] Update version in `pyproject.toml`
- [ ] Update version in `src/python_opendota/__init__.py`
- [ ] Update CHANGELOG.md with release notes
- [ ] Ensure README.md is up to date
- [ ] Review and update documentation if needed

### 2. Creating a Release

1. **Create a git tag:**
   ```bash
   git tag -a v26.0.0 -m "Release version 26.0.0"
   git push origin v26.0.0
   ```

2. **Create GitHub Release:**
   - Go to the repository's "Releases" page
   - Click "Draft a new release"
   - Select the tag you just created
   - Set release title: `v26.0.0 - OpenDota API 26.0.0 Support`
   - Add release notes from CHANGELOG.md
   - Publish the release

3. **Automated Publishing:**
   - The GitHub Action will automatically:
     - Run all tests across Python 3.9-3.12
     - Build the package
     - Publish to PyPI

### 3. Post-release

After a successful release:

1. Verify the package on PyPI: https://pypi.org/project/python-opendota/
2. Test installation: `pip install python-opendota==26.0.0`
3. Update any dependent projects

## Manual Publishing (if needed)

If the automated process fails, you can manually publish:

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build the package
uv run python -m build

# Check the package
uv run twine check dist/*

# Upload to PyPI
uv run twine upload dist/*
```

## Version Alignment

When OpenDota API releases a new version:

1. Check OpenDota API changelog
2. Update library to match API changes if any
3. Bump version to match OpenDota API version
4. Follow the release process above

## Hotfixes

For critical bug fixes between OpenDota API releases:

- Use patch version: `26.0.1`, `26.0.2`, etc.
- Document clearly that it's a library fix, not an API change
- Keep major.minor aligned with OpenDota API version