# Antioch Python

Python client library for the Antioch middleware platform.

## Environment Configuration

The library supports both staging and production environments. Set `ANTIOCH_ENV` to control which environment to use:

```bash
# Use staging environment (for internal development)
export ANTIOCH_ENV=staging

# Use production environment (default if not set)
export ANTIOCH_ENV=prod
```

This affects:
- **API endpoints**: `staging.api.antioch.com` vs `api.antioch.com`
- **Auth domain**: `staging.auth.antioch.com` vs `auth.antioch.com`
- **Local data directory**: `~/.antioch/staging/` vs `~/.antioch/prod/`

Auth credentials are stored separately per environment.

## Installation

Authenticate your local environment with GCP via the Google Cloud CLI:

```bash
gcloud auth login                                       # Login to Google Cloud
gcloud config set project proof-of-concept-staging-9072 # Set the correct project
gcloud auth application-default login                   # Create app credentials
```

This project uses [uv](https://github.com/astral-sh/uv), a fast Python package and project manager. Install it and set up authentication:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install keyring authentication globally for uv
uv tool install keyring --with keyrings.google-artifactregistry-auth

# Install all default groups in one step
uv sync
```

Install the pre-commit hooks to auto-run `uv sync` and `ruff format` on Git commit:

```bash
uv run pre-commit install
```

## Releasing to PyPI

The package is published to PyPI as `antioch-py`. To release a new version:

1. **Bump the version** in `pyproject.toml` on a feature branch:

   ```toml
   version = "2.1.0"
   ```

2. **Merge to main** via pull request

That's it! The GitHub Action automatically detects the version bump and publishes to PyPI.

### Versioning

Follow [semantic versioning](https://semver.org/):

- **MAJOR** (2.x.x → 3.0.0): Breaking API changes
- **MINOR** (2.0.x → 2.1.0): New features, backward compatible
- **PATCH** (2.0.0 → 2.0.1): Bug fixes, backward compatible
