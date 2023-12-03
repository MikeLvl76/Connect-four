from itertools import groupby

p1: dict = {"name": "p1", "color": "red", "token": "R", "playing": True}
p2: dict = {"name": "p2", "color": "yellow", "token": "Y"}

NUMBER_OF_ROWS = 7
NUMBER_OF_COLS = 6
BOARD_CELLS_CHAR = "?"
board: list[list[str]] = [
    [BOARD_CELLS_CHAR for _ in range(NUMBER_OF_COLS)] for _ in range(NUMBER_OF_ROWS)
]


def print_board() -> None:
    output = ""
    for row in board:
        output += f'{"     ".join(row)}\n'
    print(output, end="")


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

        if i + k < length + 1 and j + k < length:
            d2.append(get_location(i + k, j + k))  # bottom right

        if i - k >= 0 and j + k < length:
            d3.append(get_location(i - k, j + k))  # top right

        if i + k < length + 1 and j - k >= 0:
            d4.append(get_location(i + k, j - k))  # bottom left

    return {
        "location": (i, j, get_location(i, j)),
        "first_diagonal": [*[*d1[1::]][::-1], *d2],
        "second_diagonal": [*[*d3[1::]][::-1], *d4],
    }


def all_equal(string: str):
    return all(char == string[0] and char != BOARD_CELLS_CHAR for char in string)


def is_win(array: list[str]) -> tuple[bool, str]:
    string: str = "".join(array)
    quatuors: list[str] = []
    count: int = 4
    for i in range(len(string) - count):
        sub: str = string[i : i + count]
        quatuors.append(sub)

    for quatuor in quatuors:
        if all_equal(quatuor):
            return True, f"Winning combination: {quatuor}"

    return False, "No winning combination"


def end_game() -> str:
    for i in range(NUMBER_OF_ROWS):
        win, message = is_win(get_row(i))
        if win:
            return message

    for j in range(NUMBER_OF_COLS):
        win, message = is_win(get_col(j))
        if win:
            return message

    for i in range(NUMBER_OF_ROWS):
        for j in range(NUMBER_OF_COLS):
            diagonals = get_diagonals(i, j)
            first_diagonal = diagonals.get("first_diagonal")
            second_diagonal = diagonals.get("second_diagonal")

            first_diagonal_win, message = is_win(first_diagonal)
            second_diagonal_win, msg = is_win(second_diagonal)
            
            if first_diagonal_win:
                return message
            if second_diagonal_win:
                return msg

    return "Game not finished!"


def insert() -> None:
    while True:
        index = int(input("Choose column index (from 0 to 5): "))

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
        print(end_game())

        p1.update({"playing": not p1.get("playing")})


if __name__ == "__main__":
    print_board()
    # diagonals = get_diagonals(0, 0)
    # first_diagonal = diagonals.get("first_diagonal")
    # print(is_win(first_diagonal))
    insert()
