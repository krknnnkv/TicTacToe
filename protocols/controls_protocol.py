from typing import Protocol, Tuple, List


class ControlsProtocol(Protocol):
    def next_move(self, options: List[Tuple[int, int]]) -> Tuple[int, int]:...