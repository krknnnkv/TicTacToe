from typing import List
from app.player import Player
import random


class Orchestrator:
    def __init__(self, players : List[Player]) -> None:
        self.players = players
        self._current_player = random.randrange(len(players))

    def next_player(self) -> Player:
        current = self._current_player
        self._current_player += 1
        self._current_player %= len(self.players)
        return self.players[current]
