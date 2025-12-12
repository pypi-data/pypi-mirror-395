# Usage

The mkdocstrings-luau handler allows you to generate API documentation from Luau source code.

## Basic Usage

To use the handler in your MkDocs documentation, add the following to your `mkdocs.yml`:

```yaml
plugins:
  - mkdocstrings:
      handlers:
        luau:
          paths: [src]  # Where your Luau source files are located
```

Then, in your Markdown documentation files, you can reference Luau modules and functions:

```markdown
# My Luau Module

::: example

This will render documentation for the `example.luau` file.
```

## Features

The handler currently supports:

- **Module documentation**: Extracts module-level documentation from comments at the beginning of files
- **Function signatures**: Parses function definitions with parameters and return types
- **Type annotations**: Supports Luau type annotations (e.g., `parameter: type`, `: returnType`)
- **Documentation comments**: Extracts comments before functions as docstrings
- **Parameters**: Documents function parameters with types and default values

## Example

Given a Luau file `math.luau`:

```lua
-- Mathematical utility functions

-- Add two numbers together
-- Returns the sum of a and b
function add(a: number, b: number): number
    return a + b
end

-- Calculate the square of a number
function square(x: number): number
    return x * x
end
```

You can document it with:

```markdown
::: math
```

This will generate documentation showing:
- The module description
- Each function with its signature
- Parameters with type annotations
- Return type information
- Function docstrings

## Configuration Options

See the [Configuration](configuration/index.md) section for available options to customize the handler behavior.
