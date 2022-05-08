from __future__ import annotations
from abc import ABC
from pysat.solvers import Glucose3
from random import randint
import tkinter as tk
from tkinter.messagebox import showerror, showinfo
from typing import TYPE_CHECKING
from clause_creation import define_clauses
from misc_funcs import disable_cell_text, i_to_rc
if TYPE_CHECKING:
    from initial_setup import App


class SatSolver(Glucose3, ABC):
    # SAT solver class
    """

    """
    def __init__(self) -> None:
        super().__init__()


def solve_sudoku(root: App) -> None:

    cell_option = root.misc_solve_options.cell_option.get()
    cell_texts = root.puzzle_grid.cell_texts
    solve_button = root.solve_clear.solve_button
    clear_button = root.solve_clear.clear_button
    grid_dim = root.puzzle_config.grid_dim

    is_valid, puzzle = get_input(cell_texts, grid_dim)  # Bool, is user input valid; Puzzle input as a list of lists
    if is_valid and (cell_option == "check_progress"):
        check_progress(puzzle, root)
    elif is_valid:
        sat_solver = SatSolver()
        define_clauses(puzzle, sat_solver, root)
        if sat_solver.solve():  # There exists a solution
            decode(sat_solver, root)
        else:
            showerror(title="Error", message="No solution found.")
        disable_cell_text(cell_texts, grid_dim)
        solve_button["state"] = "disabled"
        clear_button["state"] = "normal"
        sat_solver.delete()


def get_input(cell_texts: list[tk.Text], grid_dim: int) -> tuple[bool, list[list[str]]]:
    # Retrieves an input from the grid, and also checks if it is a valid input or not
    puzzle = []
    row = []
    is_valid = True
    for i in range(grid_dim ** 2):
        if cell_texts[i].get("1.0", 'end - 1c') == "":
            row.append("0")  # Puts a 0 where the user hasn't entered anything
        elif not (cell_texts[i].get("1.0", 'end - 1c')).isnumeric():  # Check that input is numeric
            showerror(title="Error", message="Only enter numbers.")
            is_valid = False
            break
        elif int(cell_texts[i].get("1.0", 'end - 1c')) > grid_dim:
            showerror(title="Error", message="Numbers must be less than " + str(grid_dim + 1))
            is_valid = False
            break
        else:
            row.append(cell_texts[i].get("1.0"))
        if (i + 1) % grid_dim == 0:  # Check if on the last cell of a row
            puzzle.append(row)  # Add row to puzzle
            row = []
    return is_valid, puzzle


def decode(sat_solver: SatSolver, root: App) -> list[str]:
    # Converts the solution into values for display, and then displays them

    cell_option = root.misc_solve_options.cell_option.get()
    grid_dim = root.puzzle_config.grid_dim
    cell_texts = root.puzzle_grid.cell_texts
    display_answer = root.puzzle_grid.display_answer

    solution = sat_solver.get_model()  # Solution provided by the SAT solver
    true_vars = []
    for i in solution:
        if i > 0:  # Only use the variables that aren't negated, i.e. the variables that are true
            true_vars.append(i)
    row = 0
    column = 0
    true_vars_decoded = []
    for i in true_vars:
        # Convert variables back to usable values for a sudoku grid
        true_vars_decoded.append(i - (grid_dim * column) - ((grid_dim ** 2) * row))
        column = column + 1
        if column == grid_dim:
            row = row + 1
            column = 0

    if cell_option == "all":
        for i in range(grid_dim ** 2):
            if cell_texts[i].get("1.0") == "\n":
                show_answer(cell_texts, true_vars_decoded, i)

    if cell_option == "random":
        empty_cell = False
        random_cell = None
        while not empty_cell:
            # Generate random cell
            random_cell = randint(0, (grid_dim ** 2) - 1)
            if cell_texts[random_cell].get("1.0") == "\n":
                empty_cell = True
        show_answer(cell_texts, true_vars_decoded, random_cell)

    if cell_option == "specific":
        for i in range(grid_dim ** 2):
            if cell_texts[i].get("1.0") == "\n":
                if display_answer[i]:
                    show_answer(cell_texts, true_vars_decoded, i)

    if cell_option == "check_progress":
        return true_vars_decoded


def show_answer(cell_texts: list[tk.Text], true_vars_decoded: list[str], index: int) -> None:
    # Displays the answer in a cell text box
    cell_texts[index].insert("1.0", true_vars_decoded[index])
    cell_texts[index].tag_add("make blue", "1.0", "end")
    cell_texts[index].tag_config("make blue", foreground="blue")


def check_progress(puzzle: list[list[str]], root: App) -> None:

    solve_button = root.solve_clear.solve_button
    clear_button = root.solve_clear.solve_button
    cell_texts = root.puzzle_grid.cell_texts
    grid_dim = root.puzzle_config.grid_dim
    display_answer = root.puzzle_grid.display_answer

    sat_solver = SatSolver()
    define_clauses(puzzle, sat_solver, root)
    if sat_solver.solve():  # The puzzle can be solved with the user's answers, ie the puzzle is correct so far
        showinfo("Congratulations", "Your progress is correct so far.")
        disable_cell_text(cell_texts, grid_dim)
        solve_button["state"] = "disabled"
        clear_button["state"] = "normal"

    else:  # Puzzle couldn't be solved with user's answers, so define original puzzle
        sat_solver.delete()
        original_puzzle = []
        row = []
        for i in range(grid_dim ** 2):
            if display_answer[i]:
                row.append(cell_texts[i].get("1.0"))
            else:
                row.append("0")
            if (i + 1) % grid_dim == 0:
                original_puzzle.append(row)
                row = []
        sat_solver2 = SatSolver()
        define_clauses(original_puzzle, sat_solver2, root)
        if not sat_solver2.solve():  # Original puzzle couldn't be solved
            showerror(title="Error", message="No solution found to original puzzle.")
            disable_cell_text(cell_texts, grid_dim)
            solve_button["state"] = "disabled"
            clear_button["state"] = "normal"
            sat_solver2.delete()

        else:  # Original puzzle can be solved
            original_puzzle_solution = decode(sat_solver2, root)
            incorrect_user_answers = []
            for i in range(grid_dim ** 2):
                row, col = i_to_rc(i, grid_dim)
                if str(original_puzzle_solution[i]) != puzzle[row][col]:
                    # Compare user answers to solution
                    incorrect_user_answers.append(i)
            for i in range(len(incorrect_user_answers)):  # Highlight incorrect user answers
                cell_texts[incorrect_user_answers[i]].tag_add("make red", "1.0", "end")
                cell_texts[incorrect_user_answers[i]].tag_config("make red", foreground="red")
            showinfo("Information", "Errors have been highlighted.")
            disable_cell_text(cell_texts, grid_dim)
            solve_button["state"] = "disabled"
            clear_button["state"] = "normal"
            sat_solver2.delete()
