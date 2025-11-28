"""
Theme color definitions and styling constants for the application.
"""


class Theme:  # pylint: disable=too-few-public-methods
    """Sophisticated deep purple theme with high contrast and refined colors."""

    # Rich purple palette - deeper, more saturated
    PURPLE_DARKEST = "#0F0520"  # Deepest purple-black
    PURPLE_DARK = "#1A0F2E"  # Dark purple (main background)
    PURPLE_MEDIUM = "#2D1B4A"  # Medium purple (subtle accents)
    PURPLE_BRIGHT = "#5B2C91"  # Bright purple (primary buttons)
    PURPLE_VIBRANT = "#7C3AED"  # Vibrant purple (hover/active)
    PURPLE_LIGHT = "#A78BFA"  # Light purple (highlights)

    # Refined grayscale with purple undertones
    WHITE = "#FFFFFF"  # Pure white for maximum contrast
    GRAY_NEAR_WHITE = "#F3F4F6"  # Near-white (subtle backgrounds)
    GRAY_LIGHT = "#D1D5DB"  # Light gray (secondary text)
    GRAY_MEDIUM = "#9CA3AF"  # Medium gray (disabled states)
    GRAY_DARK = "#4B5563"  # Dark gray
    GRAY_DARKER = "#374151"  # Darker gray
    GRAY_DARKEST = "#1F2937"  # Darkest gray

    # Accent colors with purple harmony
    ACCENT_BLUE = "#6366F1"  # Indigo-blue accent
    ACCENT_TEAL = "#14B8A6"  # Teal accent
    ACCENT_PINK = "#EC4899"  # Pink accent

    # Status colors - refined and harmonious
    WARNING = "#F59E0B"  # Warm amber
    ERROR = "#EF4444"  # Clear red
    SUCCESS = "#10B981"  # Fresh green

    # UI element colors
    BACKGROUND = PURPLE_DARK  # Main window background
    FRAME_BACKGROUND = PURPLE_MEDIUM  # Frame background
    TEXT_PRIMARY = WHITE  # Primary text color
    TEXT_SECONDARY = GRAY_LIGHT  # Secondary text color
    ENTRY_BACKGROUND = "#0F0520"  # Very dark for entry fields
    ENTRY_FOREGROUND = WHITE  # Entry field text
    ENTRY_BORDER = PURPLE_BRIGHT  # Entry field border
    TEXT_AREA_BACKGROUND = "#0F0520"  # Very dark for text areas
    TEXT_AREA_FOREGROUND = GRAY_LIGHT  # Text area text (slightly softer)

    @classmethod
    def get_stylesheet(cls) -> str:
        """
        Get complete PyQt6 stylesheet (QSS) for the application.

        Returns:
            Complete QSS string with all widget styles
        """
        return f"""
        /* Main window background */
        QMainWindow {{
            background-color: {cls.BACKGROUND};
        }}

        /* Widget backgrounds */
        QWidget {{
            background-color: {cls.BACKGROUND};
            color: {cls.TEXT_PRIMARY};
        }}

        QFrame {{
            background-color: {cls.FRAME_BACKGROUND};
        }}

        /* Primary button style */
        QPushButton.primary-button {{
            background-color: {cls.PURPLE_BRIGHT};
            color: {cls.WHITE};
            border: 3px solid {cls.PURPLE_BRIGHT};
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            cursor: pointer;
        }}

        QPushButton.primary-button:hover {{
            background-color: {cls.PURPLE_VIBRANT};
            border-color: {cls.PURPLE_VIBRANT};
        }}

        QPushButton.primary-button:pressed {{
            background-color: {cls.PURPLE_VIBRANT};
            border-color: {cls.PURPLE_VIBRANT};
        }}

        QPushButton.primary-button:disabled {{
            background-color: {cls.GRAY_DARK};
            color: {cls.GRAY_MEDIUM};
            border-color: {cls.GRAY_DARK};
        }}

        /* Secondary button style */
        QPushButton.secondary-button {{
            background-color: {cls.ACCENT_BLUE};
            color: {cls.WHITE};
            border: 3px solid {cls.ACCENT_BLUE};
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: bold;
            cursor: pointer;
        }}

        QPushButton.secondary-button:hover {{
            background-color: {cls.PURPLE_VIBRANT};
            border-color: {cls.PURPLE_VIBRANT};
        }}

        QPushButton.secondary-button:pressed {{
            background-color: {cls.PURPLE_VIBRANT};
            border-color: {cls.PURPLE_VIBRANT};
        }}

        QPushButton.secondary-button:disabled {{
            background-color: {cls.GRAY_DARKEST};
            color: {cls.GRAY_MEDIUM};
            border-color: {cls.GRAY_DARKEST};
        }}

        /* Disabled button style */
        QPushButton.disabled-button {{
            background-color: {cls.GRAY_DARKEST};
            color: {cls.GRAY_MEDIUM};
            border: 2px solid {cls.GRAY_DARKEST};
            border-radius: 4px;
            padding: 8px 16px;
        }}

        /* Label styles */
        QLabel {{
            background-color: {cls.BACKGROUND};
            color: {cls.TEXT_PRIMARY};
        }}

        /* Entry field (QLineEdit) styles */
        QLineEdit {{
            background-color: {cls.ENTRY_BACKGROUND};
            color: {cls.ENTRY_FOREGROUND};
            border: 1px solid {cls.ENTRY_BORDER};
            border-radius: 4px;
            padding: 6px 8px;
        }}

        QLineEdit:focus {{
            border: 1px solid {cls.PURPLE_VIBRANT};
        }}

        QLineEdit::selection {{
            background-color: {cls.PURPLE_BRIGHT};
            color: {cls.WHITE};
        }}

        /* Text area (QTextEdit) styles */
        QTextEdit {{
            background-color: {cls.TEXT_AREA_BACKGROUND};
            color: {cls.TEXT_AREA_FOREGROUND};
            border: 1px solid {cls.ENTRY_BORDER};
            border-radius: 4px;
            padding: 6px 8px;
        }}

        QTextEdit:focus {{
            border: 1px solid {cls.PURPLE_VIBRANT};
        }}

        QTextEdit::selection {{
            background-color: {cls.PURPLE_BRIGHT};
            color: {cls.WHITE};
        }}

        /* Scrollbar styles */
        QScrollBar:vertical {{
            background-color: {cls.PURPLE_MEDIUM};
            width: 12px;
            border: none;
        }}

        QScrollBar::handle:vertical {{
            background-color: {cls.PURPLE_BRIGHT};
            min-height: 20px;
            border-radius: 6px;
        }}

        QScrollBar::handle:vertical:hover {{
            background-color: {cls.PURPLE_VIBRANT};
        }}

        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
        }}

        QScrollBar:horizontal {{
            background-color: {cls.PURPLE_MEDIUM};
            height: 12px;
            border: none;
        }}

        QScrollBar::handle:horizontal {{
            background-color: {cls.PURPLE_BRIGHT};
            min-width: 20px;
            border-radius: 6px;
        }}

        QScrollBar::handle:horizontal:hover {{
            background-color: {cls.PURPLE_VIBRANT};
        }}

        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
        """

    @classmethod
    def get_button_stylesheet(cls, button_type: str) -> str:
        """
        Get stylesheet for a specific button type.

        Args:
            button_type: One of 'PRIMARY', 'SECONDARY', or 'DISABLED'

        Returns:
            QSS string for the button type
        """
        if button_type == "PRIMARY":
            return f"""
                QPushButton {{
                    background-color: {cls.PURPLE_BRIGHT};
                    color: {cls.WHITE};
                    border: 3px solid {cls.PURPLE_BRIGHT};
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                    cursor: pointer;
                }}
                QPushButton:hover {{
                    background-color: {cls.PURPLE_VIBRANT};
                    border-color: {cls.PURPLE_VIBRANT};
                }}
                QPushButton:pressed {{
                    background-color: {cls.PURPLE_VIBRANT};
                    border-color: {cls.PURPLE_VIBRANT};
                }}
                QPushButton:disabled {{
                    background-color: {cls.GRAY_DARK};
                    color: {cls.GRAY_MEDIUM};
                    border-color: {cls.GRAY_DARK};
                }}
            """
        if button_type == "SECONDARY":
            return f"""
                QPushButton {{
                    background-color: {cls.ACCENT_BLUE};
                    color: {cls.WHITE};
                    border: 3px solid {cls.ACCENT_BLUE};
                    border-radius: 4px;
                    padding: 8px 16px;
                    font-weight: bold;
                    cursor: pointer;
                }}
                QPushButton:hover {{
                    background-color: {cls.PURPLE_VIBRANT};
                    border-color: {cls.PURPLE_VIBRANT};
                }}
                QPushButton:pressed {{
                    background-color: {cls.PURPLE_VIBRANT};
                    border-color: {cls.PURPLE_VIBRANT};
                }}
                QPushButton:disabled {{
                    background-color: {cls.GRAY_DARKEST};
                    color: {cls.GRAY_MEDIUM};
                    border-color: {cls.GRAY_DARKEST};
                }}
            """
        if button_type == "DISABLED":
            return f"""
                QPushButton {{
                    background-color: {cls.GRAY_DARKEST};
                    color: {cls.GRAY_MEDIUM};
                    border: 2px solid {cls.GRAY_DARKEST};
                    border-radius: 4px;
                    padding: 8px 16px;
                }}
            """
        # Default to secondary
        return cls.get_button_stylesheet("SECONDARY")
