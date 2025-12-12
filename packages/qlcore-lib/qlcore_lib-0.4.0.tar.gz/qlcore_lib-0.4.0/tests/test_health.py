from qlcore.health import check_health, HealthChecker
from qlcore.config import reset_config
from qlcore.bootstrap import init_qlcore
from qlcore import __version__


def _init_testing_config():
    """Helper: initialise a minimal testing config for health checks."""
    reset_config()
    # Use testing environment; skip health checks inside init to avoid recursion
    cfg = init_qlcore("testing", run_health_checks=False)
    return cfg


def test_health_check():
    """Test health check system."""
    _init_testing_config()

    health = check_health()

    assert health.is_healthy
    assert health.version == __version__
    assert len(health.components) >= 4

    component_names = {c.name for c in health.components}
    assert "decimal_context" in component_names
    assert "imports" in component_names
    assert "configuration" in component_names
    assert "python_version" in component_names


def test_health_checker_decimal_context():
    """Test decimal context check."""
    _init_testing_config()

    checker = HealthChecker()
    component = checker.check_decimal_context()

    assert component.name == "decimal_context"
    assert component.is_healthy
    assert "precision" in component.details


def test_health_checker_imports():
    """Test imports check."""
    _init_testing_config()

    checker = HealthChecker()
    component = checker.check_imports()

    assert component.name == "imports"
    assert component.is_healthy


def test_health_checker_configuration():
    """Test configuration check."""
    _init_testing_config()

    checker = HealthChecker()
    component = checker.check_configuration()

    assert component.name == "configuration"
    assert component.is_healthy


def test_health_to_dict():
    """Test health status serialization."""
    _init_testing_config()

    health = check_health()
    data = health.to_dict()

    assert "healthy" in data
    assert "version" in data
    assert "components" in data
    assert len(data["components"]) > 0
