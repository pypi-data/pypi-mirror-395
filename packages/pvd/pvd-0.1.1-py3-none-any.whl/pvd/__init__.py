"""Paved unified SDK and CLI (remote‑only).

Import surface:

    from pvd import Agent, PolicyDeniedError, tool
    from pvd import PolicyEnforcer
    from pvd.decorators import guard_tool
"""

from .sdk import Agent, tool, PolicyDeniedError  # noqa: F401
from .enforcer import PolicyEnforcer  # noqa: F401
from .decorators import guard_tool  # noqa: F401

__version__ = "0.1.0"
version = __version__

__all__ = [
    "Agent",
    "tool",
    "PolicyDeniedError",
    "PolicyEnforcer",
    "guard_tool",
    "__version__",
    "version",
]

