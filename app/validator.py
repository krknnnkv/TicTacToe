from enum import Enum
from typing import List, Optional

from app.board import Board, CellStatus


class ValidationStatus(Enum):
    EMPTY = 0
    CROSS_WIN = 1
    ZEROS_WIN = 2
    DRAW = 3

class Validator:
    def __init__(self, board: Board):
        self.board = board

    def _validate_row(self, row : List[CellStatus]) -> bool:
        old_value = row[0]
        for value in row:
            if old_value == ValidationStatus.EMPTY:
                return False
            elif value != old_value:
                return False

        return True

    def _validate_columns(self) -> Optional[ValidationStatus]:
        columns = list(zip(*self.board.board))

        for column in columns:
            if self._validate_row(list(column)):
                if column[0] == CellStatus.CROSS_FIELD:
                    return ValidationStatus.CROSS_WIN
                else:
                    return ValidationStatus.ZEROS_WIN
        return None

    def _validate_diagonals(self) -> Optional[ValidationStatus]:
        board = self.board.board

        d1 = [board[0][0], board[1][1], board[2][2]]
        d2 = [board[0][2], board[1][1], board[2][0]]

        for d in [d1, d2]:
            if self._validate_row(d):
                if d[0] == CellStatus.CROSS_FIELD:
                    return ValidationStatus.CROSS_WIN
                else:
                    return ValidationStatus.ZEROS_WIN

        return None

    def validate1(self) -> ValidationStatus:
        for row in self.board.board:
            if self._validate_row(row):
                if row[0] == CellStatus.CROSS_FIELD:
                    return ValidationStatus.CROSS_WIN
                else:
                    return ValidationStatus.ZEROS_WIN

        result = self._validate_columns()
        if result is not None:
            return result

        result = self._validate_diagonals()
        if result is not None:
            return result

        for row in self.board.board:
            for cell in row:
                if cell == CellStatus.EMPTY_FIELD:
                    return ValidationStatus.EMPTY

        return ValidationStatus.DRAW

    def validate(self) -> ValidationStatus:
        board = self.board.board
        lines = []
        for index in range(3):
            lines.append([board[index][0], board[index][1], board[index][2]])
            lines.append([board[0][index], board[1][index], board[2][index]])

        lines.append([board[0][0], board[1][1], board[2][2]])
        lines.append([board[0][2], board[1][1], board[2][0]])

        for line in lines:
            if self._validate_row(line):
                return ValidationStatus.CROSS_WIN if line[0] == CellStatus.CROSS_FIELD else ValidationStatus.ZEROS_WIN

        for row in board:
            for cell in row:
                if cell == CellStatus.EMPTY_FIELD:
                    return ValidationStatus.EMPTY

        return ValidationStatus.DRAW
