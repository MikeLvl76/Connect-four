from typing import Union


class Type:
    random = 'random'
    fill_column = 'fill_column'
    fill_row = 'fill_row'
    follow = 'follow'

class Player:
    def __init__(
        self, name: str, token: str, color: str, playing: bool = False, ai_move: Union[str, None] = None
    ) -> None:
        self.name = name
        self.token = token
        self.color = color
        self.playing = playing
        self.ai_move = ai_move

    def __str__(self) -> str:
        return f"{self.name}"
