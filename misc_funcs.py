def clear_button_clicked_func(cell_texts, solve_button, clear_button, grid_dim):
    reset_cell_text(cell_texts, grid_dim)
    solve_button["state"] = "normal"
    clear_button["state"] = "disabled"


def i_to_rc(i, grid_dim):
    # Converts the number of a cell to row and column coordinates
    row_coordinate = i // grid_dim
    column_coordinate = i - (grid_dim * row_coordinate)
    return row_coordinate, column_coordinate


def disable_cell_text(cell_texts, grid_dim):
    # Disables all parameter text boxes
    for i in range(grid_dim ** 2):
        cell_texts[i].configure(state="disabled")


def reset_cell_text(cell_texts, grid_dim):
    # Resets all parameter text boxes to their original state
    for i in range(grid_dim ** 2):
        cell_texts[i].configure(state="normal")
        cell_texts[i].tag_add("make black", "1.0", "end")
        cell_texts[i].tag_config("make black", foreground="black")
        cell_texts[i].delete("1.0")


def size_str_to_int(number_string):
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
