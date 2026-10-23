import random
from typing import List, Tuple

from app.board import CellStatus, Board, Matrix3x3
from app.validator import ValidationStatus, Validator
from controllers.controls import Controls

WIN_SCORE = 1
LOSE_SCORE = -1
DRAW_SCORE = 0

class MinimaxInput(Controls):
    def __init__(self):
        self._validator = Validator(Board())

    def _read_key(self, value: CellStatus, board: Board, options: List[Tuple[int, int]]) -> Tuple[int, int]:
        new_board = _copy_board(board.board)
        best_score = LOSE_SCORE - 1
        best_moves : List[Tuple[int, int]] = []

        for row, column in options:
            new_board[row][column] = value
            score = self._minimax(new_board, _other(value), value)
            new_board[row][column] = CellStatus.EMPTY_FIELD

            if score > best_score:
                best_score = score
                best_moves = [(row, column)]
            elif score == best_score:
                best_moves.append((row, column))
        return random.choice(best_moves)

    def _validate(self, new_board: Matrix3x3) -> ValidationStatus:
        self._validator.board.board = new_board
        return self._validator.validate()

    def _minimax(self, new_board: Matrix3x3, current: CellStatus, me: CellStatus) -> int:
        #добавить кэширование
        result = self._validate(new_board)
        if result != ValidationStatus.EMPTY:
            score = _calculate_score(result, me)
            #закэшировать результат
            return score
        opponent = _other(current)
        if current == me:
            #наш ход ищем МАХ
            best_score = LOSE_SCORE - 1
            for row in range(3):
                for column in range(3):
                    if new_board[row][column] == CellStatus.EMPTY_FIELD:
                        new_board[row][column] = current
                        score = self._minimax(new_board, opponent, me)
                        new_board[row][column] = CellStatus.EMPTY_FIELD
                        if score > best_score:
                            best_score = score
        else:
            best_score = WIN_SCORE + 1
            for row in range(3):
                for column in range(3):
                    if new_board[row][column] == CellStatus.EMPTY_FIELD:
                        new_board[row][column] = current
                        score = self._minimax(new_board, opponent, me)
                        new_board[row][column] = CellStatus.EMPTY_FIELD
                        if score < best_score:
                            best_score = score
        return best_score

def _calculate_score(result: ValidationStatus, me: CellStatus) -> int:
    if result == ValidationStatus.DRAW:
        return DRAW_SCORE

    if result == ValidationStatus.ZEROS_WIN and me == CellStatus.ZERO_FIELD:
        return WIN_SCORE

    if result == ValidationStatus.CROSS_WIN and me == CellStatus.CROSS_FIELD:
        return WIN_SCORE

    return LOSE_SCORE

def _copy_board(board: Matrix3x3) -> Matrix3x3:
    """Глубокая копия доски: копируем каждую строку, а не только внешний список."""
    copied_board = []
    for row in board:
        copied_board.append(list(row))
    return copied_board

def _other(value: CellStatus) -> CellStatus:
    """Знак соперника: для крестика — нолик, для нолика — крестик."""
    if value == CellStatus.CROSS_FIELD:
        return CellStatus.ZERO_FIELD
    return CellStatus.CROSS_FIELD