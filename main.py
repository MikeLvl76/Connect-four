from os import system, name
from colors import Terminal_Colors

p1: dict = {
    "name": "p1",
    "color": "red",
    "token": "R",
    "playing": True,
}

p2: dict = {"name": "p2", "color": "yellow", "token": "Y"}

NUMBER_OF_ROWS = 6
NUMBER_OF_COLS = 7
BOARD_CELLS_CHAR = "\u25cf"
board: list[list[str]] = [
    [BOARD_CELLS_CHAR for _ in range(NUMBER_OF_COLS)] for _ in range(NUMBER_OF_ROWS)
]


def print_board() -> None:
    system("cls" if name == "nt" else "clear")
    red = f" {Terminal_Colors.FAIL}{BOARD_CELLS_CHAR}{Terminal_Colors.ENDC} "
    yellow = f" {Terminal_Colors.WARNING}{BOARD_CELLS_CHAR}{Terminal_Colors.ENDC} "

    print(f"   {'     '.join(str(i) for i in range(len(board[0])))}")  # column indices
    print(f"{'-' * 6 * len(board[0])}-")  # header line

    for row in board:
        formatted_row = [
            cell.center(3) if cell == BOARD_CELLS_CHAR else
            red.center(3) if cell == p1.get('token') else
            yellow.center(3)
            for cell in row
        ]

        print(f"| {' | '.join(formatted_row)} |") # each row

    print(f"{'-' * 6 * len(board[0])}-")  # footer line


def get_row(index: int) -> list[str]:
    assert index < NUMBER_OF_ROWS and index >= 0, "Row index out of bounds"
    return board[index]


def get_col(index: int) -> list[str]:
    assert index < NUMBER_OF_COLS and index >= 0, "Col index out of bounds"
    return [board[i][index] for i in range(NUMBER_OF_ROWS)]


def set_col(index: int, col: list[str]) -> None:
    assert index < NUMBER_OF_COLS and index >= 0, "Col index out of bounds"
    assert len(col) == NUMBER_OF_ROWS, "Incorrect column size"
    for i in range(NUMBER_OF_ROWS):
        board[i][index] = col[i]


def get_location(i: int, j: int) -> str:
    assert i < NUMBER_OF_ROWS and i >= 0, "Row index out of bounds"
    assert j < NUMBER_OF_COLS and j >= 0, "Col index out of bounds"
    return board[i][j]


def get_diagonals(i: int, j: int) -> dict:
    length: int = min(NUMBER_OF_ROWS, NUMBER_OF_COLS)
    d1, d2, d3, d4 = [], [], [], []

    for k in range(length):
        if i - k >= 0 and j - k >= 0:
            d1.append(get_location(i - k, j - k))  # top left

        if i + k < length and j + k < length + 1:
            d2.append(get_location(i + k, j + k))  # bottom right

        if i - k >= 0 and j + k < length + 1:
            d3.append(get_location(i - k, j + k))  # top right

        if i + k < length and j - k >= 0:
            d4.append(get_location(i + k, j - k))  # bottom left

    return {
        "location": (i, j, get_location(i, j)),
        "first_diagonal": [*[*d1[1::]][::-1], *d2],
        "second_diagonal": [*[*d3[1::]][::-1], *d4],
    }


def check_winner() -> tuple[bool, list[str], str]:
    # Check horizontally
    for row in range(NUMBER_OF_ROWS):
        for col in range(NUMBER_OF_COLS - 3):
            line = [
                get_location(row, col),
                get_location(row, col + 1),
                get_location(row, col + 2),
                get_location(row, col + 3),
            ]

            if all(
                element != BOARD_CELLS_CHAR and element == line[0] for element in line
            ):
                return (
                    True,
                    line,
                    f"Player {'P1' if line[0] == p1.get('token') else 'P2'} wins horizontally",
                )

    # Check vertically
    for row in range(NUMBER_OF_ROWS - 3):
        for col in range(NUMBER_OF_COLS):
            line = [
                get_location(row, col),
                get_location(row + 1, col),
                get_location(row + 2, col),
                get_location(row + 3, col),
            ]

            if all(
                element != BOARD_CELLS_CHAR and element == line[0] for element in line
            ):
                return (
                    True,
                    line,
                    f"Player {'P1' if line[0] == p1.get('token') else 'P2'} wins vertically",
                )

    # Check diagonally (from top-left to bottom-right)
    for row in range(NUMBER_OF_ROWS - 3):
        for col in range(NUMBER_OF_COLS - 3):
            line = [
                get_location(row, col),
                get_location(row + 1, col + 1),
                get_location(row + 2, col + 2),
                get_location(row + 3, col + 3),
            ]

            if all(
                element != BOARD_CELLS_CHAR and element == line[0] for element in line
            ):
                return (
                    True,
                    line,
                    f"Player {'P1' if line[0] == p1.get('token') else 'P2'} wins diagonally",
                )

    # Check diagonally (from top-right to bottom-left)
    for row in range(3, NUMBER_OF_ROWS):
        for col in range(NUMBER_OF_COLS - 3):
            line = [
                get_location(row, col),
                get_location(row - 1, col + 1),
                get_location(row - 2, col + 2),
                get_location(row - 3, col + 3),
            ]

            if all(
                element != BOARD_CELLS_CHAR and element == line[0] for element in line
            ):
                return (
                    True,
                    line,
                    f"Player {'P1' if line[0] == p1.get('token') else 'P2'} wins diagonally",
                )

    return False, [], "No winning combination"


def check_draw():
    for row in range(NUMBER_OF_ROWS):
        for col in range(NUMBER_OF_COLS):
            if get_location(row, col) == BOARD_CELLS_CHAR:
                return False

    return True


def insert() -> None:
    while True:
        print("P1 turn" if p1.get("playing") else "P2 turn")
        index = int(input("Choose column index (from 0 to 6): "))

        col = get_col(index)
        col_items = enumerate(col)

        token = p1.get("token") if p1.get("playing") else p2.get("token")

        token_idx = 0

        for count, value in col_items:
            if value == token:
                token_idx = count
                break

            if token != p1.get("token"):
                if value == p1.get("token"):
                    token_idx = count
                    break

            if token != p2.get("token"):
                if value == p2.get("token"):
                    token_idx = count
                    break

        if token_idx == 0:
            col[len(col) - 1] = (
                token if col[len(col) - 1] == BOARD_CELLS_CHAR else col[len(col) - 1]
            )
        else:
            col[token_idx - 1] = token

        set_col(index, col)
        print_board()

        is_end, combination, message = check_winner()

        if is_end:
            red_cell = f"{Terminal_Colors.FAIL}{BOARD_CELLS_CHAR}{Terminal_Colors.ENDC}"
            yellow_cell = f"{Terminal_Colors.WARNING}{BOARD_CELLS_CHAR}{Terminal_Colors.ENDC}"

            print(message)
            print(f"Combination: {[red_cell if cell == p1.get('token') else yellow_cell for cell in combination]}")
            break

        if check_draw():
            print("DRAW")
            break

        p1.update({"playing": not p1.get("playing")})


if __name__ == "__main__":
    print_board()
    insert()
