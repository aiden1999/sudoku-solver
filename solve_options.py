import tkinter as tk
import math
import solve


class SolveClear:
    # Solve and clear buttons
    def __init__(self, root, container):
        # container: where the frame is contained, root: app
        self.buttons_frame = tk.Frame(container)
        self.solve_button = tk.Button(self.buttons_frame, text="Solve", font=20, command=root.solve_button_clicked)
        self.solve_button.grid(column=0, row=0, padx=5)
        self.clear_button = tk.Button(self.buttons_frame, text="Clear", font=20, command=root.clear_button_clicked)
        self.clear_button.grid(column=1, row=0, padx=5)
        self.clear_button["state"] = "disabled"
        self.buttons_frame.grid(column=0, row=5, pady=5)


class MiscOptions:
    # Options for which cells to solve: all, random, specific, check progress
    def __init__(self, container, root):
        self.cell_option = tk.StringVar()  # The chosen option

        self.misc_options_frame = tk.Frame(container, borderwidth=5, relief="groove")
        cell_option_label = tk.Label(self.misc_options_frame, text="Select cells to solve:", font=20)
        cell_option_label.grid(row=0, sticky="W")

        all_radiobutton = tk.Radiobutton(self.misc_options_frame, text="All cells", value="all",
                                         variable=self.cell_option, font=20)
        all_radiobutton.grid(row=1, sticky="W")
        random_radiobutton = tk.Radiobutton(self.misc_options_frame, text="Random cell", value="random",
                                            variable=self.cell_option, font=20)
        random_radiobutton.grid(row=2, sticky="W")
        specific_radiobutton = tk.Radiobutton(self.misc_options_frame, text="Specific cell(s)", value="specific",
                                              variable=self.cell_option, font=20)
        specific_radiobutton.grid(row=3, sticky="W")
        check_progress_radiobutton = tk.Radiobutton(self.misc_options_frame, text="Check progress",
                                                    value="check_progress", variable=self.cell_option, font=20)
        check_progress_radiobutton.grid(row=4, sticky="W")
        self.cell_option.set("all")


class ChooseCellsWindow(tk.Toplevel):
    # Window to choose cell(s) to solve (specific), or to mark which cells were worked out by the user and which cells
    # are puzzle clues.
    def __init__(self, option, cell_texts, display_answer, grid_dim, root):
        super().__init__()

        self.option = option  # One of "all", "random", "specific", "check_progress"
        self.cell_texts = cell_texts  # Text boxes where values are entered onto the grid
        self.display_answer = display_answer  # List of bools, whether the answer of a cell will be displayed or not
        self.grid_dim = grid_dim  # Size of grid (one side)
        self.root = root  # The container (i.e. app)

        self.instructions_label = tk.Message(self, font=20)
        self.instructions_label.pack(pady=10, padx=10)

        self.grid_frame = tk.Frame(self)  # Frame that contains the grid of buttons
        self.cell_frames = []  # Frames that each contain an individual button
        self.grid_buttons = []  # List of buttons

        # Create inner_grid_frames, grid_buttons, display_answers
        for i in range(grid_dim ** 2):
            if self.grid_dim > 9:
                self.cell_frames.append(tk.Frame(self.grid_frame, height=30, width=30))
            else:
                self.cell_frames.append(tk.Frame(self.grid_frame, height=50, width=50))
            self.cell_frames[i].pack_propagate(0)
            self.grid_buttons.append(tk.Button(self.cell_frames[i], width=10, height=10, bg="white",
                                               command=lambda x=i: self.grid_button_clicked(x)))
            self.grid_buttons[i].pack(fill="both", expand=1)
            self.display_answer.append(False)

        # Display cell_frames, arranging into blocks
        if self.grid_dim == 6:
            for j in range(6):
                for i in range(6):
                    i_diff = i // 2
                    j_diff = j // 3
                    self.cell_frames[i + (j * 6)].grid(row=(j + j_diff), column=(i + i_diff))
            # Add space between blocks
            for i in range(6, 12):
                self.cell_frames[i].grid(pady=(0, 15))
            for i in range(18, 24):
                self.cell_frames[i].grid(pady=(0, 15))
            for i in range(36):
                if i % 6 == 2:
                    self.cell_frames[i].grid(padx=(0, 15))
        else:
            gd_sqrt = int(math.sqrt(self.grid_dim))
            for j in range(self.grid_dim):
                for i in range(self.grid_dim):
                    i_diff = i // gd_sqrt
                    j_diff = j // gd_sqrt
                    self.cell_frames[i + (j * self.grid_dim)].grid(row=(j + j_diff), column=(i + i_diff))
            # Horizontal space
            for j in range(1, gd_sqrt):
                for i in range((self.grid_dim * ((j * gd_sqrt) - 1)), self.grid_dim * (j * gd_sqrt)):
                    self.cell_frames[i].grid(pady=(0, 15))
            # Vertical space
            for j in range(1, gd_sqrt):
                for i in range(grid_dim ** 2):
                    if i % grid_dim == (gd_sqrt * j) - 1:
                        self.cell_frames[i].grid(padx=(0, 15))

        self.grid_frame.pack(padx=10, pady=10)
        self.done_button = tk.Button(self, font=20, text="Done", command=self.done_button_clicked)
        self.done_button.pack(padx=10, pady=10)

        if self.option == "check_progress":
            self.instructions_label["text"] = ("Toggle buttons so that the cells that contain provided values are "
                                               "black, so that cells that contain answers worked out by you are blue")
            self.instructions_label["width"] = 500
            for i in range(grid_dim ** 2):
                self.grid_buttons[i]["bg"] = "black"
                if self.cell_texts[i].get("1.0", 'end - 1c') == "":  # Empty cells can't be selected
                    self.grid_buttons[i]["bg"] = "white"
                    self.grid_buttons[i]["state"] = "disabled"
                else:
                    self.display_answer[i] = True  # So all cells with a number in them have display_answer be true

        if self.option == "specific":
            self.instructions_label["text"] = "Toggle buttons so that the cells to be solved are blue"
            for i in range(grid_dim ** 2):
                self.grid_buttons[i]["bg"] = "white"
                if self.cell_texts[i].get("1.0", 'end - 1c') != "":  # Cells that aren't empty can't be selected
                    self.grid_buttons[i]["bg"] = "black"
                    self.grid_buttons[i]["state"] = "disabled"
                    self.display_answer[i] = True

    def grid_button_clicked(self, i):
        # Grid button i is clicked
        grid_button_clicked_func(self.option, self.grid_buttons, self.display_answer, i)

    def done_button_clicked(self):
        solve.solve_sudoku(self.cell_texts, self.root.misc_solve_options.cell_option.get(), self.display_answer,
                           self.root.solve_clear.solve_button, self.root.solve_clear.clear_button,
                           self.root.puzzle_config.grid_dim, self.root.puzzle_config.puzzle_type.get(),
                           self.root.ks_cages, self.root.ks_totals)
        # Close window once finished
        self.destroy()


def grid_button_clicked_func(option, grid_buttons, display_answer, i):
    if option == "specific":
        if grid_buttons[i]["bg"] == "white":  # Mark cells that aren't going to be solved as to be solved
            grid_buttons[i]["bg"] = "blue"
            display_answer[i] = True
        elif grid_buttons[i]["bg"] == "blue":  # Mark cells that are going to be solved as not going to be solved
            grid_buttons[i]["bg"] = "white"
            display_answer[i] = False

    if option == "check_progress":
        if grid_buttons[i]["bg"] == "black":  # Mark original answer as user answer
            grid_buttons[i]["bg"] = "blue"
            display_answer[i] = False
        elif grid_buttons[i]["bg"] == "blue":  # Mark user answer as original answer
            grid_buttons[i]["bg"] = "black"
            display_answer[i] = True
