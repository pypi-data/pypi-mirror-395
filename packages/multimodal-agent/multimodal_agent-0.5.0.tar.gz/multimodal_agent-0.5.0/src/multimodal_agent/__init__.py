import os

from .core.agent_core import MultiModalAgent
from .rag.rag_store import SQLiteRAGStore

# Version handling
PACKAGE_ROOT = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(PACKAGE_ROOT, "..", ".."))
VERSION_PATH = os.path.join(PROJECT_ROOT, "VERSION")

try:
    with open(VERSION_PATH, "r") as f:
        __version__ = f.read().strip()
except FileNotFoundError:
    __version__ = "0.0.0"


# Lazy imports to avoid circular dependencies
def __getattr__(name):
    """
    Lazily expose MultiModalAgent and SQLiteRAGStore
    to avoid circular imports during CLI initialization.
    """
    if name == "MultiModalAgent":
        return MultiModalAgent

    if name == "SQLiteRAGStore":
        return SQLiteRAGStore

    raise AttributeError(name)


__all__ = [
    "MultiModalAgent",
    "SQLiteRAGStore",
    "__version__",
]
