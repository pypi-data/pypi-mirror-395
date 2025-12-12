# Python Version Upgrade Notes for Docker

## Issue Summary: Python 3.14 Docker Upgrade (December 2025)

### Problem

When upgrading from Python 3.13 to 3.14 in the Dockerfile, the Docker image build succeeded but the container failed at runtime with:

```
ModuleNotFoundError: No module named 'mcp_server_sqlite'
```

### Root Cause

The project uses a **multi-stage Docker build** with:
1. **Builder stage**: Uses `ghcr.io/astral-sh/uv:python3.13-alpine` to build dependencies
2. **Runtime stage**: Initially tried to use `python:3.14-alpine`

**Two critical incompatibilities were discovered:**

1. **UV Image Availability**: The `ghcr.io/astral-sh/uv:python3.14-alpine` image does not exist yet (as of December 2025)
2. **Python Version Mismatch**: When dependencies are built with Python 3.13 (builder stage) and copied to Python 3.14 (runtime stage), the virtual environment's site-packages path (`lib/python3.13/site-packages`) doesn't match what Python 3.14 expects (`lib/python3.14/site-packages`)

### What We Tried (All Failed)

1. ❌ **Update runtime stage only to 3.14** - Module not found (site-packages path mismatch)
2. ❌ **Update builder stage to 3.14** - UV image doesn't exist, build failed
3. ❌ **Fix Python symlinks from 3.13 to 3.14** - Didn't solve the site-packages path issue

### Solution

**Revert Dockerfile to Python 3.13** while keeping all other upgrades:
- ✅ All Python **dependencies** updated and verified compatible with 3.14
- ✅ `pyproject.toml` includes Python 3.14 classifier
- ✅ Local installations work perfectly on Python 3.14
- ⏳ Docker will be upgraded once `ghcr.io/astral-sh/uv:python3.14-alpine` becomes available

## Lessons Learned

### 1. Multi-Stage Builds Must Use Same Python Version

When using a multi-stage Docker build that copies a virtual environment from builder to runtime:

```dockerfile
FROM builder-image:pythonX.Y AS builder
# Build .venv here

FROM runtime-image:pythonX.Z  # ❌ X.Y ≠ X.Z will fail!
COPY --from=builder /app/.venv /app/.venv
```

**Rule**: Builder and runtime Python versions **MUST match** exactly (both X.Y).

### 2. Check UV Image Availability First

Before upgrading Python versions in Docker, verify the UV image exists:

```bash
# Check if image exists
docker pull ghcr.io/astral-sh/uv:python3.XX-alpine

# Or check on GitHub Container Registry
# https://github.com/astral-sh/uv/pkgs/container/uv
```

### 3. Upgrade Strategy for Future Python Versions

When a new Python version is released (e.g., 3.15):

**Step 1: Verify Dependency Compatibility**
```bash
# Test locally first
python3.15 -m pip install -r requirements.txt
python3.15 test_runner.py --quick
```

**Step 2: Update Project Files**
- ✅ `pyproject.toml` - Add classifier, update `requires-python` if needed
- ✅ `requirements.txt` - Update dependency versions if needed
- ✅ Update dependency lock file (`uv.lock`)

**Step 3: Check Docker Image Availability**
```bash
# Check base Python image
docker pull python:3.15-alpine

# Check UV builder image  
docker pull ghcr.io/astral-sh/uv:python3.15-alpine
```

**Step 4: Update Dockerfile (Only if both images exist)**
```dockerfile
FROM ghcr.io/astral-sh/uv:python3.15-alpine AS uv
# ...
FROM python:3.15-alpine
# ...
RUN ln -s /usr/local/bin/python3 /app/.venv/bin/python3.15
```

**Step 5: Test Docker Build**
```bash
docker build -t test .
docker run --rm test --help
```

## Current Status (December 2025)

| Component | Python Version | Status |
|-----------|---------------|--------|
| Local Development | 3.14.0 | ✅ Working |
| Dependencies | 3.10-3.14 | ✅ Compatible |
| `pyproject.toml` | 3.10-3.14 | ✅ Updated |
| CI Tests | 3.10-3.13 | ✅ Passing |
| Docker Image | 3.13 | ✅ Working |
| UV Builder Image | 3.13 | ✅ Available |

**Waiting for**: `ghcr.io/astral-sh/uv:python3.14-alpine` to become available

## Files Modified During This Upgrade

### Successful Changes (Kept)
1. `package.json` - Node.js engine: `^18.18.0 || ^20.9.0 || >=21.1.0`
2. `package.json` - ESLint 9.39.1, Prettier 3.7.4
3. `.eslintrc.js` - **NEW** - ESLint 9 backward compatibility
4. `pyproject.toml` - MCP 1.23.1, Starlette 0.50.0, Python 3.14 classifier
5. `requirements.txt` - Updated to latest versions
6. `uv.lock` - Complete dependency tree update

### Reverted Changes
1. `Dockerfile` - Reverted to `python:3.13-alpine` (both stages)
2. `Dockerfile` - Python symlink remains `python3.13`

## Monitoring for UV Python 3.14 Image

Check periodically for availability:
- GitHub: https://github.com/astral-sh/uv/pkgs/container/uv
- Or run: `docker pull ghcr.io/astral-sh/uv:python3.14-alpine`

Once available, create a new PR to upgrade the Dockerfile to Python 3.14.

## Related Issues

- Dependabot PR #45: Original Python 3.13→3.14 upgrade attempt
- Commits:
  - `9538778` - Merged all dependency updates
  - `5bd79f0` - First Docker fix attempt (failed)
  - `7ba8b2e` - Second Docker fix attempt (failed)
  - `45ff32e` - Final revert to Python 3.13 (working)

## Quick Reference: Dockerfile Python Version Change

When UV image becomes available, change these 3 lines:

```diff
- FROM ghcr.io/astral-sh/uv:python3.13-alpine AS uv
+ FROM ghcr.io/astral-sh/uv:python3.14-alpine AS uv

- FROM python:3.13-alpine
+ FROM python:3.14-alpine

- ln -s /usr/local/bin/python3 /app/.venv/bin/python3.13 && \
+ ln -s /usr/local/bin/python3 /app/.venv/bin/python3.14 && \
```

## Testing Checklist

Before merging any Python version upgrade in Docker:

- [ ] Base Python image exists and pulls successfully
- [ ] UV builder image exists and pulls successfully  
- [ ] Both images use the **same Python minor version**
- [ ] Local tests pass on new Python version
- [ ] Docker build completes successfully
- [ ] Docker container starts without import errors
- [ ] `docker run --rm <image> --help` shows help text
- [ ] CI/CD pipeline passes all checks

---

**Document Created**: December 6, 2025  
**Last Updated**: December 6, 2025  
**Status**: Active - Waiting for Python 3.14 UV image availability

