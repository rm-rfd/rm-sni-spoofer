from __future__ import annotations

import tkinter as tk
import tkinter.font as tkfont
from typing import Callable

from .theme import THEME

__all__ = ["SurfaceButton", "RoundedPanel"]


class SurfaceButton:
    def __init__(
        self,
        master: tk.Misc,
        *,
        theme: dict[str, str],
        fonts: dict[str, str],
        text: str,
        command: Callable[[], None] | None = None,
        icon_glyph: str = "",
        variant: str = "secondary",
        icon_only: bool = False,
    ) -> None:
        self._theme = theme
        self._fonts = fonts
        self._text = text
        self._command = command
        self._icon_glyph = icon_glyph
        self._variant = variant
        self._icon_only = icon_only
        self._disabled = False
        self._hovered = False

        self._parent_bg = str(master.cget("bg")) if "bg" in master.keys() else theme["shell"]
        self._canvas = tk.Canvas(
            master,
            bd=0,
            highlightthickness=0,
            relief="flat",
            takefocus=1,
            background=self._parent_bg,
            cursor="hand2",
        )
        for sequence in ("<Enter>", "<Leave>", "<Button-1>", "<Return>", "<space>", "<Configure>"):
            handler = {
                "<Enter>": self._on_enter,
                "<Leave>": self._on_leave,
                "<Button-1>": self._invoke,
                "<Return>": self._invoke,
                "<space>": self._invoke,
                "<Configure>": self._redraw,
            }[sequence]
            self._canvas.bind(sequence, handler, add="+")

        self._apply_style()

    def _style_tokens(self) -> dict[str, object]:
        base_styles: dict[str, dict[str, object]] = {
            "primary": {
                "bg": self._theme["accent"],
                "fg": self._theme["base_bg"],
                "border": self._theme["accent"],
                "hover_bg": "#ff8129",
                "hover_fg": self._theme["base_bg"],
                "hover_border": "#ff8129",
                "disabled_bg": self._theme["strong"],
                "disabled_fg": self._theme["muted"],
                "disabled_border": self._theme["strong"],
                "padx": 14,
                "pady": 6,
                "gap": 8,
                "font_size": 10,
                "icon_size": 12,
                "radius": 11,
                "min_height": 36,
                "min_width": 120,
                "content_anchor": "center",
                "draw_surface": True,
            },
            "secondary": {
                "bg": self._theme["shell"],
                "fg": self._theme["text"],
                "border": self._theme["border"],
                "hover_bg": self._theme["accent_soft"],
                "hover_fg": self._theme["text"],
                "hover_border": self._theme["accent"],
                "disabled_bg": self._theme["shell"],
                "disabled_fg": self._theme["muted"],
                "disabled_border": self._theme["input_border"],
                "padx": 14,
                "pady": 6,
                "gap": 8,
                "font_size": 10,
                "icon_size": 12,
                "radius": 11,
                "min_height": 36,
                "min_width": 120,
                "content_anchor": "center",
                "draw_surface": True,
            },
            "sidebar_primary": {
                "bg": self._theme["accent"],
                "fg": self._theme["base_bg"],
                "border": self._theme["accent"],
                "hover_bg": "#ff8129",
                "hover_fg": self._theme["base_bg"],
                "hover_border": "#ff8129",
                "disabled_bg": self._theme["strong"],
                "disabled_fg": self._theme["muted"],
                "disabled_border": self._theme["strong"],
                "padx": 16,
                "pady": 10,
                "gap": 8,
                "font_size": 10,
                "icon_size": 12,
                "radius": 11,
                "min_height": 42,
                "min_width": 0,
                "content_anchor": "center",
                "draw_surface": True,
            },
            "sidebar_outline": {
                "bg": self._theme["low"],
                "fg": self._theme["accent_text"],
                "border": self._theme["accent"],
                "hover_bg": self._theme["accent_soft"],
                "hover_fg": self._theme["accent_text"],
                "hover_border": self._theme["accent"],
                "disabled_bg": self._theme["low"],
                "disabled_fg": self._theme["muted"],
                "disabled_border": self._theme["input_border"],
                "padx": 16,
                "pady": 10,
                "gap": 8,
                "font_size": 10,
                "icon_size": 12,
                "radius": 11,
                "min_height": 42,
                "min_width": 0,
                "content_anchor": "center",
                "draw_surface": True,
            },
            "nav_active": {
                "bg": self._theme["accent_soft"],
                "fg": self._theme["accent_text"],
                "border": self._theme["accent"],
                "hover_bg": "#362419",
                "hover_fg": self._theme["accent_text"],
                "hover_border": self._theme["accent"],
                "disabled_bg": self._theme["accent_soft"],
                "disabled_fg": self._theme["muted"],
                "disabled_border": self._theme["accent"],
                "padx": 16,
                "pady": 10,
                "gap": 8,
                "font_size": 10,
                "icon_size": 12,
                "radius": 11,
                "min_height": 42,
                "min_width": 0,
                "content_anchor": "left",
                "draw_surface": True,
            },
            "header_icon": {
                "bg": self._theme["shell"],
                "fg": self._theme["muted_alt"],
                "border": self._theme["shell"],
                "hover_bg": self._theme["shell"],
                "hover_fg": self._theme["accent_text"],
                "hover_border": self._theme["shell"],
                "disabled_bg": self._theme["shell"],
                "disabled_fg": self._theme["muted"],
                "disabled_border": self._theme["shell"],
                "padx": 4,
                "pady": 4,
                "gap": 0,
                "font_size": 10,
                "icon_size": 18,
                "radius": 0,
                "min_height": 24,
                "min_width": 24,
                "content_anchor": "center",
                "draw_surface": False,
            },
        }
        return base_styles[self._variant]

    def _measure(self, style: dict[str, object]) -> tuple[int, int, int, int, int]:
        icon_width = 0
        text_width = 0
        line_height = 0

        icon_font = tkfont.Font(family=self._fonts["icon"], size=int(style["icon_size"]))
        if self._icon_glyph:
            icon_width = icon_font.measure(self._icon_glyph)
            line_height = max(line_height, icon_font.metrics("linespace"))

        show_text = not self._icon_only or not self._icon_glyph
        text_font = tkfont.Font(family=self._fonts["button"], size=int(style["font_size"]), weight="bold")
        if show_text:
            text_width = text_font.measure(self._text)
            line_height = max(line_height, text_font.metrics("linespace"))

        content_width = icon_width + text_width
        if icon_width and text_width:
            content_width += int(style["gap"])

        width = max(int(style["min_width"]), content_width + (int(style["padx"]) * 2))
        height = max(int(style["min_height"]), line_height + (int(style["pady"]) * 2))
        return width, height, icon_width, text_width, line_height

    def _rounded_points(self, x1: float, y1: float, x2: float, y2: float, radius: float) -> list[float]:
        return [
            x1 + radius,
            y1,
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]

    def _redraw(self, _event: tk.Event[tk.Misc] | None = None) -> None:
        style = self._style_tokens()
        width_hint, height_hint, icon_width, text_width, _line_height = self._measure(style)
        current_width = max(width_hint, self._canvas.winfo_width())
        current_height = max(height_hint, self._canvas.winfo_height())

        self._canvas.configure(
            width=width_hint,
            height=height_hint,
            bg=self._parent_bg,
            cursor="arrow" if self._disabled else "hand2",
        )
        self._canvas.delete("surface")
        self._canvas.delete("content")

        if bool(style["draw_surface"]):
            radius = float(style["radius"])
            self._canvas.create_polygon(
                self._rounded_points(1, 1, current_width - 1, current_height - 1, radius),
                smooth=True,
                splinesteps=36,
                fill=self._background,
                outline=self._border,
                width=1,
                tags="surface",
            )

        content_width = icon_width + text_width
        if icon_width and text_width:
            content_width += int(style["gap"])

        if style["content_anchor"] == "left":
            x = float(style["padx"])
        else:
            x = max(float(style["padx"]), (current_width - content_width) / 2)

        y = current_height / 2
        if self._icon_glyph:
            self._canvas.create_text(
                x,
                y,
                text=self._icon_glyph,
                fill=self._foreground,
                font=(self._fonts["icon"], int(style["icon_size"])),
                anchor="w",
                tags="content",
            )
            x += icon_width
            if text_width:
                x += int(style["gap"])

        if not self._icon_only or not self._icon_glyph:
            self._canvas.create_text(
                x,
                y,
                text=self._text,
                fill=self._foreground,
                font=(self._fonts["button"], int(style["font_size"]), "bold"),
                anchor="w",
                tags="content",
            )

    def _apply_style(self) -> None:
        style = self._style_tokens()
        if self._disabled:
            self._background = str(style["disabled_bg"])
            self._foreground = str(style["disabled_fg"])
            self._border = str(style["disabled_border"])
        elif self._hovered:
            self._background = str(style["hover_bg"])
            self._foreground = str(style["hover_fg"])
            self._border = str(style["hover_border"])
        else:
            self._background = str(style["bg"])
            self._foreground = str(style["fg"])
            self._border = str(style["border"])

        self._redraw()

    def _on_enter(self, _event: tk.Event[tk.Misc]) -> None:
        if self._disabled:
            return
        self._hovered = True
        self._apply_style()

    def _on_leave(self, _event: tk.Event[tk.Misc]) -> None:
        if self._disabled:
            return
        self._hovered = False
        self._apply_style()

    def _invoke(self, _event: tk.Event[tk.Misc] | None = None) -> str:
        if self._disabled or self._command is None:
            return "break"
        self._command()
        return "break"

    def state(self, state_specs: list[str]) -> None:
        for state_spec in state_specs:
            if state_spec == "disabled":
                self._disabled = True
            elif state_spec == "!disabled":
                self._disabled = False
        self._hovered = False
        self._apply_style()

    def grid(self, *args: object, **kwargs: object) -> None:
        self._canvas.grid(*args, **kwargs)

    def pack(self, *args: object, **kwargs: object) -> None:
        self._canvas.pack(*args, **kwargs)

    def place(self, *args: object, **kwargs: object) -> None:
        self._canvas.place(*args, **kwargs)


class RoundedPanel:
    def __init__(
        self,
        master: tk.Misc,
        *,
        fill: str,
        border: str,
        radius: int = 18,
        padding: tuple[int, int, int, int] = (16, 16, 16, 16),
        border_width: int = 1,
    ) -> None:
        self._fill = fill
        self._border = border
        self._radius = radius
        self._padding = padding
        self._border_width = border_width

        try:
            self._parent_bg = str(master.cget("bg"))
        except Exception:
            self._parent_bg = THEME["shell"]

        self._canvas = tk.Canvas(
            master,
            bd=0,
            highlightthickness=0,
            relief="flat",
            background=self._parent_bg,
        )
        self._content = tk.Frame(self._canvas, bg=self._fill, bd=0, highlightthickness=0)
        self._window_id = self._canvas.create_window(0, 0, anchor="nw", window=self._content)
        self._canvas.bind("<Configure>", self._redraw, add="+")
        self._content.bind("<Configure>", self._redraw, add="+")
        self._redraw()

    @property
    def content(self) -> tk.Frame:
        return self._content

    def _rounded_points(self, x1: float, y1: float, x2: float, y2: float, radius: float) -> list[float]:
        return [
            x1 + radius,
            y1,
            x1 + radius,
            y1,
            x2 - radius,
            y1,
            x2 - radius,
            y1,
            x2,
            y1,
            x2,
            y1 + radius,
            x2,
            y1 + radius,
            x2,
            y2 - radius,
            x2,
            y2 - radius,
            x2,
            y2,
            x2 - radius,
            y2,
            x2 - radius,
            y2,
            x1 + radius,
            y2,
            x1 + radius,
            y2,
            x1,
            y2,
            x1,
            y2 - radius,
            x1,
            y2 - radius,
            x1,
            y1 + radius,
            x1,
            y1 + radius,
            x1,
            y1,
        ]

    def _redraw(self, _event: tk.Event[tk.Misc] | None = None) -> None:
        width = max(2, self._canvas.winfo_width())
        pad_left, pad_top, pad_right, pad_bottom = self._padding
        content_height = max(1, self._content.winfo_reqheight())
        desired_height = max(2, content_height + pad_top + pad_bottom)
        if self._canvas.winfo_height() != desired_height:
            self._canvas.configure(height=desired_height)
        height = max(2, self._canvas.winfo_height())
        content_width = max(1, width - pad_left - pad_right)
        content_height = max(1, height - pad_top - pad_bottom)

        self._canvas.delete("surface")
        self._canvas.create_polygon(
            self._rounded_points(1, 1, width - 1, height - 1, float(self._radius)),
            smooth=True,
            splinesteps=36,
            fill=self._fill,
            outline=self._border,
            width=self._border_width,
            tags="surface",
        )
        self._canvas.coords(self._window_id, pad_left, pad_top)
        self._canvas.itemconfigure(self._window_id, width=content_width, height=content_height)

    def refresh(self) -> None:
        self._canvas.update_idletasks()
        self._redraw()

    def grid(self, *args: object, **kwargs: object) -> None:
        self._canvas.grid(*args, **kwargs)

    def pack(self, *args: object, **kwargs: object) -> None:
        self._canvas.pack(*args, **kwargs)

    def place(self, *args: object, **kwargs: object) -> None:
        self._canvas.place(*args, **kwargs)
