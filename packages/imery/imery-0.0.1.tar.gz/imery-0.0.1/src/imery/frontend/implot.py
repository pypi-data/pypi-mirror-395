"""
ImPlot widgets - plotting widgets following the standard Widget pattern
All widgets use "activated" parameter for children, just like composite widgets
"""

from imgui_bundle import implot
from imery.frontend.widget import Widget
from imery.result import Result, Ok


class ImplotLayer(Widget):
    """ImPlot layer widget - renders a single plot layer (line plot)"""

    def _pre_render(self) -> Result[bool]:
        """Render plot layer - renders line plot from data"""
        # Get buffer from metadata
        if not self._metadata:
            return Result.error("ImplotLayer: no metadata available")

        # Check if this is an openable channel
        category = self._metadata.get("category")
        openable = self._metadata.get("openable")

        if category == "channel" and openable:
            # This is an openable channel - need to call open() to get buffer
            if not self._tree_like:
                return Result.error("ImplotLayer: no tree_like available for opening channel")

            # Determine the path to open (use data-id if present)
            if isinstance(self._params, dict) and "data-id" in self._params:
                open_path = self._path / self._params["data-id"]
            else:
                open_path = self._path

            # Open the channel to get the buffer
            res = self._tree_like.open(open_path, {})
            if not res:
                return Result.error(f"ImplotLayer: failed to open channel at '{open_path}'", res)

            buffer = res.unwrapped
        else:
            # Legacy: buffer directly in metadata
            buffer = self._metadata.get("buffer")
            if not buffer:
                return Result.error(f"ImplotLayer: no buffer in metadata and not an openable channel")

        # Try to lock buffer
        if not buffer.try_lock():
            return Ok(False)  # Buffer busy, skip this frame

        try:
            # Get buffer data
            buffer_data = buffer.data
            if buffer_data is None or len(buffer_data) == 0:
                return Ok(False)  # No data to plot

            # X-axis: oldest sample at negative X, newest at 0
            xstart = -float(len(buffer_data))

            # Get label from field values
            label_res = self._field_values.get("label")
            if not label_res:
                return Result.error("ImplotLayer: failed to get label", label_res)
            label = label_res.unwrapped

            # Plot line
            implot.plot_line(label, buffer_data, xscale=1.0, xstart=xstart)

            return Ok(False)  # Layer doesn't activate
        finally:
            buffer.unlock()


class Implot(Widget):
    """ImPlot widget - creates plot context, renders layers from activated"""

    def _pre_render(self) -> Result[bool]:
        """Begin plot - returns True to render activated children"""
        # Get label from field values
        label_res = self._field_values.get("label")
        if not label_res:
            return Result.error("Implot: failed to get label", label_res)
        label = label_res.unwrapped

        # Begin plot
        if implot.begin_plot(label):
            return Ok(True)  # Plot is open, render activated children
        return Ok(False)

    def _post_render(self) -> Result[None]:
        """End plot after rendering activated children"""
        implot.end_plot()
        return Ok(None)


class ImplotGroup(Widget):
    """ImPlot group widget - creates subplots context, renders plots from activated"""

    def __init__(self, factory, namespace: str, tree_like, path, params):
        super().__init__(factory, namespace, tree_like, path, params)
        self._rows = 1
        self._cols = 1
        self._size = None

    def init(self) -> Result[None]:
        """Initialize subplot parameters"""
        if isinstance(self._params, dict):
            self._rows = self._params.get("rows", 1)
            self._cols = self._params.get("cols", 1)
            size = self._params.get("size")
            if size:
                self._size = (size[0], size[1])

        return super().init()

    def _prepare_render(self) -> Result[None]:
        # ImplotGroup doesn't need label or metadata, but needs to create self._activated
        # Create self._activated widget from "activated" param if present
        if isinstance(self._params, dict) and "activated" in self._params and self._activated is None:
            activated_spec = self._params["activated"]
            res = self._create_widget_from_spec(activated_spec)
            if not res:
                return Result.error("ImplotGroup._prepare_render: failed to create activated widget", res)
            self._activated = res.unwrapped
        return Ok(None)

    def _pre_render(self) -> Result[bool]:
        """Begin subplots - returns True to render activated children"""
        # Get label from field values
        label_res = self._field_values.get("label")
        if not label_res:
            return Result.error("ImplotGroup: failed to get label", label_res)
        label = label_res.unwrapped

        if self._size:
            if implot.begin_subplots(label, self._rows, self._cols, self._size):
                return Ok(True)  # Subplots open, render activated children
        else:
            if implot.begin_subplots(label, self._rows, self._cols):
                return Ok(True)  # Subplots open, render activated children

        return Ok(False)

    def _post_render(self) -> Result[None]:
        """End subplots after rendering activated children"""
        implot.end_subplots()
        return Ok(None)
