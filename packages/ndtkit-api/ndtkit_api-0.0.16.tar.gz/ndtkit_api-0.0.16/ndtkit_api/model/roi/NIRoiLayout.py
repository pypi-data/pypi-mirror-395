"""Wrapper for Java NIRoiLayout class.

NIRoiLayout is a specialized NIRoi representing layout ROIs. This module provides a
lightweight subclass that mirrors the Java type and reuses the NIRoi wrapper behavior.
"""
from py4j.java_gateway import JavaObject
from typing import Any, Optional, Tuple

from ...ndtkit_socket_connection import gateway
from .NIRoi import NIRoi


class NIRoiLayout(NIRoi):
    """Python wrapper for agi.ndtkit.api.model.roi.NIRoiLayout."""

    def __init__(self, java_object: JavaObject):
        super().__init__(java_object)

    @staticmethod
    def _to_java_color(value: Any) -> Any:
        """Convert a Python-friendly color representation to a java.awt.Color Java object.

        Accepts:
        - a wrapper or Java Color object (has attribute `_java_object` or is already a Java proxy)
        - a tuple/list of (r,g,b) or (r,g,b,a)
        - four separate ints passed by caller via other helpers (not used here)
        - an int (treated as packed RGB/ARGB and forwarded to Java Color(int))
        """
        # Already a Python wrapper around a Java object
        if hasattr(value, "_java_object"):
            return value._java_object

        # Already a Java proxy/object
        try:
            # Py4J Java proxies have getClass method; best-effort check
            if hasattr(value, "getClass"):
                return value
        except Exception:
            pass

        # Tuple/list of components
        if isinstance(value, (tuple, list)):
            if len(value) == 3:
                r, g, b = value
                return gateway.jvm.java.awt.Color(int(r), int(g), int(b))
            if len(value) == 4:
                r, g, b, a = value
                return gateway.jvm.java.awt.Color(int(r), int(g), int(b), int(a))

        # If it's an int, use the Color(int) constructor (packed RGB/ARGB)
        if isinstance(value, int):
            return gateway.jvm.java.awt.Color(value)

        # Last resort: try to construct from whatever is passed (may raise)
        return value

    def change_outline_color(self, color: Any) -> None:
        """Change the outline color of this ROI.

        `color` may be a Java Color, a wrapper with `_java_object`, a tuple (r,g,b) or (r,g,b,a), or an int packed RGB.
        """
        col = self._to_java_color(color)
        self._java_object.changeOutlineColor(col)

    def change_background_color(self, color: Any) -> None:
        """Change the background color of this ROI.

        `color` follows the same accepted formats as `change_outline_color`.
        """
        col = self._to_java_color(color)
        self._java_object.changeBackgroundColor(col)

    def change_outline_color_rgb(self, red: int, green: int, blue: int) -> None:
        """Convenience wrapper: change outline color by RGB components."""
        self._java_object.changeOutlineColor(gateway.jvm.java.awt.Color(int(red), int(green), int(blue)))

    def change_background_color_rgba(self, red: int, green: int, blue: int, alpha: int) -> None:
        """Convenience wrapper: change background color by RGBA components."""
        self._java_object.changeBackgroundColor(gateway.jvm.java.awt.Color(int(red), int(green), int(blue), int(alpha)))

    def change_style(self, style: Any) -> None:
        """Change the style (line stroke type) of this ROI.

        `style` may be a Java enum object, a wrapper exposing `_java_object`, or any object acceptable by the Java API.
        """
        # If caller gave a wrapper, unwrap it
        arg = getattr(style, "_java_object", style)
        # Java side expects an NIEnumLineStrokeType; many wrappers will expose a Java object or helper
        self._java_object.changeStyle(arg)

    def get_outline_color(self) -> Any:
        """Return the outline color (java.awt.Color) or a Java proxy object."""
        return self._java_object.getOutlineColor()

    def get_background_color(self) -> Optional[Any]:
        """Return the background color (java.awt.Color) or None."""
        return self._java_object.getBackgroundColor()

    def set_name(self, name: str) -> None:
        """Set the layout name (overrides base behavior)."""
        self._java_object.setName(name)

    def display_name(self, is_display_name: bool) -> None:
        """Display or hide the layout name label."""
        self._java_object.displayName(is_display_name)

    def set_name_label_location(self, x: float, y: float) -> None:
        """Move layout label to a specific pixel location (x, y)."""
        self._java_object.setNameLabelLocation(float(x), float(y))

    def set_text(self, text: str) -> None:
        """Set the layout text if this ROI is a text ROI."""
        self._java_object.setText(text)

    def get_text(self) -> str:
        """Return the layout text (or empty string)."""
        return self._java_object.getText()

    def set_text_font_size(self, font_size: int) -> None:
        """Set the layout text font size."""
        self._java_object.setTextFontSize(int(font_size))

    def set_text_font_fg_color(self, *args: Any) -> None:
        """Set the text font foreground color.

        Supports calls like:
        - set_text_font_fg_color(rgb_int)
        - set_text_font_fg_color(java_color_or_wrapper)
        - set_text_font_fg_color(r, g, b, a)
        """
        if len(args) == 1:
            self._java_object.setTextFontFGColor(self._to_java_color(args[0]))
            return
        if len(args) == 4:
            r, g, b, a = args
            self._java_object.setTextFontFGColor(gateway.jvm.java.awt.Color(int(r), int(g), int(b), int(a)).getRGB())
            return
        raise TypeError("Unsupported arguments for set_text_font_fg_color")

    def set_text_font_name(self, font_name: str) -> None:
        """Set the text font name for layout text."""
        self._java_object.setTextFontName(font_name)

    def set_texture_path(self, texture_path: str) -> None:
        """Set the texture path used for layout background (if ROIDressed)."""
        self._java_object.setTexturePath(texture_path)

    def set_texture_image(self, texture_image: Any) -> None:
        """Set the texture image (expects a java.awt.image.BufferedImage or Java proxy)."""
        self._java_object.setTextureImage(getattr(texture_image, "_java_object", texture_image))

    def set_font_style(self, font_style: int) -> None:
        """Set the layout text font style (0=PLAIN,1=BOLD,2=ITALIC)."""
        self._java_object.setFontStyle(int(font_style))

    def set_transparency(self, transparency: float) -> None:
        """Set layout transparency (float)."""
        self._java_object.setTransparency(float(transparency))
