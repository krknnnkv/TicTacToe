from typing import Tuple
from app.action_manager import ActionManager
from app.board import CellStatus
from app.validator import ValidationStatus
from protocols.controls_protocol import ControlsProtocol

WIN_REWARD = 1.0
LOSE_REWARD = -1.0
DRAW_REWARD = 0.0

class Player:
    def __init__(self, action_manager : ActionManager, value : CellStatus, controls : ControlsProtocol):
        self.action_manager = action_manager
        self.value = value
        self.controls = controls

    def next_move(self) -> Tuple[int, int]:
        board = self.action_manager.board
        options = self.action_manager.available_options()
        return self.controls.next_move(self.value, board, options)

    def game_over(self, result: ValidationStatus):
        if result == ValidationStatus.DRAW:
            reward = DRAW_REWARD
        elif self._is_my_win(result):
            reward = WIN_REWARD
        else:
            reward = LOSE_REWARD
        self.controls.game_over(reward)

    def _is_my_win(self, result: ValidationStatus) -> bool:
        if result == ValidationStatus.CROSS_WIN and self.value == CellStatus.CROSS_FIELD:
            return True

        if result == ValidationStatus.ZEROS_WIN and self.value == CellStatus.ZERO_FIELD:
            return True

        return False