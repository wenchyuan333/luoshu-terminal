"""q5-stacked-boards: 幻方盤堆立方體 × AGL 逐層相對性 (nested under q4-affine).

一盤 (Board) = 64×64 = 4096 cells ≅ F_{2^12}
非零 = 4095 = |F_{4096}^*|
64 盤堆 = 64³ = 2^18 cube; 一盤 = 1 bit

Nested location: q4-affine/q5-stacked-boards/ (q4 → boost 64 層 → cube)
"""
from .board_stack import (
    BOARD_SIDE, BOARD_CELLS, BOARD_UNITS_STAR, STACK_DEPTH, CUBE_CELLS,
    BOARD_BITS, STACK_TOTAL_BITS, D4_ORDER, AGL_ORDER,
    cell_to_field, field_to_cell, d4_apply, relativity_boost,
    board_hash, stack_hash,
)

__all__ = [
    "BOARD_SIDE", "BOARD_CELLS", "BOARD_UNITS_STAR", "STACK_DEPTH", "CUBE_CELLS",
    "BOARD_BITS", "STACK_TOTAL_BITS", "D4_ORDER", "AGL_ORDER",
    "cell_to_field", "field_to_cell", "d4_apply", "relativity_boost",
    "board_hash", "stack_hash",
]
