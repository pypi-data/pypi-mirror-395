"""Protein structure ASCII projection utilities."""

from __future__ import annotations

import math
from typing import List, Tuple


class StructureService:
    """ASCII protein structure projection/animation utils."""

    def parse_pdb_ca(self, pdb_text: str) -> List[Tuple[float, float, float]]:
        """Parse CA atoms from PDB text, centered and normalized to unit radius."""
        points: List[Tuple[float, float, float]] = []
        for line in pdb_text.splitlines():
            if not line.startswith("ATOM"):
                continue
            name = line[12:16].strip()
            if name != "CA":
                continue
            try:
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                points.append((x, y, z))
            except Exception:
                continue
        if not points:
            return []
        cx = sum(p[0] for p in points) / len(points)
        cy = sum(p[1] for p in points) / len(points)
        cz = sum(p[2] for p in points) / len(points)
        centered = [(p[0] - cx, p[1] - cy, p[2] - cz) for p in points]
        max_radius = (
            max(math.sqrt(px * px + py * py + pz * pz) for px, py, pz in centered)
            or 1.0
        )
        scale = 1.0 / max_radius
        return [(px * scale, py * scale, pz * scale) for px, py, pz in centered]

    def render_ascii(
        self,
        points: List[Tuple[float, float, float]],
        angle: float,
        rows: int = 30,
        cols: int = 80,
    ) -> str:
        """Render a single ASCII projection frame at the provided angle."""
        if not points:
            return "No structure loaded"
        cos_angle = math.cos(angle)
        sin_angle = math.sin(angle)
        cos_beta = math.cos(angle * 0.5)
        sin_beta = math.sin(angle * 0.5)
        grid = [[" "] * cols for _ in range(rows)]
        charset = ".:*oO#@"
        step = max(1, len(points) // 1500 or 1)
        for x, y, z in points[::step]:
            x1 = cos_angle * x + sin_angle * z
            z1 = -sin_angle * x + cos_angle * z
            y1 = cos_beta * y - sin_beta * z1
            z2 = sin_beta * y + cos_beta * z1
            u = int((x1 * 0.5 + 0.5) * (cols - 1))
            v = int((y1 * 0.5 + 0.5) * (rows - 1))
            if 0 <= v < rows and 0 <= u < cols:
                depth = z2 * 0.5 + 0.5
                char = charset[
                    min(len(charset) - 1, max(0, int(depth * len(charset))))
                ]
                grid[v][u] = char
        return "\n".join("".join(row) for row in grid)

    def render_frame_advance(
        self,
        points: List[Tuple[float, float, float]],
        prev_angle: float,
        rows: int = 30,
        cols: int = 80,
        delta: float = 0.12,
    ) -> Tuple[str, float]:
        """Render a frame and advance angle; returns (ascii_art, new_angle)."""
        art = self.render_ascii(points, prev_angle, rows=rows, cols=cols)
        return art, prev_angle + delta


