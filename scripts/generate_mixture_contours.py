#!/usr/bin/env python3
"""Generate smooth SVG contours for the research-page Gaussian mixture."""

from __future__ import annotations

import math
from collections import defaultdict
from pathlib import Path

WIDTH = 1000
HEIGHT = 426

X_MIN, X_MAX = 0.49, 0.94
Y_MIN, Y_MAX = 0.16, 0.82
COLS, ROWS = 180, 160
LEVELS = [0.22, 0.36, 0.52, 0.72]

MODES = [
    {"x": 0.65, "y": 0.36, "sx": 0.055, "sy": 0.065},
    {"x": 0.77, "y": 0.28, "sx": 0.062, "sy": 0.052},
    {"x": 0.84, "y": 0.48, "sx": 0.052, "sy": 0.068},
    {"x": 0.73, "y": 0.65, "sx": 0.067, "sy": 0.052},
    {"x": 0.60, "y": 0.56, "sx": 0.055, "sy": 0.062},
]


def density(x: float, y: float) -> float:
    total = 0.0
    for mode in MODES:
        dx = (x - mode["x"]) / mode["sx"]
        dy = (y - mode["y"]) / mode["sy"]
        total += math.exp(-0.5 * (dx * dx + dy * dy))
    return total


def to_px(point: tuple[float, float]) -> tuple[float, float]:
    return point[0] * WIDTH, point[1] * HEIGHT


def point_key(point: tuple[float, float]) -> tuple[int, int]:
    return round(point[0] * 1000), round(point[1] * 1000)


def interpolate(a: tuple[float, float, float], b: tuple[float, float, float], level: float) -> tuple[float, float]:
    denom = b[2] - a[2]
    t = 0.0 if abs(denom) < 1e-12 else (level - a[2]) / denom
    t = max(0.0, min(1.0, t))
    return a[0] + t * (b[0] - a[0]), a[1] + t * (b[1] - a[1])


def density_grid() -> list[list[float]]:
    return [
        [
            density(X_MIN + (X_MAX - X_MIN) * (col / COLS), Y_MIN + (Y_MAX - Y_MIN) * (row / ROWS))
            for col in range(COLS + 1)
        ]
        for row in range(ROWS + 1)
    ]


def contour_segments(values: list[list[float]], level: float) -> list[tuple[tuple[float, float], tuple[float, float]]]:
    segments = []

    for row in range(ROWS):
        for col in range(COLS):
            x0 = X_MIN + (X_MAX - X_MIN) * (col / COLS)
            x1 = X_MIN + (X_MAX - X_MIN) * ((col + 1) / COLS)
            y0 = Y_MIN + (Y_MAX - Y_MIN) * (row / ROWS)
            y1 = Y_MIN + (Y_MAX - Y_MIN) * ((row + 1) / ROWS)
            corners = [
                (x0, y0, values[row][col]),
                (x1, y0, values[row][col + 1]),
                (x1, y1, values[row + 1][col + 1]),
                (x0, y1, values[row + 1][col]),
            ]
            crossings = []

            for edge in range(4):
                a = corners[edge]
                b = corners[(edge + 1) % 4]
                if (a[2] < level <= b[2]) or (b[2] < level <= a[2]):
                    crossings.append(interpolate(a, b, level))

            if len(crossings) == 2:
                segments.append((crossings[0], crossings[1]))
            elif len(crossings) == 4:
                segments.append((crossings[0], crossings[1]))
                segments.append((crossings[2], crossings[3]))

    return segments


def stitch(segments: list[tuple[tuple[float, float], tuple[float, float]]]) -> list[list[tuple[float, float]]]:
    unused = set(range(len(segments)))
    by_key: dict[tuple[int, int], list[int]] = defaultdict(list)

    for index, segment in enumerate(segments):
        by_key[point_key(segment[0])].append(index)
        by_key[point_key(segment[1])].append(index)

    def connected(key: tuple[int, int]) -> int | None:
        return next((index for index in by_key.get(key, []) if index in unused), None)

    paths = []
    while unused:
        first_index = next(iter(unused))
        unused.remove(first_index)
        start, end = segments[first_index]
        path = [start, end]

        changed = True
        while changed:
            changed = False

            tail_match = connected(point_key(path[-1]))
            if tail_match is not None:
                unused.remove(tail_match)
                a, b = segments[tail_match]
                path.append(b if point_key(a) == point_key(path[-1]) else a)
                changed = True

            head_match = connected(point_key(path[0]))
            if head_match is not None:
                unused.remove(head_match)
                a, b = segments[head_match]
                path.insert(0, b if point_key(a) == point_key(path[0]) else a)
                changed = True

        if len(path) > 10:
            paths.append(path)

    return paths


def chaikin(points: list[tuple[float, float]], iterations: int = 2) -> list[tuple[float, float]]:
    closed = math.dist(points[0], points[-1]) < 0.004
    current = points[:-1] if closed else points

    for _ in range(iterations):
        refined = []
        pairs = zip(current, current[1:] + ([current[0]] if closed else []))
        for p0, p1 in pairs:
            refined.append((0.75 * p0[0] + 0.25 * p1[0], 0.75 * p0[1] + 0.25 * p1[1]))
            refined.append((0.25 * p0[0] + 0.75 * p1[0], 0.25 * p0[1] + 0.75 * p1[1]))
        current = refined

    return current + ([current[0]] if closed else [])


def path_d(points: list[tuple[float, float]]) -> str:
    smoothed = chaikin(points, iterations=3)
    px = [to_px(point) for point in smoothed]
    commands = [f"M {px[0][0]:.2f} {px[0][1]:.2f}"]
    for point in px[1:]:
        commands.append(f"L {point[0]:.2f} {point[1]:.2f}")
    if math.dist(smoothed[0], smoothed[-1]) < 0.004:
        commands.append("Z")
    return " ".join(commands)


def render_svg(stroke: str, fill: str, output: Path) -> None:
    values = density_grid()
    path_groups = []
    for level_index, level in enumerate(LEVELS):
        paths = stitch(contour_segments(values, level))
        opacity = 0.11 + 0.025 * level_index
        path_markup = "\n".join(
            f'    <path d="{path_d(path)}" />' for path in paths if len(path) > 16
        )
        path_groups.append(f'  <g opacity="{opacity:.2f}">\n{path_markup}\n  </g>')

    ellipses = "\n".join(
        (
            f'  <ellipse cx="{mode["x"] * WIDTH:.2f}" cy="{mode["y"] * HEIGHT:.2f}" '
            f'rx="{mode["sx"] * WIDTH * 1.5:.2f}" ry="{mode["sy"] * HEIGHT * 1.5:.2f}" />'
        )
        for mode in MODES
    )

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" fill="none">
  <g fill="{fill}" opacity="0.06" filter="url(#soften)">
{ellipses}
  </g>
  <g stroke="{stroke}" stroke-width="1.15" stroke-linecap="round" stroke-linejoin="round">
{chr(10).join(path_groups)}
  </g>
  <defs>
    <filter id="soften" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="18" />
    </filter>
  </defs>
</svg>
''',
        encoding="utf-8",
    )


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    asset_dir = root / "public" / "assets" / "research"
    render_svg("#2f7d75", "#2f7d75", asset_dir / "mixture-contours-light.svg")
    render_svg("#8dcfc4", "#8dcfc4", asset_dir / "mixture-contours-dark.svg")


if __name__ == "__main__":
    main()
