"""
Tests for Dockerfile and container build configuration.
"""
from pathlib import Path


def test_dockerfile_exists():
    """Test that Dockerfile exists."""
    dockerfile = Path(__file__).parent.parent / "Dockerfile"
    assert dockerfile.exists(), "Dockerfile not found"


def test_dockerfile_has_required_instructions():
    """Test that Dockerfile contains required instructions."""
    dockerfile = Path(__file__).parent.parent / "Dockerfile"
    content = dockerfile.read_text()
    
    # Check for essential Dockerfile instructions
    assert "FROM" in content, "Dockerfile missing FROM instruction"
    assert "WORKDIR" in content, "Dockerfile missing WORKDIR instruction"
    assert "COPY" in content, "Dockerfile missing COPY instruction"
    
    # Check that it's based on Python
    assert "python" in content.lower(), "Dockerfile should be based on Python image"


def test_dockerfile_uses_correct_python_version():
    """Test that Dockerfile uses Python 3.10 as specified."""
    dockerfile = Path(__file__).parent.parent / "Dockerfile"
    content = dockerfile.read_text()
    
    # Check for Python 3.10
    assert "python:3.10" in content.lower(), "Dockerfile should use Python 3.10"


def test_dockerignore_exists():
    """Test that .dockerignore file exists."""
    dockerignore = Path(__file__).parent.parent / ".dockerignore"
    assert dockerignore.exists(), "'.dockerignore' file not found"


def test_dockerignore_excludes_common_files():
    """Test that .dockerignore excludes common unnecessary files."""
    dockerignore = Path(__file__).parent.parent / ".dockerignore"
    content = dockerignore.read_text()
    
    # Common patterns that should be excluded
    recommended_patterns = [".git", "__pycache__", "*.pyc"]
    
    for pattern in recommended_patterns:
        assert pattern in content, f".dockerignore should exclude {pattern}"
