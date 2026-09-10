from typing import List

# A strict 3x3 matrix of integers
Matrix3x3 = List[
    List[int]
]

EMPTY_FIELD = 0
CROSS_FIELD = 1
ZERO_FIELD = 2

class Board:
    def __init__(self):
        self.board: Matrix3x3 = [[EMPTY_FIELD for _ in range(3)] for _ in range(3)]

    def set(self, row: int, col: int, value: int) -> None:
        if row < 0 or row > 2:
            raise ValueError("Invalid row")
        if col < 0 or col > 2:
            raise ValueError("Invalid column")
        if value != CROSS_FIELD and value != ZERO_FIELD:
            raise ValueError("Invalid value")

        self.board[row][col] = value

    def reset(self) -> None:
        self.board: Matrix3x3 = [[EMPTY_FIELD for _ in range(3)] for _ in range(3)]

