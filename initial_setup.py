""" Contains everything for setting up the puzzle grid.

Classes:
    App: A tkinter window that contains most of the UI for the program and acts as the main backbone.
    PuzzleConfig: UI where the user chooses what type of sudoku puzzle to solve, and in the case of standard sudoku,
        selecting the grid size.
"""

from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING
from ks_cages_setup import ks_total_clicked, KillerSudokuCageDef
from misc_funcs import size_str_to_int
from puzzle_grids import GreaterThanSudokuGrid, HyperSudokuGrid, KillerSudokuGrid, SudokuGrid
from solve import solve_sudoku
from solve_options import ChooseCellsWindow, MiscOptions, SolveClear
if TYPE_CHECKING:
    from ks_cages_setup import KillerSudokuCageDef


class App(tk.Tk):
    """ A tkinter window that contains most of the UI for the program and acts as the main backbone.

    Attributes:
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

    Methods:
        clear_button_clicked: Clears numbers from the puzzle grid.
        grid_layout_done_button_clicked: Initiates the next steps in creating the sudoku puzzle grid for the user to
            fill in.
        ks_done_button_clicked: User has finished adding a total to a killer sudoku cage.
        reset_cell_text: Resets all the text boxes (in the puzzle grid cells) to their original state.
        show_solve_options: Shows options for which cells to solve, and solve/clear buttons.
        solve_button_clicked: Solves the sudoku puzzle.
    """

    def __init__(self) -> None:
        """Initiates App"""

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
        """ Initiates the next steps in creating the sudoku puzzle grid for the user to fill in.

        If the puzzle type is killer sudoku, then another window is opened where killer sudoku cages are defined.
        Otherwise, the puzzle grid is created and the relevant UI is revealed and removed.
        """

        if self.puzzle_config.puzzle_type.get() == "sudoku":
            current_size_txt = self.puzzle_config.grid_size_combobox.get()
            self.puzzle_config.grid_dim = size_str_to_int(current_size_txt)
            self.puzzle_grid = SudokuGrid(self, self.puzzle_config.grid_dim)
            self.puzzle_grid.grid(column=0, row=0)
            App.show_solve_options(self)
            self.puzzle_config.options_frame.grid_remove()

        if self.puzzle_config.puzzle_type.get() == "killer_sudoku":
            self.killer_sudoku_cage_def = KillerSudokuCageDef(self)

        if self.puzzle_config.puzzle_type.get() == "hyper_sudoku":
            self.puzzle_config.grid_dim = 9
            self.puzzle_grid = HyperSudokuGrid(self)
            self.puzzle_grid.grid(column=0, row=0)
            App.show_solve_options(self)
            self.puzzle_config.options_frame.grid_remove()

        if self.puzzle_config.puzzle_type.get() == "greater_than_sudoku":
            self.puzzle_config.grid_dim = 9
            self.puzzle_grid = GreaterThanSudokuGrid(self)
            self.puzzle_grid.grid(column=0, row=0)
            App.show_solve_options(self)
            self.puzzle_config.options_frame.grid_remove()

    def show_solve_options(self) -> None:
        """ Shows options for which cells to solve, and solve/clear buttons. """

        self.misc_solve_options.misc_options_frame.grid(column=0, row=0)
        self.solve_clear.buttons_frame.grid(column=0, row=1)
        self.options_frame.grid(column=1, row=0, padx=(0, 20))

    def solve_button_clicked(self) -> None:
        """ Solves the sudoku puzzle.

        If the solving option is specific cell(s) or check progress, then a window is created to specify cells to solve
        (cell_option = specific) or mark which cells are worked out by the user (cell_option = check_progress).
        """

        if (self.misc_solve_options.cell_option.get() == "specific") or \
                (self.misc_solve_options.cell_option.get() == "check_progress"):
            self.choose_cells_window = ChooseCellsWindow(self)
        else:
            solve_sudoku(self)

    def clear_button_clicked(self) -> None:
        """ Clears numbers from the puzzle grid.

        Also, the solve button is re-enabled, and the clear button is disabled.
        """

        self.reset_cell_text()
        self.solve_clear.solve_button["state"] = "normal"
        self.solve_clear.clear_button["state"] = "disabled"

    def reset_cell_text(self) -> None:
        """ Resets all the text boxes (in the puzzle grid cells) to their original state.

        The text boxes are editable, the font colour becomes black, and the contents of the text boxes is deleted.
        """

        grid_dim = self.puzzle_config.grid_dim
        cell_texts = self.puzzle_grid.cell_texts
        for i in range(grid_dim ** 2):
            cell_texts[i].configure(state="normal")
            cell_texts[i].tag_add("make black", "1.0", "end")
            cell_texts[i].tag_config("make black", foreground="black")
            cell_texts[i].delete("1.0")

    def ks_done_button_clicked(self) -> None:
        """ User has finished adding a total to a killer sudoku cage.

         Either every cell is in one cage, so stops assigning cells to cages, to draw the puzzle grid. Or, not every
         cell is in a cage, so 'resets' the adding total-related UI.
         """

        all_selected, valid_total = ks_total_clicked(self)
        if all_selected:
            self.puzzle_grid = KillerSudokuGrid(self)
            self.puzzle_grid.grid(column=0, row=0)
            self.show_solve_options()
            self.puzzle_config.options_frame.grid_remove()
            self.killer_sudoku_cage_def.destroy()
            self.puzzle_config.grid_dim = 9
        else:
            if valid_total:
                self.killer_sudoku_cage_def.instructions_2_label["foreground"] = "grey"
                self.killer_sudoku_cage_def.total_text.delete(1.0, "end")
                self.killer_sudoku_cage_def.total_text["state"] = "disabled"
                self.killer_sudoku_cage_def.add_total_button["state"] = "disabled"


class PuzzleConfig:
    """ UI where the user chooses what type of sudoku puzzle to solve, and in the case of standard sudoku, selecting
    the grid size.

    Attributes:
        container (App): Where the UI is all contained.
        current_size (tk.StringVar): Size of the standard sudoku (if chosen). Used with the grid size combobox.
        grid_dim (int): Size of grid as length of a side, e.g. a 9x9 grid has grid_dim = 9. Initialises as a None type.
        grid_size_combobox (tkk.Combobox): Combobox (dropdown menu) to choose the size of grid - for standard
            sudoku only.
        grid_size_frame (tk.Frame): Frame used to contain grid size combobox and relevant label.
        options_frame (tk.Frame): Contains the frame for the puzzle type radio buttons and the frame for the grid size
            combobox.
        puzzle_type (tk.StringVar): The type of puzzle.

    Methods:
        other_rb_clicked: Hides the grid size combobox if a radiobutton for a puzzle type that is not standard sudoku
            is clicked.
        sudoku_rb_clicked: Show the grid size combobox if the standard sudoku radiobutton is clicked.
    """

    def __init__(self, container: App) -> None:
        """ Initiates PuzzleConfig. """

        self.grid_dim = None
        self.container = container
        self.puzzle_type = tk.StringVar()

        self.options_frame = tk.Frame(container, borderwidth=5, relief="groove")
        self.options_frame.grid(column=1, row=0, padx=20, pady=10)

        # Choosing the type of puzzle
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
        gt_sudoku_rb = tk.Radiobutton(puzzle_type_rb_frame, text="Greater Than Sudoku", value="greater_than_sudoku",
                                      variable=self.puzzle_type, font=20, command=self.other_rb_clicked)
        gt_sudoku_rb.grid(row=4, sticky="W")
        self.puzzle_type.set("sudoku")

        # Choosing the size of the grid
        self.grid_size_frame = tk.Frame(self.options_frame)
        self.grid_size_frame.grid(row=1, sticky="W", pady=5)
        grid_size_label = tk.Label(self.grid_size_frame, text="Choose a grid size:", font=20)
        grid_size_label.grid(column=0, row=0, )
        self.current_size = tk.StringVar()
        self.grid_size_combobox = ttk.Combobox(self.grid_size_frame, textvariable=self.current_size, state="readonly",
                                               values=["4 x 4", "6 x 6", "9 x 9", "16 x 16", "25 x 25"])
        self.grid_size_combobox.set("9 x 9")
        self.grid_size_combobox.grid(column=1, row=0, padx=5)

        # Confirming layout of puzzle grid
        grid_layout_done_button = tk.Button(self.options_frame, text="Done", font=20,
                                            command=container.grid_layout_done_button_clicked)
        grid_layout_done_button.grid(row=2, column=0, sticky="W", padx=5, pady=5)

    def sudoku_rb_clicked(self) -> None:
        """ Show the grid size combobox is the standard sudoku radiobutton is clicked. """

        self.grid_size_frame.grid(row=1, sticky="W", pady=5)

    def other_rb_clicked(self) -> None:
        """ Hides the grid size combobox if a radiobutton for a puzzle type that is not standard sudoku is clicked. """

        self.grid_size_frame.grid_remove()
