# HACS Requirements Checklist

Based on [HACS Publisher Documentation](https://www.hacs.xyz/docs/publish/integration/), this document tracks the requirements for publishing the MinderGas integration to HACS.

## ✅ Completed Requirements

### Repository Structure
- ✅ Single integration per repository
- ✅ All files located in `custom_components/mindergas/`
- ✅ Proper folder structure with all components

### manifest.json
- ✅ `manifest_version`: 2 (updated to latest)
- ✅ `domain`: "mindergas"
- ✅ `name`: "MinderGas"
- ✅ `codeowners`: ["@pietervanharen"]
- ✅ `documentation`: GitHub repository link
- ✅ `issue_tracker`: GitHub issues link
- ✅ `version`: 1.0.0
- ✅ `homeassistant`: 2024.1.0+
- ✅ `requirements`: aiohttp>=3.8.0
- ✅ `config_flow`: true

### hacs.json
- ✅ Proper manifest with all required fields
- ✅ `issue_tracker` field added
- ✅ `render_readme`: true
- ✅ Consistent with manifest.json requirements

### Code Quality
- ✅ Python files validated (no syntax errors)
- ✅ JSON files validated
- ✅ Proper error handling
- ✅ Async/await patterns used correctly
- ✅ Home Assistant best practices followed
- ✅ Type hints and docstrings present

### Documentation
- ✅ README.md with setup instructions
- ✅ DOCKER_SETUP.md for development
- ✅ TESTING.md with comprehensive test scenarios
- ✅ METER_RESTRICTIONS.md for feature documentation
- ✅ ARCHITECTURE.md with technical details
- ✅ CONTRIBUTING.md for developers
- ✅ LICENSE (MIT)

### Translations
- ✅ English (en.json) translations
- ✅ Dutch (nl.json) translations
- ✅ Bilingual config_flow support
- ✅ Error messages in both languages

### GitHub Integration
- ✅ GitHub Actions for validation (.github/workflows/validate.yml)
- ✅ .gitignore for sensitive files
- ✅ CODE_OF_CONDUCT.md
- ✅ CONTRIBUTING.md

## 🔄 To-Do Before Publishing to HACS

### 1. Home Assistant Brands Registration (REQUIRED)
**Status:** ✅ PREPARED (Ready to submit)

The integration needs to be registered in the [home-assistant/brands](https://github.com/home-assistant/brands) repository.

**Status**: Files prepared in `.brands/custom_integrations/mindergas/`:
- ✅ `icon.svg` - Custom MinderGas icon (green meter theme)
- ✅ `manifest.json` - Integration metadata

**Steps to Complete**:
1. Fork https://github.com/home-assistant/brands
2. Create branch: `add-mindergas-integration`
3. Copy files from `.brands/custom_integrations/mindergas/` to your fork
4. Push branch and create Pull Request
5. Wait for maintainer review and merge

**Detailed Guide**: See [BRANDS_REGISTRATION.md](BRANDS_REGISTRATION.md)

### 2. GitHub Releases (PREFERRED)
**Status:** ⚠️ NOT IMPLEMENTED

HACS prefers repositories with GitHub releases for better version distribution.

**Steps:**
1. Tag releases with semantic versioning (e.g., `v1.0.0`)
2. Create GitHub releases with changelog
3. HACS will automatically detect and present them

**Recommended Workflow:**
- Create release when incrementing version in manifest.json
- Include changelog and breaking changes
- HACS shows 5 latest releases to users

### 3. Repository Configuration
**Status:** ✅ READY

Ensure repository settings:
- ✅ Public repository
- ✅ GitHub issues enabled
- ✅ License specified (MIT)
- ✅ README with installation instructions

## 📋 Pre-Publication Checklist

Before submitting to HACS:

- [x] Devcontainer setup created (.devcontainer/)
- [x] Brands files prepared (.brands/custom_integrations/mindergas/)
- [ ] **[NEXT]** Fork home-assistant/brands repository
- [ ] **[NEXT]** Create PR with brands files
- [ ] **[NEXT]** Wait for brands PR to be merged
- [ ] Test integration in Home Assistant 2024.1.0+
- [ ] Verify all 5 sensors are created correctly
- [ ] Test time window restrictions (00:05-01:00)
- [ ] Test random time feature
- [ ] Verify Dutch language support
- [ ] Test Docker setup (./quick_start.sh)
- [ ] Run all tests from TESTING.md
- [ ] Verify error handling and logging
- [ ] Check integration appears in HACS search

## 🚀 Publishing to HACS

Once all requirements are met:

1. **GitHub Repository Settings:**
   - Ensure public repository
   - Add descriptive repository description
   - Add relevant topics: `home-assistant`, `hacs`, `integration`, `mindergas`

2. **HACS Configuration:**
   - Verify repository can be found at: https://github.com/pietervanharen/mindergas-hass
   - HACS will automatically detect and add the integration

3. **HACS Options:**
   - The integration is automatically discoverable once home-assistant/brands PR is merged
   - No additional steps needed after brands registration

## 📚 Reference Documentation

- [DEVCONTAINER.md](DEVCONTAINER.md) - VS Code devcontainer setup for development
- [BRANDS_REGISTRATION.md](BRANDS_REGISTRATION.md) - Step-by-step brands PR guide
- [HACS Publisher Docs - Integrations](https://www.hacs.xyz/docs/publish/integration/)
- [Home Assistant Developer Docs - Creating Integration Manifest](https://developers.home-assistant.io/docs/creating_integration_manifest)
- [Home Assistant Brands Repository](https://github.com/home-assistant/brands)
- [HACS Discord Server](https://discord.gg/apgchf8)

## 📝 Notes

- Integration structure and code quality meet HACS standards
- All manifest.json requirements are met
- hacs.json is properly configured
- Documentation is comprehensive
- Tests are provided and ready
- Docker setup enables easy development and testing
- Home Assistant Brands registration is the main blocker for HACS publication

## 🔗 Related Resources

- Integration Repository: https://github.com/pietervanharen/mindergas-hass
- MinderGas API: https://www.mindergas.nl/api
- Home Assistant: https://www.home-assistant.io/
- HACS: https://hacs.xyz/
