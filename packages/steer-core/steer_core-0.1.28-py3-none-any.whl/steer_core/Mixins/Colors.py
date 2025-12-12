import numpy as np
import plotly.colors as pc

import pandas as pd
import numpy as np


class ColorMixin:
    """
    A class to manage colors, including conversion between hex and RGB formats,
    and generating color gradients.
    """

    @staticmethod
    def rgb_tuple_to_hex(rgb):
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    @staticmethod
    def get_colorway(color1, color2, n):
        """
        Generate a list of n hex colors interpolated between two HTML hex colors.

        Parameters
        ----------
        color1 : str
            The first color in HTML hex format (e.g., '#ff0000').
        color2 : str
            The second color in HTML hex format (e.g., '#0000ff').
        n : int
            The number of colors to generate in the gradient.
        """
        # Convert hex to RGB (0–255)
        rgb1 = np.array(pc.hex_to_rgb(color1))
        rgb2 = np.array(pc.hex_to_rgb(color2))

        # Interpolate and convert to hex
        colors = [
            ColorMixin.rgb_tuple_to_hex(tuple(((1 - t) * rgb1 + t * rgb2).astype(int)))
            for t in np.linspace(0, 1, n)
        ]

        return colors

    @staticmethod
    def adjust_fill_opacity(color_str: str, opacity: float) -> str:
        """
        Adjust the fill opacity of any color format while preserving line opacity.

        Parameters
        ----------
        color_str : str
            Color in any format (hex, rgb, rgba, named)
        opacity : float
            Target opacity (0.0 to 1.0)

        Returns
        -------
        str
            Color string with adjusted opacity in rgba format
        """
        if not color_str:
            return color_str

        if "rgba" in color_str:
            return ColorMixin._update_rgba_opacity(color_str, opacity)
        elif "rgb" in color_str:
            return color_str.replace("rgb(", "rgba(").replace(")", f", {opacity})")
        elif color_str.startswith("#"):
            return ColorMixin._hex_to_rgba(color_str, opacity)

        # For named colors, try to convert or return as-is
        return color_str

    @staticmethod
    def _hex_to_rgba(hex_color: str, opacity: float) -> str:
        """
        Convert hex color to rgba with specified opacity.

        Parameters
        ----------
        hex_color : str
            Hex color string (e.g., '#FF0000')
        opacity : float
            Target opacity (0.0 to 1.0)

        Returns
        -------
        str
            RGBA color string
        """
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            try:
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                return f"rgba({r}, {g}, {b}, {opacity})"
            except ValueError:
                return hex_color
        elif len(hex_color) == 3:
            # Handle short hex format (#RGB -> #RRGGBB)
            try:
                r = int(hex_color[0] * 2, 16)
                g = int(hex_color[1] * 2, 16)
                b = int(hex_color[2] * 2, 16)
                return f"rgba({r}, {g}, {b}, {opacity})"
            except ValueError:
                return hex_color

        return hex_color

    @staticmethod
    def _update_rgba_opacity(rgba_str: str, opacity: float) -> str:
        """
        Update the opacity component of an existing rgba color string.

        Parameters
        ----------
        rgba_str : str
            Existing rgba color string (e.g., 'rgba(255, 0, 0, 0.5)')
        opacity : float
            New opacity value (0.0 to 1.0)

        Returns
        -------
        str
            Updated rgba color string
        """
        if "rgba(" not in rgba_str:
            return rgba_str

        try:
            # Extract RGB components and replace alpha
            rgb_part = rgba_str.split("rgba(")[1].rsplit(",", 1)[0]
            return f"rgba({rgb_part}, {opacity})"
        except (IndexError, ValueError):
            return rgba_str

    @staticmethod
    def get_color_format(color_str: str) -> str:
        """
        Detect the format of a color string.

        Parameters
        ----------
        color_str : str
            Color string in any format

        Returns
        -------
        str
            Color format: 'hex', 'rgb', 'rgba', 'hsl', 'hsla', 'named', or 'unknown'
        """
        if not color_str or not isinstance(color_str, str):
            return "unknown"

        color_str = color_str.strip().lower()

        if color_str.startswith("#"):
            return "hex"
        elif color_str.startswith("rgba("):
            return "rgba"
        elif color_str.startswith("rgb("):
            return "rgb"
        elif color_str.startswith("hsla("):
            return "hsla"
        elif color_str.startswith("hsl("):
            return "hsl"
        else:
            return "named"  # Could be a named color like 'red', 'blue'

    @staticmethod
    def validate_opacity(opacity: float, param_name: str = "opacity") -> None:
        """
        Validate that opacity is within valid range.

        Parameters
        ----------
        opacity : float
            Opacity value to validate
        param_name : str
            Parameter name for error messages

        Raises
        ------
        ValueError
            If opacity is not between 0.0 and 1.0
        """
        if not isinstance(opacity, (int, float)):
            raise ValueError(f"{param_name} must be a number, got {type(opacity)}")

        if not (0.0 <= opacity <= 1.0):
            raise ValueError(f"{param_name} must be between 0.0 and 1.0, got {opacity}")

    @staticmethod
    def adjust_trace_opacity(trace, opacity: float) -> None:
        """
        Adjust opacity of a plotly trace in-place.

        Parameters
        ----------
        trace : plotly trace object
            The trace to modify
        opacity : float
            Target opacity (0.0 to 1.0)
        """
        ColorMixin.validate_opacity(opacity)

        # Adjust fill color if present
        if hasattr(trace, "fillcolor") and trace.fillcolor:
            trace.fillcolor = ColorMixin.adjust_fill_opacity(trace.fillcolor, opacity)

        # Adjust marker color if present
        if (
            hasattr(trace, "marker")
            and hasattr(trace.marker, "color")
            and trace.marker.color
        ):
            trace.marker.color = ColorMixin.adjust_fill_opacity(
                trace.marker.color, opacity
            )

        # Adjust line color if present (but maybe keep line opacity at 1.0?)
        if hasattr(trace, "line") and hasattr(trace.line, "color") and trace.line.color:
            trace.line.color = ColorMixin.adjust_fill_opacity(trace.line.color, opacity)
