from typing import Optional, Tuple

import pygame

from app.board import Board, CellStatus
from app.validator import ValidationStatus

STATUS_TEXT = {
    ValidationStatus.CROSS_WIN : "CROSSES WIN!!!",
    ValidationStatus.ZEROS_WIN : "ZEROS WIN!!!",
    ValidationStatus.DRAW : "DRAW"
}

CELL_SIZE = 150
LINE_WIDTH = 4
MARK_PADDING = 30
STATUS_HEIGHT = 60
FONT_SIZE = 36

BACKGROUND_COLOR = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
CROSS_COLOR = (220, 50, 50)
ZERO_COLOR = (50, 50, 220)
HIGHLIGHT_COLOR = (255, 235, 120)
OCCUPIED_HIGHLIGHT_COLOR = (255, 150, 150)
TEXT_COLOR = (0, 0, 0)

class Graphic:
    def __init__(self, board : Board):
        self.board = board
        board_size = CELL_SIZE * len(board.board)
        self.screen = pygame.display.set_mode((board_size, board_size + STATUS_HEIGHT))
        pygame.display.set_caption("TicTacToe")
        self.font = pygame.font.Font(None, FONT_SIZE)

    def _draw_grid(self) -> None:
        size = CELL_SIZE * 3
        for i in range(1, 3):
            offset = i * CELL_SIZE
            pygame.draw.line(self.screen, LINE_COLOR, (offset, 0), (offset, size), LINE_WIDTH)
            pygame.draw.line(self.screen, LINE_COLOR, (0, offset), (size, offset), LINE_WIDTH)
        pygame.draw.line(self.screen, LINE_COLOR, (0, size), (size, size), LINE_WIDTH)

    def _cell_rect(self, row: int, col: int) -> pygame.Rect:
        return pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)

    def _draw_cross(self, row: int, col: int) -> None:
        rect = self._cell_rect(row, col).inflate(-2 * MARK_PADDING, -2 * MARK_PADDING)
        pygame.draw.line(self.screen, CROSS_COLOR, rect.topleft, rect.bottomright, LINE_WIDTH * 2)
        pygame.draw.line(self.screen, CROSS_COLOR, rect.topright, rect.bottomleft, LINE_WIDTH * 2)

    def _draw_zero(self, row: int, col: int) -> None:
        rect = self._cell_rect(row, col)
        radius = CELL_SIZE // 2 - MARK_PADDING
        pygame.draw.circle(self.screen, ZERO_COLOR, rect.center, radius, LINE_WIDTH * 2)

    def _draw_status(self, last_validation_result) -> None:
        text = STATUS_TEXT.get(last_validation_result)
        if text is None:
            return
        board_size = CELL_SIZE * 3
        surface = self.font.render(text, True, TEXT_COLOR)
        rect = surface.get_rect(center=(board_size // 2, board_size + STATUS_HEIGHT // 2))
        self.screen.blit(surface, rect)

    def _draw_highlight(self, row: int, col: int) -> None:
        occupied = self.board.board[row][col] != CellStatus.EMPTY_FIELD
        color = OCCUPIED_HIGHLIGHT_COLOR if occupied else HIGHLIGHT_COLOR
        pygame.draw.rect(self.screen, color, self._cell_rect(row, col))

    def render(self, selected_cell: Optional[Tuple[int, int]] = None,
               last_validation_result = ValidationStatus.EMPTY):
        self.screen.fill(BACKGROUND_COLOR)

        if selected_cell is not None:
            self._draw_highlight(*selected_cell)

        self._draw_grid()

        for row in range(3):
            for col in range(3):
                value = self.board.board[row][col]
                if value == CellStatus.CROSS_FIELD:
                    self._draw_cross(row, col)
                if value == CellStatus.ZERO_FIELD:
                    self._draw_zero(row, col)

        self._draw_status(last_validation_result)
        pygame.display.flip()