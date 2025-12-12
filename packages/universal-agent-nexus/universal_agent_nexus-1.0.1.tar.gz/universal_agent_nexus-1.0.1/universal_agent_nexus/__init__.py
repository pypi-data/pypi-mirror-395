"""Universal Agent Nexus package."""

__version__ = "1.0.0"

__all__ = [
    "__version__",
    "load_manifest",
    "load_manifest_str",
]


def load_manifest(path):
    """Load a manifest from a YAML file path."""
    from .manifest import load_manifest as _load_manifest
    return _load_manifest(path)


def load_manifest_str(yaml_content):
    """Load a manifest from a YAML string."""
    from .manifest import load_manifest_str as _load_manifest_str
    return _load_manifest_str(yaml_content)


# Import adapters lazily to avoid import errors when deps not installed
try:
    from . import adapters
except ImportError:
    pass

try:
    from . import observability
except ImportError:
    pass

try:
    from . import cli
except ImportError:
    pass
