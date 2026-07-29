## GitHub Workflows

This repository uses GitHub Actions to automate validation, packaging, and security checks for the application.

### Workflow Summary

| Workflow | File | Purpose | Trigger |
|---|---|---|---|
| Build | .github/workflows/build.yml | Verifies that the Docker image builds successfully | Push to `main`, pull requests |
| Publish Docker Image | .github/workflows/publish-image.yml | Builds and publishes the container image to GitHub Container Registry (GHCR) | Push to `main`, tags matching `v*` |
| Security Scan | .github/workflows/security.yml | Scans the repository for vulnerabilities using Trivy | Push to `main`, pull requests |

### 1. Build
The build workflow checks out the repository and runs a Docker build to confirm the image can be created successfully.

- Triggered on pushes to `main`
- Also runs for pull requests
- Helps catch build issues early

### 2. Publish Docker Image
The publish workflow builds and pushes the application image to GHCR.

- Uses `docker/login-action` to authenticate with GitHub Container Registry
- Uses `docker/metadata-action` to generate image metadata
- Publishes images tagged as:
  - `latest`
  - the current commit SHA

### 3. Security Scan
The security workflow runs Trivy to identify known vulnerabilities in the repository contents.

- Scans filesystem content for `CRITICAL` and `HIGH` severity issues
- Runs automatically for pushes to `main` and pull requests

### Notes
- The build and security workflows provide continuous validation for changes.
- The image publish workflow is intended for release-ready changes and versioned tags.
- No additional secrets are required beyond the default GitHub token permissions for package publishing.