"""
Custom styled widget classes that apply the application theme.
"""

import tkinter as tk
from tkinter import scrolledtext
from typing import Literal

from ui.theme import Theme


class StyledButton(tk.Button):  # pylint: disable=too-many-ancestors
    """Styled button widget with theme-aware variants."""

    def __init__(
        self,
        parent: tk.Widget,
        button_type: Literal["PRIMARY", "SECONDARY", "DISABLED"] = "SECONDARY",
        **kwargs,
    ) -> None:
        """
        Initialize a styled button.

        Args:
            parent: Parent widget
            button_type: Button style variant (PRIMARY, SECONDARY, or DISABLED)
            **kwargs: Additional arguments passed to tk.Button
        """
        style = Theme.get_button_style(button_type)
        # Extract disabled colors (not supported on all platforms, especially macOS)
        disabled_bg = style.pop("disabledbackground")
        disabled_fg = style.pop("disabledforeground")
        # Merge style with kwargs (kwargs take precedence)
        button_kwargs = {**style, **kwargs}
        super().__init__(parent, **button_kwargs)
        # Try to set disabled colors (may not be supported on macOS)
        try:
            self.config(disabledbackground=disabled_bg, disabledforeground=disabled_fg)
        except tk.TclError:
            # Disabled colors not supported on this platform (e.g., macOS)
            # System will use default disabled appearance
            pass


class StyledLabel(tk.Label):
    """Styled label widget with theme colors."""

    def __init__(
        self,
        parent: tk.Widget,
        foreground: str | None = None,
        background: str | None = None,
        **kwargs,
    ) -> None:
        """
        Initialize a styled label.

        Args:
            parent: Parent widget
            foreground: Text color (defaults to Theme.TEXT_PRIMARY)
            background: Background color (defaults to Theme.BACKGROUND)
            **kwargs: Additional arguments passed to tk.Label
        """
        label_kwargs = {
            "foreground": foreground or Theme.TEXT_PRIMARY,
            "background": background or Theme.BACKGROUND,
            **kwargs,
        }
        super().__init__(parent, **label_kwargs)


class StyledEntry(tk.Entry):  # pylint: disable=too-many-ancestors
    """Styled entry widget with theme colors."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        parent: tk.Widget,
        background: str | None = None,
        foreground: str | None = None,
        insertbackground: str | None = None,
        selectbackground: str | None = None,
        selectforeground: str | None = None,
        highlightbackground: str | None = None,
        highlightcolor: str | None = None,
        **kwargs,
    ) -> None:
        """
        Initialize a styled entry field.

        Args:
            parent: Parent widget
            background: Background color (defaults to Theme.ENTRY_BACKGROUND)
            foreground: Text color (defaults to Theme.ENTRY_FOREGROUND)
            insertbackground: Cursor color (defaults to Theme.ENTRY_FOREGROUND)
            selectbackground: Selection background (defaults to Theme.PURPLE_LIGHT)
            selectforeground: Selection text (defaults to Theme.WHITE)
            highlightbackground: Border color when not focused (defaults to Theme.ENTRY_BORDER)
            highlightcolor: Border color when focused (defaults to Theme.PURPLE_LIGHTER)
            **kwargs: Additional arguments passed to tk.Entry
        """
        entry_kwargs = {
            "background": background or Theme.ENTRY_BACKGROUND,
            "foreground": foreground or Theme.ENTRY_FOREGROUND,
            "insertbackground": insertbackground or Theme.ENTRY_FOREGROUND,
            "selectbackground": selectbackground or Theme.PURPLE_LIGHT,
            "selectforeground": selectforeground or Theme.WHITE,
            "highlightbackground": highlightbackground or Theme.ENTRY_BORDER,
            "highlightcolor": highlightcolor or Theme.PURPLE_LIGHTER,
            "highlightthickness": 1,
            "borderwidth": 0,
            "relief": "flat",
            **kwargs,
        }
        super().__init__(parent, **entry_kwargs)


class StyledText(scrolledtext.ScrolledText):  # pylint: disable=too-many-ancestors
    """Styled text widget with theme colors for status/log areas."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        parent: tk.Widget,
        background: str | None = None,
        foreground: str | None = None,
        insertbackground: str | None = None,
        selectbackground: str | None = None,
        selectforeground: str | None = None,
        **kwargs,
    ) -> None:
        """
        Initialize a styled text area.

        Args:
            parent: Parent widget
            background: Background color (defaults to Theme.TEXT_AREA_BACKGROUND)
            foreground: Text color (defaults to Theme.TEXT_AREA_FOREGROUND)
            insertbackground: Cursor color (defaults to Theme.TEXT_AREA_FOREGROUND)
            selectbackground: Selection background (defaults to Theme.PURPLE_LIGHT)
            selectforeground: Selection text (defaults to Theme.WHITE)
            **kwargs: Additional arguments passed to scrolledtext.ScrolledText
        """
        text_kwargs = {
            "background": background or Theme.TEXT_AREA_BACKGROUND,
            "foreground": foreground or Theme.TEXT_AREA_FOREGROUND,
            "insertbackground": insertbackground or Theme.TEXT_AREA_FOREGROUND,
            "selectbackground": selectbackground or Theme.PURPLE_LIGHT,
            "selectforeground": selectforeground or Theme.WHITE,
            "borderwidth": 0,
            "relief": "flat",
            "wrap": tk.WORD,
            **kwargs,
        }
        super().__init__(parent, **text_kwargs)
