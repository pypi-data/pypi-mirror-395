from pathlib import Path
from imery.types import TreeLike, DataPath, Object
from imery.result import Result, Ok

from typing import Optional, Dict


def to_pascal_case(name: str) -> str:
    """Convert hyphenated name to PascalCase (e.g., 'same-line' -> 'SameLine')"""
    return ''.join(part.capitalize() for part in name.split('-'))


class WidgetFactory(Object):
    """
    Factory for creating widgets

    Uses TreeLike for data access and creates appropriate Widget subclasses
    """

    def __init__(self, widget_definitions: Dict[str, dict]):
        """
        Args:
            widget_definitions: Dictionary of widget_name -> widget definition from Lang
        """
        super().__init__()
        self._widget_cache = {}  # Cache of primitive + YAML widget definitions

        # Store YAML widget definitions from Lang
        self._yaml_widgets = widget_definitions

    def init(self) -> Result[None]:
        """Load primitive widget classes"""
        # Cache primitive widgets by dynamically importing
        import imery.frontend.widgets as widgets_module
        import imery.frontend.composite as composite_module
        import imery.frontend.implot as implot_module
        import imery.frontend.table as table_module

        primitive_names = [
            "text", "bullet-text", "separator-text", "separator", "same-line",
            "input-text", "input-int", "slider-int", "slider-float",
            "combo", "checkbox", "button", "popup", "tooltip",
            "tree-node", "collapsing-header", "indent", "menu", "menu-item"
        ]

        for name in primitive_names:
            class_name = to_pascal_case(name)
            try:
                widget_class = getattr(widgets_module, class_name)
                self._widget_cache[name] = widget_class
            except AttributeError:
                return Result.error(f"Primitive widget class '{class_name}' not found in widgets module")

        # Cache composite widget
        self._widget_cache["composite"] = composite_module.Composite

        # Register implot widgets from separate module
        self._widget_cache["implot"] = implot_module.Implot
        self._widget_cache["implot-layer"] = implot_module.ImplotLayer
        self._widget_cache["implot-group"] = implot_module.ImplotGroup

        # Register table widgets from separate module
        self._widget_cache["table"] = table_module.Table
        self._widget_cache["row"] = table_module.Row
        self._widget_cache["column"] = table_module.Column

        # Add YAML widgets to cache
        self._widget_cache.update(self._yaml_widgets)

        return Ok(None)

    def create_widget(self, widget_name: str, tree_like: TreeLike, data_path: DataPath, params=None) -> Result["Widget"]:
        """
        Create widget from widget_name

        Args:
            widget_name: Widget name (e.g., "demo_widgets.demo-form", "text", "button")
            tree_like: TreeLike instance (can be None)
            path: DataPath to data
            params: Parameters for the widget (can be None)

        Returns:
            Result[Widget]: Created widget instance
        """
        # Extract namespace if present
        if '.' in widget_name:
            namespace = widget_name.rsplit('.', 1)[0]
            lookup_name = widget_name
        else:
            namespace = ""
            lookup_name = widget_name

        # Smart lookup: try with full name first, then without namespace (for primitives)
        cached_item = None
        if lookup_name in self._widget_cache:
            cached_item = self._widget_cache[lookup_name]
        elif '.' in lookup_name:
            # Try without namespace (e.g., "demo_widgets.text" -> "text")
            widget_only = lookup_name.split('.')[-1]
            if widget_only in self._widget_cache:
                cached_item = self._widget_cache[widget_only]
                lookup_name = widget_only

        if cached_item is None:
            return Result.error(f"Widget '{widget_name}' not found in cache")

        # Check if it's a primitive (cached_item is a class)
        if isinstance(cached_item, type):
            # It's a primitive widget class
            return cached_item.create(
                factory=self,
                namespace=namespace,
                tree_like=tree_like,
                data_path=data_path,
                params=params if params is not None else {}
            )
        elif isinstance(cached_item, dict) and "type" in cached_item:
            # New format: {"type": "...", "body": ..., other metadata...}
            widget_type = cached_item["type"]

            if widget_type == "composite":
                from imery.frontend.composite import Composite
                return Composite.create(
                    factory=self,
                    namespace=namespace,
                    tree_like=tree_like,
                    data_path=data_path,
                    params=cached_item
                )
            elif widget_type == "popup":
                from imery.frontend.widgets import Popup
                return Popup.create(
                    factory=self,
                    namespace=namespace,
                    tree_like=tree_like,
                    data_path=data_path,
                    params=cached_item
                )
            elif widget_type == "tooltip":
                from imery.frontend.widgets import Tooltip
                return Tooltip.create(
                    factory=self,
                    namespace=namespace,
                    tree_like=tree_like,
                    data_path=data_path,
                    params=cached_item
                )
            else:
                return Result.error(f"Unknown widget type '{widget_type}'")
        else:
            # Old format: list (backward compatibility)
            from imery.frontend.widget import Composite
            return Composite.create(
                factory=self,
                namespace=namespace,
                tree_like=tree_like,
                path=path,
                params=cached_item
            )

    def dispose(self) -> Result[None]:
        return Ok(None)
