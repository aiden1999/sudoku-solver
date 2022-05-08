from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
from ks_cages_setup import ks_total_clicked
from misc_funcs import size_str_to_int
from puzzle_grids import GreaterThanSudokuGrid, HyperSudokuGrid, KillerSudokuGrid, SudokuGrid
from solve import solve_sudoku
from solve_options import ChooseCellsWindow, MiscOptions, SolveClear
if TYPE_CHECKING:
    from ks_cages_setup import KillerSudokuCageDef


class App(tk.Tk):
    """A tkinter window that contains most of the UI for the program and acts as the main backbone.

    Attributes
        choose_cells_window (ChooseCellsWindow): Window for marking cells when using specific cell option or check
            progress option. Has None type initially as it is not created unless it is needed.
        killer_sudoku_cage_def (KillerSudokuCageDef): A window where the cages of a killer sudoku puzzle are defined.
            Has None type initially as the window is not created until the user has chosen to solve a killer sudoku
            puzzle.
        ks_cages (list[list[int]]): A list of lists (each list represents a cage) of ints (each int represents a cell
            in said cage). Initially an empty list.
        ks_totals (list[int]): A list of ints. ks_totals[i] is the total of the cage in ks_cages[i].
        misc_solve_options (MiscOptions): A set of tkinter radio buttons that allow the user to choose whether they
            want to be shown the entire solution, a random cell, specific cell(s) of their choosing, or to check their
            current progress.
        options_frame (tk.Frame): Contains the solving options radio buttons, and the 'solve' and 'clear' buttons.
        puzzle_config (PuzzleConfig): Contains the UI for choosing the type of puzzle to solve. The first thing the
            user would see.
        puzzle_grid (GreaterThanSudokuGrid, HyperSudokuGrid, KillerSudokuGrid, or SudokuGrid): The actual sudoku puzzle
            grid. Has None type when initially created, as the user would have not yet decided which type of sudoku
            puzzle they are solving.
        solve_clear (SolveClear): Contains a frame with the 'solve' and 'clear' buttons.

    Methods
        clear_button_clicked: Clear numbers from the puzzle grid.
        grid_layout_done_button_clicked: What happens after the user has decided which type of sudoku puzzle to solve.
            Initiates the next steps in creating the sudoku puzzle grid for the user to fill in.
        ks_done_button_clicked:
        reset_cell_text
        show_solve_options
        solve_button_clicked
    """
    def __init__(self) -> None:
        super().__init__()

        self.puzzle_grid = None
        self.options_frame = tk.Frame()
        self.misc_solve_options = MiscOptions(self.options_frame)
        self.solve_clear = SolveClear(self, self.options_frame)
        self.killer_sudoku_cage_def = None
        self.choose_cells_window = None
        self.ks_cages = []
        self.ks_totals = []
        self.puzzle_config = PuzzleConfig(self)  # Create window for choosing the type of puzzle

        self.title("Puzzle Solver")

    def grid_layout_done_button_clicked(self) -> None:
        if self.puzzle_config.puzzle_type.get() == "sudoku":
            # Get the chosen grid size (string) and convert to an int
            current_size_txt = self.puzzle_config.grid_size_combobox.get()
            self.puzzle_config.grid_dim = size_str_to_int(current_size_txt)
            # Create and display the sudoku grid
            self.puzzle_grid = SudokuGrid(self, self.puzzle_config.grid_dim)
            self.puzzle_grid.grid(column=0, row=0)
            App.show_solve_options(self)  # Show the options for solving the puzzle
            self.puzzle_config.options_frame.grid_remove()  # Hide the sudoku type selection UI

        if self.puzzle_config.puzzle_type.get() == "killer_sudoku":
            # Open a window to define where killer sudoku cages are and their totals
            self.killer_sudoku_cage_def = KillerSudokuCageDef(self)

        if self.puzzle_config.puzzle_type.get() == "hyper_sudoku":
            self.puzzle_config.grid_dim = 9
            # Create and display the hyper sudoku grid
            self.puzzle_grid = HyperSudokuGrid(self)
            self.puzzle_grid.grid(column=0, row=0)
            App.show_solve_options(self)  # Show the options for solving the puzzle
            self.puzzle_config.options_frame.grid_remove()  # Hide the sudoku type selection UI

        if self.puzzle_config.puzzle_type.get() == "greater_than_sudoku":
            self.puzzle_config.grid_dim = 9
            # Create and display the greater than sudoku grid
            self.puzzle_grid = GreaterThanSudokuGrid(self)
            self.puzzle_grid.grid(column=0, row=0)
            App.show_solve_options(self)  # Show the options for solving the puzzle
            self.puzzle_config.options_frame.grid_remove()  # Hide the sudoku type selection UI

    def show_solve_options(self) -> None:
        # Show options for which cells to solve, and solve/clear buttons
        # Create and display the UI for the different solving options (solve all/solve random cell/solve specific cell
        # /check progress)
        self.misc_solve_options.misc_options_frame.grid(column=0, row=0)
        # Create and display the UI for the solve/clear buttons
        self.solve_clear.buttons_frame.grid(column=0, row=1)
        self.options_frame.grid(column=1, row=0, padx=(0, 20))

    def solve_button_clicked(self) -> None:
        # Solve the sudoku puzzle
        if (self.misc_solve_options.cell_option.get() == "specific") or \
                (self.misc_solve_options.cell_option.get() == "check_progress"):
            # Create window to specify cells to solve (cell_option = specific) or mark which cells are worked out by
            # the user.
            self.choose_cells_window = ChooseCellsWindow(self)
        else:
            solve_sudoku(self)

    def clear_button_clicked(self) -> None:
        self.reset_cell_text()
        self.solve_clear.solve_button["state"] = "normal"
        self.solve_clear.clear_button["state"] = "disabled"

    def reset_cell_text(self) -> None:
        # Resets all parameter text boxes to their original state

        grid_dim = self.puzzle_config.grid_dim
        cell_texts = self.puzzle_grid.cell_texts

        for i in range(grid_dim ** 2):
            cell_texts[i].configure(state="normal")
            cell_texts[i].tag_add("make black", "1.0", "end")
            cell_texts[i].tag_config("make black", foreground="black")
            cell_texts[i].delete("1.0")

    def ks_done_button_clicked(self) -> None:
        # Button for where the user has finished typing a cage's total has been clicked
        all_selected, valid_total = ks_total_clicked(self)
        if all_selected:  # Every cell is in one cage, stop assigning cells to cages, so puzzle grid can be drawn
            # Create and display the killer sudoku grid.
            self.puzzle_grid = KillerSudokuGrid(self)
            self.puzzle_grid.grid(column=0, row=0)
            self.show_solve_options()
            self.puzzle_config.options_frame.grid_remove()
            self.killer_sudoku_cage_def.destroy()
            self.puzzle_config.grid_dim = 9
        else:  # Not every cell is in a cage, so 'reset' the adding total-related UI
            if valid_total:
                self.killer_sudoku_cage_def.instructions_2_label["foreground"] = "grey"
                self.killer_sudoku_cage_def.total_text.delete(1.0, "end")
                self.killer_sudoku_cage_def.total_text["state"] = "disabled"
                self.killer_sudoku_cage_def.add_total_button["state"] = "disabled"


class PuzzleConfig:  # Choose what type of sudoku puzzle to solve, and selecting grid size for standard sudoku
    def __init__(self, container: App) -> None:
        self.grid_dim = None  # Size of grid as length of a side, e.g. a 9x9 grid has grid_dim = 9
        self.container = container
        self.puzzle_type = tk.StringVar()

        # Grid options: shows on launch
        self.options_frame = tk.Frame(container, borderwidth=5, relief="groove")
        self.options_frame.grid(column=1, row=0, padx=20, pady=10)

        # Choosing the type of puzzle - set of radio buttons with different choices available
        puzzle_type_rb_frame = tk.Frame(self.options_frame)
        puzzle_type_rb_frame.grid(row=0, sticky="W")
        puzzle_type_label = tk.Label(puzzle_type_rb_frame, text="Select a type of puzzle to solve:", font=20)
        puzzle_type_label.grid(row=0, sticky="W")
        sudoku_rb = tk.Radiobutton(puzzle_type_rb_frame, text="Sudoku", value="sudoku", variable=self.puzzle_type,
                                   font=20, command=self.sudoku_rb_clicked)
        sudoku_rb.grid(row=1, sticky="W")
        killer_sudoku_rb = tk.Radiobutton(puzzle_type_rb_frame, text="Killer Sudoku", value="killer_sudoku",
                                          variable=self.puzzle_type, font=20, command=self.other_rb_clicked)
        killer_sudoku_rb.grid(row=2, sticky="W")
        hyper_sudoku_rb = tk.Radiobutton(puzzle_type_rb_frame, text="Hyper Sudoku", value="hyper_sudoku",
                                         variable=self.puzzle_type, font=20, command=self.other_rb_clicked)
        hyper_sudoku_rb.grid(row=3, sticky="W")
        greater_than_sudoku_rb = tk.Radiobutton(puzzle_type_rb_frame, text="Greater Than Sudoku",
                                                value="greater_than_sudoku", variable=self.puzzle_type, font=20,
                                                command=self.other_rb_clicked)
        greater_than_sudoku_rb.grid(row=4, sticky="W")
        self.puzzle_type.set("sudoku")

        # Choosing the size of the grid - dropdown menu for standard sudoku only
        self.grid_size_frame = tk.Frame(self.options_frame)
        self.grid_size_frame.grid(row=1, sticky="W", pady=5)
        grid_size_label = tk.Label(self.grid_size_frame, text="Choose a grid size:", font=20)
        grid_size_label.grid(column=0, row=0, )
        self.current_size = tk.StringVar()
        self.grid_size_combobox = ttk.Combobox(self.grid_size_frame, textvariable=self.current_size)
        self.grid_size_combobox["values"] = ("4 x 4", "6 x 6", "9 x 9", "16 x 16", "25 x 25")
        self.grid_size_combobox["state"] = "readonly"
        self.grid_size_combobox.set("9 x 9")
        self.grid_size_combobox.grid(column=1, row=0, padx=5)

        # Confirming layout of puzzle grid
        grid_layout_done_button = tk.Button(self.options_frame, text="Done", font=20,
                                            command=container.grid_layout_done_button_clicked)
        grid_layout_done_button.grid(row=2, column=0, sticky="W", padx=5, pady=5)

    def sudoku_rb_clicked(self) -> None:
        self.grid_size_frame.grid(row=1, sticky="W", pady=5)  # Show the grid size dropdown menu

    def other_rb_clicked(self) -> None:
        self.grid_size_frame.grid_remove()  # Hide the grid size dropdown menu
