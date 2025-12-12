"""
Widget subclasses - primitive widgets for imgui
"""

import math
from imgui_bundle import imgui
from imery.frontend.widget import Widget
from imery.result import Result, Ok


class Text(Widget):
    """Text display widget"""

    def _pre_render_head(self) -> Result[None]:
        res = self._field_values.get("label")
        if not res:
            return Result.error("Text: failed to get label", res)
        imgui.text(res.unwrapped)
        return Ok(None)  # Text widget never opens


class BulletText(Widget):
    """Bullet text widget - text with bullet point"""

    def _pre_render_head(self) -> Result[None]:
        res = self._field_values.get("label")
        if not res:
            return Result.error("BulletText: failed to get label", res)
        imgui.bullet_text(res.unwrapped)
        return Ok(None)


class SeparatorText(Widget):
    """Separator with text label"""

    def _pre_render_head(self) -> Result[None]:
        res = self._field_values.get("label")
        if not res:
            return Result.error("SeparatorText: failed to get label", res)
        imgui.separator_text(res.unwrapped)
        return Ok(None)


class Separator(Widget):
    """Separator widget"""

    def _prepare_render(self) -> Result[None]:
        # Separator doesn't need label or metadata
        return Ok(None)

    def _pre_render_head(self) -> Result[None]:
        imgui.separator()
        return Ok(None)


class SameLine(Widget):
    """SameLine widget"""

    def _prepare_render(self) -> Result[None]:
        # SameLine doesn't need label or metadata
        return Ok(None)

    def _pre_render_head(self) -> Result[None]:
        imgui.same_line()
        return Ok(None)


class InputText(Widget):
    """Text input widget"""

    def _pre_render_head(self) -> Result[None]:
        if not self._data_path:
            return Result.error("InputText requires path (id)")

        # Get value using field_values
        value_res = self._field_values.get("label")
        if not value_res:
            return Result.error(f"InputText: failed to get value", value_res)
        value = value_res.unwrapped

        imgui_id = f"###{self.uid}"

        changed, new_val = imgui.input_text(imgui_id, str(value))
        if changed:
            set_res = self._field_values.set("label", new_val)
            if not set_res:
                return Result.error(f"InputText: failed to set value", set_res)

        return Ok(None)


class InputInt(Widget):
    """Integer input widget"""

    def _pre_render_head(self) -> Result[None]:
        if not self._data_path:
            return Result.error("InputInt requires path (id)")

        # Get value using field_values
        value_res = self._field_values.get("label")
        if not value_res:
            return Result.error(f"InputInt: failed to get value", value_res)
        value = value_res.unwrapped

        # Validate integer value
        try:
            int_value = int(value)
        except (ValueError, TypeError) as e:
            return Result.error(f"InputInt: invalid integer value '{value}' at path '{self._data_path}'")

        imgui_id = f"###{self.uid}"

        changed, new_val = imgui.input_int(imgui_id, int_value)
        if changed:
            set_res = self._field_values.set("label", new_val)
            if not set_res:
                return Result.error(f"InputInt: failed to set value", set_res)

        return Ok(None)


class SliderInt(Widget):
    """Integer slider widget"""

    def _pre_render_head(self) -> Result[None]:
        if not self._data_path:
            return Result.error("SliderInt requires path (id)")

        # Get value using field_values
        value_res = self._field_values.get("label")
        if not value_res:
            return Result.error(f"SliderInt: failed to get value", value_res)
        current_value = value_res.unwrapped

        if not isinstance(self._params, dict):
            return Result.error(f"SliderInt params must be dict, got {type(self._params)}")

        minv = self._params.get("min", 0)
        maxv = self._params.get("max", 100)
        scale = self._params.get("scale", "linear")
        display_format = self._params.get("display-format", None)

        if current_value is None or current_value == "":
            current_value = minv
            set_res = self._field_values.set("label", minv)
            if not set_res:
                return Result.error(f"SliderInt: failed to set default", set_res)

        imgui_id = f"###{self.uid}"

        if scale == "log":
            # Logarithmic scale
            log_min = math.log2(minv)
            log_max = math.log2(maxv)
            log_value = math.log2(current_value)

            if display_format:
                formatted_value = display_format.format(value=current_value)
            else:
                formatted_value = f"2^{int(log_value)} = {int(current_value)}"

            imgui.text(formatted_value)
            changed, log_value = imgui.slider_float(imgui_id, log_value, log_min, log_max, "")

            if changed:
                new_val = int(2 ** log_value)
                set_res = self._field_values.set("label", new_val)
                if not set_res:
                    return Result.error(f"SliderInt: failed to set value", set_res)
        else:
            # Linear scale
            changed, new_val = imgui.slider_int(imgui_id, int(current_value), int(minv), int(maxv))
            if changed:
                set_res = self._field_values.set("label", new_val)
                if not set_res:
                    return Result.error(f"SliderInt: failed to set value", set_res)

        return Ok(None)


class SliderFloat(Widget):
    """Float slider widget"""

    def _pre_render_head(self) -> Result[None]:
        if not self._data_path:
            return Result.error("SliderFloat requires path (id)")

        # Get value using field_values
        value_res = self._field_values.get("label")
        if not value_res:
            return Result.error(f"SliderFloat: failed to get value", value_res)
        current_value = float(value_res.unwrapped)

        if not isinstance(self._params, dict):
            return Result.error(f"SliderFloat params must be dict, got {type(self._params)}")

        minv = float(self._params.get("min", 0.0))
        maxv = float(self._params.get("max", 1.0))

        imgui_id = f"###{self.uid}"

        changed, new_val = imgui.slider_float(imgui_id, current_value, minv, maxv)
        if changed:
            set_res = self._field_values.set("label", new_val)
            if not set_res:
                return Result.error(f"SliderFloat: failed to set value", set_res)

        return Ok(None)


class Combo(Widget):
    """Combo box widget"""


    def _pre_render_head(self) -> Result[None]:
        if not self._data_path:
            return Result.error("Combo requires path (id)")

        # Get value using field_values
        value_res = self._field_values.get("label")
        if not value_res:
            return Result.error(f"Combo: failed to get value", value_res)
        current_value = value_res.unwrapped

        if not isinstance(self._params, dict):
            return Result.error(f"Combo params must be dict, got {type(self._params)}")

        items = self._params.get("items", [])

        try:
            idx = items.index(str(current_value))
        except ValueError:
            idx = 0

        imgui_id = f"###{self.uid}"
        changed, idx = imgui.combo(imgui_id, idx, items)
        if changed and 0 <= idx < len(items):
            set_res = self._field_values.set("label", items[idx])
            if not set_res:
                return Result.error(f"Combo: failed to set value", set_res)

        return Ok(None)


class Checkbox(Widget):
    """Checkbox widget"""


    def _pre_render_head(self) -> Result[None]:
        if not self._data_path:
            return Result.error("Checkbox requires path (id)")

        # Get value using field_values
        value_res = self._field_values.get("label")
        if not value_res:
            return Result.error(f"Checkbox: failed to get value", value_res)
        current_value = str(value_res.unwrapped).lower() in ("true", "1", "yes")

        imgui_id = f"###{self.uid}"

        changed, new_val = imgui.checkbox(imgui_id, current_value)
        if changed:
            set_res = self._field_values.set("label", str(new_val))
            if not set_res:
                return Result.error(f"Checkbox: failed to set value", set_res)

        return Ok(None)


class Button(Widget):
    """Button widget - uses generic event system for clicks"""

    def _pre_render_head(self) -> Result[None]:
        """Render button core - returns True if clicked"""
        label_res = self._field_values.get("label")
        if not label_res:
            return Result.error("Button: failed to get label", label_res)
        label = label_res.unwrapped

        clicked = imgui.button(f"{label}###{self.uid}")
        if clicked:
            self._is_body_activated = True
            # print("Button: _pre_render_head")

        return Ok(None)


class Popup(Widget):
    """Popup widget - uses activated event for content"""


    def init(self) -> Result[None]:
        """Initialize popup and call imgui.open_popup()"""
        # Call imgui.open_popup() - first stage of imgui popup creation

        imgui.open_popup(self.uid)
        # print("Popup: init:")
        # Initialize events (including activated)
        return super().init()

    def _pre_render_head(self) -> Result[None]:
        """Render popup - returns True if open, False if closed"""
        # Check if popup is open
        popup_opened = imgui.begin_popup(self.uid)
        self._is_body_activated = popup_opened
        if self._render_cycle == 0:
            # workarround for Popup as in first render cycle it returns always 0
            self._is_open = True
        else:
            self._is_open = popup_opened
            self._is_body_activated = popup_opened
        # print(f"Popup: pre_render_head: render_cycle: {self._render_cycle}, is_body_activated: {self._is_body_activated}, popup_opened: {popup_opened}")
        return Ok(None)

    def _post_render_head(self) -> Result[None]:
        """End popup after rendering"""
        # print("Popup: _post_render_head:", self._is_body_activated)
        if self._is_body_activated:
            imgui.end_popup()
        return Ok(None)


class Tooltip(Widget):
    """Tooltip widget - uses activated event for content, like TreeLike widgets"""

    def _pre_render_head(self) -> Result[None]:
        """Render tooltip - always returns True to trigger activated event"""
        tooltip_opened = imgui.begin_tooltip()
        if self._render_cycle == 0:
            # workarround for Popup as in first render cycle it returns always 0
            self._is_open = True
            self._is_body_activated = True
        else:
            self._is_open = tooltip_opened
            self._is_body_activated = tooltip_opened
        return Ok(None)  # Always "open" to show content via activated event

    def _post_render_head(self) -> Result[None]:
        """End tooltip after rendering activated content"""
        imgui.end_tooltip()
        return Ok(None)

    def dispose(self) -> Result[None]:
        return Ok(None)


class TreeNode(Widget):
    """Tree node widget - renders collapsible tree structure"""

    def _pre_render_head(self) -> Result[None]:
        """Render tree node core"""

        # print("TreeNode: _pre_render_head:", self.uid, self._render_cycle)
        if self._render_cycle == 0:
            # on the first cycle we set the body as activated to solve the chicken-egg dependency between
            # creating the body widget and "if should create"
            # we cannot create first the body widget as for button-popup flow the popup needs to be created after
            # the button event. The button is detecting the popup creation if pre_render_head is setting the body_activated to true
            self._should_create_body = True
            return Ok(None)

        label_res = self._field_values.get("label", "NO-LABEL-DETECTED")
        if not label_res:
            return Result.error("TreeNode: failed to get label", label_res)
        label = label_res.unwrapped

        imgui_id = f"{label}###{self.uid}"

        # Check if body exists and is not empty
        has_body = self._body is not None and not self._body.is_empty
        # print("TreeNode: _pre_render_head:", self.uid, self._render_cycle, self._body.is_empty)

        if has_body:
            # Has body - render as expandable
            self._is_body_activated = imgui.tree_node(imgui_id)
        else:
            # No body - render as leaf (no arrow), never open
            imgui.tree_node_ex(imgui_id, imgui.TreeNodeFlags_.leaf | imgui.TreeNodeFlags_.no_tree_push_on_open)
            self._is_body_activated = False  # Leaf nodes are never "opened"

        return Ok(None)

    
    def _post_render_head(self) -> Result[None]:
        """Pop tree node after rendering - only if has body"""
        if self._is_body_activated:
            imgui.tree_pop()
        return Ok(None)


class CollapsingHeader(Widget):
    """Collapsing header widget - similar to tree node but different visual style"""

    def _pre_render_head(self) -> Result[None]:
        """Render collapsing header core"""
        label_res = self._field_values.get("label")
        if not label_res:
            return Result.error("CollapsingHeader: failed to get label", label_res)
        label = label_res.unwrapped

        imgui_id = f"{label}###{self.uid}"
        self._is_body_activated = imgui.collapsing_header(imgui_id)
        return Ok(None)



class Indent(Widget):
    """Indent widget - indents body content"""

    def _pre_render_head(self) -> Result[None]:
        """Render indent - always opens to render body"""

        res = self._field_values.get("width", 0.0)
        if not res:
            return Result.error("Indent: failed to get 'width'", res)
        width = res.unwrapped
        if width != 0.0:
            imgui.indent(width)
        else:
            imgui.indent()
        self._is_body_activated = True
        return Ok(None)  


    def _post_render_head(self) -> Result[None]:
        """Unindent after rendering"""
        res = self._field_values.get("width", 0.0)
        if not res:
            return Result.error("Indent: failed to get 'width'", res)
        width = res.unwrapped
        if width != 0.0:
            imgui.unindent(width)
        else:
            imgui.unindent()
        return Ok(None)


class Menu(Widget):
    """Menu widget - wraps content in imgui menu"""

    def _pre_render_head(self) -> Result[None]:
        """Render menu core"""
        res = self._field_values.get("label", "NO-LABEL")
        if not res:
            return Result.error("Menu: failed to get 'label'", res)
        label = res.unwrapped
        res = self._field_values.get("enabled", True)
        if not res:
            return Result.error("Menu: failed to get 'enabled'", res)
        enabled = res.unwrapped

        self._is_body_activated = imgui.begin_menu(label, enabled)
        return Ok(None)

    def _post_render_head(self) -> Result[None]:
        """End menu after rendering"""
        imgui.end_menu()
        return Ok(None)


class MenuItem(Widget):
    """Menu item widget - clickable menu entry"""

    def _pre_render_head(self) -> Result[None]:
        """Render menu item - returns True if clicked"""
        res = self._field_values.get("label")
        if not res:
            return Result.error("MenuItem: failed to get 'label'", res)
        label = res.unwrapped

        res = self._field_values.get("shortcut", "")
        if not res:
            return Result.error("MenuItem: could not get 'shortcut'", res)
        shortcut = res.unwrapped

        res = self._field_values.get("selection", False)
        if not res:
            return Result.error("MenuItem: could not get 'selection'", res)
        selection = res.unwrapped

        res = self._field_values.get("enabled", True)
        if not res:
            return Result.error("MenuItem: could not get 'enabled'", res)
        enabled = res.unwrapped

        clicked, _ = imgui.menu_item(label, shortcut, selection, enabled)

        self._is_body_activated = clicked
        return Ok(None)  # Return True if clicked (can render body)
