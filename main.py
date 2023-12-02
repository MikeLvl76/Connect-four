from json import dumps

p1: dict = {"name": "p1", "color": "red", "token": "R", "playing": True}

p2: dict = {"name": "p2", "color": "yellow", "token": "Y", "playing": False}

NUMBER_OF_ROWS = 7
NUMBER_OF_COLS = 6
board: list[list[str]] = [
    ["1" if i == j else "0" for i in range(NUMBER_OF_COLS)]
    for j in range(NUMBER_OF_ROWS)
]


def print_board() -> None:
    output = ""
    for row in board:
        output += f'{"     ".join(row)}\n'
    print(output)


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


def is_win(array: list[str]):
    string: str = "".join(array)
    res: dict = {}
    for i in range(len(string) - 1):
        sub: str = string[i : i + 1]
        freq: int = res.get(sub) or 0
        res[sub]: int = freq + 1

    most_frequent_name: str = ""
    most_frequent_value: int = 0

    for item in res.items():
        if item[1] > most_frequent_value:
            most_frequent_name, most_frequent_value = item

    return most_frequent_name, most_frequent_value == 4


def insert() -> None:
    while True:
        index = int(input("Choose column index (from 0 to 5): "))
        col = get_col(index)

        try:
            idx = col.index(p1["token"] if p1["playing"] else p2["token"])
            opponent_token_idx = col.index(
                p2["token"] if p1["playing"] else p1["token"]
            )

            if idx > 0 or opponent_token_idx > 0:  # both tokens exist
                if (
                    idx > opponent_token_idx
                ):  # player token inserted before opponent token
                    col[opponent_token_idx - 1] = (
                        p1["token"] if p1["playing"] else p2["token"]
                    )
                else:  # player token inserted after opponent token
                    col[idx - 1] = p1["token"] if p1["playing"] else p2["token"]
                set_col(index, col)

        except ValueError:
            print("ValueError")
            if col[len(col) - 1] == p1["token"] if p1["playing"] else p2["token"]:
                col[len(col) - 2] = p2["token"] if p2["playing"] else p1["token"]
            else:
                col[len(col) - 1] = p1["token"] if p1["playing"] else p2["token"]
            set_col(index, col)

        print_board()

        if p1["playing"]:
            p1["playing"], p2["playing"] = p2["playing"], p1["playing"]

        elif p2["playing"]:
            p2["playing"], p1["playing"] = p1["playing"], p2["playing"]


if __name__ == "__main__":
    print_board()
    # diagonals = get_diagonals(0, 0)
    # first_diagonal = diagonals.get("first_diagonal")
    # print(is_win(first_diagonal))
    # print(get_diagonals(4, 5))
    insert()
