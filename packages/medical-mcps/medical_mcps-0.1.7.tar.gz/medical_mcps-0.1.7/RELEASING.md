# Release Guide

This document describes how to create and publish releases for the medical-mcps package.

## Overview

Releases are automated via GitHub Actions. When you push a git tag with the format `v*.*.*`, the following happens automatically:

1. **PyPI Release**: Package is built and published to PyPI via trusted publishing
2. **Docker Image**: Multi-platform Docker image is built and pushed to Docker Hub
3. **GitHub Release**: GitHub release is created with release notes and signed artifacts
4. **Cloud Run Deployment**: Latest Docker image is automatically deployed to Google Cloud Run

## Prerequisites

### One-Time Setup

#### 1. PyPI Trusted Publishing

Configure PyPI to accept releases from GitHub Actions:

1. Go to https://pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"
3. Fill in:
   - **PyPI Project Name**: `medical-mcps`
   - **Owner**: `pascalwhoop` (your GitHub username)
   - **Repository name**: `medical-mcps`
   - **Workflow name**: `publish-pypi.yml`
   - **Environment name**: `pypi`
4. Click "Add"

Note: For the first release, you may need to manually create the PyPI project first, or use the "pending publisher" feature which will automatically create the project on first publish.

#### 2. Docker Hub Secrets

Add Docker Hub credentials to GitHub repository secrets:

1. Go to https://hub.docker.com/settings/security
2. Create a new access token with "Read & Write" permissions
3. Go to your GitHub repository → Settings → Secrets and variables → Actions
4. Add the following secrets:
   - **DOCKERHUB_USERNAME**: Your Docker Hub username
   - **DOCKERHUB_TOKEN**: The access token you created

## Release Process

### 1. Update Version

Edit `pyproject.toml` and update the version number:

```toml
[project]
name = "medical-mcps"
version = "0.2.0"  # Update this
```

### 2. Update Changelog (Optional but Recommended)

If you maintain a CHANGELOG.md, update it with the new version and changes.

### 3. Commit Changes

```bash
git add pyproject.toml
git commit -m "Bump version to 0.2.0"
git push origin main
```

### 4. Create and Push Tag

```bash
# Create an annotated tag
git tag -a v0.2.0 -m "Release version 0.2.0"

# Push the tag (this triggers the release workflows)
git push origin v0.2.0
```

### 5. Monitor Release

Watch the GitHub Actions workflows:

1. Go to https://github.com/pascalwhoop/medical-mcps/actions
2. You should see two workflows running:
   - **Publish to PyPI** - Builds and publishes to PyPI
   - **Publish Docker Image** - Builds and pushes Docker image

Both workflows should complete successfully. If either fails, check the logs for errors.

### 6. Verify Release

After the workflows complete:

**PyPI:**
```bash
# Check PyPI page
open https://pypi.org/project/medical-mcps/

# Test installation
pip install medical-mcps==0.2.0
```

**Docker Hub:**
```bash
# Check Docker Hub page
open https://hub.docker.com/r/<your-username>/medical-mcps/tags

# Test image
docker pull <your-username>/medical-mcps:0.2.0
docker pull <your-username>/medical-mcps:latest
```

**GitHub Release:**
```bash
# Check releases page
open https://github.com/pascalwhoop/medical-mcps/releases
```

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR** (X.0.0): Incompatible API changes
- **MINOR** (0.X.0): Add functionality in a backward compatible manner
- **PATCH** (0.0.X): Backward compatible bug fixes

Examples:
- `v0.1.0` → `v0.1.1` (bug fix)
- `v0.1.1` → `v0.2.0` (new feature)
- `v0.2.0` → `v1.0.0` (breaking change)

## Docker Image Tags

The Docker workflow automatically creates the following tags:

- `v0.2.0` - Specific version
- `0.2` - Major.minor version
- `0` - Major version
- `latest` - Latest release (only for default branch)
- `main-<sha>` - Branch and commit SHA

Users can pin to any of these tags depending on their needs:
```bash
# Pin to exact version
docker pull username/medical-mcps:v0.2.0

# Auto-update minor/patch versions
docker pull username/medical-mcps:0.2

# Always get latest
docker pull username/medical-mcps:latest
```

## Troubleshooting

### PyPI Publish Fails

**Error:** "Trusted publishing exchange failure"
- **Solution:** Verify PyPI trusted publisher configuration matches exactly
- Check that the repository name, workflow name, and environment name are correct

**Error:** "Project already exists"
- **Solution:** If this is the first release, you may need to register the project name on PyPI first
- Alternatively, wait for the pending publisher to be approved

### Docker Publish Fails

**Error:** "authentication required"
- **Solution:** Verify DOCKERHUB_USERNAME and DOCKERHUB_TOKEN secrets are set correctly
- Ensure the token has "Read & Write" permissions

**Error:** "repository does not exist"
- **Solution:** The repository will be created automatically on first push
- Ensure your Docker Hub username in the secrets is correct

### Tag Already Exists

If you need to re-release a version:

```bash
# Delete local tag
git tag -d v0.2.0

# Delete remote tag
git push origin :refs/tags/v0.2.0

# Recreate tag
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

**Warning:** Deleting and recreating tags is not recommended for public releases. Consider creating a new patch version instead (e.g., v0.2.1).

## Manual Release (Emergency)

If automated releases fail, you can release manually:

### Manual PyPI Release

```bash
# Build package
uv build

# Upload to PyPI (requires PyPI API token)
uv publish
```

### Manual Docker Release

```bash
# Build and push
docker buildx build --platform linux/amd64,linux/arm64 \
  -t username/medical-mcps:v0.2.0 \
  -t username/medical-mcps:latest \
  --push .
```

## Best Practices

1. **Test before releasing**: Run full test suite with `make test-all`
2. **Review changes**: Check `git log` since last release
3. **Update documentation**: Ensure README and docs reflect changes
4. **Clear git status**: Ensure working directory is clean
5. **Use annotated tags**: Always use `git tag -a` (not lightweight tags)
6. **One version, one tag**: Don't reuse or move tags
7. **Monitor releases**: Watch GitHub Actions to ensure successful completion
8. **Verify installations**: Test PyPI and Docker installations after release

## Security

- **Sigstore signing**: PyPI releases are automatically signed with Sigstore
- **Attestations**: GitHub generates build provenance attestations
- **No tokens in repository**: All credentials stored as GitHub secrets
- **Trusted publishing**: PyPI releases don't require API tokens
