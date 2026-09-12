from typing import List, Tuple

from protocols.controls_protocol import ControlsProtocol


class Controls(ControlsProtocol):

    def _read_key(self, options: List[Tuple[int, int]]) -> Tuple[int, int]:
        raise NotImplementedError

    def next_move(self, options: List[Tuple[int, int]]) -> Tuple[int, int]:
        return self._read_key(options)