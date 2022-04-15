import tkinter as tk
import math
import ks_cages_setup
import misc_funcs


class SudokuGrid(tk.Canvas):
    def __init__(self, container, grid_size, cell_texts, display_answer):
        super().__init__(container)
        if grid_size == 25:
            cell_width = 36
        else:
            cell_width = 50
        self["width"] = (grid_size * cell_width) + 50
        self["height"] = (grid_size * cell_width) + 50
        # Drawing the outline of the grid
        c1 = 25
        c2 = (grid_size * cell_width) + 25
        self.create_polygon(c1, c1, c1, c2, c2, c2, c2, c1, width=10, fill="white", outline="black")
        # Drawing the bold lines of the grid
        bold_lines = []
        if grid_size == 6:
            bold_lines.append(self.create_line(175, 25, 175, 325, width=8))
            bold_lines.append(self.create_line(25, 125, 325, 125, width=8))
            bold_lines.append(self.create_line(25, 225, 325, 225, width=8))
        else:
            bold_start = int(25 + (cell_width * math.sqrt(grid_size)))
            bold_stop = int(26 + (cell_width * (grid_size - math.sqrt(grid_size))))
            bold_step = int(cell_width * math.sqrt(grid_size))
            for i in range(bold_start, bold_stop, bold_step):
                bold_lines.append(self.create_line(i, c1, i, c2, width=8))
                bold_lines.append(self.create_line(c1, i, c2, i, width=8))
        # Drawing the light lines of the grid
        light_lines = []
        light_start = 25 + cell_width
        light_stop = 26 + (cell_width * (grid_size - 1))
        light_step = cell_width
        for i in range(light_start, light_stop, light_step):
            light_lines.append(self.create_line(i, c1, i, c2, width=4))
            light_lines.append(self.create_line(c1, i, c2, i, width=4))
        # Create cell_texts text boxes, which hold the user inputted values
        if grid_size == 25:
            for i in range(625):
                cell_texts.append(tk.Text(self, height=1, width=2, font=("Arial", 12), relief="flat"))
                display_answer.append(False)
        if grid_size == 16:
            for i in range(256):
                cell_texts.append(tk.Text(self, height=1, width=2, font=("Arial", 19), relief="flat"))
                display_answer.append(False)
        else:
            for i in range(grid_size ** 2):
                cell_texts.append(tk.Text(self, height=1, width=1, font=("Arial", 19), relief="flat"))
                display_answer.append(False)
        # Add containers to hold text boxes
        grid_windows = []
        for j in range(grid_size):
            for i in range(grid_size):
                grid_windows.append(self.create_window(25 + ((i + 0.5) * cell_width), 25 + ((j + 0.5) * cell_width)))
                self.itemconfigure(grid_windows[i + (j * grid_size)], window=cell_texts[i + (j * grid_size)])


class KillerSudokuGrid(tk.Canvas):
    def __init__(self, container, cell_texts, display_answer):
        super().__init__(container)
        self["width"] = 500
        self["height"] = 500
        # Colouring cell backgrounds for different killer sudoku cages
        cell_colours = ks_cages_setup.generate_ks_colours(container.ks_cages)
        for i in range(81):
            cell_row, cell_column = misc_funcs.i_to_rc(i, 9)
            row_1 = 25 + (cell_row * 50)
            row_2 = 75 + (cell_row * 50)
            col_1 = 25 + (cell_column * 50)
            col_2 = 75 + (cell_column * 50)
            self.create_polygon(col_1, row_1, col_1, row_2, col_2, row_2, col_2, row_1, fill=cell_colours[i])
        # Drawing the outline of the grid
        c1 = 25
        c2 = 475
        self.create_polygon(c1, c1, c1, c2, c2, c2, c2, c1, width=10, fill="", outline="black")
        # Drawing the bold lines of the grid
        bold_lines = []
        for i in range(175, 326, 150):
            bold_lines.append(self.create_line(i, c1, i, c2, width=8))
            bold_lines.append(self.create_line(c1, i, c2, i, width=8))
        # Drawing the light lines of the grid
        light_lines = []
        for i in range(75, 426, 50):
            light_lines.append(self.create_line(i, c1, i, c2, width=4))
            light_lines.append(self.create_line(c1, i, c2, i, width=4))
        # Create cell_texts text boxes, which hold the user inputted values
        for i in range(81):
            cell_texts.append(tk.Text(self, height=1, width=1, font=("Arial", 19), relief="flat",
                                      background=cell_colours[i]))
            display_answer.append(False)
        # Add killer sudoku totals text boxes
        ks_totals_labels = []
        ks_totals_windows = []
        for i in range(len(container.ks_cages)):
            top_left_cell = min(container.ks_cages[i])
            tl_cell_row = misc_funcs.i_to_rc(top_left_cell, 9)[0]
            tl_cell_col = misc_funcs.i_to_rc(top_left_cell, 9)[1]
            ks_totals_labels.append(tk.Label(self, height=1, font=("Arial", 8), bd=0, text=container.ks_totals[i],
                                             bg=cell_colours[top_left_cell]))
            ks_totals_windows.append(self.create_window(38 + (tl_cell_col * 50), 38 + (tl_cell_row * 50)))
            self.itemconfigure(ks_totals_windows[i], window=ks_totals_labels[i])
        # Add containers to hold text boxes
        grid_windows = []
        for j in range(9):
            for i in range(9):
                grid_windows.append(self.create_window(25 + ((i + 0.5) * 50), 25 + ((j + 0.5) * 50)))
                self.itemconfigure(grid_windows[i + (j * 9)], window=cell_texts[i + (j * 9)])


class HyperSudokuGrid(tk.Canvas):
    def __init__(self, container, cell_texts, display_answer):
        super().__init__(container)
        self["width"] = 500
        self["height"] = 500
        # Drawing the outline of the grid
        c1 = 25
        c2 = 475
        self.create_polygon(c1, c1, c1, c2, c2, c2, c2, c1, width=10, fill="white", outline="black")
        # Drawing extra 3x3 boxes for hyper sudoku
        self.create_polygon(75, 75, 75, 225, 225, 225, 225, 75, fill="light blue")  # Top left
        self.create_polygon(75, 275, 75, 425, 225, 425, 225, 275, fill="light blue")  # Bottom left
        self.create_polygon(275, 75, 425, 75, 425, 225, 275, 225, fill="light blue")  # Top right
        self.create_polygon(275, 275, 275, 425, 425, 425, 425, 275, fill="light blue")  # Bottom right
        # Drawing the bold lines of the grid
        bold_lines = []
        for i in range(175, 326, 150):
            bold_lines.append(self.create_line(i, c1, i, c2, width=8))
            bold_lines.append(self.create_line(c1, i, c2, i, width=8))
        # Drawing the light lines of the grid
        light_lines = []
        for i in range(75, 426, 50):
            light_lines.append(self.create_line(i, c1, i, c2, width=4))
            light_lines.append(self.create_line(c1, i, c2, i, width=4))
        # Create cell_texts text boxes, which hold the user inputted values
        for i in range(81):
            cell_texts.append(tk.Text(self, height=1, width=1, font=("Arial", 19), relief="flat"))
            display_answer.append(False)
        # Changing text box background colours for hyper sudoku
        for i in range(10, 35, 9):
            for j in range(0, 37, 36):
                cell_texts[i + j]["background"] = "light blue"
                cell_texts[i + j + 1]["background"] = "light blue"
                cell_texts[i + j + 2]["background"] = "light blue"
                cell_texts[i + j + 4]["background"] = "light blue"
                cell_texts[i + j + 5]["background"] = "light blue"
                cell_texts[i + j + 6]["background"] = "light blue"
        # Add containers to hold text boxes
        grid_windows = []
        for j in range(9):
            for i in range(9):
                grid_windows.append(self.create_window(25 + ((i + 0.5) * 50), 25 + ((j + 0.5) * 50)))
                self.itemconfigure(grid_windows[i + (j * 9)], window=cell_texts[i + (j * 9)])


class GreaterThanSudokuGrid(tk.Canvas):
    def __init__(self, container, cell_texts, display_answer, horizontal_buttons, vertical_buttons, horizontal_greater,
                 vertical_greater):
        super().__init__(container)

        self.horizontal_buttons = horizontal_buttons
        self.vertical_buttons = vertical_buttons
        self.horizontal_greater = horizontal_greater
        self.vertical_greater = vertical_greater

        for i in range(54):
            self.horizontal_greater.append("left")
            self.vertical_greater.append("up")

        self["width"] = 500
        self["height"] = 500
        # Drawing the outline of the grid
        c1 = 25
        c2 = 475
        self.create_polygon(c1, c1, c1, c2, c2, c2, c2, c1, width=10, fill="white", outline="black")
        # Drawing the bold lines of the grid
        bold_lines = []
        for i in range(175, 326, 150):
            bold_lines.append(self.create_line(i, c1, i, c2, width=8))
            bold_lines.append(self.create_line(c1, i, c2, i, width=8))
        # Drawing the light lines of the grid
        light_lines = []
        for i in range(75, 426, 50):
            light_lines.append(self.create_line(i, c1, i, c2, width=4))
            light_lines.append(self.create_line(c1, i, c2, i, width=4))
        # Create cell_texts text boxes, which hold user inputted values
        for i in range(81):
            cell_texts.append(tk.Text(self, height=1, width=1, font=("Arial", 19), relief="flat"))
            display_answer.append(False)
        # Add containers to hold text boxes
        grid_windows = []
        for j in range(9):
            for i in range(9):
                grid_windows.append(self.create_window(25 + ((i + 0.5) * 50), 25 + ((j + 0.5) * 50)))
                self.itemconfigure(grid_windows[i + (j * 9)], window=cell_texts[i + (j * 9)])
        # Create buttons to change greater than orientation
        # Horizontal buttons: > or <, vertical buttons: ^ or v
        for i in range(54):
            self.horizontal_buttons.append(tk.Button(self, width=2, height=1, bg="yellow",
                                                     command=lambda x=i: self.horizontal_button_clicked(x)))
            self.vertical_buttons.append(tk.Button(self, width=2, height=1, bg="yellow",
                                                   command=lambda x=i: self.vertical_button_clicked(x)))
        # Add containers to hold buttons
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

    def horizontal_button_clicked(self, i):
        # Horizontal (< or >) greater than sudoku button clicked
        if self.horizontal_buttons[i]["text"] == "":
            # The button has never been clicked
            self.horizontal_buttons[i]["text"] = ">"
            self.horizontal_buttons[i]["bg"] = "white"
        elif self.horizontal_buttons[i]["text"] == ">":
            self.horizontal_buttons[i]["text"] = "<"
            self.horizontal_greater[i] = "right"
        elif self.horizontal_buttons[i]["text"] == "<":
            self.horizontal_buttons[i]["text"] = ">"
            self.horizontal_greater[i] = "left"

    def vertical_button_clicked(self, i):
        # Vertical ( ∧ or v) greater than sudoku button clicked
        if self.vertical_buttons[i]["text"] == "":
            # The button has never been clicked
            self.vertical_buttons[i]["text"] = "v"
            self.vertical_buttons[i]["bg"] = "white"
        elif self.vertical_buttons[i]["text"] == "v":
            self.vertical_buttons[i]["text"] = "^"
            self.vertical_greater[i] = "down"
        elif self.vertical_buttons[i]["text"] == "^":
            self.vertical_buttons[i]["text"] = "v"
            self.vertical_greater[i] = "up"
