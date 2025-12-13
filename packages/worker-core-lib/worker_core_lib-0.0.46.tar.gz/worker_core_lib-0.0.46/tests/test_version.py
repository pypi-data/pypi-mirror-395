"""
Tests for version extraction and validation.
"""
import re
from pathlib import Path


def test_version_in_pyproject_toml():
    """Test that version is properly defined in pyproject.toml."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    assert pyproject_path.exists(), "pyproject.toml not found"
    
    content = pyproject_path.read_text()
    
    # Check that version is defined
    version_match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    assert version_match is not None, "Version not found in pyproject.toml"
    
    version = version_match.group(1)
    
    # Validate version format (should be semantic versioning)
    version_pattern = r'^\d+\.\d+\.\d+$'
    assert re.match(version_pattern, version), f"Version {version} does not match semantic versioning pattern"


def test_version_consistency():
    """Test that version format is valid for Docker tagging."""
    pyproject_path = Path(__file__).parent.parent / "pyproject.toml"
    content = pyproject_path.read_text()
    
    version_match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
    version = version_match.group(1)
    
    # Version should not contain characters that are invalid for Docker tags
    # Docker tags allow: lowercase and uppercase letters, digits, underscores, periods, and hyphens
    # But version should follow semver
    assert not any(c in version for c in [' ', '/', '\\', ':', '@']), \
        f"Version {version} contains invalid characters for Docker tags"
