# Home Assistant Brands Registration Guide

This guide walks you through the process of registering the MinderGas integration with the Home Assistant Brands repository, a required step for HACS publication.

## What is Home Assistant Brands?

The [home-assistant/brands](https://github.com/home-assistant/brands) repository is the official registry for Home Assistant integration branding:
- Icons and logos for UI display
- Integration metadata
- Author information
- Documentation links

This is **required** for HACS to recognize and properly display your integration.

## Prerequisites

1. **GitHub Account** - Already have one ✅
2. **Git** - For fork and pull request
3. **SVG Icon** - Provided in `.brands/custom_integrations/mindergas/icon.svg`
4. **Manifest** - Provided in `.brands/custom_integrations/mindergas/manifest.json`

## Step-by-Step Guide

### Step 1: Fork the Brands Repository

1. Go to https://github.com/home-assistant/brands
2. Click **Fork** (top-right corner)
3. Select your account as destination
4. Wait for fork to complete

### Step 2: Clone Your Fork Locally

```bash
# Clone your forked repository
git clone https://github.com/YOUR_USERNAME/brands.git
cd brands

# Add upstream remote (for keeping in sync)
git remote add upstream https://github.com/home-assistant/brands.git
```

### Step 3: Create a New Branch

```bash
# Create feature branch
git checkout -b add-mindergas-integration

# Keep your main branch clean
```

### Step 4: Copy Integration Files

In your cloned brands repository, create the directory structure:

```bash
mkdir -p custom_integrations/mindergas
```

Copy from this project:
- `.brands/custom_integrations/mindergas/icon.svg` → `custom_integrations/mindergas/icon.svg`
- `.brands/custom_integrations/mindergas/manifest.json` → `custom_integrations/mindergas/manifest.json`

Or manually create them:

#### manifest.json

```json
{
  "codeowners": ["@pietervanharen"],
  "documentation": "https://github.com/pietervanharen/mindergas-hass",
  "issues": "https://github.com/pietervanharen/mindergas-hass/issues"
}
```

#### icon.svg

Use the SVG file from `.brands/custom_integrations/mindergas/icon.svg` in this project.

### Step 5: Validate Your Changes

Home Assistant Brands has validation checks. Ensure:

```bash
# Check file exists and is valid SVG
file custom_integrations/mindergas/icon.svg
# Should output: SVG Scalable Vector Graphics image

# Validate JSON
python -m json.tool custom_integrations/mindergas/manifest.json > /dev/null && echo "✓ Valid JSON"
```

### Step 6: Commit Your Changes

```bash
# Stage files
git add custom_integrations/mindergas/

# Commit with descriptive message
git commit -m "Add MinderGas integration branding

- Integration: MinderGas
- Domain: mindergas
- Icon: Custom SVG design
- Author: @pietervanharen
- Repository: https://github.com/pietervanharen/mindergas-hass"
```

### Step 7: Push to Your Fork

```bash
# Push feature branch
git push origin add-mindergas-integration
```

### Step 8: Create Pull Request

1. Go to https://github.com/home-assistant/brands
2. Click **Pull requests** tab
3. Click **New Pull Request**
4. Click **compare across forks**
5. Select:
   - Base: `home-assistant/brands` (main)
   - Compare: `YOUR_USERNAME/brands` (add-mindergas-integration)
6. Click **Create Pull Request**

#### PR Title
```
Add MinderGas integration
```

#### PR Description
```markdown
## Integration Details

- **Name**: MinderGas
- **Domain**: mindergas
- **Repository**: https://github.com/pietervanharen/mindergas-hass
- **Description**: Monitor and report gas usage with MinderGas API

## Type of Change

- [ ] New integration branding
- [ ] Update existing integration
- [ ] Fix/improvement

## Validation

- [x] SVG icon is valid
- [x] Icon dimensions are appropriate
- [x] manifest.json is valid JSON
- [x] All required fields present
- [x] Links are correct

## Related Links

- Integration Repository: https://github.com/pietervanharen/mindergas-hass
- Issue Tracker: https://github.com/pietervanharen/mindergas-hass/issues
```

### Step 9: Wait for Review & Merge

1. **CI/CD Checks**: Automated validation will run
   - SVG format validation
   - JSON schema validation
   - File structure verification

2. **Maintainer Review**: Home Assistant maintainers review the PR
   - Usually 24-48 hours
   - May request icon improvements
   - May ask for metadata clarifications

3. **Approval & Merge**: Once approved, your PR will be merged
   - HACS will immediately recognize your integration
   - Your icon appears in Home Assistant UI

## Icon Guidelines

The SVG icon should:

### Size & Format
- ✅ Valid SVG format
- ✅ Square aspect ratio (192x192px or 256x256px recommended)
- ✅ Include `viewBox` attribute
- ✅ Self-contained (no external resources)

### Design
- ✅ Clear at small sizes (24px)
- ✅ Professional appearance
- ✅ Related to integration purpose (gas/meter/measurement)
- ✅ Avoid overly complex designs
- ✅ Color contrast for readability

### Current Icon
The provided icon:
- Shows a gas flame/arrow pointing down (usage reduction theme)
- Includes a meter gauge circle
- Uses green (#2ecc71) for positive/eco theme
- Dark green (#1a472a) for contrast

### If You Want to Improve

You can modify `.brands/custom_integrations/mindergas/icon.svg`:

1. Open in Illustrator, Figma, or text editor
2. Adjust colors, shapes, or text
3. Test at different sizes
4. Validate it's still valid SVG
5. Update your PR if needed

## Troubleshooting

### PR Fails Validation

**Issue**: SVG validation fails
- **Solution**: Ensure file is valid SVG, check syntax in XML

**Issue**: JSON validation fails
- **Solution**: Validate with `python -m json.tool manifest.json`

**Issue**: File structure incorrect
- **Solution**: Ensure path is `custom_integrations/mindergas/`

### Icon Not Showing

**Issue**: Icon not visible after merge
- **Solution**: HACS cache refreshes every few hours
- **Workaround**: Manually add integration with custom repository URL

### PR Takes Too Long

**Issue**: No feedback for weeks
- **Solution**: 
  - Comment on PR asking for status
  - Check if requirements are met
  - Contact Home Assistant Discord for help

## After Approval

Once merged into home-assistant/brands:

1. ✅ Your integration appears in HACS
2. ✅ Icon displays in Home Assistant UI
3. ✅ Integration is discoverable to users
4. ✅ Users can install directly from HACS

## Publishing to HACS

After your brands PR is merged:

1. **HACS Auto-Detection** (usually within 24 hours)
   - HACS crawler discovers your GitHub repository
   - Your integration becomes available

2. **Manual HACS Submission** (if needed)
   - Visit https://hacs.xyz/docs/publish/start/
   - Follow submission instructions
   - HACS will validate and add your repository

3. **User Installation**
   - Users go to HACS → Integrations
   - Search "MinderGas"
   - Install your integration

## Integration Checklist

Before submitting your brands PR, ensure:

- [x] Repository is public
- [x] manifest.json exists in `custom_components/mindergas/`
- [x] All manifest required fields present
- [x] Documentation URL is correct
- [x] Issues URL is correct
- [x] License is specified (MIT)
- [x] Code follows Home Assistant standards
- [x] README.md is present and complete
- [x] GitHub Actions validation passes
- [x] No hardcoded credentials

## Quick Links

- **Brands Repository**: https://github.com/home-assistant/brands
- **Integration Repository**: https://github.com/pietervanharen/mindergas-hass
- **HACS Documentation**: https://hacs.xyz/
- **HA Developer Docs**: https://developers.home-assistant.io/
- **PR Template**: Use the example above

## Need Help?

1. **Check Existing PRs**: Search brands repo for similar integrations
2. **HA Community**: https://community.home-assistant.io/
3. **HA Discord**: https://discord.gg/home-assistant
4. **HACS Discord**: https://discord.gg/apgchf8
5. **GitHub Issues**: On this repository

## Related Documentation

- [HACS_REQUIREMENTS.md](HACS_REQUIREMENTS.md) - Overall HACS requirements
- [CONTRIBUTING.md](CONTRIBUTING.md) - Developer guidelines
- [DOCKER_SETUP.md](DOCKER_SETUP.md) - Docker setup for testing
- [README.md](README.md) - Integration overview
