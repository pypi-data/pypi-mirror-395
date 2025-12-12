# Parser for Luau source code.

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from mkdocstrings_handlers.luau._internal.models import LuauFunction, LuauModule, LuauParameter


class LuauParser:
    """Parser for Luau source code."""

    # Patterns for parsing Luau
    _FUNCTION_PATTERN = re.compile(
        r"^\s*(?:local\s+)?function\s+([a-zA-Z_][a-zA-Z0-9_\.]*)\s*\((.*?)\)",
        re.MULTILINE,
    )
    _COMMENT_PATTERN = re.compile(r"^\s*--\s*(.*?)$", re.MULTILINE)
    _TYPE_ANNOTATION_PATTERN = re.compile(r":\s*([a-zA-Z_][a-zA-Z0-9_<>|,\s]*)")
    _RETURN_TYPE_PATTERN = re.compile(r"\)\s*:\s*([a-zA-Z_][a-zA-Z0-9_<>|,\s]*)")

    def __init__(self, base_dir: Path) -> None:
        """Initialize the parser.

        Parameters:
            base_dir: The base directory for resolving paths.
        """
        self._base_dir = base_dir

    def parse_file(self, filepath: Path) -> LuauModule:
        """Parse a Luau file.

        Parameters:
            filepath: Path to the Luau file.

        Returns:
            A LuauModule containing the parsed data.
        """
        if not filepath.exists():
            msg = f"File not found: {filepath}"
            raise FileNotFoundError(msg)

        content = filepath.read_text(encoding="utf-8")
        module_name = filepath.stem
        module_path = (
            str(filepath.relative_to(self._base_dir))
            .replace("/", ".")
            .replace("\\", ".")
            .replace(".luau", "")
            .replace(".lua", "")
        )

        module = LuauModule(
            name=module_name,
            path=module_path,
            filepath=str(filepath),
            docstring=self._extract_module_docstring(content),
        )

        # Parse functions
        functions = self._parse_functions(content, module_path)
        module.functions = functions

        return module

    def _extract_module_docstring(self, content: str) -> str:
        """Extract module-level documentation from the beginning of the file.

        Parameters:
            content: The file content.

        Returns:
            The module docstring.
        """
        lines = content.split("\n")
        docstring_lines = []

        for line in lines:
            stripped = line.strip()
            if stripped.startswith("--"):
                # Remove the comment marker and add to docstring
                doc_line = stripped[2:].strip()
                if doc_line:
                    docstring_lines.append(doc_line)
            elif stripped and not stripped.startswith("--"):
                # Stop at first non-comment, non-empty line
                break

        return "\n".join(docstring_lines)

    def _parse_functions(self, content: str, module_path: str) -> list[LuauFunction]:
        """Parse all functions from the content.

        Parameters:
            content: The file content.
            module_path: The module path prefix.

        Returns:
            A list of parsed functions.
        """
        functions = []
        lines = content.split("\n")

        for match in self._FUNCTION_PATTERN.finditer(content):
            func_name = match.group(1)
            params_str = match.group(2).strip()
            lineno = content[: match.start()].count("\n") + 1

            # Extract docstring (comments before the function)
            docstring = self._extract_function_docstring(lines, lineno - 1)

            # Parse parameters
            parameters = self._parse_parameters(params_str)

            # Try to extract return type from the full function signature
            return_type = self._extract_return_type(content, match.end())

            # Build signature
            params_sig = ", ".join(
                f"{p.name}{f': {p.type}' if p.type else ''}{f' = {p.default}' if p.default else ''}" for p in parameters
            )
            signature = f"function {func_name}({params_sig}){f': {return_type}' if return_type else ''}"

            function = LuauFunction(
                name=func_name.split(".")[-1],  # Get the last part for nested functions
                path=f"{module_path}.{func_name}",
                parameters=parameters,
                return_type=return_type,
                docstring=docstring,
                lineno=lineno,
                signature=signature,
            )
            functions.append(function)

        return functions

    def _extract_function_docstring(self, lines: list[str], func_lineno: int) -> str:
        """Extract the docstring for a function from preceding comments.

        Parameters:
            lines: All lines in the file.
            func_lineno: The line number where the function is defined (0-indexed).

        Returns:
            The function docstring.
        """
        docstring_lines: list[str] = []
        # Look backwards from the function line
        for i in range(func_lineno - 1, -1, -1):
            line = lines[i].strip()
            if line.startswith("--"):
                doc_line = line[2:].strip()
                docstring_lines.insert(0, doc_line)
            elif line:
                # Stop at first non-comment, non-empty line
                break

        return "\n".join(docstring_lines)

    def _parse_parameters(self, params_str: str) -> list[LuauParameter]:
        """Parse function parameters.

        Parameters:
            params_str: The parameters string from the function signature.

        Returns:
            A list of parsed parameters.
        """
        if not params_str:
            return []

        parameters = []
        # Split by comma, but be careful with type annotations that might contain commas
        param_parts = self._split_params(params_str)

        for param_str in param_parts:
            param_str = param_str.strip()  # noqa: PLW2901
            if not param_str:
                continue

            # Check for type annotation
            type_match = self._TYPE_ANNOTATION_PATTERN.search(param_str)
            if type_match:
                param_name = param_str[: type_match.start()].strip()
                param_type = type_match.group(1).strip()
            else:
                param_name = param_str
                param_type = None

            # Check for default value
            if "=" in param_name:
                parts = param_name.split("=", 1)
                param_name = parts[0].strip()
                default_value = parts[1].strip()
            else:
                default_value = None

            parameters.append(LuauParameter(name=param_name, type=param_type, default=default_value))

        return parameters

    def _split_params(self, params_str: str) -> list[str]:
        """Split parameters by comma, respecting nested brackets.

        Parameters:
            params_str: The parameters string.

        Returns:
            A list of parameter strings.
        """
        params = []
        current = []
        depth = 0

        for char in params_str:
            if char in "<({[":
                depth += 1
                current.append(char)
            elif char in ">)}]":
                depth -= 1
                current.append(char)
            elif char == "," and depth == 0:
                params.append("".join(current))
                current = []
            else:
                current.append(char)

        if current:
            params.append("".join(current))

        return params

    def _extract_return_type(self, content: str, func_end_pos: int) -> str | None:
        """Extract return type annotation after function signature.

        Parameters:
            content: The full file content.
            func_end_pos: The position where the function parameters end.

        Returns:
            The return type or None.
        """
        # Look for ": Type" pattern after the closing parenthesis
        remaining = content[func_end_pos : func_end_pos + 100]  # Look ahead a bit
        # Match ": Type" pattern, stopping at newline or specific characters
        match = re.match(r"\s*:\s*([a-zA-Z_][a-zA-Z0-9_<>|,\s]*?)(?:\s*\n|\s*--|\s*$)", remaining)
        if match:
            return match.group(1).strip()
        return None

    def parse_identifier(self, identifier: str) -> Any:
        """Parse an identifier and return the corresponding object.

        Parameters:
            identifier: The identifier to parse (e.g., "module.function").

        Returns:
            The parsed object (module or function).
        """
        # Try to find the file
        parts = identifier.split(".")

        # Try different file extensions and paths
        possible_paths = [
            self._base_dir / f"{identifier.replace('.', '/')}.luau",
            self._base_dir / f"{identifier.replace('.', '/')}.lua",
            self._base_dir / f"{parts[0]}.luau",
            self._base_dir / f"{parts[0]}.lua",
        ]

        for filepath in possible_paths:
            if filepath.exists():
                module = self.parse_file(filepath)

                # If the filepath exactly matches the dotted identifier converted to a path
                # (for example identifier 'src.init' -> 'src/init.luau'), treat it as a module
                # request and return the module immediately. This avoids interpreting the last
                # dot segment as a function name when the file path explicitly exists.
                exact_luau = self._base_dir / f"{identifier.replace('.', '/')}.luau"
                exact_lua = self._base_dir / f"{identifier.replace('.', '/')}.lua"
                if filepath in (exact_luau, exact_lua):
                    return module

                # If looking for a specific function inside a module (e.g. 'module.func'),
                # try to locate the function in the parsed module.
                if len(parts) > 1:
                    func_name = parts[-1]
                    for func in module.functions:
                        if func.name == func_name:
                            return func
                    # Function not found
                    raise FileNotFoundError(f"Function '{func_name}' not found in module '{parts[0]}'")

                return module

        # If no file found, raise error
        msg = f"Could not find Luau file for identifier: {identifier}"
        raise FileNotFoundError(msg)
