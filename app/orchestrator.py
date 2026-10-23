from typing import List, Optional
from app.player import Player
import random


class Orchestrator:
    def __init__(self, players : List[Player], first_player: Optional[int] = None) -> None:
        self.players = players
        if first_player is None:
            self._current_player = random.randrange(len(players))
        else:
            self._current_player = first_player

    def next_player(self) -> Player:
        current = self._current_player
        self._current_player += 1
        self._current_player %= len(self.players)
        return self.players[current]
