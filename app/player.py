from typing import Tuple
from app.action_manager import ActionManager
from app.board import CellStatus
from protocols.controls_protocol import ControlsProtocol


class Player:
    def __init__(self, action_manager : ActionManager, value : CellStatus, controls : ControlsProtocol):
        self.action_manager = action_manager
        self.value = value
        self.controls = controls

    def next_move(self) -> Tuple[int, int]:
        return self.controls.next_move(self.action_manager.available_options())