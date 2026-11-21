#!/usr/bin/env python3
"""VELMORA - a travel poster for a place that isn't there.

Writes /output/entry.png (1024x1024 RGB PNG) using only the standard
library. Deterministic: fixed seed, no clock, no network, no fonts.
Pure-Python PNG encoder (zlib + struct). Bitmap 5x7 font authored here.
"""

import math
import os
import random
import struct
import zlib

W = 1024
H = 1024
OUT = "/output/entry.png"

# ---------------------------------------------------------------- palette
INK = (24, 18, 44)        # deep indigo, title block
CREAM = (250, 238, 210)   # title cream
GOLD = (244, 196, 108)    # sun gold
CORAL = (232, 122, 88)    # sunset coral
TEAL_D = (16, 84, 96)     # deep sea teal
TEAL = (34, 138, 138)     # sea teal
TEAL_L = (92, 190, 178)   # light sea
PURPLE = (74, 52, 110)    # far ridge
PURPLE_L = (104, 78, 138) # near ridge
GREEN = (46, 120, 84)     # island grass
GREEN_D = (30, 88, 62)
ROCK = (122, 84, 96)      # island underside
ROCK_D = (88, 58, 74)
SKY_TOP = (38, 32, 86)
SKY_MID = (96, 62, 118)
SKY_LOW = (214, 110, 84)

# ---------------------------------------------------------------- bitmap font
# 5 wide x 7 tall, '#' = on. Authored in this session.
FONT = {
    "A": (".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "B": ("####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."),
    "C": (".####", "#....", "#....", "#....", "#....", "#....", ".####"),
    "D": ("####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."),
    "E": ("#####", "#....", "#....", "####.", "#....", "#....", "#####"),
    "F": ("#####", "#....", "#....", "####.", "#....", "#....", "#...."),
    "G": (".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."),
    "H": ("#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"),
    "I": (".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "J": ("..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."),
    "K": ("#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"),
    "L": ("#....", "#....", "#....", "#....", "#....", "#....", "#####"),
    "M": ("#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "#...#", "####.", "#....", "#....", "#...."),
    "Q": (".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"),
    "R": ("####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"),
    "S": (".####", "#....", "#....", ".###.", "....#", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "W": ("#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"),
    "X": ("#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"),
    "Y": ("#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."),
    "Z": ("#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"),
    "0": (".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."),
    "1": ("..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."),
    "2": (".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"),
    "3": ("####.", "....#", "....#", ".###.", "....#", "....#", "####."),
    "4": ("...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."),
    "5": ("#####", "#....", "####.", "....#", "....#", "#...#", ".###."),
    "6": (".###.", "#....", "####.", "#...#", "#...#", "#...#", ".###."),
    "7": ("#####", "....#", "...#.", "...#.", "..#..", "..#..", "..#.."),
    "8": (".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."),
    "9": (".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."),
    ".": (".....", ".....", ".....", ".....", ".....", ".##..", ".##.."),
    "-": (".....", ".....", ".....", ".###.", ".....", ".....", "....."),
    "'": ("..#..", "..#..", ".....", ".....", ".....", ".....", "....."),
    "*": (".....", ".....", ".##..", ".##..", ".##..", ".....", "....."),
    " ": (".....", ".....", ".....", ".....", ".....", ".....", "....."),
}

# ---------------------------------------------------------------- canvas
buf = bytearray(W * H * 3)


def px(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i], buf[i + 1], buf[i + 2] = c


def rect(x0, y0, x1, y1, c):
    x0 = max(0, x0); y0 = max(0, y0)
    x1 = min(W, x1); y1 = min(H, y1)
    for y in range(y0, y1):
        i = (y * W + x0) * 3
        r, g, b = c
        for x in range(x0, x1):
            buf[i] = r; buf[i + 1] = g; buf[i + 2] = b
            i += 3


def hline(x0, x1, y, c):
    if 0 <= y < H:
        for x in range(max(0, x0), min(W, x1)):
            px(x, y, c)


def lerp(a, b, t):
    return tuple(int(a[k] + (b[k] - a[k]) * t) for k in range(3))


def vgrad(y0, y1, c0, c1, steps=48):
    # banded gradient: few flat bands compress far better in the PNG
    span = max(1, y1 - y0)
    for s in range(steps):
        ya = y0 + span * s // steps
        yb = y0 + span * (s + 1) // steps
        rect(0, ya, W, yb, lerp(c0, c1, s / max(1, steps - 1)))


def disc(cx, cy, r, c):
    for y in range(cy - r, cy + r + 1):
        dy = y - cy
        dx = int(math.sqrt(max(0, r * r - dy * dy)))
        hline(cx - dx, cx + dx + 1, y, c)


def ring(cx, cy, rx, ry, thick, c):
    # flat elliptical ring band, drawn as two arcs of short segments
    for k in range(361):
        a = math.radians(k)
        for t in range(thick):
            x = int(cx + (rx + t - thick // 2) * math.cos(a))
            y = int(cy + (ry + t - thick // 2) * math.sin(a) * 0.32)
            px(x, y, c)


def poly(points, c):
    # scanline fill of a simple polygon
    ys = [p[1] for p in points]
    for y in range(max(0, min(ys)), min(H, max(ys) + 1)):
        xs = []
        n = len(points)
        for i in range(n):
            x0, y0 = points[i]
            x1, y1 = points[(i + 1) % n]
            if (y0 <= y < y1) or (y1 <= y < y0):
                t = (y - y0) / (y1 - y0)
                xs.append(x0 + t * (x1 - x0))
        xs.sort()
        for j in range(0, len(xs) - 1, 2):
            hline(int(xs[j]), int(xs[j + 1]) + 1, y, c)


def ridge(base_y, amp, color, seed, step=16):
    rng = random.Random(seed)
    pts = [(-20, H)]
    x = -20
    while x < W + 20:
        pts.append((x, base_y - rng.randint(0, amp)))
        x += step
    pts.append((W + 20, H))
    poly(pts, color)


def text(s, x, y, scale, c, gap=None):
    if gap is None:
        gap = scale
    cx = x
    for ch in s:
        glyph = FONT.get(ch, FONT[" "])
        for row in range(7):
            for col in range(5):
                if glyph[row][col] == "#":
                    rect(cx + col * scale, y + row * scale,
                         cx + (col + 1) * scale, y + (row + 1) * scale, c)
        cx += 6 * scale + gap
    return cx


def text_w(s, scale, gap=None):
    if gap is None:
        gap = scale
    return len(s) * (6 * scale + gap) - gap


def centered(s, y, scale, c):
    text(s, (W - text_w(s, scale)) // 2, y, scale, c)


# ---------------------------------------------------------------- scene
# Sky: indigo top -> violet -> coral horizon
vgrad(0, 300, SKY_TOP, SKY_MID, 24)
vgrad(300, 640, SKY_MID, SKY_LOW, 24)

# Stars in the upper sky (fixed seed)
rng = random.Random(20261121)
for _ in range(90):
    sx = rng.randint(0, W - 1)
    sy = rng.randint(0, 240)
    sc = rng.choice([CREAM, GOLD, (200, 200, 230)])
    px(sx, sy, sc)
    if rng.random() < 0.25:
        px(sx + 1, sy, sc)

# Ringed planet / great sun
disc(700, 268, 132, GOLD)
disc(700, 268, 108, (250, 214, 140))
disc(700, 268, 84, (252, 228, 168))
ring(700, 268, 205, 205, 7, CREAM)
ring(700, 268, 232, 232, 4, GOLD)

# Far ridge
ridge(640, 150, PURPLE, 11)
# Near ridge
ridge(640, 90, PURPLE_L, 23)

# Floating islands -------------------------------------------------------
def island(cx, top, w, h, seed):
    r = random.Random(seed)
    # grassy top
    poly([(cx - w, top), (cx + w, top),
          (cx + int(w * 0.72), top + int(h * 0.55)),
          (cx + int(w * 0.30), top + h),
          (cx - int(w * 0.30), top + h),
          (cx - int(w * 0.72), top + int(h * 0.55))], GREEN)
    poly([(cx - w, top), (cx + w, top),
          (cx + int(w * 0.72), top + int(h * 0.55)),
          (cx + int(w * 0.30), top + h),
          (cx - int(w * 0.30), top + h),
          (cx - int(w * 0.72), top + int(h * 0.55))], GREEN)
    # rock underside
    poly([(cx - int(w * 0.72), top + int(h * 0.55)),
          (cx + int(w * 0.72), top + int(h * 0.55)),
          (cx + int(w * 0.18), top + int(h * 1.9)),
          (cx - int(w * 0.18), top + int(h * 1.9))], ROCK)
    poly([(cx - int(w * 0.40), top + int(h * 0.55)),
          (cx + int(w * 0.40), top + int(h * 0.55)),
          (cx + int(w * 0.10), top + int(h * 1.9)),
          (cx - int(w * 0.10), top + int(h * 1.9))], ROCK_D)
    # trees: little triangles
    for _ in range(7):
        tx = cx + r.randint(-w + 18, w - 18)
        th = r.randint(16, 30)
        poly([(tx, top - th), (tx - 9, top), (tx + 9, top)], GREEN_D)
        rect(tx - 1, top, tx + 2, top + 6, (60, 40, 30))
    # waterfall falling from the island edge
    fx = cx + r.randint(-w // 2, w // 2)
    for wy in range(top + h, top + h + 150, 6):
        rect(fx - 3, wy, fx + 3, wy + 4, (210, 235, 240))
        rect(fx + 8, wy + 3, fx + 11, wy + 6, (180, 215, 225))


island(300, 330, 190, 46, 5)
island(760, 420, 130, 38, 9)
island(150, 470, 90, 30, 13)

# Sea: teal gradient with sun reflection
vgrad(640, H, TEAL_D, TEAL, 20)
vgrad(640, 700, TEAL, TEAL_L, 6)
# sun glitter column under the planet
for k in range(46):
    gy = 660 + k * 7
    gw = 26 + k * 3
    hline(700 - gw, 700 + gw, gy, GOLD if k % 3 else (250, 214, 140))
    hline(700 - gw // 2, 700 + gw // 2, gy + 3, (250, 226, 170))
# wave streaks (fixed seed)
rng = random.Random(77)
for _ in range(70):
    wx = rng.randint(0, W - 60)
    wy = rng.randint(660, 1000)
    wl = rng.randint(20, 70)
    hline(wx, wx + wl, wy, TEAL_L if rng.random() < 0.5 else (150, 205, 195))

# Birds
def bird(bx, by, s, c):
    for k in range(s):
        px(bx - k, by - k // 2, c)
        px(bx + k, by - k // 2, c)


for bx, by, bs, bc in [(180, 210, 9, INK), (240, 180, 7, INK), (520, 150, 8, INK),
                   (860, 200, 9, INK), (600, 120, 6, INK)]:
    bird(bx, by, bs, bc)

# ---------------------------------------------------------------- title block
# dark band across the lower sea, title in cream
rect(0, 812, W, 1024, INK)
hline(0, W, 812, GOLD)
hline(0, W, 816, GOLD)
centered("VELMORA", 852, 13, CREAM)
# gold rule under title
tw = text_w("VELMORA", 13)
rect((W - tw) // 2, 852 + 7 * 13 + 16, (W + tw) // 2, 852 + 7 * 13 + 20, GOLD)
centered("THE ISLES THAT RISE WITH THE TIDE", 972, 4, GOLD)

# ---------------------------------------------------------------- PNG encode
def chunk(typ, data):
    out = struct.pack(">I", len(data)) + typ + data
    out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    return out


def main():
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter none
        raw += buf[y * W * 3:(y + 1) * W * 3]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = (b"\x89PNG\r\n\x1a\n"
           + chunk(b"IHDR", ihdr)
           + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
           + chunk(b"IEND", b""))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(png)
    print("wrote", OUT, len(png), "bytes")


if __name__ == "__main__":
    main()
