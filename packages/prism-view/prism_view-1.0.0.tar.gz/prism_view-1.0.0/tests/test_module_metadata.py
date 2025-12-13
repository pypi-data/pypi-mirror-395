"""
Tests for prism-view module metadata.

Verifies __version__, __icon__, and __requires__ are properly defined.
"""

import re


def test_version_is_defined():
    """__version__ should be defined."""
    from prism.view import __version__

    assert __version__ is not None
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_version_follows_semver():
    """__version__ should follow semantic versioning (X.Y.Z)."""
    from prism.view import __version__

    # SemVer pattern: MAJOR.MINOR.PATCH with optional pre-release
    semver_pattern = r"^\d+\.\d+\.\d+(-[a-zA-Z0-9.]+)?$"
    assert re.match(semver_pattern, __version__), (
        f"Version '{__version__}' does not follow SemVer format"
    )


def test_icon_is_defined():
    """__icon__ should be defined as the eye emoji."""
    from prism.view import __icon__

    assert __icon__ is not None
    assert isinstance(__icon__, str)
    assert __icon__ == "👁️"


def test_requires_is_defined():
    """__requires__ should list dependencies on other Prism libraries."""
    from prism.view import __requires__

    assert __requires__ is not None
    assert isinstance(__requires__, list)


def test_requires_includes_prism_config():
    """__requires__ should include prism-config as a dependency."""
    from prism.view import __requires__

    assert "prism-config" in __requires__


def test_module_docstring_exists():
    """Module should have a docstring."""
    import prism.view

    assert prism.view.__doc__ is not None
    assert len(prism.view.__doc__) > 0
    assert "Prism View" in prism.view.__doc__


def test_all_exports_defined():
    """__all__ should be defined and contain metadata exports."""
    from prism.view import __all__

    assert "__version__" in __all__
    assert "__icon__" in __all__
    assert "__requires__" in __all__
