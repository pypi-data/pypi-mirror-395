#!/usr/bin/env python3
# src/geminiai_cli/ui.py


import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.text import Text

from .config import NEON_GREEN, NEON_CYAN, NEON_YELLOW, NEON_MAGENTA, NEON_RED, RESET

# Export console for use in other modules
console = Console()

def cprint(color, text):
    """
    Legacy cprint wrapper using rich.
    concatenates color (ANSI) + text + RESET and renders it using Text.from_ansi
    to ensure ANSI codes are displayed correctly.
    """
    # Check if color or text is None to prevent TypeError
    color = str(color) if color is not None else ""
    text = str(text) if text is not None else ""

    # Check if color is an ANSI string.
    # If it is an ANSI string, Text.from_ansi will parse it.

    full_text = color + text + RESET

    try:
        # Use simple print if we suspect Text.from_ansi is causing issues with nested styles in Rich
        # Or just strip ANSI codes if we want to be safe, but we want colors.

        # The error seems to be deeper in Rich when it encounters a Style object where it expects a string.
        # This might be because we are feeding it something that it tries to parse as a style name but fails.
        # However, we are passing a Text object to console.print()

        # Let's try to just print the text with the color style if 'color' argument matches known styles.
        # But 'color' here is an ANSI code string.

        console.print(Text.from_ansi(full_text))
    except AttributeError:
        # Fallback to standard print if Rich fails
        print(full_text)

def banner():
    """
    Displays the ALICE banner using a Rich Panel.
    """
    title = "[bold cyan]🚀  ALICE (GEMINI AUTOMATION)  🚀[/]"
    panel = Panel(Align.center(title), style="bold magenta", expand=False)
    console.print(panel)
    console.print("") # Newline
