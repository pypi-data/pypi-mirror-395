# Scripts

This directory contains utility scripts for the ytdl project.

## generate_assets.py

Programmatically generates SVG asset with the current version embedded.

### Features

- **Dynamic version detection**: Automatically reads version from:
  1. `setuptools_scm` (preferred)
  2. Git tags (fallback)
  3. Hardcoded default (last resort)

- **Generates social preview SVG**:
  - `assets/social-preview.svg` - Static social preview for GitHub (1280x640)

- **Premium design**: Solid gold/black theme with:
  - Clean typography with system fonts
  - Guaranteed rendering across platforms
  - Version badge dynamically embedded

### Usage

```bash
# Run manually
python3 scripts/generate_assets.py

# Automatic during release
# The bump-version workflow runs this automatically
```

### Output

```
🎨 Generating SVG asset for version 1.2.3

✓ Generated social-preview.svg (version: 1.2.3)

✨ Done! Asset generated in /path/to/assets
```

### Integration

The asset is automatically regenerated during the release process:

1. **Bump Version workflow** triggers
2. New version tag is created
3. `generate_assets.py` runs with new version
4. Asset is committed and pushed
5. GitHub release is created

This ensures the version badge always matches the actual release version.

### Design Specifications

#### Social Preview (`social-preview.svg`)

- **Dimensions**: 1280x640px (GitHub's standard)
- **Static image** (no animations for compatibility)
- **Includes**:
  - Large title in solid gold (#FFD700)
  - Subtitle describing the project
  - 3 feature bullets
  - Install command
  - Version badge (dynamically embedded)
- **Colors**:
  - Background: Black (#0a0a0a)
  - Title: Solid gold (#FFD700)
  - Text: Gray shades (#888, #AAA, #666, #555)

### Why Programmatic Generation?

1. **Version sync**: Asset always shows correct version
2. **Consistency**: Generated from single source of truth
3. **Maintainability**: Change design in one place
4. **Automation**: No manual updates needed
5. **Validation**: Code ensures valid SVG syntax

### Development

To modify the design:

1. Edit `generate_assets.py`
2. Run the script to preview
3. Open SVG in browser to test
4. Commit changes

The workflow will use the updated design for future releases.
