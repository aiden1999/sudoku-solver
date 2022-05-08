from __future__ import annotations
from math import sqrt
from typing import TYPE_CHECKING
from misc_funcs import i_to_rc
if TYPE_CHECKING:
    from initial_setup import App
    from solve import SatSolver


def define_clauses(puzzle: list[list[str]], sat_solver: SatSolver, root: App) -> None:

    sudoku_type = root.puzzle_config.puzzle_type.get()
    grid_dim = root.puzzle_config.grid_dim

    if sudoku_type == "sudoku":
        define_standard_clauses(puzzle, sat_solver, grid_dim)
    if sudoku_type == "killer_sudoku":
        define_killer_sudoku_clauses(puzzle, sat_solver, root)
    if sudoku_type == "hyper_sudoku":
        define_hyper_sudoku_clauses(puzzle, sat_solver)
    if sudoku_type == "greater_than_sudoku":
        define_gt_sudoku_clauses(puzzle, sat_solver, root)


def define_standard_clauses(puzzle: list[list[str]], sat_solver: SatSolver, grid_dim: int) -> None:
    # Creates clauses for standard Sudoku rules

    # Clauses for known values in the puzzle
    for r in range(grid_dim):
        for c in range(grid_dim):
            if int(puzzle[r][c]) != 0:
                sat_solver.add_clause([ncr_to_var(int(puzzle[r][c]), c, r, grid_dim)])
    # Each cell gets at least one number
    for r in range(grid_dim):
        for c in range(grid_dim):
            clause_temp = []
            for n in range(1, grid_dim + 1):
                clause_temp.append(ncr_to_var(n, c, r, grid_dim))
            sat_solver.add_clause(clause_temp)
    # Every number occurs at most once per row
    for r in range(grid_dim):
        for n in range(1, grid_dim + 1):
            for c in range(grid_dim - 1):
                for c_prime in range(c + 1, grid_dim):
                    sat_solver.add_clause(two_neg_clauses(n, c, r, n, c_prime, r, grid_dim))
    # Every number occurs at most one per column
    for c in range(grid_dim):
        for n in range(1, grid_dim + 1):
            for r in range(grid_dim - 1):
                for r_prime in range(r + 1, grid_dim):
                    sat_solver.add_clause(two_neg_clauses(n, c, r, n, c, r_prime, grid_dim))
    # Every number occurs at most once per block
    if grid_dim == 6:
        for r in range(0, grid_dim, 2):
            for c in range(0, grid_dim, 3):
                blocks_rule(sat_solver, c, r, grid_dim)
    else:
        sr_dim = int(sqrt(grid_dim))
        for r in range(0, grid_dim, sr_dim):
            for c in range(0, grid_dim, sr_dim):
                blocks_rule(sat_solver, c, r, grid_dim)


def blocks_rule(sat_solver: SatSolver, start_col: int, start_row: int, grid_dim: int) -> None:
    # Creates clauses to check that every number occurs at most once per block, for a specific block
    if grid_dim == 6:
        for n in range(1, 7):
            for r in range(start_row, start_row + 2):
                for c in range(start_col, start_col + 3):
                    for r_prime in range(start_row, start_row + 2):
                        for c_prime in range(start_col, start_col + 3):
                            if col_row_mod(c, r, grid_dim) < col_row_mod(c_prime, r_prime, grid_dim):
                                sat_solver.add_clause(two_neg_clauses(n, c, r, n, c_prime, r_prime, grid_dim))
    else:
        sr_dim = int(sqrt(grid_dim))
        for n in range(1, grid_dim + 1):
            for r in range(start_row, start_row + sr_dim):
                for c in range(start_col, start_col + sr_dim):
                    for r_prime in range(start_row, start_row + sr_dim):
                        for c_prime in range(start_col, start_col + sr_dim):
                            if col_row_mod(c, r, grid_dim) < col_row_mod(c_prime, r_prime, grid_dim):
                                sat_solver.add_clause(two_neg_clauses(n, c, r, n, c_prime, r_prime, grid_dim))


def two_neg_clauses(n1: int, c1: int, r1: int, n2: int, c2: int, r2: int, grid_dim: int) -> list[int]:
    # Returns two negation clauses, to be added to the DIMACS file
    return [- ncr_to_var(n1, c1, r1, grid_dim), - ncr_to_var(n2, c2, r2, grid_dim)]


def ncr_to_var(number: int, column: int, row: int, grid_dim: int) -> int:
    # Converts a combination of a number, a column and a row to a unique identifier
    return int(number + (grid_dim * column) + ((grid_dim ** 2) * row))


def col_row_mod(column: int, row: int, grid_dim: int) -> int:
    # Numbers a cell within a block, based on column and row. E.g. for a 3x3 block, would return
    # 0 | 1 | 2
    # 3 | 4 | 5
    # 6 | 7 | 8
    # not matter what block it is.
    if grid_dim == 6:
        return (column % 3) + 3 * (row % 2)
    else:
        sr_dim = int(sqrt(grid_dim))
        return (column % sr_dim) + sr_dim * (row % sr_dim)


def define_killer_sudoku_clauses(puzzle: list[list[str]], sat_solver: SatSolver, root: App) -> None:

    cages = root.ks_cages
    totals = root.ks_totals

    x_var = 730
    # Killer sudoku summation rules
    all_permutations = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(len(totals)):
        total = totals[i]
        number_of_cells = len(cages[i])
        # Generate all the permutations of length number_of_cells
        if all_permutations[number_of_cells - 1] == 0:
            ps = []
            for n1 in range(1, 10):
                if number_of_cells == 1:
                    ps.append([n1])
                else:
                    for n2 in range(1, 10):
                        if number_of_cells == 2:
                            ps.append([n1, n2])
                        else:
                            for n3 in range(1, 10):
                                if number_of_cells == 3:
                                    ps.append([n1, n2, n3])
                                else:
                                    for n4 in range(1, 10):
                                        if number_of_cells == 4:
                                            ps.append([n1, n2, n3, n4])
                                        else:
                                            for n5 in range(1, 10):
                                                if number_of_cells == 5:
                                                    ps.append([n1, n2, n3, n4, n5])
                                                else:
                                                    for n6 in range(1, 10):
                                                        if number_of_cells == 6:
                                                            ps.append([n1, n2, n3, n4, n5, n6])
                                                        else:
                                                            for n7 in range(1, 10):
                                                                if number_of_cells == 7:
                                                                    ps.append([n1, n2, n3, n4, n5, n6, n7])
                                                                else:
                                                                    for n8 in range(1, 10):
                                                                        if number_of_cells == 8:
                                                                            ps.append([n1, n2, n3, n4, n5, n6, n7, n8])
                                                                        else:
                                                                            for n9 in range(1, 10):
                                                                                ps.append([n1, n2, n3, n4, n5, n6, n7,
                                                                                           n8, n9])
            # Remove permutations with duplicate values
            permutations_no_copies = []
            for permutation in ps:
                temp_list = []
                for num in permutation:
                    if num not in temp_list:
                        temp_list.append(num)
                if len(temp_list) == number_of_cells:
                    permutations_no_copies.append(temp_list)
            all_permutations[number_of_cells - 1] = permutations_no_copies
        # Remove permutations that don't sum to the correct value
        correct_permutations = []
        for permutation in all_permutations[number_of_cells - 1]:
            permutation_sum = 0
            for num in permutation:
                permutation_sum = permutation_sum + num
            if permutation_sum == total:
                correct_permutations.append(permutation)
        # Encode number, column, row to unique variable
        encoded_permutations = []
        for permutation in correct_permutations:
            encoded_permutation = []
            for j in range(number_of_cells):
                current_cell = cages[i][j]
                current_row, current_column = i_to_rc(current_cell, 9)
                current_number = permutation[j]
                encoded_permutation.append(ncr_to_var(current_number, current_column, current_row, 9))
            encoded_permutations.append(encoded_permutation)
        # Convert DNF to CNF and add CNF clauses
        x_var = dnf_to_cnf(encoded_permutations, x_var, sat_solver)
    # Standard sudoku rules (including numbers already in puzzle)
    define_standard_clauses(puzzle, sat_solver, 9)


def define_hyper_sudoku_clauses(puzzle: list[list[str]], sat_solver: SatSolver) -> None:
    blocks_rule(sat_solver, 1, 1, 9)  # Top left
    blocks_rule(sat_solver, 1, 5, 9)  # Bottom left
    blocks_rule(sat_solver, 5, 1, 9)  # Top right
    blocks_rule(sat_solver, 5, 5, 9)  # Bottom right
    define_standard_clauses(puzzle, sat_solver, 9)


def define_gt_sudoku_clauses(puzzle: list[list[str]], sat_solver: SatSolver, root: App) -> None:

    horizontal_greater = root.puzzle_grid.horizontal_greater
    vertical_greater = root.puzzle_grid.vertical_greater

    for i in range(81):
        greater_than_count = 0
        if i in [0, 3, 6, 27, 30, 33, 54, 57, 60]:  # Top left corner
            edges_count = 2
            right_i = int(i * (2 / 3))
            down_i = int(right_i + ((i % 9) / 3))
            if horizontal_greater[right_i] == "left":
                greater_than_count = greater_than_count + 1
            if vertical_greater[down_i] == "up":
                greater_than_count = greater_than_count + 1
        elif i in [2, 5, 8, 29, 32, 35, 56, 59, 62]:  # Top right corner
            edges_count = 2
            left_i = int(((2 * i) - 1) / 3)
            down_i = int(left_i + (((i % 9) + 1) / 3))
            if horizontal_greater[left_i] == "right":
                greater_than_count = greater_than_count + 1
            if vertical_greater[down_i] == "up":
                greater_than_count = greater_than_count + 1
        elif i in [18, 21, 24, 45, 48, 51, 72, 75, 78]:  # Bottom left corner
            edges_count = 2
            right_i = int(i * (2 / 3))
            up_i = int(right_i - (3 - ((i % 9) / 3)))
            if horizontal_greater[right_i] == "left":
                greater_than_count = greater_than_count + 1
            if vertical_greater[up_i] == "down":
                greater_than_count = greater_than_count + 1
        elif i in [20, 23, 26, 47, 50, 53, 74, 77, 80]:  # Bottom right corner
            edges_count = 2
            left_i = int(((2 * i) - 1) / 3)
            up_i = int(left_i - (3 - (((i % 9) + 1) / 3)))
            if horizontal_greater[left_i] == "right":
                greater_than_count = greater_than_count + 1
            if vertical_greater[up_i] == "down":
                greater_than_count = greater_than_count + 1
        elif i in [1, 4, 7, 28, 31, 34, 55, 58, 61]:  # Top side
            edges_count = 3
            left_i = int((i - 1) * (2 / 3))
            right_i = left_i + 1
            down_i = int(right_i + (((i % 9) - 1) / 3))
            if horizontal_greater[left_i] == "right":
                greater_than_count = greater_than_count + 1
            if horizontal_greater[right_i] == "left":
                greater_than_count = greater_than_count + 1
            if vertical_greater[down_i] == "up":
                greater_than_count = greater_than_count + 1
        elif i in [9, 12, 15, 36, 39, 42, 63, 66, 69]:  # Left side
            edges_count = 3
            up_i = int((i % 9) + (18 * (i // 30)))
            right_i = int(i * (2 / 3))
            down_i = up_i + 9
            if vertical_greater[up_i] == "down":
                greater_than_count = greater_than_count + 1
            if horizontal_greater[right_i] == "left":
                greater_than_count = greater_than_count + 1
            if vertical_greater[down_i] == "up":
                greater_than_count = greater_than_count + 1
        elif i in [11, 14, 17, 38, 41, 44, 65, 68, 71]:  # Right side
            edges_count = 3
            up_i = int((i % 9) + (18 * (i // 30)))
            left_i = int(((i + 1) * (2 / 3)) - 1)
            down_i = up_i + 9
            if vertical_greater[up_i] == "down":
                greater_than_count = greater_than_count + 1
            if horizontal_greater[left_i] == "right":
                greater_than_count = greater_than_count + 1
            if vertical_greater[down_i] == "up":
                greater_than_count = greater_than_count + 1
        elif i in [19, 22, 25, 46, 49, 52, 73, 76, 79]:  # Bottom side
            edges_count = 3
            up_i = i - (((i // 30) + 1) * 9)
            left_i = int((i - 1) * (2 / 3))
            right_i = left_i + 1
            if vertical_greater[up_i] == "down":
                greater_than_count = greater_than_count + 1
            if horizontal_greater[left_i] == "right":
                greater_than_count = greater_than_count + 1
            if horizontal_greater[right_i] == "left":
                greater_than_count = greater_than_count + 1
        else:  # Centre cell
            edges_count = 4
            up_i = i - (((i // 30) + 1) * 9)
            left_i = int((i - 1) * (2 / 3))
            right_i = left_i + 1
            down_i = up_i + 9
            if vertical_greater[up_i] == "down":
                greater_than_count = greater_than_count + 1
            if horizontal_greater[left_i] == "right":
                greater_than_count = greater_than_count + 1
            if horizontal_greater[right_i] == "left":
                greater_than_count = greater_than_count + 1
            if vertical_greater[down_i] == "up":
                greater_than_count = greater_than_count + 1
        i_row, i_col = i_to_rc(i, 9)
        en = [0]  # Encoded numbers
        for j in range(1, 10):
            en.append(ncr_to_var(j, i_col, i_row, 9))
        if edges_count == 2:
            if greater_than_count == 2:
                sat_solver.add_clause([en[9], en[8], en[7], en[6], en[5], en[4], en[3]])
            elif greater_than_count == 1:
                sat_solver.add_clause([en[8], en[7], en[6], en[5], en[4], en[3], en[2]])
            else:
                sat_solver.add_clause([en[7], en[6], en[5], en[4], en[3], en[2], en[1]])
        elif edges_count == 3:
            if greater_than_count == 3:
                sat_solver.add_clause([en[9], en[8], en[7], en[6], en[5], en[4]])
            elif greater_than_count == 2:
                sat_solver.add_clause([en[8], en[7], en[6], en[5], en[4], en[3]])
            elif greater_than_count == 1:
                sat_solver.add_clause([en[7], en[6], en[5], en[4], en[3], en[2]])
            else:
                sat_solver.add_clause([en[6], en[5], en[4], en[3], en[2], en[1]])
        else:
            if greater_than_count == 4:
                sat_solver.add_clause([en[9], en[8], en[7], en[6], en[5]])
            elif greater_than_count == 3:
                sat_solver.add_clause([en[8], en[7], en[6], en[5], en[4]])
            elif greater_than_count == 2:
                sat_solver.add_clause([en[7], en[6], en[5], en[4], en[3]])
            elif greater_than_count == 1:
                sat_solver.add_clause([en[6], en[5], en[4], en[3], en[2]])
            else:
                sat_solver.add_clause([en[5], en[4], en[3], en[2], en[1]])
    x_var = 730
    for i in range(len(horizontal_greater)):
        left_cell = i + (i // 2)  # location of cell to the left of the inequality sign (0 to 79)
        right_cell = left_cell + 1  # location of cell to the right of the inequality sign (1 to 80)
        left_cell_encoded = [0]
        right_cell_encoded = [0]
        left_r, left_c = i_to_rc(left_cell, 9)
        right_r, right_c = i_to_rc(right_cell, 9)
        for j in range(1, 10):
            left_cell_encoded.append(ncr_to_var(j, left_c, left_r, 9))
            right_cell_encoded.append(ncr_to_var(j, right_c, right_r, 9))
        dnf_clause = []
        for left_num in range(1, 10):
            for right_num in range(1, 10):
                if (left_num > right_num) and (horizontal_greater[i] == "left"):
                    dnf_clause.append([left_cell_encoded[left_num], right_cell_encoded[right_num]])
                if (left_num < right_num) and (horizontal_greater[i] == "right"):
                    dnf_clause.append([left_cell_encoded[left_num], right_cell_encoded[right_num]])
        #  Convert DNF to CNF
        x_var = dnf_to_cnf(dnf_clause, x_var, sat_solver)
    for i in range(len(vertical_greater)):
        up_cell = i + (9 * (i // 18))
        down_cell = up_cell + 9
        up_cell_encoded = [0]
        down_cell_encoded = [0]
        up_r, up_c = i_to_rc(up_cell, 9)
        down_r, down_c = i_to_rc(down_cell, 9)
        for j in range(1, 10):
            up_cell_encoded.append(ncr_to_var(j, up_c, up_r, 9))
            down_cell_encoded.append(ncr_to_var(j, down_c, down_r, 9))
        dnf_clause = []
        for up_num in range(1, 10):
            for down_num in range(1, 10):
                if (up_num > down_num) and (vertical_greater[i] == "up"):
                    dnf_clause.append([up_cell_encoded[up_num], down_cell_encoded[down_num]])
                if (up_num < down_num) and (vertical_greater[i] == "down"):
                    dnf_clause.append([up_cell_encoded[up_num], down_cell_encoded[down_num]])
        # Convert DNF to CNF
        x_var = dnf_to_cnf(dnf_clause, x_var, sat_solver)
    # Standard sudoku rules (including numbers already in puzzle
    define_standard_clauses(puzzle, sat_solver, 9)


def dnf_to_cnf(dnf_clause: list[list[int]], x_var: int, sat_solver: SatSolver) -> int:
    x_var_new = x_var
    for sub_clause in dnf_clause:
        temp_clause = [x_var_new]
        for num in sub_clause:
            temp_clause.append(- num)
        sat_solver.add_clause(temp_clause)
        for num in sub_clause:
            temp_clause = [- x_var_new, num]
            sat_solver.add_clause(temp_clause)
        x_var_new = x_var_new + 1
    sat_solver.add_clause([x_var_new])
    total_sub_clauses = len(dnf_clause)
    all_x_var = [- x_var_new]
    for i in range(total_sub_clauses):
        old_x_var = x_var_new - (i + 1)
        sat_solver.add_clause([x_var_new, - old_x_var])
        all_x_var.append(old_x_var)
    sat_solver.add_clause(all_x_var)
    x_var_new = x_var_new + 1
    return x_var_new
