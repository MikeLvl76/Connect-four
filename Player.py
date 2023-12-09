from typing import Union


class Player_Type:
    RANDOM = 'random'
    FOLLOW = 'follow'
    OPPOSITE = 'opposite'

class Player:
    def __init__(
        self, name: str, token: str, color: str, playing: bool = False, ai_move: Union[str, None] = None
    ) -> None:
        self.name: str = name
        self.token: str = token
        self.color: str = color
        self.playing: bool = playing
        self.ai_move: Union[str, None] = ai_move
        self.moves: list[tuple[int, int, str]] = []
        
    def save_move(self, i: int, j: int, token: str) -> None:
        self.moves.append((i, j, token))

    def __str__(self) -> str:
        return f"{self.name}"
