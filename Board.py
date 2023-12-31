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
    
    def is_col_full(self, index: int) -> bool:
        col = self.get_col(index)
        return all(element != self.default_char for element in col)
    
    def get_nearest_available_column(self, index: int) -> int:
        if index >= self.cols_count:
            index = self.cols_count - 1
            
        if self.is_col_full(index):
            if index == 0:
                index += 1
            elif index == self.cols_count - 1:
                index -= 1

            # left
            for i in range(index, -1, -1):
                current_column = self.get_col(i)
                if any(element == self.default_char for element in current_column):
                    return i
                
            # right
            for i in range(index, self.cols_count):
                current_column = self.get_col(i)
                if any(element == self.default_char for element in current_column):
                    return i

        return index

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
                index = randint(0, self.cols_count - 1)
                
            else:
                opponent_player = self.first_player if current_player == self.second_player else self.second_player
                if len(opponent_player.moves) == 0:
                    index = randint(0, self.cols_count - 1)
                    
                else:
                    last_move_index = opponent_player.moves[-1][1]
                    if ai_move == Player_Type.FOLLOW:
                        if last_move_index < self.cols_count:
                            next_index = last_move_index + 1
                            
                            next_index = self.get_nearest_available_column(next_index)
                            if current_player.token in self.get_col(next_index):
                                next_index -= 1

                            index = next_index
                            
                    elif ai_move == Player_Type.OPPOSITE:
                            opposite_index = abs(last_move_index - (self.cols_count - 1))
                            opposite_col = self.get_col(opposite_index)
                            
                            if all(element != self.default_char for element in opposite_col):
                                opposite_index = self.get_nearest_available_column(opposite_index)

                            index = opposite_index
        else:
            while not (0 <= index <= self.cols_count - 1):
                try:
                    index = int(input(f"Choose column index (from 0 to {self.cols_count - 1}): "))
                    if not (0 <= index <= self.cols_count - 1):
                        print(f"Index must be between 0 and {self.cols_count - 1}.")
                except ValueError:
                    print("Please enter a valid integer.")
        

        available_index = self.get_nearest_available_column(index)
        col = self.get_col(available_index)
        col_items = enumerate(col)
        token_idx = 0
        
        for count, value in col_items:
            if value == current_player.token or \
            (current_player.token != self.first_player.token and value == self.first_player.token) or \
            (current_player.token != self.second_player.token and value == self.second_player.token):
                token_idx = count
                break

        if token_idx == 0:
            last_index = len(col) - 1
            if col[last_index] == self.default_char:
                col[last_index] = current_player.token
                current_player.save_move(last_index, available_index, current_player.token)   
        else:
            col[token_idx - 1] = current_player.token
            current_player.save_move(token_idx - 1, available_index, current_player.token)
           
        self.set_col(available_index, col)
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
        return all(self.get_location(row, col) != self.default_char for row in range(self.rows_count) for col in range(self.cols_count))


    def print(self) -> None:
        system("cls" if name == "nt" else "clear")

        cell_width = 5  # Cell width
        column_indices = ''.join(f'  {i:^{cell_width - 1}}' for i in range(self.cols_count))
        horizontal_line = '+' + '+'.join('-' * cell_width for _ in range(self.cols_count)) + '+'

        print(column_indices)  # column indices
        print(horizontal_line)  # header line

        for row in self.board:
            formatted_row = [
                cell.center(cell_width) if cell == self.default_char
                else f'{self.first_player.color:^{cell_width}}' if cell == self.first_player.token
                else f'{self.second_player.color:^{cell_width}}'
                for cell in row
            ]
            print(f'|{ "|".join(formatted_row) }|'.center(cell_width * self.cols_count + self.cols_count - 1))  # each row
            print(horizontal_line)  
