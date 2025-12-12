# GitHub Workflows Documentation

## 🚨 **Supply Chain Attestation Fix - September 30, 2025**

**Problem:** The v2.6.0 tag was missing supply chain attestations due to conflicting workflows.

**Root Cause:** Multiple workflows were building Docker images with different attestation configurations:
- `docker-build.yml` - Proper attestations with `provenance: mode=max` and `sbom: true`
- `docker-publish.yml` - Missing attestations in build step
- `publish-mcp.yml` - Manual attestation approach causing conflicts

**Solution:** Consolidated to single authoritative workflow with proper attestations.

## 📋 **Active Workflows**

### `docker-build.yml` - **PRIMARY DOCKER WORKFLOW**
- **Triggers:** Push to master, version tags (v*), PRs
- **Features:**
  - ✅ Multi-platform builds (amd64, arm64)
  - ✅ Supply chain attestations (`provenance: mode=max`, `sbom: true`)
  - ✅ Security scanning with Docker Scout
  - ✅ Comprehensive testing (Python 3.11, 3.12, 3.13)
  - ✅ Proper tag generation:
    - `latest` for master branch
    - `v2.6.0` for version tags (preserves v prefix)
    - `master-YYYYMMDD-HHMMSS-<commit>` for master commits
    - `sha-<commit>` for version tags

### `ci.yml` - **CONTINUOUS INTEGRATION**
- **Triggers:** Push to main/develop/master, PRs
- **Features:**
  - ✅ Multi-version Python testing (3.10, 3.11, 3.12, 3.13)
  - ✅ Linting with flake8
  - ✅ Basic Docker build verification
  - ✅ SQLite version compatibility checks

### `security-update.yml` - **SECURITY MONITORING**
- **Triggers:** Weekly schedule (Sundays 2 AM UTC), manual
- **Features:**
  - ✅ Safety security audit
  - ✅ Bandit security linter
  - ✅ Dependency update monitoring

## 🚫 **Disabled Workflows**

### `docker-publish.yml.disabled` - **DISABLED**
- **Reason:** Conflicted with docker-build.yml, missing attestations
- **Status:** Renamed to .disabled to prevent execution

### `publish-mcp.yml.disabled` - **DISABLED**
- **Reason:** Manual attestation approach caused conflicts
- **Status:** Renamed to .disabled to prevent execution

## 🔧 **Supply Chain Security Features**

All Docker images now include:
- ✅ **Build Provenance** - Cryptographic proof of build process
- ✅ **SBOM (Software Bill of Materials)** - Complete dependency manifest
- ✅ **Multi-arch Support** - amd64 and arm64 with unified attestations
- ✅ **Security Scanning** - Docker Scout vulnerability assessment
- ✅ **Reproducible Builds** - SHA-pinned tags for verification

## 📊 **Tag Strategy**

| Tag Type | Example | When Created | Attestations |
|----------|---------|--------------|--------------|
| `latest` | `latest` | Master branch push | ✅ Full |
| Version | `v2.6.0` | Git tag push | ✅ Full |
| Master SHA | `master-20250930-153516-5b602d3` | Master branch push | ✅ Full |
| Version SHA | `sha-5b602d3` | Git tag push | ✅ Full |

## 🚀 **Usage**

### For Version Releases:
1. Create and push a git tag: `git tag v2.7.0 && git push origin v2.7.0`
2. `docker-build.yml` automatically builds and pushes with full attestations
3. All tags (`latest`, `v2.7.0`, `sha-<commit>`) have identical attestations

### For Development:
1. Push to master branch
2. `docker-build.yml` creates `latest` and `master-YYYYMMDD-HHMMSS-<commit>` tags
3. Both tags have full supply chain attestations

## 🔍 **Verification**

To verify attestations are working:
```bash
# Check attestations for latest tag
docker buildx imagetools inspect writenotenow/sqlite-mcp-server:latest --format "{{json .Provenance}}"

# Check attestations for version tag
docker buildx imagetools inspect writenotenow/sqlite-mcp-server:v2.6.0 --format "{{json .Provenance}}"
```

## 📝 **Maintenance Notes**

- **Only modify `docker-build.yml`** for Docker-related changes
- **Never re-enable disabled workflows** without careful review
- **Test attestations** after any workflow changes
- **Monitor Docker Hub** for attestation presence on new builds
