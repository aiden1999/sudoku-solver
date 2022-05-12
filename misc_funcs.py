import tkinter as tk


def i_to_rc(i: int, grid_dim: int) -> tuple[int, int]:
    """ Converts the index of a cell to row and column coordinates.

    Args:
        i (int): The index of a cell.
        grid_dim: Height/width of the grid. E.g. for a 9 x 9 grid, grid_dim = 9.

    Returns: A pair of integers, row_coordinate and column coordinate.
    """
    row_coordinate = i // grid_dim
    column_coordinate = i - (grid_dim * row_coordinate)
    return row_coordinate, column_coordinate


def disable_cell_text(cell_texts: list[tk.Text], grid_dim: int) -> None:
    # Disables all parameter text boxes
    for i in range(grid_dim ** 2):
        cell_texts[i].configure(state="disabled")


def size_str_to_int(number_string: str) -> int:
    if number_string == "4 x 4":
        return 4
    if number_string == "6 x 6":
        return 6
    if number_string == "9 x 9":
        return 9
    if number_string == "16 x 16":
        return 16
    if number_string == "25 x 25":
        return 25
