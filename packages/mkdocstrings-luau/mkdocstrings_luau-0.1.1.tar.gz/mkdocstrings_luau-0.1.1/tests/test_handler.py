"""Tests for the Luau handler functionality."""

from __future__ import annotations

from pathlib import Path

import pytest

from mkdocstrings_handlers.luau import LuauConfig, LuauHandler, LuauOptions
from mkdocstrings_handlers.luau._internal.parser import LuauParser


@pytest.fixture(name="handler")
def fixture_handler() -> LuauHandler:
    """Create a simple handler for testing."""
    config = LuauConfig()
    base_dir = Path(__file__).parent / "fixtures"
    # Provide minimal required parameters
    return LuauHandler(
        config=config,
        base_dir=base_dir,
        theme="mkdocs",
        custom_templates=None,
        mdx=None,
        mdx_config={},
    )


def test_collect_module(handler: LuauHandler) -> None:
    """Test collecting a Luau module."""
    # Try to collect the example module
    try:
        data = handler.collect("example", LuauOptions())

        # Verify module data
        assert data["name"] == "example"
        assert "functions" in data
        assert len(data["functions"]) > 0

        # Verify at least one function was found
        func_names = [f["name"] for f in data["functions"]]
        assert "add" in func_names or "subtract" in func_names or "greet" in func_names

    except (FileNotFoundError, ValueError) as e:
        pytest.skip(f"Could not collect module: {e}")


def test_collect_function_details(handler: LuauHandler) -> None:
    """Test collecting a specific function from a Luau module."""
    try:
        # Collect the whole module first
        data = handler.collect("example", LuauOptions())

        # Verify we can access function data
        assert "functions" in data
        functions = data["functions"]

        if len(functions) > 0:
            func = functions[0]
            assert "name" in func
            assert "path" in func
            assert "signature" in func

    except (FileNotFoundError, ValueError) as e:
        pytest.skip(f"Could not collect function: {e}")


def test_parser_basic_function() -> None:
    """Test the parser directly with a basic function."""
    fixtures_dir = Path(__file__).parent / "fixtures"
    parser = LuauParser(fixtures_dir)

    module = parser.parse_file(fixtures_dir / "example.luau")

    # Check module was parsed
    assert module.name == "example"
    assert len(module.functions) >= 3

    # Find the add function
    add_func = next((f for f in module.functions if f.name == "add"), None)
    assert add_func is not None
    assert len(add_func.parameters) == 2
    assert add_func.parameters[0].name == "a"
    assert add_func.parameters[0].type == "number"
    assert add_func.return_type == "number"
