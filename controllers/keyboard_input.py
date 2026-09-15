from typing import Tuple, List

import pygame

from controllers.controls import Controls
from render.graphic import Graphic

MOVES = {
    pygame.K_LEFT: (0, -1),
    pygame.K_RIGHT: (0, 1),
    pygame.K_UP: (-1, 0),
    pygame.K_DOWN: (1, 0),
}

class KeyboardInput(Controls):
    def __init__(self, renderer : Graphic):
        self.renderer = renderer
        self.cursor: Tuple[int, int] = (0, 0)

    def _read_key(self, options: List[Tuple[int, int]]) -> Tuple[int, int]:
        self.renderer.render(selected_cell=self.cursor)
        while True:
            event = pygame.event.wait()
            if event.type == pygame.QUIT:
                raise SystemExit
            if event.type != pygame.KEYDOWN:
                continue
            if event.key in MOVES:
                row, col = self.cursor
                direction_row, direction_col = MOVES[event.key]
                row += direction_row
                col += direction_col
                row = max(0, row)
                row = min(row, 2)
                col = max(0, col)
                col = min(col, 2)
                self.cursor = (row, col)
                self.renderer.render(selected_cell=self.cursor)
            elif event.key == pygame.K_RETURN and self.cursor in options:
                return self.cursor
