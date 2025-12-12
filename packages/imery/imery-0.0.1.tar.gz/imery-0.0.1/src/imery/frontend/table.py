"""
Table widgets - table layout widgets following the standard Widget pattern
All widgets use "activated" parameter for children, just like composite widgets
"""

from imgui_bundle import imgui
from imery.frontend.widget import Widget
from imery.result import Result, Ok


class Table(Widget):
    """Table widget - creates table context, renders rows from activated"""

    def _pre_render(self) -> Result[bool]:
        """Begin table - returns True to render activated children"""
        # Get label from field values
        label_res = self._field_values.get("label")
        if not label_res:
            return Result.error("Table: failed to get label", label_res)
        label = label_res.unwrapped

        # Get number of columns from params
        if not isinstance(self._params, dict):
            return Result.error(f"Table params must be dict, got {type(self._params)}")

        num_columns = self._params.get("columns", 1)

        # Get flags from params
        flags = imgui.TableFlags_.none
        flags_list = self._params.get("flags", [])
        for flag_name in flags_list:
            flag_attr = flag_name.replace("-", "_")
            if hasattr(imgui.TableFlags_, flag_attr):
                flags |= getattr(imgui.TableFlags_, flag_attr)

        # Begin table
        if imgui.begin_table(label, num_columns, flags):
            return Ok(True)  # Table is open, render activated children
        return Ok(False)

    def _post_render(self) -> Result[None]:
        """End table after rendering activated children"""
        imgui.end_table()
        return Ok(None)


class Row(Widget):
    """Row widget - advances to next table row, renders columns from activated"""

    def _pre_render(self) -> Result[bool]:
        """Advance to next row - returns True to render activated children"""
        # Get min height from params
        min_height = 0.0
        if isinstance(self._params, dict):
            min_height = self._params.get("min-height", 0.0)

        # Get flags from params
        flags = imgui.TableRowFlags_.none
        if isinstance(self._params, dict):
            flags_list = self._params.get("flags", [])
            for flag_name in flags_list:
                flag_attr = flag_name.replace("-", "_")
                if hasattr(imgui.TableRowFlags_, flag_attr):
                    flags |= getattr(imgui.TableRowFlags_, flag_attr)

        # Call table_next_row
        imgui.table_next_row(flags, min_height)
        return Ok(True)  # Always render activated children


class Column(Widget):
    """Column widget - advances to next table column, renders content from activated"""

    def _pre_render(self) -> Result[bool]:
        """Advance to next column - returns True to render activated children"""
        # Call table_next_column
        imgui.table_next_column()
        return Ok(True)  # Always render activated children
