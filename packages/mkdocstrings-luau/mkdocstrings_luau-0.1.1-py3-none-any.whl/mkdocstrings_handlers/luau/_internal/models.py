# Data models for Luau objects.

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class LuauParameter:
    """Represents a parameter in a Luau function."""

    name: str
    """The parameter name."""
    type: str | None = None
    """The parameter type annotation."""
    default: str | None = None
    """The default value."""


@dataclass
class LuauFunction:
    """Represents a Luau function."""

    name: str
    """The function name."""
    path: str
    """The fully qualified path."""
    parameters: list[LuauParameter] = field(default_factory=list)
    """The function parameters."""
    return_type: str | None = None
    """The return type annotation."""
    docstring: str = ""
    """The function documentation."""
    lineno: int = 0
    """The line number where the function is defined."""
    signature: str = ""
    """The function signature."""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "path": self.path,
            "parameters": [{"name": p.name, "type": p.type, "default": p.default} for p in self.parameters],
            "return_type": self.return_type,
            "docstring": self.docstring,
            "lineno": self.lineno,
            "signature": self.signature,
        }


@dataclass
class LuauModule:
    """Represents a Luau module."""

    name: str
    """The module name."""
    path: str
    """The fully qualified path."""
    functions: list[LuauFunction] = field(default_factory=list)
    """Functions defined in the module."""
    docstring: str = ""
    """The module documentation."""
    filepath: str | None = None
    """The file path."""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "path": self.path,
            "functions": [f.to_dict() for f in self.functions],
            "docstring": self.docstring,
            "filepath": self.filepath,
        }
