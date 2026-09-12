from enum import Enum
from typing import List


class CellStatus(Enum):
    EMPTY_FIELD = 0
    CROSS_FIELD = 1
    ZERO_FIELD = 2

# A strict 3x3 matrix of integers
Matrix3x3 = List[
    List[CellStatus]
]

class Board:
    def __init__(self):
        self.board: Matrix3x3 = [[CellStatus.EMPTY_FIELD for _ in range(3)] for _ in range(3)]

    def set(self, row: int, col: int, value: CellStatus) -> None:
        if row < 0 or row > 2:
            raise ValueError("Invalid row")
        if col < 0 or col > 2:
            raise ValueError("Invalid column")
        if value == CellStatus.EMPTY_FIELD:
            raise ValueError("Invalid value")

        self.board[row][col] = value

    def reset(self) -> None:
        self.board: Matrix3x3 = [[CellStatus.EMPTY_FIELD for _ in range(3)] for _ in range(3)]

