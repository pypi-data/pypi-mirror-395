# Pre-Publish Checklist for sdf-loss

This checklist outlines all steps to complete before running `uv publish` to publish the sdf-loss package to PyPI.

## ✅ Completed Tasks

These items have been completed and verified:

- [x] **Code implementation** - All loss functions implemented and working
- [x] **Test suite** - Comprehensive tests written and passing (35/35 tests pass)
- [x] **Code quality** - Ruff linting and formatting applied
- [x] **Code cleanup** - Removed commented test code, cleaned up imports
- [x] **Documentation** - README.md with examples and usage
- [x] **Project metadata** - pyproject.toml configured
- [x] **License** - MIT License file present

## 🔍 Manual Review Required

These items need your personal review and updates before publishing:

### 1. Update Package Metadata in `pyproject.toml`
example
**Current placeholders that need updating:**

```toml
[project]
name = "sdf-loss"
version = "0.1.0"  # ⚠️ Confirm version number
authors = [
    { name = "Harald", email = "your.email@example.com" }  # ⚠️ UPDATE EMAIL
]

[project.urls]
Homepage = "https://github.com/yourusername/sdf_loss"  # ⚠️ UPDATE USERNAME
Repository = "https://github.com/yourusername/sdf_loss"  # ⚠️ UPDATE USERNAME
Issues = "https://github.com/yourusername/sdf_loss/issues"  # ⚠️ UPDATE USERNAME
```

**Action items:**
- [x] Update author email address
- [x] Update GitHub URLs with correct username/organization
- [x] Confirm version number (0.1.0 for initial release is standard)
- [ ] Verify all project metadata is accurate

### 2. Update README.md Placeholders

**Lines that reference placeholder URLs:**

- Line 26: `git clone https://github.com/yourusername/sdf_loss.git`
- Lines 220-226: Citation section (update or remove if not applicable yet)

**Action items:**
- [x] Update GitHub clone URL in installation section
- [ ] Update or remove citation section (can add later when published)

### 3. Update LICENSE Copyright Year

**Current:** `Copyright (c) 2025 Halyjo`

**Action items:**
- [x] Verify copyright year (update to 2025 if publishing in 2025)
- [x] Confirm copyright holder name

### 4. PyPI Account Setup

**Action items:**
- [x] Create PyPI account at https://pypi.org/account/register/ (if not already done)
- [x] Enable Two-Factor Authentication (2FA) on PyPI account
- [x] Create API token at https://pypi.org/manage/account/token/
- [ ] Test publishing to TestPyPI first (recommended): https://test.pypi.org/

### 5. Build and Test Package Locally

**Before publishing, test the build process:**

```bash
# Build the package
uv build

# Check the build output in dist/
ls -la dist/

# Install locally in development mode to test
uv pip install -e .

# Test import works
python -c "from sdf_loss import DiSCoLoss; print('Import successful!')"

# Run tests one final time
uv run pytest tests/ -v
```

**Action items:**
- [ ] Run `uv build` successfully
- [ ] Verify dist/ contains .whl and .tar.gz files
- [ ] Test local installation works
- [ ] Final test run passes all 35 tests

### 6. Git Repository Preparation

**Action items:**
- [ ] Commit all changes with clear commit message
- [ ] Create and push git tag for version: `git tag v0.1.0 && git push origin v0.1.0`
- [ ] Ensure GitHub repository is public (if publishing to public PyPI)
- [ ] Push all code to GitHub before publishing

### 7. Optional but Recommended

**Additional quality improvements:**

- [ ] Add GitHub Actions CI/CD for automated testing
- [ ] Add badges to README (PyPI version, tests status, license)
- [ ] Create CHANGELOG.md to track versions
- [ ] Add CONTRIBUTING.md if accepting contributions
- [ ] Consider adding example notebooks or scripts in `examples/` directory

## 📦 Publishing Process

Once all the above items are complete:

### Test Publishing (Recommended First Step)

```bash
# Publish to TestPyPI first
uv publish --publish-url https://test.pypi.org/legacy/

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ sdf-loss

# Verify it works
python -c "from sdf_loss import DiSCoLoss; print('Test install works!')"
```

### Production Publishing

```bash
# When ready, publish to production PyPI
uv publish

# After publishing, test installation from PyPI
pip install sdf-loss

# Verify
python -c "from sdf_loss import DiSCoLoss; print('Production install works!')"
```

## 🎯 Post-Publishing Tasks

After successful publication:

- [ ] Verify package appears on PyPI: https://pypi.org/project/sdf-loss/
- [ ] Test installation on clean environment
- [ ] Create GitHub release with release notes
- [ ] Announce on relevant channels (if desired)
- [ ] Update documentation with correct PyPI installation command

## ⚠️ Important Notes

1. **Package name availability**: The name "sdf-loss" must be available on PyPI. Check at https://pypi.org/project/sdf-loss/ (should show 404 if available)

2. **Version immutability**: Once published, you cannot change or delete a version. You can only yank it (hide from default searches).

3. **Build artifacts**: The `dist/` directory will be created during build. Consider adding it to `.gitignore`.

4. **Dependencies**: The package specifies minimum versions for dependencies (torch>=1.10.0, etc.). Verify these work with current package versions.

## 📝 Summary

**Ready to publish when:**
- ✅ All manual review items are checked
- ✅ Package builds successfully (`uv build`)
- ✅ All tests pass (35/35)
- ✅ Metadata is updated and accurate
- ✅ Code is committed and pushed to GitHub
- ✅ TestPyPI publication tested (optional but recommended)

**Final command to publish:**
```bash
uv publish
```

Good luck with your publication! 🚀
