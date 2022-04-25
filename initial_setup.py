import tkinter as tk
from tkinter import ttk
import misc_funcs
import ks_cages_setup
import puzzle_grids
import solve_options
import solve


class App(tk.Tk):  # Main app class
    def __init__(self):
        super().__init__()

        self.misc_solve_options = None  # Frame containing random, specific cell, check progress etc.
        self.killer_sudoku_cage_def = None  # Window where the cages of a killer sudoku puzzle are defined
        self.choose_cells_window = None  # Window for choosing cells when using specific cell option or check progress
        self.solve_clear = None  # Frame containing solve and clear buttons
        self.options_frame = tk.Frame()  # Frame containing options (random etc.) and solve/clear buttons
        self.ks_cages = []  # List of lists (cages) of ints (cells)
        self.ks_totals = []  # List of ints, ks_totals[n] corresponds to ks_cages[n]

        self.title("Puzzle Solver")
        self.puzzle_config = PuzzleConfig(self)  # create window for choosing the type of puzzle

    def grid_layout_done_button_clicked(self):
        # Clicked when the user has decided what sort of sudoku puzzle they would like to solve
        if self.puzzle_config.puzzle_type.get() == "sudoku":
            current_size_txt = self.puzzle_config.grid_size_combobox.get()
            self.puzzle_config.grid_dim = misc_funcs.size_str_to_int(current_size_txt)
            puzzle_grid = puzzle_grids.SudokuGrid(self, self.puzzle_config.grid_dim)
            puzzle_grid.grid(column=0, row=0)
            App.show_solve_options(self)
            self.puzzle_config.options_frame.grid_remove()

        if self.puzzle_config.puzzle_type.get() == "killer_sudoku":
            self.killer_sudoku_cage_def = ks_cages_setup.KillerSudokuCageDef(self)
            # Opens a window to define where killer sudoku cages are and their totals

        if self.puzzle_config.puzzle_type.get() == "hyper_sudoku":
            self.puzzle_config.grid_dim = 9
            puzzle_grid = puzzle_grids.HyperSudokuGrid(self)
            puzzle_grid.grid(column=0, row=0)
            App.show_solve_options(self)
            self.puzzle_config.options_frame.grid_remove()

        if self.puzzle_config.puzzle_type.get() == "greater_than_sudoku":
            self.puzzle_config.grid_dim = 9
            puzzle_grid = puzzle_grids.GreaterThanSudokuGrid(self)
            puzzle_grid.grid(column=0, row=0)
            App.show_solve_options(self)
            self.puzzle_config.options_frame.grid_remove()

    def show_solve_options(self):
        # Show options for which cells to solve, and solve/clear buttons
        self.misc_solve_options = solve_options.MiscOptions(self.options_frame)
        self.misc_solve_options.misc_options_frame.grid(column=0, row=0)
        self.solve_clear = solve_options.SolveClear(self, self.options_frame)
        self.solve_clear.buttons_frame.grid(column=0, row=1)
        self.options_frame.grid(column=1, row=0, padx=(0, 20))

    def solve_button_clicked(self):
        # Solve the sudoku puzzle
        if self.misc_solve_options.cell_option.get() == ("specific" or "check_progress"):
            self.choose_cells_window = solve_options.ChooseCellsWindow(self)
        else:
            solve.solve_sudoku(self)

    def clear_button_clicked(self):
        # Clear user-entered numbers on the sudoku grid
        misc_funcs.clear_button_clicked_func(self)

    def ks_done_button_clicked(self):
        # Button for where the user has finished typing a cage's total has been clicked
        all_selected, valid_total = ks_cages_setup.ks_total_clicked(self)
        if all_selected:  # Every cell is in one cage, stop assigning cells to cages, so puzzle grid can be drawn
            puzzle_grid = puzzle_grids.KillerSudokuGrid(self)
            puzzle_grid.grid(column=0, row=0)
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
    def __init__(self, container):
        self.grid_dim = None  # Size of grid as length of a side, e.g. a 9x9 grid has grid_dim = 9
        self.container = container
        self.puzzle_type = tk.StringVar()

        # Grid options: shows on launch
        self.options_frame = tk.Frame(container, borderwidth=5, relief="groove")
        self.options_frame.grid(column=1, row=0, padx=20, pady=10)

        # Choosing the type of puzzle
        puzzle_type_radiobutton_frame = tk.Frame(self.options_frame)
        puzzle_type_radiobutton_frame.grid(row=0, sticky="W")
        puzzle_type_label = tk.Label(puzzle_type_radiobutton_frame, text="Select a type of puzzle to solve:", font=20)
        puzzle_type_label.grid(row=0, sticky="W")

        sudoku_radiobutton = tk.Radiobutton(puzzle_type_radiobutton_frame, text="Sudoku", value="sudoku",
                                            variable=self.puzzle_type, font=20, command=self.sudoku_radiobutton_clicked)
        sudoku_radiobutton.grid(row=1, sticky="W")
        killer_sudoku_radiobutton = tk.Radiobutton(puzzle_type_radiobutton_frame, text="Killer Sudoku",
                                                   value="killer_sudoku", variable=self.puzzle_type, font=20,
                                                   command=self.other_radiobutton_clicked)
        killer_sudoku_radiobutton.grid(row=2, sticky="W")
        hyper_sudoku_radiobutton = tk.Radiobutton(puzzle_type_radiobutton_frame, text="Hyper Sudoku",
                                                  value="hyper_sudoku", variable=self.puzzle_type, font=20,
                                                  command=self.other_radiobutton_clicked)
        hyper_sudoku_radiobutton.grid(row=3, sticky="W")
        greater_than_sudoku_radiobutton = tk.Radiobutton(puzzle_type_radiobutton_frame, text="Greater Than Sudoku",
                                                         value="greater_than_sudoku", variable=self.puzzle_type,
                                                         font=20, command=self.other_radiobutton_clicked)
        greater_than_sudoku_radiobutton.grid(row=4, sticky="W")
        self.puzzle_type.set("sudoku")

        # Choosing the size of the grid
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

    def sudoku_radiobutton_clicked(self):
        self.grid_size_frame.grid(row=1, sticky="W", pady=5)  # Show the grid size dropdown menu

    def other_radiobutton_clicked(self):
        self.grid_size_frame.grid_remove()  # Hide the grid size dropdown menu
