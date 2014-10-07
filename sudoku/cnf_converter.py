from os.path import join
import itertools

from dimacs.dimacs import encode
from file_operations.file_operations import clean_directories, write_cnf, call_sat_solver, read_sat_output


def create_matrix(mypath, graph_name):
    """reads sudoku into a multidimensional array"""
    matrix = []
    with open(join(mypath, graph_name), 'r') as fh:
        for idx, line in enumerate(fh):
            row = []
            els = line.split(", ")
            for el_index, el in enumerate(els):
                num_val = int(el)
                row.append(num_val)
            matrix.append(row)
    return matrix


def map_to_dimacs(row, col, num, negation=False):
    mapping = "x" + str(row) + str(col) + str(num)
    mapping = 81 * row + 9 * col + num + 1
    return ("-" if negation else "") + str(mapping)


def convert_to_cnf(file_name):
    matrix = create_matrix("sudokus", file_name)
    size = len(matrix)
    lines = []
    matrix_range = range(size)

    #set the assigned variables
    for row in matrix_range:
        for col in matrix_range:
            for num in matrix_range:
                if matrix[row][col] == num + 1:
                    lines.append([map_to_dimacs(row, col, num)])

    #each cell has at least one number assigned
    for row in matrix_range:
        for col in matrix_range:
            line = []
            for num in matrix_range:
                line.append(map_to_dimacs(row, col, num))
            lines.append(line)

    #a row should contain at least every number
    for num in matrix_range:
        for row in matrix_range:
            line = []
            for col in matrix_range:
                line.append(map_to_dimacs(row, col, num))
            lines.append(line)

    # a row should contain at most every number
    for num in matrix_range:
        for row in matrix_range:
            for idx, col0 in enumerate(matrix_range):
                for col1 in matrix_range[idx+1:]:
                    line = [map_to_dimacs(row, col0, num, negation=True), map_to_dimacs(row, col1, num, negation=True)]
                    lines.append(line)

    #a col should contain at least every number
    for num in matrix_range:
        for col in matrix_range:
            line = []
            for row in matrix_range:
                line.append(map_to_dimacs(row, col, num))
            lines.append(line)

    #a col should contain at most every number
    for num in matrix_range:
        for col in matrix_range:
            for idx, row0 in enumerate(matrix_range):
                for row1 in matrix_range[idx+1:]:
                    line = [map_to_dimacs(row0, col, num, negation=True), map_to_dimacs(row1, col, num, negation=True)]
                    lines.append(line)

    num_blocks = 3
    block_size = size / num_blocks
    block_range = range(block_size)

    for outer_row in block_range:
        rows = [r + block_size * outer_row for r in block_range]
        for outer_col in block_range:
            cols = [c + block_size * outer_col for c in block_range]
            cartesian = [el for el in itertools.product(rows, cols)]
            for num in matrix_range:
                line = []
                for pair in cartesian:
                    #an NxN block should contain at least every number
                    line.append(map_to_dimacs(pair[0], pair[1], num))
                lines.append(line)

    for outer_row in block_range:
        rows = [r + block_size * outer_row for r in block_range]
        for outer_col in block_range:
            cols = [c + block_size * outer_col for c in block_range]
            cartesian = [el for el in itertools.product(rows, cols)]
            #an NxN block should contain at most every number
            for num in matrix_range:
                for idx, pair0 in enumerate(cartesian):
                    for pair1 in cartesian[idx+1:]:
                        line = [map_to_dimacs(pair0[0], pair0[1], num, negation=True), map_to_dimacs(pair1[0], pair1[1], num, negation=True)]
                        lines.append(line)

    number_of_vars = size ** 3
    number_of_clauses = len(lines)
    output = encode(number_of_vars, number_of_clauses, lines)
    print output

    #print graphs

    cnfs_path = "cnfs"
    solutions_path = "solutions"

    cnf_file_name, cnf_full_file_name = write_cnf(cnfs_path, file_name, output, number_of_vars, number_of_clauses)

    sat_output, sat_output_full_file_name = call_sat_solver(solutions_path, cnf_file_name, cnf_full_file_name)

    sat_satisfiable, sat_variables = read_sat_output(sat_output_full_file_name)

    for row in matrix_range:
        for col in matrix_range:
            for num in matrix_range:
                mapping = map_to_dimacs(row, col, num)
                if mapping in sat_variables:
                    matrix[row][col] = num + 1
    print "solution"
    for row in matrix_range:
        print str(matrix[row])
    with open(sat_output_full_file_name+"_human_readable", 'w') as fh:
        for row in matrix_range:
            str_row= str(matrix[row]).strip("[]") + "\n"
            fh.write(str_row)

