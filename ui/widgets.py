"""
Custom styled widget classes that apply the application theme.
"""

from typing import Literal

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QTextEdit

from ui.theme import Theme


class StyledButton(QPushButton):  # pylint: disable=too-many-ancestors
    """Styled button widget with theme-aware variants."""

    def __init__(
        self,
        parent,
        button_type: Literal["PRIMARY", "SECONDARY", "DISABLED"] = "SECONDARY",
        text: str = "",
        **kwargs,
    ) -> None:
        """
        Initialize a styled button.

        Args:
            parent: Parent widget
            button_type: Button style variant (PRIMARY, SECONDARY, or DISABLED)
            text: Button text
            **kwargs: Additional arguments passed to QPushButton
        """
        super().__init__(text, parent)
        
        # Apply stylesheet based on button type
        button_stylesheet = Theme.get_button_stylesheet(button_type)
        self.setStyleSheet(button_stylesheet)
        
        if button_type == "DISABLED":
            self.setEnabled(False)
        
        # Apply any additional kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                getattr(self, key)(value)


class StyledLabel(QLabel):
    """Styled label widget with theme colors."""

    def __init__(
        self,
        parent,
        text: str = "",
        foreground: str | None = None,
        background: str | None = None,
        **kwargs,
    ) -> None:
        """
        Initialize a styled label.

        Args:
            parent: Parent widget
            text: Label text
            foreground: Text color (defaults to Theme.TEXT_PRIMARY)
            background: Background color (defaults to Theme.BACKGROUND)
            **kwargs: Additional arguments passed to QLabel
        """
        super().__init__(text, parent)
        
        # Apply colors via stylesheet
        fg_color = foreground or Theme.TEXT_PRIMARY
        bg_color = background or Theme.BACKGROUND
        
        self.setStyleSheet(f"""
            QLabel {{
                color: {fg_color};
                background-color: {bg_color};
            }}
        """)
        
        # Apply any additional kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                getattr(self, key)(value)


class StyledEntry(QLineEdit):  # pylint: disable=too-many-ancestors
    """Styled entry widget with theme colors."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        parent,
        background: str | None = None,
        foreground: str | None = None,
        insertbackground: str | None = None,  # pylint: disable=unused-argument
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
            selectbackground: Selection background (defaults to Theme.PURPLE_BRIGHT)
            selectforeground: Selection text (defaults to Theme.WHITE)
            highlightbackground: Border color when not focused (defaults to Theme.ENTRY_BORDER)
            highlightcolor: Border color when focused (defaults to Theme.PURPLE_VIBRANT)
            **kwargs: Additional arguments passed to QLineEdit
        """
        super().__init__(parent)
        
        # Use theme defaults if not specified
        bg_color = background or Theme.ENTRY_BACKGROUND
        fg_color = foreground or Theme.ENTRY_FOREGROUND
        sel_bg = selectbackground or Theme.PURPLE_BRIGHT
        sel_fg = selectforeground or Theme.WHITE
        border_color = highlightbackground or Theme.ENTRY_BORDER
        focus_color = highlightcolor or Theme.PURPLE_VIBRANT
        
        # Apply stylesheet
        self.setStyleSheet(f"""
            QLineEdit {{
                background-color: {bg_color};
                color: {fg_color};
                border: 1px solid {border_color};
                border-radius: 4px;
                padding: 6px 8px;
            }}
            QLineEdit:focus {{
                border: 1px solid {focus_color};
            }}
            QLineEdit::selection {{
                background-color: {sel_bg};
                color: {sel_fg};
            }}
        """)
        
        # Apply any additional kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                getattr(self, key)(value)


class StyledText(QTextEdit):  # pylint: disable=too-many-ancestors
    """Styled text widget with theme colors for status/log areas."""

    def __init__(  # pylint: disable=too-many-arguments
        self,
        parent,
        background: str | None = None,
        foreground: str | None = None,
        insertbackground: str | None = None,  # pylint: disable=unused-argument
        selectbackground: str | None = None,
        selectforeground: str | None = None,
        height: int | None = None,  # pylint: disable=unused-argument
        state: str | None = None,
        **kwargs,
    ) -> None:
        """
        Initialize a styled text area.

        Args:
            parent: Parent widget
            background: Background color (defaults to Theme.TEXT_AREA_BACKGROUND)
            foreground: Text color (defaults to Theme.TEXT_AREA_FOREGROUND)
            insertbackground: Cursor color (defaults to Theme.TEXT_AREA_FOREGROUND)
            selectbackground: Selection background (defaults to Theme.PURPLE_BRIGHT)
            selectforeground: Selection text (defaults to Theme.WHITE)
            height: Preferred height in lines (not directly used in PyQt6, kept for compatibility)
            state: "disabled" or "normal" - sets read-only state
            **kwargs: Additional arguments passed to QTextEdit
        """
        super().__init__(parent)
        
        # Use theme defaults if not specified
        bg_color = background or Theme.TEXT_AREA_BACKGROUND
        fg_color = foreground or Theme.TEXT_AREA_FOREGROUND
        sel_bg = selectbackground or Theme.PURPLE_BRIGHT
        sel_fg = selectforeground or Theme.WHITE
        
        # Apply stylesheet
        self.setStyleSheet(f"""
            QTextEdit {{
                background-color: {bg_color};
                color: {fg_color};
                border: 1px solid {Theme.ENTRY_BORDER};
                border-radius: 4px;
                padding: 6px 8px;
            }}
            QTextEdit:focus {{
                border: 1px solid {Theme.PURPLE_VIBRANT};
            }}
            QTextEdit::selection {{
                background-color: {sel_bg};
                color: {sel_fg};
            }}
        """)
        
        # Handle state (read-only)
        if state in ("disabled", "DISABLED"):
            self.setReadOnly(True)
        else:
            self.setReadOnly(False)
        
        # Set word wrap
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        
        # Apply any additional kwargs
        for key, value in kwargs.items():
            if hasattr(self, key):
                getattr(self, key)(value)
