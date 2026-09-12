from typing import Tuple, List

from app.board import Board, CellStatus


class ActionManager:
    def __init__(self, board : Board):
        self.board = board

    def available_options(self) -> List[Tuple[int, int]]:
        options = []
        size = len(self.board.board)
        for row in range(size):
            for col in range(size):
                if self.board.board[row][col] == CellStatus.EMPTY_FIELD:
                    options.append((row, col))

        return options