from os import system, name
from random import randint
from time import sleep
from typing import Union
from Player import Player, Player_Type


class Board:
    def __init__(
        self,
        rows: int,
        cols: int,
        default_char: str,
        first_player: Player,
        second_player: Player,
    ) -> None:
        self.rows_count = rows
        self.cols_count = cols
        self.default_char = default_char
        self.board = [
            [default_char for _ in range(self.cols_count)]
            for _ in range(self.rows_count)
        ]
        self.first_player = first_player
        self.second_player = second_player
        self.turn = 0

    def get_row(self, index: int) -> list[str]:
        assert index < self.rows_count and index >= 0, f"Index {index} for row is out of bounds"
        return self.board[index]

    def get_col(self, index: int) -> list[str]:
        assert index < self.cols_count and index >= 0, f"Index {index} for column is out of bounds"
        return [self.board[i][index] for i in range(self.rows_count)]

    def set_col(self, index: int, col: list[str]) -> None:
        assert index < self.cols_count and index >= 0, f"Index {index} for column is out of bounds"
        assert len(col) == self.rows_count, "Incorrect column size"
        for i in range(self.rows_count):
            self.board[i][index] = col[i]

    def get_location(self, i: int, j: int) -> str:
        assert i < self.rows_count and i >= 0, f"Index {i} for row is out of bounds"
        assert j < self.cols_count and j >= 0, f"Index {j} for column is out of bounds"
        return self.board[i][j]

    def get_diagonals(self, i: int, j: int) -> dict:
        length: int = min(self.rows_count, self.cols_count)
        d1, d2, d3, d4 = [], [], [], []

        for k in range(length):
            if i - k >= 0 and j - k >= 0:
                d1.append(self.get_location(i - k, j - k))  # top left

            if i + k < length and j + k < length + 1:
                d2.append(self.get_location(i + k, j + k))  # bottom right

            if i - k >= 0 and j + k < length + 1:
                d3.append(self.get_location(i - k, j + k))  # top right

            if i + k < length and j - k >= 0:
                d4.append(self.get_location(i + k, j - k))  # bottom left

        return {
            "location": (i, j, self.get_location(i, j)),
            "first_diagonal": [*[*d1[1::]][::-1], *d2],
            "second_diagonal": [*[*d3[1::]][::-1], *d4],
        }

    def play(self) -> None:
        current_player = self.first_player if self.first_player.playing else self.second_player
        print(f'Number of turn played: {self.turn}')
        print(f"{current_player.name} {current_player.color} turn...")
        index = -1

        if current_player.ai_move:
            ai_move = current_player.ai_move
            print(f'{current_player.name} thinking...')
            sleep(3)
            if ai_move == Player_Type.RANDOM:
                index = randint(0, len(self.board[0]) - 1)
            if ai_move == Player_Type.FOLLOW:
                opponent = self.first_player if current_player == self.second_player else self.second_player
                last_move_index = opponent.moves[len(opponent.moves) - 1][1]
                if last_move_index < self.cols_count:
                    next_index = last_move_index + 1
                    if next_index == len(self.board[0]):
                        print(last_move_index, next_index)
                        assert False, "TODO: choose new index because board size is reached"  
                    index = next_index
                    
                # last_move_index = opponent.moves[len(opponent.moves) - 1][1]
                # index = last_move_index if last_move_index < self.rows_count else last_move_index + 1
        else:
            while not (0 <= index <= len(self.board[0]) - 1):
                try:
                    index = int(input(f"Choose column index (from 0 to {len(self.board[0]) - 1}): "))
                    if not (0 <= index <= len(self.board[0]) - 1):
                        print(f"Index must be between 0 and {len(self.board[0]) - 1}.")
                except ValueError:
                    print("Please enter a valid integer.")
        

        col = self.get_col(index)
        col_items = enumerate(col)
        token_idx = 0

        for count, value in col_items:
            if value == current_player.token:
                token_idx = count
                break

            if current_player.token != self.first_player.token and value == self.first_player.token:
                token_idx = count
                break

            if current_player.token != self.second_player.token and value == self.second_player.token:
                token_idx = count
                break

        if token_idx == 0:
            col[len(col) - 1] = (
                current_player.token if col[len(col) - 1] == self.default_char else col[len(col) - 1]
            )
            current_player.save_move(len(col) - 1, index, current_player.token)   
        else:
            col[token_idx - 1] = current_player.token
            current_player.save_move(token_idx - 1, index, current_player.token)
           
        self.set_col(index, col)
        self.print()

        self.first_player.playing = not self.first_player.playing
        self.turn += 1
        
    
    def get_winner_from_line(self, row_range: tuple[int, int, int], col_range: tuple[int, int, int], direction: str) -> Union[Player, None]:
        for row in range(*row_range):
            for col in range(*col_range):
                line = []
                if direction == 'horizontal':
                    line = [self.get_location(row, col + i) for i in range(4)]
                elif direction == 'vertical':
                    line = [self.get_location(row + i, col) for i in range(4)]
                elif direction == 'top_left_bottom_right':
                    line = [self.get_location(row + i, col + i) for i in range(4)]
                elif direction == 'top_right_bottom_left':
                    line = [self.get_location(row - i, col + i) for i in range(4)]

                if all(element != self.default_char and element == line[0] for element in line):
                    return (self.first_player if line[0] == self.first_player.token else self.second_player)

        return None

    def get_winner(self) -> Union[Player, None]:      
        winner_horizontal = self.get_winner_from_line((0, self.rows_count, 1), (0, self.cols_count - 3, 1), 'horizontal')
        winner_vertical = self.get_winner_from_line((0, self.rows_count - 3, 1), (0, self.cols_count, 1), 'vertical')
        winner_top_left_bottom_right = self.get_winner_from_line((0, self.rows_count - 3, 1), (0, self.cols_count - 3, 1), 'top_left_bottom_right')
        winner_top_right_bottom_left = self.get_winner_from_line((3, self.rows_count, 1), (0, self.cols_count - 3, 1), 'top_right_bottom_left')

        
        return winner_horizontal or winner_vertical or winner_top_left_bottom_right or winner_top_right_bottom_left


    def is_draw(self) -> bool:
        for row in range(self.rows_count):
            for col in range(self.cols_count):
                if self.get_location(row, col) == self.default_char:
                    return False

        return True

    def print(self) -> None:
        system("cls" if name == "nt" else "clear")

        print(f"   {'     '.join(str(i) for i in range(len(self.board[0])))}")  # column indices
        print(f"{'-' * 6 * len(self.board[0])}-")  # header line

        for row in self.board:
            formatted_row = [
                cell.center(3)
                if cell == self.default_char
                else self.first_player.color.center(3)
                if cell == self.first_player.token
                else self.second_player.color.center(3)
                for cell in row
            ]
            print(f"| {' | '.join(formatted_row)} |")  # each row

        print(f"{'-' * 6 * len(self.board[0])}-")  # footer line
