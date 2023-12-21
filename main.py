from cmd_prompt_colors import color_string
from player import Player, Player_Type
from board import Board

if __name__ == "__main__":
    p1 = Player("Player 1", "R", color_string('YELLOW', '\u25cf'), True)
    p2 = Player("Player 2", "Y", color_string('RED', '\u25cf'))

    board = Board(6, 7, '\u25cf', p1, p2)

    while True:
        board.print()
        board.play()

        winner = board.get_winner()
        if winner:
            print(f"{winner.name} {winner.color} won!")
            print(f"Number of turn played: {board.turn}")
            break

        if board.is_draw():
            print('Draw!')
            print(f"Number of turn played: {board.turn}")
            break

