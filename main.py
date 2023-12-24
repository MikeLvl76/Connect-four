from os import name, system
from cmd_prompt_colors import color_string, colors
from Player import Player
from Board import Board

def main():
    system("cls" if name == "nt" else "clear")
    
    player_1_name = input('Player 1, type your name: ')
    
    while len(player_1_name) < 3:
        print('Name size too short.')
        player_1_name = input('Player 1, type your name: ')
        
    player_2_name = input('Player 2, type your name: ')
        
    while len(player_2_name) < 3:
        print('Name size too short.')
        player_2_name = input('Player 2, type your name: ')
    
    color_list = list(colors.keys())[:-1:]
    player_1_prompt = f'{player_1_name}, choose your color among this list:\n{", ".join(color_list)}\n'
    player_1_color = input(player_1_prompt)
    
    while player_1_color not in color_list:
        print('Please select a color from the list.')
        player_1_color = input(player_1_prompt)
    
    color_list.remove(player_1_color)
    player_2_prompt = f'{player_2_name}, choose your color among this list:\n{", ".join(color_list)}\n'
    player_2_color = input(player_2_prompt)
    
    while player_2_color not in color_list:
        print('Please select a color from the list.')
        player_2_color = input(player_2_prompt)
    
    p1 = Player(player_1_name, "R", color_string(player_1_color, '\u25cf'), True)
    p2 = Player(player_2_name, "Y", color_string(player_2_color, '\u25cf'))

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

if __name__ == "__main__":
    main()
