import tkinter as tk
import random
from tkinter import messagebox
import misc_funcs
import initial_setup


class KillerSudokuCageDef(tk.Toplevel):
    def __init__(self, root: initial_setup.App) -> None:
        super().__init__()

        self.ks_count = 0  # Number of cells that are currently in the current cage

        grid_frame = tk.Frame(self)  # Frame that contains block_frames
        instructions_1_label = tk.Label(self, font=20, text="Select adjacent cells to form one cage")
        instructions_1_label.pack(pady=10, padx=10)

        # Creating smaller frames to contain buttons
        self.grid_buttons = []
        cell_frames = []  # Frames that each contain one button
        for i in range(81):  # Put buttons into frames
            cell_frames.append(tk.Frame(grid_frame, height=50, width=50))
            # noinspection PyTypeChecker
            cell_frames[i].pack_propagate(0)
            self.grid_buttons.append(tk.Button(cell_frames[i], width=10, height=10, bg="white",
                                               command=lambda x=i: self.grid_button_clicked(x)))
            self.grid_buttons[i].pack(fill="both", expand=1)

        # Arranging the cell frames into block frames
        for j in range(9):
            for i in range(9):
                i_diff = i // 3
                j_diff = j // 3
                cell_frames[i + (j * 9)].grid(row=(j + j_diff), column=(i + i_diff))
        # Add space between blocks
        for i in range(18, 27):
            cell_frames[i].grid(pady=(0, 15))
        for i in range(45, 54):
            cell_frames[i].grid(pady=(0, 15))
        for i in range(81):
            if i % 9 == 2:
                cell_frames[i].grid(padx=(0, 15))
            if i % 9 == 5:
                cell_frames[i].grid(padx=(0, 15))

        # Placing the grid frame onto the window
        grid_frame.pack(padx=10, pady=10)

        # Button for when the user has finished defining which cells make up one cage
        self.cage_done_button = tk.Button(self, font=20, text="Add cage's total", state="disabled",
                                          command=self.cage_done_button_clicked)
        self.cage_done_button.pack(padx=10, pady=10)

        self.instructions_2_label = tk.Label(self, font=20, text="Enter the total for this cage", foreground="grey")
        self.instructions_2_label.pack(padx=10, pady=10)

        self.total_text = tk.Text(self, font=20, height=1, width=10, state="disabled")
        self.total_text.pack(padx=10, pady=10)

        self.add_total_button = tk.Button(self, font=20, text="Done, define next cage", state="disabled",
                                          command=root.ks_done_button_clicked)
        self.add_total_button.pack(padx=10, pady=10)

    def grid_button_clicked(self, i: int) -> None:
        # Button in grid clicked
        self.ks_count = ks_grid_button_clicked(i, self.grid_buttons, self.ks_count)
        if self.ks_count == 9:  # Warn the user that they have reached the maximum cage size
            for j in range(81):
                if self.grid_buttons[j]["bg"] == "white":
                    self.grid_buttons[j]["state"] = "disabled"
            messagebox.showwarning("Warning", "You have reached the maximum cage size")
            self.cage_done_button["state"] = "normal"
        elif self.ks_count == 8:  # Enables the grid buttons if the user went down from 9 to 8
            for j in range(81):
                if self.grid_buttons[j]["bg"] == "white":
                    self.grid_buttons[j]["state"] = "normal"
            self.cage_done_button["state"] = "normal"
        # Can only click done button if at least one cell has been selected (at least one button clicked)
        elif self.ks_count > 0:
            self.cage_done_button["state"] = "normal"
        else:
            self.cage_done_button["state"] = "disabled"

    def cage_done_button_clicked(self) -> None:
        # Cells that are in a cage have been defined
        for i in range(81):
            self.grid_buttons[i]["state"] = "disabled"
        # Relevant UI is now visible/usable
        self.instructions_2_label["foreground"] = "black"
        self.total_text["state"] = "normal"
        self.add_total_button["state"] = "normal"
        self.ks_count = 0
        self.cage_done_button["state"] = "disabled"


def ks_grid_button_clicked(i: int, grid_buttons: list[tk.Button], ks_count: int) -> int:
    # Toggles grid buttons between selected and not selected
    count = ks_count
    if grid_buttons[i]["bg"] == "white":  # Mark cell as part of a cage
        grid_buttons[i]["bg"] = "blue"
        count = count + 1
    elif grid_buttons[i]["bg"] == "blue":
        grid_buttons[i]["bg"] = "white"
        count = count - 1
    return count  # Returns the number of cells that are in the current cage


def ks_total_clicked(root: initial_setup.App) -> tuple[bool, bool]:

    grid_buttons = root.killer_sudoku_cage_def.grid_buttons
    ks_cages = root.ks_cages
    total_text = root.killer_sudoku_cage_def.total_text
    ks_totals = root.ks_totals

    # User has entered the total and is therefore finished with defining the cage
    cage_size = 0
    for i in range(81):
        if grid_buttons[i]["bg"] == "blue":
            cage_size = cage_size + 1
    total = int(total_text.get("1.0", 'end - 1c'))
    if total > cage_max_total(cage_size):
        messagebox.showerror("Error", "The total for this cage is too large")
        return False, False
    else:
        cage = []
        chosen_button_count = 0  # Buttons that have been clicked overall, i.e. the no. of cells that belong to a cage
        for i in range(81):
            if grid_buttons[i]["bg"] == "blue":  # Button has been selected
                cage.append(i)  # Add its location to the current cage
                grid_buttons[i]["state"] = "disabled"
                grid_buttons[i]["bg"] = "dark grey"
            if grid_buttons[i]["bg"] == "dark grey":  # All buttons whose corresponding cell belongs to a cage
                chosen_button_count = chosen_button_count + 1
            else:
                grid_buttons[i]["state"] = "normal"
        ks_cages.append(cage)
        ks_totals.append(total)
        if chosen_button_count == 81:  # All cells are in a cage
            return True, True
        else:
            return False, True


def generate_ks_colours(cages: list[list[int]]) -> list[str]:
    # Assign colours to the cages such that adjacent cages are not the same colour
    possible_colours = ["light blue", "pink", "pale green", "light goldenrod", "tomato", "sienna1", "orchid1"]
    chosen_colours = []
    for i in range(81):
        chosen_colours.append("white")
    for cage in cages:
        cage_adj_colours = []
        colour_choice = None
        for cell in cage:  # Determine adjacent colours
            cell_row = misc_funcs.i_to_rc(cell, 9)[0]
            cell_col = misc_funcs.i_to_rc(cell, 9)[1]
            if cell == 0:  # Top left corner
                cage_adj_colours.append(chosen_colours[1])
                cage_adj_colours.append(chosen_colours[9])
                cage_adj_colours.append(chosen_colours[10])
            elif cell == 8:  # Top right corner
                cage_adj_colours.append(chosen_colours[7])
                cage_adj_colours.append(chosen_colours[16])
                cage_adj_colours.append(chosen_colours[17])
            elif cell == 72:  # Bottom left corner
                cage_adj_colours.append(chosen_colours[63])
                cage_adj_colours.append(chosen_colours[64])
                cage_adj_colours.append(chosen_colours[73])
            elif cell == 80:  # Bottom right corner
                cage_adj_colours.append(chosen_colours[79])
                cage_adj_colours.append(chosen_colours[71])
                cage_adj_colours.append(chosen_colours[70])
            elif cell_row == 0:  # Top row
                cage_adj_colours.append(chosen_colours[cell - 1])
                cage_adj_colours.append(chosen_colours[cell + 1])
                cage_adj_colours.append(chosen_colours[cell + 9])
                cage_adj_colours.append(chosen_colours[cell + 8])
                cage_adj_colours.append(chosen_colours[cell + 10])
            elif cell_row == 8:  # Bottom row
                cage_adj_colours.append(chosen_colours[cell - 1])
                cage_adj_colours.append(chosen_colours[cell + 1])
                cage_adj_colours.append(chosen_colours[cell - 9])
                cage_adj_colours.append(chosen_colours[cell - 8])
                cage_adj_colours.append(chosen_colours[cell - 10])
            elif cell_col == 0:  # Left column
                cage_adj_colours.append(chosen_colours[cell - 9])
                cage_adj_colours.append(chosen_colours[cell - 8])
                cage_adj_colours.append(chosen_colours[cell + 1])
                cage_adj_colours.append(chosen_colours[cell + 9])
                cage_adj_colours.append(chosen_colours[cell + 10])
            elif cell_col == 8:  # Right column
                cage_adj_colours.append(chosen_colours[cell - 9])
                cage_adj_colours.append(chosen_colours[cell - 10])
                cage_adj_colours.append(chosen_colours[cell - 1])
                cage_adj_colours.append(chosen_colours[cell + 8])
                cage_adj_colours.append(chosen_colours[cell + 9])
            else:  # All other cells
                cage_adj_colours.append(chosen_colours[cell - 10])
                cage_adj_colours.append(chosen_colours[cell - 9])
                cage_adj_colours.append(chosen_colours[cell - 8])
                cage_adj_colours.append(chosen_colours[cell - 1])
                cage_adj_colours.append(chosen_colours[cell + 1])
                cage_adj_colours.append(chosen_colours[cell + 8])
                cage_adj_colours.append(chosen_colours[cell + 9])
                cage_adj_colours.append(chosen_colours[cell + 10])
        valid_colour = False
        while not valid_colour:
            colour_choice = random.choice(possible_colours)
            valid_colour = True
            for colour in cage_adj_colours:
                if colour == colour_choice:
                    valid_colour = False
                    break
        for cell in cage:
            chosen_colours[cell] = colour_choice
    return chosen_colours


def cage_max_total(cage_size: int) -> int:
    max_total = 0
    for i in range(cage_size):
        max_total = max_total + (9 - i)
    return max_total
