from typing import List

from app.board import Board

EMPTY = 0
CROSS_WIN = 1
ZEROS_WIN = 2
DRAW = 3

class Validator:
    def __init__(self, board: Board):
        self.board = board

    def _validate_row(self, row : List[int]) -> bool:
        old_value = row[0]
        for value in row:
            if old_value == EMPTY:
                return False
            elif value != old_value:
                return False

        return True

    def validate(self) -> int:
        for row in self.board.board:
            if self._validate_row(row):
                if row[0] == CROSS_WIN:
                    return CROSS_WIN
                else:
                    return ZEROS_WIN

        return 0