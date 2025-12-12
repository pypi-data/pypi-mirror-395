# Release Checklist: v6.6.0

## 📋 Pre-Release Verification

### ✅ Version Configuration
- [x] **pyproject.toml** - Version set to `6.6.0` (line 3)
- [x] **CHANGELOG.md** - v6.6.0 entry added with complete feature list
- [x] **README.md** - All examples working and up-to-date
- [x] **Dependencies** - No new dependencies added

### ✅ Backwards Compatibility
- [x] **TypedDict Structure** - All new fields are optional (not `Required`)
- [x] **Method Signatures** - All new parameters have default values (`NOT_GIVEN`)
- [x] **API Compatibility** - No breaking changes to existing API
- [x] **Type Safety** - Proper type annotations for all new fields

### ✅ New Features (9 Tracing Fields)
- [x] `credential_alias` - Human-readable API key name
- [x] `environment` - Deployment environment (production, staging, development)
- [x] `operation_subtype` - Additional operation detail
- [x] `parent_transaction_id` - Parent transaction for distributed tracing
- [x] `region` - Cloud region identifier
- [x] `retry_number` - Retry attempt counter
- [x] `trace_name` - Human-readable trace label (max 256 chars)
- [x] `trace_type` - Categorical workflow identifier (max 128 chars)
- [x] `transaction_name` - Human-friendly operation name

### ✅ Documentation
- [x] **README.md** - PyPI badge fixed (removed angle brackets)
- [x] **README.md** - Missing `import httpx` added to timeout example
- [x] **CHANGELOG.md** - Complete v6.6.0 entry with all changes
- [x] **PR Template** - Added `.github/pull_request_template.md`

### ✅ Code Quality
- [x] No syntax errors
- [x] No import errors
- [x] Type hints correct
- [x] Docstrings complete for all new fields

---

## 🔍 What Changed in v6.6.0

### API Changes
**Added:** 9 new optional fields to `AICreateCompletionParams` for trace visualization and observability

**Impact:** NONE - All fields are optional, existing code works without modification

### Documentation Changes
1. Fixed PyPI badge rendering (removed broken angle bracket syntax)
2. Added missing `import httpx` to timeout configuration example
3. Added pull request template for better workflow

---

## 🧪 Testing Status

### Automated Tests
- ✅ TypedDict structure validated (46 total fields, 9 new optional)
- ✅ Method signature validated (all new fields have defaults)
- ✅ Backwards compatibility verified (old-style calls work)
- ✅ New field usage verified (new-style calls work)

### Manual Verification
- ✅ Existing middleware packages compatible (OpenAI, Ollama, Google, Anthropic, LiteLLM)
- ✅ No code changes required in any middleware
- ✅ All README examples tested and working

---

## 📦 Build Verification

### Current State
```bash
Version: 6.6.0
Python: >= 3.8
Dependencies: No changes
Build System: hatchling (unchanged)
```

### Distribution Files
Previous versions in `dist/`:
- `revenium_metering-6.4.0-py3-none-any.whl`
- `revenium_metering-6.4.0.tar.gz`
- `revenium_metering-6.5.0-py3-none-any.whl`
- `revenium_metering-6.5.0.tar.gz`

**Action Required:** Build v6.6.0 distribution files

---

## 🚀 Release Steps

### 1. Merge Documentation PR
```bash
# Current branch: docs/fix-readme-badge-and-examples
# Merge this PR first to update README and add PR template
```

### 2. Build Distribution
```bash
cd revenium-metering-python
rye build --clean
```

**Expected Output:**
- `dist/revenium_metering-6.6.0-py3-none-any.whl`
- `dist/revenium_metering-6.6.0.tar.gz`

### 3. Test Installation
```bash
# Test in clean environment
python -m venv test_env
source test_env/bin/activate
pip install dist/revenium_metering-6.6.0-py3-none-any.whl

# Verify
python -c "import revenium_metering; print(revenium_metering.__version__)"
# Expected: 6.6.0
```

### 4. Publish to PyPI
```bash
export PYPI_TOKEN="your-pypi-token"
./bin/publish-pypi
```

**Or manually:**
```bash
rye publish --yes --token=$PYPI_TOKEN
```

### 5. Post-Publish Verification
- [ ] Check PyPI page: https://pypi.org/project/revenium_metering/
- [ ] Verify version shows as 6.6.0
- [ ] Verify README renders correctly (badge should display)
- [ ] Test installation: `pip install revenium-metering==6.6.0`

### 6. Tag Release
```bash
git tag -a v6.6.0 -m "Release v6.6.0 - Add trace visualization fields"
git push origin v6.6.0
```

### 7. Create GitHub Release
- Go to: https://github.com/revenium/revenium-metering-python/releases/new
- Tag: v6.6.0
- Title: "v6.6.0 - Trace Visualization & Observability"
- Description: Copy from CHANGELOG.md

---

## ✅ Final Checklist

### Before Publishing
- [x] Version bumped to 6.6.0
- [x] CHANGELOG updated
- [x] README fixed and tested
- [x] All new fields documented
- [x] Backwards compatibility verified
- [ ] Documentation PR merged
- [ ] Distribution built
- [ ] Installation tested

### After Publishing
- [ ] PyPI page verified
- [ ] Version 6.6.0 visible
- [ ] README renders correctly
- [ ] Badge displays properly
- [ ] Git tag created
- [ ] GitHub release created

---

## 🎯 Success Criteria

✅ **All criteria met:**
1. Version 6.6.0 in pyproject.toml
2. CHANGELOG.md updated with complete feature list
3. README.md fixed (badge + httpx import)
4. All new fields are optional
5. Zero breaking changes
6. Backwards compatibility verified
7. Documentation complete

---

## 🔒 Risk Assessment

**Risk Level:** LOW ✅

**Rationale:**
- All changes are additive (new optional fields)
- No modifications to existing required fields
- No dependency changes
- Extensive backwards compatibility testing
- All middleware packages verified compatible

**Confidence:** HIGH ✅

---

## 📊 Summary

**Status:** ✅ READY FOR RELEASE

**Version:** 6.6.0  
**Type:** Minor (backwards compatible feature addition)  
**Breaking Changes:** None  
**New Features:** 9 optional tracing/observability fields  
**Documentation:** Fixed and improved  
**Risk:** Low  

**Recommendation:** PROCEED WITH PUBLICATION TO PYPI

