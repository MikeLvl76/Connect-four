from json import dumps

p1: dict = {"name": "p1", "color": "red", "token": "R", "playing": False}

p2: dict = {"name": "p2", "color": "yellow", "token": "Y", "playing": False}

NUMBER_OF_ROWS = 7
NUMBER_OF_COLS = 6
board: list[list[str]] = [
    [f"{i * 6 + j + 1}" for i in range(NUMBER_OF_COLS)] for j in range(NUMBER_OF_ROWS)
]


def print_board() -> None:
    output = ""
    for row in board:
        output += f'{"     ".join(row)}\n'
    print(output)


def get_row(index: int) -> list[str]:
    return board[index]


def get_col(index: int) -> list[str]:
    return [board[i][index] for i in range(len(board))]


def get_location(i: int, j: int) -> str:
    assert i < NUMBER_OF_ROWS, "Row index out of bounds"
    assert j < NUMBER_OF_COLS, "Col index out of bounds"
    return board[i][j]


def get_diagonals(i: int, j: int, **kwargs: dict) -> dict:
    length: int = min(NUMBER_OF_ROWS, NUMBER_OF_COLS)
    d1, d2, d3, d4 = [], [], [], []

    for k in range(length):
        if i - k < 0 or j - k < 0:
            break
        d1.append(get_location(i - k, j - k))  # top left

    for k in range(length):
        if i + k > length or j - k < 0:
            break
        d2.append(get_location(i + k, j - k))  # bottom left

    for k in range(length):
        if i - k < 0 or j + k > length - 1:
            break
        d3.append(get_location(i - k, j + k))  # top right

    for k in range(length):
        if i + k > length or j + k > length - 1:
            break
        d4.append(get_location(i + k, j + k))  # bottom right

    return {
        "location": (i, j, get_location(i, j)),
        "top_left": d1,
        "bottom_left": d2,
        "top_right": d3,
        "bottom_right": d4,
    }


def insert() -> None:
    row_input = int(input("Choose row: "))
    col_input = int(input("Choose column: "))
    print(row_input, col_input)


if __name__ == "__main__":
    print_board()
    print(dumps(get_diagonals(3, 4), indent=4))
