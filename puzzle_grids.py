""" Creating the different puzzle grids.

Classes:
    SudokuGrid: The grid of a standard sudoku puzzle.
    KillerSudokuGrid: The grid of a killer sudoku puzzle.
    HyperSudokuGrid: The grid of a hyper sudoku puzzle.
    GreaterThanSudokuGrid: The grid of a greater than sudoku puzzle.
"""

from __future__ import annotations
import tkinter as tk
from math import sqrt
from typing import TYPE_CHECKING
from ks_cages_setup import generate_ks_colours
from misc_funcs import i_to_rc
if TYPE_CHECKING:
    from initial_setup import App


class SudokuGrid(tk.Canvas):
    """The grid of a standard sudoku puzzle.

    Attributes:
        cell_texts (list[tk.Text]): Text boxes where one goes in each cell in the grid, where numbers will be entered.
        display_answer (list[bool]): Marks whether a cell's answer will be displayed or not.
    """

    def __init__(self, container: App, grid_size: int) -> None:
        """ Initiates SudokuGrid. """

        super().__init__(container)

        self.cell_texts = []
        self.display_answer = []

        if grid_size == 25:
            cell_width = 36
        else:
            cell_width = 50
        self["width"] = (grid_size * cell_width) + 50
        self["height"] = (grid_size * cell_width) + 50

        # Grid outline
        c1 = 25
        c2 = (grid_size * cell_width) + 25
        self.create_polygon(c1, c1, c1, c2, c2, c2, c2, c1, width=10, fill="white", outline="black")

        # Grid bold lines
        bold_lines = []
        if grid_size == 6:
            bold_lines.append(self.create_line(175, 25, 175, 325, width=8))
            bold_lines.append(self.create_line(25, 125, 325, 125, width=8))
            bold_lines.append(self.create_line(25, 225, 325, 225, width=8))
        else:
            bold_start = int(25 + (cell_width * sqrt(grid_size)))
            bold_stop = int(26 + (cell_width * (grid_size - sqrt(grid_size))))
            bold_step = int(cell_width * sqrt(grid_size))
            for i in range(bold_start, bold_stop, bold_step):
                bold_lines.append(self.create_line(i, c1, i, c2, width=8))
                bold_lines.append(self.create_line(c1, i, c2, i, width=8))

        # Grid light lines
        light_lines = []
        light_start = 25 + cell_width
        light_stop = 26 + (cell_width * (grid_size - 1))
        light_step = cell_width
        for i in range(light_start, light_stop, light_step):
            light_lines.append(self.create_line(i, c1, i, c2, width=4))
            light_lines.append(self.create_line(c1, i, c2, i, width=4))

        # Create cell_texts text boxes
        if grid_size == 25:
            for i in range(625):
                self.cell_texts.append(tk.Text(self, height=1, width=2, font=("Arial", 12), relief="flat"))
                self.display_answer.append(False)
        if grid_size == 16:
            for i in range(256):
                self.cell_texts.append(tk.Text(self, height=1, width=2, font=("Arial", 19), relief="flat"))
                self.display_answer.append(False)
        else:
            for i in range(grid_size ** 2):
                self.cell_texts.append(tk.Text(self, height=1, width=1, font=("Arial", 19), relief="flat"))
                self.display_answer.append(False)

        # Containers to hold text boxes
        grid_windows = []
        for j in range(grid_size):
            for i in range(grid_size):
                grid_windows.append(self.create_window(25 + ((i + 0.5) * cell_width), 25 + ((j + 0.5) * cell_width)))
                self.itemconfigure(grid_windows[i + (j * grid_size)], window=self.cell_texts[i + (j * grid_size)])


class KillerSudokuGrid(tk.Canvas):
    """The grid of a killer sudoku puzzle.

    Attributes:
        cell_texts (list[tk.Text]): Text boxes where one goes in each cell in the grid, where number will be entered.
        display_answer (list[bool]): Marks whether a cell's answer will be displayed or not.
    """

    def __init__(self, container: App) -> None:
        """ Initiates KillerSudokuGrid. """

        super().__init__(container)

        self.cell_texts = []
        self.display_answer = []

        self["width"] = 500
        self["height"] = 500

        # Colouring cell backgrounds
        cell_colours = generate_ks_colours(container.ks_cages)
        for i in range(81):
            cell_row, cell_column = i_to_rc(i, 9)
            row_1 = 25 + (cell_row * 50)
            row_2 = 75 + (cell_row * 50)
            col_1 = 25 + (cell_column * 50)
            col_2 = 75 + (cell_column * 50)
            self.create_polygon(col_1, row_1, col_1, row_2, col_2, row_2, col_2, row_1, fill=cell_colours[i])

        # Grid outline
        c1 = 25
        c2 = 475
        self.create_polygon(c1, c1, c1, c2, c2, c2, c2, c1, width=10, fill="", outline="black")

        # Grid bold lines
        bold_lines = []
        for i in range(175, 326, 150):
            bold_lines.append(self.create_line(i, c1, i, c2, width=8))
            bold_lines.append(self.create_line(c1, i, c2, i, width=8))

        # DGrid light lines
        light_lines = []
        for i in range(75, 426, 50):
            light_lines.append(self.create_line(i, c1, i, c2, width=4))
            light_lines.append(self.create_line(c1, i, c2, i, width=4))

        # cell_texts text boxes
        for i in range(81):
            self.cell_texts.append(tk.Text(self, height=1, width=1, font=("Arial", 19), relief="flat",
                                           background=cell_colours[i]))
            self.display_answer.append(False)

        # Killer sudoku totals text boxes
        ks_totals_labels = []
        ks_totals_windows = []
        for i in range(len(container.ks_cages)):
            top_left_cell = min(container.ks_cages[i])
            tl_cell_row = i_to_rc(top_left_cell, 9)[0]
            tl_cell_col = i_to_rc(top_left_cell, 9)[1]
            ks_totals_labels.append(tk.Label(self, height=1, font=("Arial", 8), bd=0, text=container.ks_totals[i],
                                             bg=cell_colours[top_left_cell]))
            ks_totals_windows.append(self.create_window(38 + (tl_cell_col * 50), 38 + (tl_cell_row * 50)))
            self.itemconfigure(ks_totals_windows[i], window=ks_totals_labels[i])

        # Containers to hold text boxes
        grid_windows = []
        for j in range(9):
            for i in range(9):
                grid_windows.append(self.create_window(25 + ((i + 0.5) * 50), 25 + ((j + 0.5) * 50)))
                self.itemconfigure(grid_windows[i + (j * 9)], window=self.cell_texts[i + (j * 9)])


class HyperSudokuGrid(tk.Canvas):
    """ The grid of a hyper sudoku puzzle.

    Attributes:
        cell_texts (list[tk.Text]): Text boxes where one goes in each cell in the grid, where numbers will be entered.
        display_answer (list[bool]): Marks whether a cell's answer will be displayed or not.
    """

    def __init__(self, container: App) -> None:
        """ Initiates HyperSudokuGrid. """

        super().__init__(container)

        self.cell_texts = []
        self.display_answer = []

        self["width"] = 500
        self["height"] = 500

        # Grid Outline
        c1 = 25
        c2 = 475
        self.create_polygon(c1, c1, c1, c2, c2, c2, c2, c1, width=10, fill="white", outline="black")

        # Extra 3x3 boxes for hyper sudoku
        self.create_polygon(75, 75, 75, 225, 225, 225, 225, 75, fill="light blue")  # Top left
        self.create_polygon(75, 275, 75, 425, 225, 425, 225, 275, fill="light blue")  # Bottom left
        self.create_polygon(275, 75, 425, 75, 425, 225, 275, 225, fill="light blue")  # Top right
        self.create_polygon(275, 275, 275, 425, 425, 425, 425, 275, fill="light blue")  # Bottom right

        # Bold grid lines
        bold_lines = []
        for i in range(175, 326, 150):
            bold_lines.append(self.create_line(i, c1, i, c2, width=8))
            bold_lines.append(self.create_line(c1, i, c2, i, width=8))

        # Light grid lines
        light_lines = []
        for i in range(75, 426, 50):
            light_lines.append(self.create_line(i, c1, i, c2, width=4))
            light_lines.append(self.create_line(c1, i, c2, i, width=4))

        # cell_text text boxes
        for i in range(81):
            self.cell_texts.append(tk.Text(self, height=1, width=1, font=("Arial", 19), relief="flat"))
            self.display_answer.append(False)

        # Change text box background colours for hyper sudoku
        for i in range(10, 35, 9):
            for j in range(0, 37, 36):
                self.cell_texts[i + j]["background"] = "light blue"
                self.cell_texts[i + j + 1]["background"] = "light blue"
                self.cell_texts[i + j + 2]["background"] = "light blue"
                self.cell_texts[i + j + 4]["background"] = "light blue"
                self.cell_texts[i + j + 5]["background"] = "light blue"
                self.cell_texts[i + j + 6]["background"] = "light blue"

        # Containers to hold text boxes
        grid_windows = []
        for j in range(9):
            for i in range(9):
                grid_windows.append(self.create_window(25 + ((i + 0.5) * 50), 25 + ((j + 0.5) * 50)))
                self.itemconfigure(grid_windows[i + (j * 9)], window=self.cell_texts[i + (j * 9)])


class GreaterThanSudokuGrid(tk.Canvas):
    """ The grid of a greater than sudoku puzzle.

    Attributes:
        cell_texts (list[tk.Text]): Text boxes where one goes in each cell in the grid, where number will be entered.
        display_answer (list[bool]): Marks whether a cell's answer will be displayed or not.
        horizontal_buttons (list[tk.Button]): Buttons that are on a vertical edge between two cells, i.e. they have one
            cell to the left and another to the right. Used to swap the inequality symbol between > and <.
        horizontal_greater (list[str]): Each string is either "left" or "right", depending on which cell's value is
            greater. horizontal_greater[i] corresponds to the button at horizontal_buttons[i].
        vertical_buttons (list[tk.Button]): Buttons that are on a horizontal edge between two cells, i.e. they have one
            cell above and another below. Used to swap the inequality symbol between v and ^.
        vertical_greater (list[str]): Each string is either "up" or "down", depending on which cell's value is greater.
            vertical_greater[i] corresponds to the button at vertical_buttons[i].

    Methods:
        horizontal_button_clicked: Changes the direction of the inequality symbol.
        vertical_button_clicked: Changes the direction of the inequality symbol.
    """

    def __init__(self, container: App) -> None:
        """ Initiates GreaterThanSudokuGrid. """

        super().__init__(container)

        self.horizontal_buttons = []
        self.vertical_buttons = []
        self.horizontal_greater = []
        self.vertical_greater = []
        self.cell_texts = []
        self.display_answer = []

        # Initiate horizontal_greater and vertical_greater
        for i in range(54):
            self.horizontal_greater.append("left")
            self.vertical_greater.append("up")

        self["width"] = 500
        self["height"] = 500

        # Grid outline
        c1 = 25
        c2 = 475
        self.create_polygon(c1, c1, c1, c2, c2, c2, c2, c1, width=10, fill="white", outline="black")

        # Bold grid lines
        bold_lines = []
        for i in range(175, 326, 150):
            bold_lines.append(self.create_line(i, c1, i, c2, width=8))
            bold_lines.append(self.create_line(c1, i, c2, i, width=8))

        # Light grid lines
        light_lines = []
        for i in range(75, 426, 50):
            light_lines.append(self.create_line(i, c1, i, c2, width=4))
            light_lines.append(self.create_line(c1, i, c2, i, width=4))

        # cell_texts text boxes
        for i in range(81):
            self.cell_texts.append(tk.Text(self, height=1, width=1, font=("Arial", 19), relief="flat"))
            self.display_answer.append(False)

        # Add containers to hold text boxes
        grid_windows = []
        for j in range(9):
            for i in range(9):
                grid_windows.append(self.create_window(25 + ((i + 0.5) * 50), 25 + ((j + 0.5) * 50)))
                self.itemconfigure(grid_windows[i + (j * 9)], window=self.cell_texts[i + (j * 9)])

        # Horizontal buttons: > or <, vertical buttons: ^ or v
        for i in range(54):
            self.horizontal_buttons.append(tk.Button(self, width=1, height=1, bg="yellow",
                                                     command=lambda x=i: self.horizontal_button_clicked(x)))
            self.vertical_buttons.append(tk.Button(self, width=1, height=1, bg="yellow",
                                                   command=lambda x=i: self.vertical_button_clicked(x)))
        horizontal_button_windows = []
        vertical_button_windows = []
        for i in range(9):
            horizontal_button_windows.append(self.create_window(75, 25 + ((i + 0.5) * 50)))
            horizontal_button_windows.append(self.create_window(125, 25 + ((i + 0.5) * 50)))
            horizontal_button_windows.append(self.create_window(225, 25 + ((i + 0.5) * 50)))
            horizontal_button_windows.append(self.create_window(275, 25 + ((i + 0.5) * 50)))
            horizontal_button_windows.append(self.create_window(375, 25 + ((i + 0.5) * 50)))
            horizontal_button_windows.append(self.create_window(425, 25 + ((i + 0.5) * 50)))
        for i in range(2):
            for j in range(9):
                vertical_button_windows.append(self.create_window((j + 1) * 50, 75 + (50 * i)))
        for i in range(2):
            for j in range(9):
                vertical_button_windows.append(self.create_window((j + 1) * 50, 225 + (50 * i)))
        for i in range(2):
            for j in range(9):
                vertical_button_windows.append(self.create_window((j + 1) * 50, 375 + (50 * i)))
        for i in range(54):
            self.itemconfigure(horizontal_button_windows[i], window=self.horizontal_buttons[i])
            self.itemconfigure(vertical_button_windows[i], window=self.vertical_buttons[i])

    def horizontal_button_clicked(self, i: int) -> None:
        """ Changes the direction of the inequality symbol.

        Changes the text on a horizontal_buttons button from > to < (and vice versa) and horizontal_greater string
        from "left" to "right" (and vice versa).

        Args:
            i (int): Index of the button, has a value from 0 to 53 (inclusive).
        """

        if self.horizontal_buttons[i]["text"] == "":  # The button has never been clicked
            self.horizontal_buttons[i]["text"] = ">"
            self.horizontal_buttons[i]["bg"] = "white"
        elif self.horizontal_buttons[i]["text"] == ">":
            self.horizontal_buttons[i]["text"] = "<"
            self.horizontal_greater[i] = "right"
        elif self.horizontal_buttons[i]["text"] == "<":
            self.horizontal_buttons[i]["text"] = ">"
            self.horizontal_greater[i] = "left"

    def vertical_button_clicked(self, i: int) -> None:
        """ Changes the direction of the inequality symbol.

        Changes the text on a vertical_buttons button from ^ to v (and vice versa) and vertical_greater string from
        "down" to "up" (and vice versa).

        Args:
            i (int): Index of the button, has value from 0 to 53 (inclusive).
        """

        if self.vertical_buttons[i]["text"] == "":  # The button has never been clicked
            self.vertical_buttons[i]["text"] = "v"
            self.vertical_buttons[i]["bg"] = "white"
        elif self.vertical_buttons[i]["text"] == "v":
            self.vertical_buttons[i]["text"] = "^"
            self.vertical_greater[i] = "down"
        elif self.vertical_buttons[i]["text"] == "^":
            self.vertical_buttons[i]["text"] = "v"
            self.vertical_greater[i] = "up"
