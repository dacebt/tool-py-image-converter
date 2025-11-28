"""
Theme color definitions and styling constants for the application.
"""

from typing import TypedDict


class ButtonStyle(TypedDict):
    """Button style configuration."""

    background: str
    foreground: str
    activebackground: str
    activeforeground: str
    disabledbackground: str
    disabledforeground: str
    borderwidth: int
    relief: str


class Theme:  # pylint: disable=too-few-public-methods
    """Deep purple theme with white and grayscale accents."""

    # Deep purple palette
    PURPLE_DARKEST = "#1A0D2E"  # Very dark purple (almost black)
    PURPLE_DARK = "#2D1B3D"  # Dark purple (main background)
    PURPLE_MEDIUM = "#4A2C5A"  # Medium purple
    PURPLE_LIGHT = "#6B46C1"  # Light purple (primary buttons)
    PURPLE_LIGHTER = "#8B5CF6"  # Lighter purple (hover states)

    # White and grayscale
    WHITE = "#FFFFFF"  # Primary text color
    GRAY_LIGHT = "#E5E7EB"  # Light gray (secondary text)
    GRAY_MEDIUM = "#9CA3AF"  # Medium gray
    GRAY_DARK = "#6B7280"  # Dark gray
    GRAY_DARKER = "#374151"  # Darker gray (secondary buttons)
    GRAY_DARKEST = "#1F2937"  # Darkest gray

    # Status colors
    WARNING = "#F59E0B"  # Amber/yellow for warnings
    ERROR = "#EF4444"  # Red for errors
    SUCCESS = "#10B981"  # Green for success

    # UI element colors
    BACKGROUND = PURPLE_DARK  # Main window background
    FRAME_BACKGROUND = PURPLE_MEDIUM  # Frame background
    TEXT_PRIMARY = WHITE  # Primary text color
    TEXT_SECONDARY = GRAY_LIGHT  # Secondary text color
    ENTRY_BACKGROUND = GRAY_DARKEST  # Entry field background
    ENTRY_FOREGROUND = WHITE  # Entry field text
    ENTRY_BORDER = PURPLE_LIGHT  # Entry field border
    TEXT_AREA_BACKGROUND = GRAY_DARKEST  # Text area background
    TEXT_AREA_FOREGROUND = WHITE  # Text area text

    @classmethod
    def get_button_style(cls, button_type: str) -> ButtonStyle:
        """
        Get button style configuration for the specified button type.

        Args:
            button_type: One of 'PRIMARY', 'SECONDARY', or 'DISABLED'

        Returns:
            ButtonStyle dictionary with styling configuration
        """
        if button_type == "PRIMARY":
            return ButtonStyle(
                background=cls.PURPLE_LIGHT,
                foreground=cls.WHITE,
                activebackground=cls.PURPLE_LIGHTER,
                activeforeground=cls.WHITE,
                disabledbackground=cls.GRAY_DARK,
                disabledforeground=cls.GRAY_MEDIUM,
                borderwidth=0,
                relief="flat",
            )
        if button_type == "SECONDARY":
            return ButtonStyle(
                background=cls.GRAY_DARKER,
                foreground=cls.WHITE,
                activebackground=cls.GRAY_DARK,
                activeforeground=cls.WHITE,
                disabledbackground=cls.GRAY_DARKEST,
                disabledforeground=cls.GRAY_MEDIUM,
                borderwidth=0,
                relief="flat",
            )
        if button_type == "DISABLED":
            return ButtonStyle(
                background=cls.GRAY_DARK,
                foreground=cls.GRAY_MEDIUM,
                activebackground=cls.GRAY_DARK,
                activeforeground=cls.GRAY_MEDIUM,
                disabledbackground=cls.GRAY_DARK,
                disabledforeground=cls.GRAY_MEDIUM,
                borderwidth=0,
                relief="flat",
            )
        # Default to secondary style
        return cls.get_button_style("SECONDARY")
