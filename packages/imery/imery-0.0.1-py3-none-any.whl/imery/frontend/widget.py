"""
Widget - Base class and primitive widgets for imgui
Each widget gets TreeLike and path for data access
"""

from imgui_bundle import imgui
from imery.frontend.types import Visual
from imery.backend.types import TreeLike
from imery.types import DataPath, Object
from imery.result import Result, Ok

from typing import Optional, Dict, Any


class FieldValues(Object):
    """
    Helper class that implements the logic of handling (read/write) of field values of a widget
    The value can be static in the definition of the widget or obtained from the data
    """
    def __init__(self, tree_like: TreeLike, data_path: DataPath, params: Optional[Dict]):
        self._tree_like = tree_like
        self._data_path = data_path
        self._params = params
        self._data_map = None

    def init(self)->Result[None]:
        if not isinstance(self._params, dict):
            self._data_map = {}
            return Ok(None)
        self._data_map = self._params.get("data-map")
        if self._data_map:
            if not isinstance(self._data_map, dict):
                return Result.error("FieldValues.init: data-map should be dictionary")
        else:
            self._data_map = {}
        return Ok(None)

    def dispose(self)->Result[None]:
        return Ok(None)

    def _resolve_metadata_path(self, key: str) -> Result[DataPath]:
        """
        Resolve metadata path for a field key using data-map if present.

        Args:
            key: Field name (e.g., "label")

        Returns:
            Result[DataPath]: Resolved path for metadata access
        """
        # Check if data-map exists and has mapping for this key
        if key in self._data_map:
            mapping = self._data_map[key]
            if not isinstance(mapping, str):
                return Result.error(f"FieldValues: _resolve_metadata_path: mapping value should be string, got {type(mapping)}")

            if mapping.startswith("/"):
                return Ok(DataPath(mapping))
            else: 
                return Ok(self._data_path / mapping)
        # No mapping - use key as metadata key at current data_path
        return Ok(self._data_path / key)

    def get(self, key: str, default_value: Any = None) -> Result[Any]:
        """
        Get field value - checks static params first, then dynamic from tree_like metadata.

        Args:
            key: Field name (e.g., "label")

        Returns:
            Result with field value, or Error if not found
        """
        # Handle string params: treat as "label" value
        if self._params and isinstance(self._params, str):
            if key == "label":
                return Ok(self._params)
            # For other keys, fall through to tree_like lookup

        # Check if key exists directly in params dict (static value)
        if self._params and isinstance(self._params, dict) and key in self._params:
            return Ok(self._params[key])

        # No static value - try to get from tree_like metadata
        if not self._tree_like:
            if default_value is None:
                return Result.error(f"FieldValues.get: no tree_like available and key '{key}' not in params")
            else:
                return Ok(default_value)

        res = self._resolve_metadata_path(key)
        if not res:
            return Result.error(f"FieldValues: get: Could not resolve metadata path for '{key}'", res)
        full_path = res.unwrapped

        # Get metadata value (path includes key as last component)
        res = self._tree_like.get(full_path)
        if not res:
            if default_value is None:
                return Result.error(f"FieldValues.get: failed to get '{key}' from tree_like at path '{full_path}'", res)
            else:
                return Ok(default_value)

        return Ok(res.unwrapped)

    def set(self, key: str, value: Any) -> Result[None]:
        """
        Set field value - writes to tree_like metadata.

        Args:
            key: Field name (e.g., "label")
            value: Value to set

        Returns:
            Result[None]
        """
        if not self._tree_like:
            return Result.error(f"FieldValues.set: no tree_like available")

        # Check if there's a data-map for this key
        if self._data_map and isinstance(self._data_map, dict) and key in self._data_map:
            # Use mapped value
            mapped = self._data_map[key]

            # Check if mapped value is an absolute path
            if isinstance(mapped, str) and mapped.startswith("/"):
                # Absolute path - use it directly
                full_path = DataPath(mapped)
            else:
                # Relative path or metadata key - build path
                node_path = self._data_path
                full_path = node_path / mapped
        else:
            # No mapping - resolve path normally
            path_res = self._resolve_metadata_path(key)
            if not path_res:
                return Result.error(f"FieldValues.set: failed to resolve path for key '{key}'", path_res)
            node_path = path_res.unwrapped
            full_path = node_path / key


        # Set metadata value (path includes key as last component)
        res = self._tree_like.set(full_path, value)
        if not res:
            return Result.error(f"FieldValues.set: failed to set '{key}' at path '{full_path}'", res)

        return Ok(None)


class WidgetBase(Visual):
    pass

class Widget(WidgetBase):
    """Base class for all widgets"""

    def __init__(self, factory, namespace: str, tree_like: TreeLike, data_path: DataPath, params: Optional[Dict] = None):
        """
        Args:
            factory: WidgetFactory for creating nested widgets
            namespace: Current namespace (e.g., "demo_widgets")
            tree_like: TreeLike instance for data access (can be None)
            path: DataPath to data in the tree
            params: Widget parameters (dict or other type depending on widget)
        """
        super().__init__()
        # print("Widget: __init__:", self.__class__.__name__, self.uid)
        self._factory = factory
        self._namespace = namespace
        self._tree_like = tree_like
        self._data_path = data_path
        self._params = params
        self._style_color_count = 0
        self._style_var_count = 0
        self._metadata = None
        self._event_handlers = {}  # event_name -> list of command specs (lazy evaluated)
        self._body = None  # Body widget created from activated event
        self._is_body_activated = False # 
        self._should_create_body = False
        self._is_open = True

        self._data_path = data_path

        self._field_values = None
        self._render_cycle = -1


    def init(self) -> Result[None]:
        """Initialize widget - override in subclasses if needed"""
        # print("Widget: init:", self.__class__.__name__, self.uid)
        res = FieldValues.create(self._tree_like, self._data_path, self._params)
        if not res:
            return Result.error("Widget: failed to create FieldValues", res)
        self._field_values = res.unwrapped
        res = self._init_events()
        if not res:
            return Result.error("Widget: failed to initialize events", res)

        return Ok(None)

    @property
    def is_open(self):
        return self._is_open

    @property
    def is_empty(self) -> bool:
        """Check if widget has no content - override in subclasses"""
        return True

    def _init_events(self) -> Result[None]:
        """Parse and store event specifications from params"""
        if not isinstance(self._params, dict):
            return Ok(None)

        # List of supported event names
        event_names = ["on-active", "on-click", "on-double-click", "on-right-click", "on-hover"]

        # Check each event in params
        for event_name in event_names:
            event_spec = self._params.get(event_name)
            if event_spec is not None:
                self._event_handlers[event_name] = self._normalize_event_spec(event_spec)

        return Ok(None)

    def _evaluate_condition(self, condition, metadata: dict) -> bool:
        """
        Evaluate a condition against metadata.

        Condition can be:
        - list → implicit AND (all conditions must be true)
        - dict with single field: value → metadata[field] == value
        - dict with "and": [conditions] → all must be true
        - dict with "or": [conditions] → at least one must be true
        - dict with "not": condition → negate the condition

        Args:
            condition: Condition specification (list or dict)
            metadata: Metadata dict to check against

        Returns:
            bool: True if condition passes, False otherwise
        """
        # List → implicit AND
        if isinstance(condition, list):
            return all(self._evaluate_condition(c, metadata) for c in condition)

        if not isinstance(condition, dict):
            return False

        # Check for logical operators
        if "and" in condition:
            conditions = condition["and"]
            if isinstance(conditions, list):
                return all(self._evaluate_condition(c, metadata) for c in conditions)
            # Single condition (collapsed list)
            return self._evaluate_condition(conditions, metadata)

        if "or" in condition:
            conditions = condition["or"]
            if isinstance(conditions, list):
                return any(self._evaluate_condition(c, metadata) for c in conditions)
            # Single condition (collapsed list)
            return self._evaluate_condition(conditions, metadata)

        if "not" in condition:
            inner_condition = condition["not"]
            return not self._evaluate_condition(inner_condition, metadata)

        # Simple field comparison: {field: expected_value}
        # Should have exactly one key
        if len(condition) == 1:
            field_name, expected_value = next(iter(condition.items()))
            actual_value = metadata.get(field_name)
            return actual_value == expected_value

        # Multiple keys but no logical operator → invalid, return False
        return False

    def _normalize_event_spec(self, event_spec) -> list:
        """
        Normalize event specification into a list of commands.

        Event spec can be:
        - string "default" → [{"action": "default"}]
        - string (other) → [{"action": "show", "what": string}]
        - dict with action keys (show/dispatch) → [{"action": "show"/"dispatch", ...}]
        - dict (other) → [{"action": "show", "what": dict}] (widget spec)
        - list → normalize each item

        Returns:
            list: List of command dicts, each with "action", "what"/"message", optional "when"
        """
        # print("Widget: _normalize_event_spec", self.__class__.__name__, self.uid)
        # List → normalize each item
        if isinstance(event_spec, list):
            normalized_commands = []
            for item in event_spec:
                # Recursively normalize each item (collapsed form)
                # print("Widget: _normalize_event_spec, calling recursive", self.__class__.__name__, self.uid)
                normalized_item = self._normalize_event_spec(item)
                normalized_commands.extend(normalized_item)
            return normalized_commands

        # String "default" → {"action": "default"}
        if isinstance(event_spec, str):
            if event_spec == "default":
                return [{"action": "default"}]
            else:
                return [{"action": "show", "what": event_spec}]

        # Dict → check if it's an action spec or widget spec
        if isinstance(event_spec, dict):
            # Check if it has action keys
            if "show" in event_spec:
                return [{"action": "show", "what": event_spec["show"]}]
            elif "dispatch" in event_spec:
                return [{"action": "dispatch", "message": event_spec["dispatch"]}]
            elif "action" in event_spec:
                # Already in normalized format
                return [event_spec]
            else:
                # Treat as widget spec (inline widget definition)
                return [{"action": "show", "what": event_spec}]

        return []

    def _execute_event_commands(self, event_name: str) -> Result[None]:
        """
        Execute commands for an event.

        For each command:
        - Check "when" condition (if present)
        - Execute action: "show" or "dispatch"
        - Lazy create widgets on first execution

        Args:
            event_name: Name of the event ("clicked", "hovered", etc.)

        Returns:
            Result[None]
        """
        if event_name not in self._event_handlers:
            return Ok(None)

        commands = self._event_handlers[event_name]

        for i, cmd_spec in enumerate(commands):
            if not isinstance(cmd_spec, dict):
                continue

            # Check condition if present
            if "when" in cmd_spec:
                condition = cmd_spec["when"]
                if self._metadata and not self._evaluate_condition(condition, self._metadata):
                    continue  # Condition not met, skip this command

            # Get action (normalized format: {"action": "show"/"dispatch"/"default", "what": ...})
            action = cmd_spec.get("action")
            if action == "show":
                widget_spec = cmd_spec.get("what")
            elif action == "dispatch":
                message = cmd_spec.get("message") or cmd_spec.get("what")
            elif action == "default":
                # Default action - no additional data needed
                pass
            else:
                return Result.error(f"Unknown action in {event_name} event: {cmd_spec}")

            print(f"Widget: _execute_event_commands, action: {action}")
            # Execute action
            if action == "default":
                # Default action: for "click" events, set "selected" field
                if event_name == "on-click":
                    set_res = self._field_values.set("selection", str(self._data_path))
                    if not set_res:
                        return Result.error(f"default action failed to set selected", set_res)
                # For other events, default does nothing

            elif action == "show":
                # For "body" event, create self._body instead of per-command widget
                    # For other events, use per-command widget instance
                if "widget-instance" not in cmd_spec:
                    # Lazy create widget
                    res = self._create_widget_from_spec(widget_spec)
                    if not res:
                        return Result.error(f"Failed to create widget for {event_name} event", res)
                    cmd_spec["widget-instance"] = res.unwrapped

                # Render the widget
                widget = cmd_spec["widget-instance"]
                res = widget.render()
                if not res:
                    return Result.error(f"Failed to render widget for {event_name} event", res)

            elif action == "dispatch":
                # Placeholder for dispatch
                # TODO: Implement dispatch to dispatcher
                pass

        return Ok(None)


    def _create_widget_from_spec(self, widget_spec) -> Result:
        """
        Create a widget from a specification.

        Args:
            widget_spec: String (widget name), dict (inline widget), or list (composite)

        Returns:
            Result[Widget]: Created widget instance
        """

        # String → widget reference
        if isinstance(widget_spec, str):
            widget_name = widget_spec
            if '.' not in widget_name and self._namespace:
                full_widget_name = f"{self._namespace}.{widget_name}"
            else:
                full_widget_name = widget_spec
            return self._factory.create_widget(full_widget_name, self._tree_like, self._data_path)

        # Dict or list → composite - use factory to avoid circular import
        if isinstance(widget_spec, (dict, list)):
            params = {"type": "composite", "body": [widget_spec] if isinstance(widget_spec, dict) else widget_spec}
            # Use full widget name with namespace to preserve context
            full_widget_name = f"{self._namespace}.composite" if self._namespace else "composite"
            return self._factory.create_widget(full_widget_name, self._tree_like, self._data_path, params)

        return Result.error(f"Invalid widget spec type: {type(widget_spec)}")

    def _prepare_render(self) -> Result[None]:
        """Prepare for rendering: load metadata and label"""
        # Get metadata first if we have a data tree
        if self._tree_like:
            # Determine metadata path: path / data-id if data-id present, otherwise path
            if isinstance(self._params, dict) and "data-id" in self._params:
                metadata_path = self._data_path / self._params["data-id"]
            else:
                metadata_path = self._data_path

            # Get metadata
            res = self._tree_like.get_metadata(metadata_path)
            if not res:
                return Result.error(f"_prepare_render: failed to get metadata at path '{metadata_path}'", res)
            self._metadata = res.unwrapped


        return Ok(None)

    def _apply_style_dict(self, style_dict: dict) -> Result[None]:
        """Apply a single style dictionary (colors and vars)"""
        for style_name, style_value in style_dict.items():
            # Convert hyphenated name to underscore for enum lookup
            enum_name = style_name.replace("-", "_")

            # Try to find it as a color first
            try:
                color_enum = getattr(imgui.Col_, enum_name)
                # Convert list to ImVec4 if needed
                if isinstance(style_value, list):
                    if len(style_value) == 4:
                        color = imgui.ImVec4(style_value[0], style_value[1], style_value[2], style_value[3])
                    else:
                        return Result.error(f"Style color '{style_name}' requires 4 components, got {len(style_value)}")
                else:
                    return Result.error(f"Style color '{style_name}' must be a list")

                imgui.push_style_color(color_enum, color)
                self._style_color_count += 1
                continue
            except AttributeError:
                pass  # Not a color, try style var

            # Try to find it as a style var
            try:
                var_enum = getattr(imgui.StyleVar_, enum_name)
                # Convert list to ImVec2 if needed, otherwise use scalar
                if isinstance(style_value, list):
                    if len(style_value) == 2:
                        vec = imgui.ImVec2(style_value[0], style_value[1])
                        imgui.push_style_var(var_enum, vec)
                    else:
                        return Result.error(f"Style var '{style_name}' requires 1 or 2 components, got {len(style_value)}")
                else:
                    # Scalar value
                    imgui.push_style_var(var_enum, float(style_value))

                self._style_var_count += 1
                continue
            except AttributeError:
                return Result.error(f"Unknown style attribute '{style_name}'")

        return Ok(None)

    def _push_styles(self) -> Result[None]:
        """Push styles before rendering"""
        if not isinstance(self._params, dict):
            return Ok(None)

        # Apply default style first
        style = self._params.get("style")
        if style and isinstance(style, dict):
            res = self._apply_style_dict(style)
            if not res:
                return Result.error("_push_styles: failed to apply default style", res)

        # Apply style-mapping based on metadata conditions
        style_mapping = self._params.get("style-mapping")
        if style_mapping and self._metadata:
            # style-mapping can be:
            # 1. Dict (old format): {field_name: style_dict, ...} - backward compatible
            # 2. List (new format): [{when: condition, style: style_dict}, ...]

            if isinstance(style_mapping, dict):
                # Old format: dict keys are field names to check
                for field_name, field_style in style_mapping.items():
                    # Simple field name - check if exists and truthy
                    condition = {field_name: True}

                    # Evaluate condition
                    if self._evaluate_condition(condition, self._metadata):
                        # Apply the style for this condition
                        if isinstance(field_style, dict):
                            res = self._apply_style_dict(field_style)
                            if not res:
                                return Result.error(f"_push_styles: failed to apply style-mapping for '{field_name}'", res)

            elif isinstance(style_mapping, list):
                # New format: list of {when: condition, style: style_dict}
                for mapping_entry in style_mapping:
                    if not isinstance(mapping_entry, dict):
                        continue

                    condition = mapping_entry.get("when")
                    entry_style = mapping_entry.get("style")

                    if condition is None or entry_style is None:
                        continue

                    # Evaluate condition
                    if self._evaluate_condition(condition, self._metadata):
                        # Apply the style
                        if isinstance(entry_style, dict):
                            res = self._apply_style_dict(entry_style)
                            if not res:
                                return Result.error(f"_push_styles: failed to apply style-mapping for condition", res)

        return Ok(None)

    def _pop_styles(self) -> Result[None]:
        """Pop styles after rendering - called by subclasses"""
        if self._style_color_count > 0:
            imgui.pop_style_color(self._style_color_count)
            self._style_color_count = 0

        if self._style_var_count > 0:
            imgui.pop_style_var(self._style_var_count)
            self._style_var_count = 0

        return Ok(None)

    def _pre_render_head(self) -> Result[None]:
        """Render widget core - must be implemented by subclasses
        """
        return Result.error("_pre_render_head() not implemented")

    def _post_render_head(self) -> Result[None]:
        """Widget-specific post-render cleanup - override in subclasses if needed

        Examples:
            TreeNode: imgui.tree_pop() if widget was opened
            Menu: imgui.end_menu() if widget was opened
            Indent: imgui.unindent() always
        """
        return Ok(None)

    def render(self) -> Result[None]:
        """Unified render flow for all widgets"""
        # Prepare: load metadata and label
        self._render_cycle = self._render_cycle + 1
        res = self._prepare_render()
        if not res:
            return Result.error("render: prepare_render failed", res)

        # Push styles
        res = self._push_styles()
        if not res:
            return Result.error("render: _push_styles failed", res)

        # First Render the "head", in case of Button, the button is itself the head
        # and the widget activated is the body, even if rendered in the "same window" or in popup or modal
        res = self._pre_render_head()
        if not res:
            self._pop_styles()
            return Result.error("render: pre_render failed", res)

        res = self._detect_and_execute_events()
        if not res:
            self._pop_styles()
            return Result.error("render: event execution failed", res)

        if self._body is None and (self._is_body_activated or self._should_create_body):
            # print(f"Widget: render:", self.__class__.__name__, self._is_body_activated, self.uid)
            if isinstance(self._params, dict) and "body" in self._params and self._body is None:
                activated_spec = self._params["body"]
                # print("Widget: render: creating body", self.__class__.__name__, self.uid)
                res = self._create_widget_from_spec(activated_spec)
                if not res:
                    return Result.error("_prepare_render: failed to create activated widget", res)
                self._body = res.unwrapped


        if self._is_body_activated:
            if self._body:
                res = self._body.render()

                if not res:
                    self._pop_styles()
                    return Result.error("render: activated render failed", res)

            # Widget-specific post-render (cleanup like tree_pop, end_menu, etc.)
            # Must be called whenever body is activated, even if body widget doesn't exist yet
            res = self._post_render_head()
            if not res:
                self._pop_styles()
                return Result.error("render: _post_render_head failed", res)


        # Pop styles
        res = self._pop_styles()
        if not res:
            return Result.error("render: post_render_head failed", res)

        if self._body and not self._body.is_open:
            # print("Widget: render: setting body to None", self.__class__.__name__, self.uid)
            self._is_body_activated = False
            self._body = None

        return Ok(None)

    def _detect_and_execute_events(self) -> Result[None]:
        """Detect ImGui events and execute corresponding event handlers"""
        # activated event - triggered by widget return value
        if self._is_body_activated and "on-active" in self._event_handlers:
            res = self._execute_event_commands("on-active")
            if not res:
                return Result.error("Failed to execute activated event", res)

        # clicked event - left mouse button
        if imgui.is_item_clicked(0) and "on-click" in self._event_handlers:
            res = self._execute_event_commands("on-click")
            if not res:
                return Result.error("Failed to execute clicked event", res)

        # right-clicked event - right mouse button
        if imgui.is_item_clicked(1) and "on-right-click" in self._event_handlers:
            res = self._execute_event_commands("on-right-click")
            if not res:
                return Result.error("Failed to execute right-clicked event", res)

        # double-clicked event
        if imgui.is_item_hovered() and imgui.is_mouse_double_clicked(0) and "on-double-click" in self._event_handlers:
            res = self._execute_event_commands("on-double-click")
            if not res:
                return Result.error("Failed to execute double-clicked event", res)

        # hovered event
        if imgui.is_item_hovered() and "on-hover" in self._event_handlers:
            res = self._execute_event_commands("on-hover")
            if not res:
                return Result.error("Failed to execute hovered event", res)

        return Ok(None)

    def dispose(self) -> Result[None]:
        """Cleanup widget resources"""
        return Ok(None)

