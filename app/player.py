from typing import Tuple
from app.action_manager import ActionManager


class Player:
    def __init__(self, action_manager : ActionManager, value : int):
        self.action_manager = action_manager
        self.value = value

    def next_move(self) -> Tuple[int, int]:
        return 0,0