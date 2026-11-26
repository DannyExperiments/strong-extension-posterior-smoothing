#!/usr/bin/env python3
"""Render the two exact fixed-half worked examples."""
from functools import lru_cache
from math import cos, pi, sin
from os import environ
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 648, 442
BG, PANEL = "#0b1627", "#14273e"
INK, MUTED = "#eff7fe", "#bed2e3"
PLUS, MINUS, GOLD = "#68e4c2", "#ffb082", "#f9d66d"
CASES = (
    ("x AND x", ("C1: x", "C2: x"), (0, 0, 0, 1), "3/4", "1/2"),
    ("x AND NOT x", ("C1: x", "C2: not x"), (0, 1, 0, 1), "7/12", "7/16"),
)


@lru_cache
def font(size, bold=False):
    key = "Q432_BOLD_FONT" if bold else "Q432_FONT"
    name = "Arial Bold.ttf" if bold else "Arial.ttf"
    local = Path("/System/Library/Fonts/Supplemental") / name
    return ImageFont.truetype(environ.get(key, str(local)), size)


def label(draw, position, text, size, color=INK, bold=False, anchor=None):
    draw.text(position, text, fill=color, font=font(size, bold), anchor=anchor)


def image(case, turn):
    title, clauses, routes, rplus, result = case
    frame = Image.new("RGB", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(frame)
    label(d, (20, 12), "One late observation, two branches", 31, bold=True)
    label(d, (20, 56), f"Formula: {title}", 23, GOLD, True)
    d.rounded_rectangle((14, 92, 634, 337), radius=16, fill=PANEL)
    for x, text in ((98, "1 · Start"), (310, "2 · Route"), (535, "3 · Emit")):
        label(d, (x, 112), text, 19, MUTED, True, "mm")

    def project(item):
        x, y, z = item
        return x + 0.2*z*sin(turn), 223 + y*cos(turn) - z*sin(turn)

    source = tuple(map(project, ((98, -50, 25), (98, 64, -24))))
    unit = tuple(map(project, ((310, -74, 8), (310, -30, -12), (310, 14, 9), (310, 68, -18))))
    literal = tuple(map(project, ((535, -44, -16), (535, 57, 18))))

    def link(a, b, color):
        x, y = a
        xx, yy = b
        d.line(((x+51, y), (xx-62, yy)), fill=color, width=3)
        d.polygon(((xx-62, yy), (xx-70, yy-4), (xx-70, yy+4)), fill=color)

    def node(at, text, color, width=117):
        x, y = at
        d.rounded_rectangle((x-width/2, y-15, x+width/2, y+15), radius=8,
                            fill=BG, outline=color, width=2)
        label(d, at, text, 20, color, True, "mm")

    for i, at in enumerate(unit):
        color = MINUS if i == 3 else PLUS
        link(source[1 if i == 3 else 0], at, color)
        link(at, literal[routes[i]], color)
    for at, text, color in zip(source, ("+ : 1/4", "- : 3/4"), (PLUS, MINUS)):
        node(at, text, color, 101)
    for i, (at, text) in enumerate(zip(unit, clauses + ("Variable +", "Variable -"))):
        node(at, text, MINUS if i == 3 else PLUS)
    for at, text in zip(literal, ("x : 3/4", "not x : 1/4")):
        node(at, text, GOLD, 128)
    label(d, (20, 352), f"Evidence likelihoods: + {rplus}    - 1/4", 23, bold=True)
    label(d, (20, 389), f"Upper posterior: {result}", 25, PLUS, True)
    label(d, (385, 392), "Cutoff = 1/2", 22, MUTED, True)
    return frame


if __name__ == "__main__":
    frames = [image(case, .46*sin(2*pi*i/18)) for case in CASES for i in range(18)]
    palette_samples = Image.new("RGB", (2*WIDTH, HEIGHT))
    palette_samples.paste(frames[0], (0, 0))
    palette_samples.paste(frames[18], (WIDTH, 0))
    palette = palette_samples.quantize(colors=96)
    frames = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    output = Path(__file__).with_name("three-time-smoothing.gif")
    frames[0].save(output, save_all=True, append_images=frames[1:], duration=150, loop=0, optimize=True)
