from __future__ import annotations
from math import sqrt
import tkinter as tk
from typing import TYPE_CHECKING
from solve import solve_sudoku

if TYPE_CHECKING:
    from initial_setup import App


class SolveClear:
    """
    Attributes:
        buttons_frame (tk.Frame):
        clear_button (tk.Button):
        solve_button (tk.Button):
    """
    def __init__(self, root: App, container: tk.Frame) -> None:
        # container: where the frame is contained, root: app
        self.buttons_frame = tk.Frame(container)
        self.solve_button = tk.Button(self.buttons_frame, text="Solve", font=20, command=root.solve_button_clicked)
        self.solve_button.grid(column=0, row=0, padx=5)
        self.clear_button = tk.Button(self.buttons_frame, text="Clear", font=20, command=root.clear_button_clicked)
        self.clear_button.grid(column=1, row=0, padx=5)
        self.clear_button["state"] = "disabled"
        self.buttons_frame.grid(column=0, row=5, pady=5)


class MiscOptions:
    """
    Attributes:
        cell_option (tk.StringVar):
        misc_options_frame (tk.Frame):
    """
    def __init__(self, container: tk.Frame) -> None:
        self.cell_option = tk.StringVar()  # The chosen option

        self.misc_options_frame = tk.Frame(container, borderwidth=5, relief="groove")
        cell_option_label = tk.Label(self.misc_options_frame, text="Select cells to solve:", font=20)
        cell_option_label.grid(row=0, sticky="W")

        all_rb = tk.Radiobutton(self.misc_options_frame, text="All cells", value="all", variable=self.cell_option,
                                font=20)
        all_rb.grid(row=1, sticky="W")
        random_rb = tk.Radiobutton(self.misc_options_frame, text="Random cell", value="random", font=20,
                                   variable=self.cell_option)
        random_rb.grid(row=2, sticky="W")
        specific_rb = tk.Radiobutton(self.misc_options_frame, text="Specific cell(s)", value="specific", font=20,
                                     variable=self.cell_option)
        specific_rb.grid(row=3, sticky="W")
        check_progress_rb = tk.Radiobutton(self.misc_options_frame, text="Check progress", value="check_progress",
                                           variable=self.cell_option, font=20)
        check_progress_rb.grid(row=4, sticky="W")
        self.cell_option.set("all")


class ChooseCellsWindow(tk.Toplevel):
    # Window to choose cell(s) to solve (specific), or to mark which cells were worked out by the user and which cells
    # are puzzle clues.
    """
    Attributes:
        display_answer (list[bool]):
        done_button (tk.Button):
        grid_buttons (list[tk.Button]):
        option (str):

    Methods:
        done_button_clicked:
        grid_button_clicked:
    """
    def __init__(self, root: App) -> None:
        super().__init__()

        self.option = root.misc_solve_options.cell_option.get()  # One of "all", "random", "specific", "check_progress"
        self.display_answer = root.puzzle_grid.display_answer  # List of bools
        cell_texts = root.puzzle_grid.cell_texts  # Text boxes where values are entered onto the grid
        grid_dim = root.puzzle_config.grid_dim  # Size of grid (one side)

        self.grid_buttons = []  # List of buttons

        instructions_label = tk.Message(self, font=20)
        instructions_label.pack(pady=10, padx=10)

        grid_frame = tk.Frame(self)  # Frame that contains the grid of buttons
        cell_frames = []  # Frames that each contain an individual button

        # Create inner_grid_frames, grid_buttons, display_answers
        for i in range(grid_dim ** 2):
            if grid_dim > 9:
                cell_frames.append(tk.Frame(grid_frame, height=30, width=30))
            else:
                cell_frames.append(tk.Frame(grid_frame, height=50, width=50))
            # noinspection PyTypeChecker
            cell_frames[i].pack_propagate(0)
            self.grid_buttons.append(tk.Button(cell_frames[i], width=10, height=10, bg="white",
                                               command=lambda x=i: self.grid_button_clicked(x)))
            self.grid_buttons[i].pack(fill="both", expand=1)
            self.display_answer.append(False)

        # Display cell_frames, arranging into blocks
        if grid_dim == 6:
            for j in range(6):
                for i in range(6):
                    i_diff = i // 2
                    j_diff = j // 3
                    cell_frames[i + (j * 6)].grid(row=(j + j_diff), column=(i + i_diff))
            # Add space between blocks
            for i in range(6, 12):
                cell_frames[i].grid(pady=(0, 15))
            for i in range(18, 24):
                cell_frames[i].grid(pady=(0, 15))
            for i in range(36):
                if i % 6 == 2:
                    cell_frames[i].grid(padx=(0, 15))
        else:
            gd_sqrt = int(sqrt(grid_dim))
            for j in range(grid_dim):
                for i in range(grid_dim):
                    i_diff = i // gd_sqrt
                    j_diff = j // gd_sqrt
                    cell_frames[i + (j * grid_dim)].grid(row=(j + j_diff), column=(i + i_diff))
            # Horizontal space
            for j in range(1, gd_sqrt):
                for i in range((grid_dim * ((j * gd_sqrt) - 1)), grid_dim * (j * gd_sqrt)):
                    cell_frames[i].grid(pady=(0, 15))
            # Vertical space
            for j in range(1, gd_sqrt):
                for i in range(grid_dim ** 2):
                    if i % grid_dim == (gd_sqrt * j) - 1:
                        cell_frames[i].grid(padx=(0, 15))

        grid_frame.pack(padx=10, pady=10)
        self.done_button = tk.Button(self, font=20, text="Done", command=lambda x=root: self.done_button_clicked(x))
        self.done_button.pack(padx=10, pady=10)

        if self.option == "check_progress":
            instructions_label["text"] = ("Toggle buttons so that the cells that contain provided values are "
                                          "black, so that cells that contain answers worked out by you are blue")
            instructions_label["width"] = 500
            for i in range(grid_dim ** 2):
                self.grid_buttons[i]["bg"] = "black"
                if cell_texts[i].get("1.0", 'end - 1c') == "":  # Empty cells can't be selected
                    self.grid_buttons[i]["bg"] = "white"
                    self.grid_buttons[i]["state"] = "disabled"
                else:
                    self.display_answer[i] = True  # So all cells with a number in them have display_answer be true

        if self.option == "specific":
            instructions_label["text"] = "Toggle buttons so that the cells to be solved are blue"
            for i in range(grid_dim ** 2):
                self.grid_buttons[i]["bg"] = "white"
                if cell_texts[i].get("1.0", 'end - 1c') != "":  # Cells that aren't empty can't be selected
                    self.grid_buttons[i]["bg"] = "black"
                    self.grid_buttons[i]["state"] = "disabled"
                    self.display_answer[i] = True

    def grid_button_clicked(self, i: int) -> None:
        # Grid button i is clicked
        if self.option == "specific":
            if self.grid_buttons[i]["bg"] == "white":  # Mark cells that aren't going to be solved as to be solved
                self.grid_buttons[i]["bg"] = "blue"
                self.display_answer[i] = True
            elif self.grid_buttons[i]["bg"] == "blue":  # Reverse of above
                self.grid_buttons[i]["bg"] = "white"
                self.display_answer[i] = False
        if self.option == "check_progress":
            if self.grid_buttons[i]["bg"] == "black":  # Mark original answer as user answer
                self.grid_buttons[i]["bg"] = "blue"
                self.display_answer[i] = False
            elif self.grid_buttons[i]["bg"] == "blue":  # Mark user answer as original answer
                self.grid_buttons[i]["bg"] = "black"
                self.display_answer[i] = True

    def done_button_clicked(self, root: App) -> None:
        solve_sudoku(root)
        # Close window once finished
        self.destroy()
