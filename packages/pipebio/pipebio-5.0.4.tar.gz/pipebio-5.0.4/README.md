# PipeBio Python SDK

This is based on the library originally created as part of the [api-examples](https://github.com/pipebio/api-examples).

## Installation

### From PyPI
```shell
# Using pip
pip install pipebio

# Using uv (recommended)
uv pip install pipebio
```

### For Development
```shell
# Clone the repository
git clone https://github.com/pipebio/python-library.git
cd python-library

# Create and activate a conda environment, install dependencies
uv pip install ".[build,dev]"
```

Note: When using zsh shell, make sure to quote the `.[build,dev]` argument as shown above to prevent glob pattern interpretation.




## Testing
The package includes unit tests and integration tests located in the `tests` directory:

### Unit Tests
Located in `tests/unit/`, these tests can be run using:
```shell
pytest -v tests/unit/
```

This will discover and run all test files matching the pattern `*_test.py` in the `tests` directory.

### Integration Tests
Located in `tests/integration/`, these tests verify the package's functionality:

1. **Environment Setup**
   ```shell
   # Set up required API credentials; add the following to your .env file in project root.
   # Tests will only run in intellij by default which has support for reading .env files and because
   # we have setup configs to do that.
   
   ## GCP
   # PIPE_API_URL=https://antibody-dev.com
   # PIPE_API_KEY=TODO
   
   ## AWS
   PIPE_API_URL=https://pipebio.dev-engteam1.dev.bnch.services/
   PIPE_API_KEY=TODO
   ```

2. **Running Tests**
```shell
pytest -v tests/integration/
```

### Version Compatibility
The package is tested to work with:
- All supported Python versions (see `pyproject.toml` for specific version requirements)
- Explicitly prevents installation on unsupported Python versions with clear error messages
- Tested on both Linux (Ubuntu) and macOS environments

If you're developing new features, make sure to add appropriate tests and verify that all tests pass before submitting changes.

## Versioning and Releases
To deploy a new version of this package:

1. Ensure you're on the `master` branch and your working directory is clean (all changes committed)
2. Use the release script to bump the version, which will create a tag that triggers the release process:

```shell
# Bump version and trigger release workflow:
./bin/release.py --bump patch  # For bug fixes (1.0.0 → 1.0.1)
./bin/release.py --bump minor  # For new features (1.0.0 → 1.1.0)
./bin/release.py --bump major  # For breaking changes (1.0.0 → 2.0.0)

# Re-run a release without bumping the version:
./bin/release.py --retag                   # Re-tag the current version
./bin/release.py --version 2.3.3           # Tag a specific version
./bin/release.py --retag --skip-testpypi   # Re-tag and skip TestPyPI (for already published versions)
```

The release script will:
- For `--bump`: Bump version, create a tag, and push changes to master
- For `--retag`: Create or update a tag for the current version
- For `--version`: Create or update a tag for a specific version
- Create a git tag in the format `vX.Y.Z`
- Push the tag to origin
- This will trigger the GitHub Actions release workflow

You can do a dry run first to see what would happen:
```shell
./bin/release.py --bump patch --dry-run
./bin/release.py --retag --dry-run
```

### Release Workflow

The release process follows these steps:

1. When a tag is pushed, GitHub Actions builds the package and publishes it to TestPyPI
2. You receive a notification that the package is ready for verification in TestPyPI
3. You can test the package by installing it from TestPyPI:
   ```shell
   deactivate
   uv venv .venv-testing
   source .venv-testing/bin/activate
   uv pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple pipebio==X.Y.Z
   ```
4. After verifying the package works correctly, approve the deployment to PyPI:
   - Go to the GitHub repository
   - Navigate to Actions tab
   - Find the running workflow
   - Click "Review deployments" button
   - Approve the "production" environment

The same built package that was tested on TestPyPI will then be published to PyPI, ensuring consistency between environments.

## PyPi documentation
The documentation shown on PyPi is pulled from the `DESCRIPTION.md` file, which is configured in the setup.py file in the line:
```python
long_description=Path("DESCRIPTION.md").read_text(encoding='UTF-8'),
```

# Github actions user accounts
- In both engteam1 and antibody-dev.com we use the user sdk-tester@pipebio.com (emails go to PipeBio leadership staff)
- We have a seperate API key for each (AWS/GCP) in actions