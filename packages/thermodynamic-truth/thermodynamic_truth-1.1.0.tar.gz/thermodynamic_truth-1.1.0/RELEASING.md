# Release Process for ThermoTruth Protocol

This document describes the complete release process for publishing new versions of the `thermodynamic-truth` package to PyPI and GitHub Packages.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Prerequisites](#prerequisites)
3. [Automated Release (Recommended)](#automated-release-recommended)
4. [Manual Release (Emergency/Hotfix)](#manual-release-emergencyhotfix)
5. [Version Numbering](#version-numbering)
6. [Security & Verification](#security--verification)
7. [Troubleshooting](#troubleshooting)
8. [Post-Release Checklist](#post-release-checklist)

---

## Quick Start

**TL;DR**: Push a git tag starting with `v` and everything happens automatically.

```bash
# 1. Update version in setup.py
vim setup.py  # Change version="1.0.0" to version="1.1.0"

# 2. Commit the version bump
git add setup.py
git commit -m "chore: Bump version to 1.1.0"

# 3. Create and push the tag
git tag -a v1.1.0 -m "Release v1.1.0"
git push origin main
git push origin v1.1.0

# 4. Wait ~2 minutes, package is live on PyPI + GitHub Packages
```

---

## Prerequisites

### For Automated Releases (First-Time Setup)

#### 1. Configure PyPI Trusted Publishing

**This is required only once per project.**

1. Go to https://pypi.org/manage/account/publishing/
2. Click "Add a new pending publisher"
3. Fill in:
   - **PyPI Project Name**: `thermodynamic-truth`
   - **Owner**: `Kuonirad`
   - **Repository name**: `thermo-truth-proto`
   - **Workflow name**: `publish.yml`
   - **Environment name**: `pypi`
4. Click "Add"

**Why this works**: GitHub Actions uses OIDC (OpenID Connect) to prove its identity to PyPI. No API tokens stored anywhere. Zero secrets to leak.

#### 2. Verify GitHub Permissions

Ensure the repository has:
- ✅ Actions enabled (Settings → Actions → General)
- ✅ Workflow permissions set to "Read and write" (Settings → Actions → General → Workflow permissions)

### For Manual Releases

Install publishing tools:

```bash
pip install build twine sigstore
```

---

## Automated Release (Recommended)

### Step 1: Prepare the Release

#### Update Version Number

Edit `setup.py`:

```python
setup(
    name="thermodynamic-truth",
    version="1.1.0",  # ← Change this
    ...
)
```

**Versioning rules**: Follow [Semantic Versioning 2.0.0](https://semver.org/)
- `MAJOR.MINOR.PATCH` (e.g., `1.2.3`)
- Increment `MAJOR` for breaking changes
- Increment `MINOR` for new features (backward compatible)
- Increment `PATCH` for bug fixes

#### Update CHANGELOG.md

Add release notes:

```markdown
## [1.1.0] - 2025-12-01

### Added
- New annealing schedule: adaptive exponential decay
- Byzantine detection with entropy thresholds

### Fixed
- PoW timestamp validation bug (#42)

### Changed
- Improved consensus convergence speed by 15%
```

#### Commit Changes

```bash
git add setup.py CHANGELOG.md
git commit -m "chore: Bump version to 1.1.0"
git push origin main
```

### Step 2: Create and Push the Tag

```bash
# Create annotated tag (recommended)
git tag -a v1.1.0 -m "Release v1.1.0: Adaptive annealing and Byzantine detection"

# Push the tag
git push origin v1.1.0
```

**Important**: The tag **must** start with `v` (e.g., `v1.0.0`, `v2.1.3-beta.1`)

### Step 3: Monitor the Workflow

1. Go to https://github.com/Kuonirad/thermo-truth-proto/actions
2. Click on the running "Publish to PyPI and GitHub Packages" workflow
3. Watch the jobs complete (~2 minutes):
   - ✅ Build distribution packages
   - ✅ Generate SBOM
   - ✅ Publish to PyPI
   - ✅ Publish to GitHub Packages
   - ✅ Sign with Sigstore
   - ✅ Create GitHub Release
   - ✅ Verify publication

### Step 4: Verify the Release

**Check PyPI:**
```bash
pip install thermodynamic-truth==1.1.0 --no-cache-dir
python -c "import thermodynamic_truth; print(thermodynamic_truth.__version__)"
```

**Check GitHub Packages:**
```bash
pip install thermodynamic-truth==1.1.0 \
  --index-url https://pypi.pkg.github.com/Kuonirad/simple/
```

**Check GitHub Release:**
- Visit https://github.com/Kuonirad/thermo-truth-proto/releases
- Verify artifacts are attached:
  - `thermodynamic_truth-1.1.0-py3-none-any.whl`
  - `thermodynamic_truth-1.1.0.tar.gz`
  - `thermodynamic_truth-1.1.0-py3-none-any.whl.sigstore` (signature)
  - `sbom.json` (Software Bill of Materials)

---

## Manual Release (Emergency/Hotfix)

Use this only when:
- GitHub Actions is down
- You need an immediate hotfix
- The automated workflow is broken

### Step 1: Build the Package

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info

# Build distributions
python -m build

# Verify the build
twine check dist/*
```

### Step 2: Publish to PyPI

**Option A: Using Trusted Publishing (if configured)**

```bash
# This will fail if not run from GitHub Actions
# Only works if you've set up trusted publishing
python -m twine upload dist/*
```

**Option B: Using API Token**

1. Get a PyPI API token: https://pypi.org/manage/account/token/
2. Create `~/.pypirc`:

```ini
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmc...  # Your token here
```

3. Upload:

```bash
twine upload dist/*
```

### Step 3: Sign with Sigstore

```bash
# Sign all distributions
sigstore sign dist/*

# Verify signatures
sigstore verify identity dist/*.whl \
  --cert-identity your-email@example.com \
  --cert-oidc-issuer https://github.com/login/oauth
```

### Step 4: Create GitHub Release

```bash
# Create tag
git tag -a v1.1.0 -m "Emergency hotfix: Critical PoW bug"
git push origin v1.1.0

# Create release via GitHub CLI
gh release create v1.1.0 \
  --title "Release v1.1.0" \
  --notes "Emergency hotfix for PoW validation" \
  dist/*
```

---

## Version Numbering

### Semantic Versioning

Follow [SemVer 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
```

**Examples:**
- `1.0.0` - Initial stable release
- `1.1.0` - New feature, backward compatible
- `1.1.1` - Bug fix
- `2.0.0` - Breaking change
- `2.0.0-alpha.1` - Pre-release
- `2.0.0-beta.2+20251201` - Pre-release with build metadata

### Pre-Release Versions

For testing before stable release:

```bash
# Alpha (early testing)
git tag v2.0.0-alpha.1

# Beta (feature complete, testing)
git tag v2.0.0-beta.1

# Release Candidate (final testing)
git tag v2.0.0-rc.1

# Stable
git tag v2.0.0
```

**Installation:**
```bash
# Stable only (default)
pip install thermodynamic-truth

# Include pre-releases
pip install thermodynamic-truth --pre
```

---

## Security & Verification

### Verify Package Signatures

All releases are signed with [Sigstore](https://www.sigstore.dev/) (keyless signing).

**Verify a wheel:**

```bash
pip install sigstore

sigstore verify identity \
  thermodynamic_truth-1.1.0-py3-none-any.whl \
  --cert-identity https://github.com/Kuonirad/thermo-truth-proto/.github/workflows/publish.yml@refs/tags/v1.1.0 \
  --cert-oidc-issuer https://token.actions.githubusercontent.com
```

**What this proves:**
- ✅ Package was built by GitHub Actions
- ✅ From the `publish.yml` workflow
- ✅ For the specific tag `v1.1.0`
- ✅ No tampering after build

### SLSA Provenance

Every release includes SLSA Level 3 provenance attestation.

**View provenance:**

```bash
gh attestation verify \
  thermodynamic_truth-1.1.0-py3-none-any.whl \
  --owner Kuonirad
```

**What this proves:**
- ✅ Build environment (GitHub Actions runner)
- ✅ Build steps executed
- ✅ Source commit hash
- ✅ Build reproducibility

### Software Bill of Materials (SBOM)

Every release includes a CycloneDX SBOM.

**Download SBOM:**

```bash
gh release download v1.1.0 --pattern sbom.json
```

**Analyze dependencies:**

```bash
# Install SBOM tools
pip install cyclonedx-bom

# View dependency tree
cat sbom.json | jq '.components[] | {name, version, licenses}'
```

---

## Troubleshooting

### "Trusted publishing is not configured"

**Problem**: PyPI rejects the upload with:

```
ERROR: Trusted publishing is not configured for this project
```

**Solution**: Configure trusted publishing on PyPI (see [Prerequisites](#prerequisites))

### "Tag already exists"

**Problem**:

```
fatal: tag 'v1.0.0' already exists
```

**Solution**: Either delete the tag or use a new version:

```bash
# Option 1: Delete and recreate
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# Option 2: Use a new version
git tag -a v1.0.1 -m "Release v1.0.1"
git push origin v1.0.1
```

### "File already exists on PyPI"

**Problem**:

```
ERROR: File already exists. Use a different version number.
```

**Solution**: You cannot overwrite PyPI releases. Increment the version:

```bash
# If you uploaded 1.0.0 by mistake, use 1.0.1
vim setup.py  # Change to version="1.0.1"
git add setup.py
git commit -m "chore: Bump to 1.0.1"
git tag v1.0.1
git push origin main v1.0.1
```

**To remove a bad release from PyPI** (use sparingly):

```bash
# Yank the version (hides from pip, but doesn't delete)
pip install pkginfo
twine upload --repository pypi --skip-existing dist/*
# Then go to https://pypi.org/manage/project/thermodynamic-truth/releases/
# Click "Options" → "Yank release"
```

### Workflow Fails on "Publish to PyPI"

**Check the logs:**

1. Go to Actions tab
2. Click the failed workflow
3. Click "Publish to PyPI" job
4. Read the error message

**Common causes:**
- Trusted publishing not configured
- Version already exists on PyPI
- Package name typo in `setup.py`
- Missing required metadata

### GitHub Packages Upload Fails

**Problem**: GitHub Packages requires authentication even for public packages.

**Solution**: Ensure `GITHUB_TOKEN` has `packages: write` permission (already configured in workflow).

---

## Post-Release Checklist

After a successful release:

- [ ] Verify package on PyPI: https://pypi.org/project/thermodynamic-truth/
- [ ] Verify GitHub Release: https://github.com/Kuonirad/thermo-truth-proto/releases
- [ ] Test installation: `pip install thermodynamic-truth==X.Y.Z`
- [ ] Run smoke test: `python -c "from thermodynamic_truth.core import ThermodynamicTruth; print('OK')"`
- [ ] Update documentation if needed
- [ ] Announce release (Twitter, Discord, mailing list, etc.)
- [ ] Close related GitHub issues/PRs
- [ ] Update project roadmap

---

## Deprecating/Yanking Releases

### Yank a Release on PyPI

If a release has a critical bug:

1. Go to https://pypi.org/manage/project/thermodynamic-truth/releases/
2. Find the version
3. Click "Options" → "Yank release"
4. Provide a reason: "Critical bug in PoW validation"

**Effect**: The version is hidden from `pip install` but still accessible with explicit version:

```bash
# This will skip yanked versions
pip install thermodynamic-truth

# This still works (for existing users)
pip install thermodynamic-truth==1.0.0
```

### Delete a GitHub Release

```bash
gh release delete v1.0.0 --yes
git push origin :refs/tags/v1.0.0
```

---

## Advanced: Release Branches

For long-term support (LTS) versions:

```bash
# Create release branch
git checkout -b release/1.x
git push origin release/1.x

# Backport fixes
git cherry-pick <commit-hash>

# Tag from release branch
git tag v1.2.5
git push origin v1.2.5
```

---

## Contact & Support

- **Issues**: https://github.com/Kuonirad/thermo-truth-proto/issues
- **Discussions**: https://github.com/Kuonirad/thermo-truth-proto/discussions
- **Security**: See [SECURITY.md](SECURITY.md) for vulnerability reporting

---

## References

- [Semantic Versioning](https://semver.org/)
- [PyPI Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
- [Sigstore Documentation](https://docs.sigstore.dev/)
- [SLSA Framework](https://slsa.dev/)
- [CycloneDX SBOM](https://cyclonedx.org/)
- [GitHub Actions OIDC](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

---

**Last Updated**: December 1, 2025  
**Maintainer**: Kuonirad  
**Version**: 1.0
