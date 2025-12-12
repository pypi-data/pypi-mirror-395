"""
キャンバスサイズ計算
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class CanvasSize:
    """キャンバスサイズ"""
    width: int
    height: int


def parse_aspect_ratio(ratio: str) -> Tuple[int, int]:
    """アスペクト比文字列をパース"""
    parts = ratio.split(":")
    return int(parts[0]), int(parts[1])


def calculate_canvas_size(
    aspect_ratio: str,
    base_width: int = 1080,
) -> CanvasSize:
    """アスペクト比からキャンバスサイズを計算"""
    w_ratio, h_ratio = parse_aspect_ratio(aspect_ratio)
    height = int(base_width * h_ratio / w_ratio)
    return CanvasSize(width=base_width, height=height)
