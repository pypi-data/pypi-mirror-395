# This module implements a handler for Luau.

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar

from mkdocs.exceptions import PluginError
from mkdocstrings import BaseHandler, CollectionError, CollectorItem, get_logger

from mkdocstrings_handlers.luau._internal.config import LuauConfig, LuauOptions
from mkdocstrings_handlers.luau._internal.parser import LuauParser

if TYPE_CHECKING:
    from collections.abc import Mapping, MutableMapping

    from mkdocs.config.defaults import MkDocsConfig
    from mkdocstrings import HandlerOptions


_logger = get_logger(__name__)


class LuauHandler(BaseHandler):
    """The Luau handler class."""

    name: ClassVar[str] = "luau"
    """The handler's name."""

    domain: ClassVar[str] = "luau"
    """The cross-documentation domain/language for this handler."""
    # Typically: the file extension, like `py`, `go` or `rs`.
    # For non-language handlers, use the technology/tool name, like `openapi` or `click`.

    enable_inventory: ClassVar[bool] = False
    """Whether this handler is interested in enabling the creation of the `objects.inv` Sphinx inventory file."""

    fallback_theme: ClassVar[str] = "material"
    """The theme to fallback to."""

    def __init__(self, config: LuauConfig, base_dir: Path, **kwargs: Any) -> None:
        """Initialize the handler.

        Parameters:
            config: The handler configuration.
            base_dir: The base directory of the project.
            **kwargs: Arguments passed to the parent constructor.
        """
        super().__init__(**kwargs)

        self.config = config
        """The handler configuration."""
        self.base_dir = base_dir
        """The base directory of the project."""
        self.global_options = config.options
        """The global configuration options."""

        self._collected: dict[str, CollectorItem] = {}
        self._parser = LuauParser(base_dir)
        """The Luau parser instance."""

    def get_options(self, local_options: Mapping[str, Any]) -> HandlerOptions:
        """Get combined default, global and local options.

        Arguments:
            local_options: The local options.

        Returns:
            The combined options.
        """
        extra = {**self.global_options.get("extra", {}), **local_options.get("extra", {})}
        options = {**self.global_options, **local_options, "extra": extra}
        try:
            return LuauOptions.from_data(**options)
        except Exception as error:
            raise PluginError(f"Invalid options: {error}") from error

    def collect(self, identifier: str, options: LuauOptions) -> CollectorItem:  # noqa: ARG002
        """Collect data given an identifier and selection configuration."""
        # Check if already collected
        if identifier in self._collected:
            return self._collected[identifier]

        try:
            # Parse the identifier and get the corresponding object
            obj = self._parser.parse_identifier(identifier)

            # Convert to CollectorItem-compatible dictionary
            data = obj.to_dict() if hasattr(obj, "to_dict") else obj

            # Store in collected items
            self._collected[identifier] = data

        except FileNotFoundError as error:
            raise CollectionError(f"Could not collect '{identifier}': {error}") from error
        except Exception as error:
            raise CollectionError(f"Error collecting '{identifier}': {error}") from error
        else:
            return data

    def render(self, data: CollectorItem, options: LuauOptions, *, locale: str | None = None) -> str:  # noqa: ARG002
        """Render a template using provided data and configuration options."""
        # Choose template based on data type
        if "functions" in data:
            # This is a module
            template = self.env.get_template("module.html.jinja")
        elif "parameters" in data:
            # This is a function
            template = self.env.get_template("function.html.jinja")
        else:
            # Fallback to generic data template
            template = self.env.get_template("data.html.jinja")

        # All the following variables will be available in the Jinja templates.
        return template.render(
            config=options,
            data=data,
            heading_level=options.heading_level,
            root=True,
        )

    def get_aliases(self, identifier: str) -> tuple[str, ...]:
        """Get aliases for a given identifier."""
        try:
            data = self._collected[identifier]
        except KeyError:
            return ()
        # Update the following code to return the canonical identifier and any aliases.
        # `data` can be either an object with attributes or a plain dict (depending on parser
        # implementation). Support both access patterns.
        if hasattr(data, "path"):
            return (data.path,)
        if isinstance(data, dict) and "path" in data:
            return (data["path"],)
        return ()

    def update_env(self, config: dict) -> None:  # noqa: ARG002
        """Update the Jinja environment with any custom settings/filters/options for this handler.

        Parameters:
            config: MkDocs configuration, read from `mkdocs.yml`.
        """
        self.env.trim_blocks = True
        self.env.lstrip_blocks = True
        self.env.keep_trailing_newline = False

    # You can also implement the `get_inventory_urls` and `load_inventory` methods
    # if you want to support loading object inventories.
    # You can also implement the `render_backlinks` method if you want to support backlinks.


def get_handler(
    handler_config: MutableMapping[str, Any],
    tool_config: MkDocsConfig,
    **kwargs: Any,
) -> LuauHandler:
    """Simply return an instance of `LuauHandler`.

    Arguments:
        handler_config: The handler configuration.
        tool_config: The tool (SSG) configuration.

    Returns:
        An instance of `LuauHandler`.
    """
    base_dir = Path(tool_config.config_file_path or "./mkdocs.yml").parent
    return LuauHandler(
        config=LuauConfig.from_data(**handler_config),
        base_dir=base_dir,
        **kwargs,
    )
