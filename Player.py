class Player:

    def __init__(self, name: str, token: str, color: str, playing: bool = False) -> None:
        self.name = name
        self.token = token
        self.color = color
        self.playing = playing

    def __str__(self) -> str:
        return f"{self.name}"