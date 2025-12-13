"""
Tests for CI/CD workflow configuration.
"""
import yaml
from pathlib import Path


def test_docker_publish_workflow_exists():
    """Test that the docker-publish workflow exists."""
    workflow_path = Path(__file__).parent.parent / ".github" / "workflows" / "docker-publish.yml"
    assert workflow_path.exists(), "docker-publish.yml workflow not found"


def test_docker_publish_workflow_valid_yaml():
    """Test that the docker-publish workflow is valid YAML."""
    workflow_path = Path(__file__).parent.parent / ".github" / "workflows" / "docker-publish.yml"
    
    with open(workflow_path) as f:
        try:
            config = yaml.safe_load(f)
            assert config is not None, "Workflow file is empty"
        except yaml.YAMLError as e:
            raise AssertionError(f"Invalid YAML in docker-publish.yml: {e}")


def test_docker_publish_workflow_has_required_triggers():
    """Test that the workflow triggers on required branches."""
    workflow_path = Path(__file__).parent.parent / ".github" / "workflows" / "docker-publish.yml"
    
    with open(workflow_path) as f:
        config = yaml.safe_load(f)
    
    # Check push triggers (YAML parses 'on' as True/boolean)
    # This is a known PyYAML issue with reserved words
    triggers = config.get("on") or config.get(True)
    assert triggers is not None, "Workflow missing triggers section"
    assert "push" in triggers, "Workflow missing push trigger"
    
    push_branches = triggers["push"]["branches"]
    assert "master" in push_branches or "main" in push_branches, \
        "Workflow should trigger on master or main branch"
    assert "develop" in push_branches, \
        "Workflow should trigger on develop branch"


def test_docker_publish_workflow_has_build_job():
    """Test that the workflow has a build job."""
    workflow_path = Path(__file__).parent.parent / ".github" / "workflows" / "docker-publish.yml"
    
    with open(workflow_path) as f:
        config = yaml.safe_load(f)
    
    assert "jobs" in config, "Workflow missing jobs section"
    jobs = config["jobs"]
    
    # Should have at least one job
    assert len(jobs) > 0, "Workflow has no jobs defined"
    
    # Common job names for build/test
    job_names = list(jobs.keys())
    assert any("build" in name.lower() or "test" in name.lower() for name in job_names), \
        "Workflow should have a build or test job"


def test_docker_publish_workflow_runs_tests():
    """Test that the workflow runs tests."""
    workflow_path = Path(__file__).parent.parent / ".github" / "workflows" / "docker-publish.yml"
    
    content = workflow_path.read_text()
    
    # Should mention pytest somewhere
    assert "pytest" in content.lower(), "Workflow should run pytest"


def test_docker_publish_workflow_builds_docker_image():
    """Test that the workflow builds Docker images."""
    workflow_path = Path(__file__).parent.parent / ".github" / "workflows" / "docker-publish.yml"
    
    content = workflow_path.read_text()
    
    # Should use docker build actions
    assert "docker/build-push-action" in content or "docker build" in content, \
        "Workflow should build Docker images"


def test_docker_publish_workflow_pushes_to_ghcr():
    """Test that the workflow pushes to GitHub Container Registry."""
    workflow_path = Path(__file__).parent.parent / ".github" / "workflows" / "docker-publish.yml"
    
    content = workflow_path.read_text()
    
    # Should reference ghcr.io
    assert "ghcr.io" in content, "Workflow should push to ghcr.io"


def test_docker_publish_workflow_has_permissions():
    """Test that the workflow has appropriate permissions."""
    workflow_path = Path(__file__).parent.parent / ".github" / "workflows" / "docker-publish.yml"
    
    with open(workflow_path) as f:
        config = yaml.safe_load(f)
    
    jobs = config.get("jobs", {})
    
    # At least one job should have permissions
    has_permissions = False
    for job_name, job_config in jobs.items():
        if "permissions" in job_config:
            permissions = job_config["permissions"]
            # Should have packages write permission for GHCR
            if permissions.get("packages") == "write":
                has_permissions = True
                break
    
    assert has_permissions, "Workflow should have packages:write permission"
