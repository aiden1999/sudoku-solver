import math
import misc_funcs


def define_clauses(puzzle, sat_solver, grid_dim, sudoku_type, cages, totals):
    if sudoku_type == "sudoku":
        define_standard_clauses(puzzle, sat_solver, grid_dim)
    if sudoku_type == "killer_sudoku":
        define_killer_sudoku_clauses(puzzle, sat_solver, cages, totals)
    if sudoku_type == "hyper_sudoku":
        define_hyper_sudoku_clauses(puzzle, sat_solver)


def define_standard_clauses(puzzle, sat_solver, grid_dim):
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
        sr_dim = int(math.sqrt(grid_dim))
        for r in range(0, grid_dim, sr_dim):
            for c in range(0, grid_dim, sr_dim):
                blocks_rule(sat_solver, c, r, grid_dim)


def blocks_rule(sat_solver, start_col, start_row, grid_dim):
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
        sr_dim = int(math.sqrt(grid_dim))
        for n in range(1, grid_dim + 1):
            for r in range(start_row, start_row + sr_dim):
                for c in range(start_col, start_col + sr_dim):
                    for r_prime in range(start_row, start_row + sr_dim):
                        for c_prime in range(start_col, start_col + sr_dim):
                            if col_row_mod(c, r, grid_dim) < col_row_mod(c_prime, r_prime, grid_dim):
                                sat_solver.add_clause(two_neg_clauses(n, c, r, n, c_prime, r_prime, grid_dim))


def two_neg_clauses(n1, c1, r1, n2, c2, r2, grid_dim):
    # Returns two negation clauses, to be added to the DIMACS file
    return [- ncr_to_var(n1, c1, r1, grid_dim), - ncr_to_var(n2, c2, r2, grid_dim)]


def ncr_to_var(number, column, row, grid_dim):
    # Converts a combination of a number, a column and a row to a unique identifier
    return number + (grid_dim * column) + ((grid_dim ** 2) * row)


def col_row_mod(column, row, grid_dim):
    # Numbers a cell within a block, based on column and row. E.g. for a 3x3 block, would return
    # 0 | 1 | 2
    # 3 | 4 | 5
    # 6 | 7 | 8
    # not matter what block it is.
    if grid_dim == 6:
        return (column % 3) + 3 * (row % 2)
    else:
        sr_dim = int(math.sqrt(grid_dim))
        return (column % sr_dim) + sr_dim * (row % sr_dim)


def define_killer_sudoku_clauses(puzzle, sat_solver, cages, totals):
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
                current_row = misc_funcs.i_to_rc(current_cell, 9)[0]
                current_column = misc_funcs.i_to_rc(current_cell, 9)[1]
                current_number = permutation[j]
                encoded_permutation.append(ncr_to_var(current_number, current_column, current_row, 9))
            encoded_permutations.append(encoded_permutation)
        # Convert DNF to CNF and add CNF clauses
        for permutation in encoded_permutations:
            temp_clause = [x_var]
            for num in permutation:
                temp_clause.append(- num)
            sat_solver.add_clause(temp_clause)  # X1 -A -B
            for num in permutation:
                temp_clause = [- x_var, num]
                sat_solver.add_clause(temp_clause)  # -X1 A
            x_var = x_var + 1
        sat_solver.add_clause([x_var])  # X(N + 1)
        total_permutations = len(encoded_permutations)
        all_x_var = [- x_var]
        for j in range(total_permutations):
            old_x_var = x_var - (j + 1)
            sat_solver.add_clause([x_var, - old_x_var])
            all_x_var.append(old_x_var)
        sat_solver.add_clause(all_x_var)
        x_var = x_var + 1
    # Standard sudoku rules (including numbers already in puzzle)
    define_standard_clauses(puzzle, sat_solver, 9)


def define_hyper_sudoku_clauses(puzzle, sat_solver):
    blocks_rule(sat_solver, 1, 1, 9)  # Top left
    blocks_rule(sat_solver, 1, 5, 9)  # Bottom left
    blocks_rule(sat_solver, 5, 1, 9)  # Top right
    blocks_rule(sat_solver, 5, 5, 9)  # Bottom right
    define_standard_clauses(puzzle, sat_solver, 9)
