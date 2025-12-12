#!/usr/bin/env python3
"""
Generate SVG assets for the ytdl project.

This script creates:
- Social preview SVG for GitHub repository

Version is automatically read from setuptools_scm or git tags.
"""

import os
import subprocess
from pathlib import Path
from typing import Optional


def get_version() -> str:
    """Get the current version from git tags or setuptools_scm."""
    try:
        # Try setuptools_scm first
        from setuptools_scm import get_version as scm_version
        version = scm_version(root='..', relative_to=__file__)
        # Clean up dev versions for display
        if '+' in version:
            version = version.split('+')[0]
        if '.dev' in version:
            version = version.split('.dev')[0]
        return version
    except Exception:
        pass

    try:
        # Fallback to git tags
        result = subprocess.run(
            ['git', 'describe', '--tags', '--abbrev=0'],
            capture_output=True,
            text=True,
            check=True
        )
        version = result.stdout.strip()
        # Remove 'v' prefix if present
        return version.lstrip('v')
    except Exception:
        pass

    # Ultimate fallback
    return "1.0.0"


def generate_social_preview_svg(version: str, output_path: Path) -> None:
    """Generate the static social preview SVG for GitHub."""

    svg_content = f'''<svg viewBox="0 0 1280 640" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="1280" height="640" fill="#0a0a0a"/>

  <!-- Title -->
  <text x="640" y="220" font-size="100" font-weight="700" text-anchor="middle" fill="#FFD700" font-family="system-ui, -apple-system, sans-serif">
    ytdl
  </text>

  <!-- Subtitle -->
  <text x="640" y="270" font-size="28" text-anchor="middle" fill="#888" font-family="system-ui, sans-serif">
    Interactive YouTube Downloader
  </text>

  <!-- Features -->
  <g transform="translate(440, 340)">
    <text x="0" y="0" font-size="18" fill="#AAA" font-family="system-ui, sans-serif">
      ⚡ Interactive menu system
    </text>
    <text x="0" y="40" font-size="18" fill="#AAA" font-family="system-ui, sans-serif">
      🎯 Smart playlist detection
    </text>
    <text x="0" y="80" font-size="18" fill="#AAA" font-family="system-ui, sans-serif">
      🎵 HD audio extraction
    </text>
  </g>

  <!-- Install command -->
  <text x="640" y="520" font-size="20" text-anchor="middle" fill="#666" font-family="Monaco, 'Courier New', monospace">
    $ pip install ytdl-interactive
  </text>

  <!-- Version badge -->
  <text x="640" y="580" font-size="16" text-anchor="middle" fill="#555" font-family="system-ui, sans-serif">
    v{version}
  </text>
</svg>'''

    output_path.write_text(svg_content)
    print(f"✓ Generated social-preview.svg (version: {version})")


def main():
    """Main entry point."""
    # Get version
    version = get_version()
    print(f"\n🎨 Generating SVG asset for version {version}\n")

    # Get project root and assets directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    assets_dir = project_root / 'assets'
    assets_dir.mkdir(exist_ok=True)

    # Generate social preview SVG
    generate_social_preview_svg(version, assets_dir / 'social-preview.svg')

    print(f"\n✨ Done! Asset generated in {assets_dir}\n")


if __name__ == '__main__':
    main()
