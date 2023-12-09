from colors import Terminal_Colors
from Player import Player, Player_Type
from Board import Board

if __name__ == "__main__":
    p1 = Player("Player 1", "R", f" {Terminal_Colors.FAIL}\u25cf{Terminal_Colors.ENDC} ", True, ai_move=Player_Type.FOLLOW)
    p2 = Player("Player 2", "Y", f" {Terminal_Colors.WARNING}\u25cf{Terminal_Colors.ENDC} ", ai_move=Player_Type.OPPOSITE)

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

