"""Spinner frame presets for terminal UIs.

Note: Not all terminals render every Unicode glyph identically. Keep a few
ASCII-friendly presets as well. You can trim this list later.
"""

from __future__ import annotations

# filestate: python-constant-sort
# Braille-style spinner (smooth, compact, good Unicode support in modern terminals)
ARROW_FRAMES: list[str] = ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"]
ARROW_THIN_FRAMES: list[str] = ["←", "↖", "↑", "↗", "→", "↘", "↓", "↙"]
ASCII_WAVE_FRAMES: list[str] = ["_", "-", "^", "-", "_"]
BAR_FRAMES: list[str] = [
    "▁",
    "▂",
    "▃",
    "▄",
    "▅",
    "▆",
    "▇",
    "█",
    "▇",
    "▆",
    "▅",
    "▄",
    "▃",
    "▂",
]
BLOCK_SHADES_FRAMES: list[str] = ["░", "▒", "▓", "█", "▓", "▒"]
BOUNCE_FRAMES: list[str] = [
    "⠁",
    "⠂",
    "⠄",
    "⡀",
    "⢀",
    "⠠",
    "⠐",
    "⠈",
]
BRAILLE_SPINNER_FRAMES: list[str] = [
    "⣷",
    "⣯",
    "⣟",
    "⡿",
    "⢿",
    "⣻",
    "⣽",
    "⣾",
]
CIRCLE_QUADRANT_FRAMES: list[str] = [
    "◐",
    "◓",
    "◑",
    "◒",
]
CLASSIC_CIRCLE_FRAMES: list[str] = ["◴", "◷", "◶", "◵"]
CLOCK_FRAMES: list[str] = [
    "🕛",
    "🕐",
    "🕑",
    "🕒",
    "🕓",
    "🕔",
    "🕕",
    "🕖",
    "🕗",
    "🕘",
    "🕙",
    "🕚",
]
DEFAULT_SPINNER_FRAMES: list[str] = BRAILLE_SPINNER_FRAMES
DOT_PULSE_FRAMES: list[str] = ["∙    ", "∙∙   ", "∙∙∙  ", "∙∙∙∙ ", "∙∙∙∙∙", "     "]
DOTS_BOUNCE_FRAMES: list[str] = [".  ", ".. ", "...", " ..", "  .", "   "]
DOTS_FRAMES: list[str] = ["․  ", "․․ ", "․․․", "   "]
ELLIPSIS_FRAMES: list[str] = ["", ".", "..", "..."]
GROW_VERTICAL_FRAMES: list[str] = ["▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"]
LINE_SPINNER_FRAMES: list[str] = ["-", "\\", "|", "/"]
PIPE_SPINNER_FRAMES: list[str] = ["|", "/", "-", "\\"]
QUADRANT_FRAMES: list[str] = ["▖", "▘", "▝", "▗"]
SQUARE_FRAMES: list[str] = ["▖", "▘", "▝", "▗"]
TOGGLE_FRAMES: list[str] = ["⊶", "⊷"]
TOGGLE_SQUARE_FRAMES: list[str] = ["▮", "▯"]
TRIANGLE_FRAMES: list[str] = ["◢", "◣", "◤", "◥"]
