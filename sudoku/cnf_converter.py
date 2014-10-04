from os.path import join, isfile, abspath
from os import listdir
import subprocess


def create_matrix(mypath, graph_name):
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


def create_dimacs_line(lines):
    output = ""
    for line in lines:
        output += " ".join(line) + " 0\n"
    return output


def map_to_dimacs(row, col, num, negation=False):
    mapping = "x" + str(row) + str(col) + str(num)
    mapping = 81 * row + 9 * col + num + 1
    return ("-" if negation else "") + str(mapping)


def get_file_names(mypath):
    return [f for f in listdir(mypath) if isfile(join(mypath, f))]


def convert(input_name):
    matrix = create_matrix("sudokus", input_name)
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

    #each cell has at most one number assigned
    # for row in matrix_range:
    #     for col in matrix_range:
    #         for num0 in matrix_range:
    #             for num1 in range(num0+1, size):
    #                 line = [map_to_dimacs(row, col, num0, negation=True), map_to_dimacs(row, col, num1, negation=True)]
    #                 lines.append(line)

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
            for col0 in matrix_range:
                for col1 in range(col0+1, size):
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
            for row0 in matrix_range:
                for row1 in range(row0+1, size):
                    line = [map_to_dimacs(row0, col, num, negation=True), map_to_dimacs(row1, col, num, negation=True)]
                    lines.append(line)

    #an NxN block should contain at least every number
    for num in matrix_range:
        for row in matrix_range:
            line = []
            for col in matrix_range:
                row %= size
                col %= size
                line.append(map_to_dimacs(row, col, num))
            lines.append(line)

    #an NxN block should contain at most every number
    for num in matrix_range:
        for row in matrix_range:
            for col0 in matrix_range:
                for col1 in range(col0+1, size):
                    row %= size
                    col0 %= size
                    col1 %= size
                    line = [map_to_dimacs(row, col0, num, negation=True), map_to_dimacs(row, col1, num, negation=True)]
                    lines.append(line)

    output = create_dimacs_line(lines)
    print output

    number_of_variables = size ** 3
    number_of_clauses = len(lines)

    output = "p cnf %s %s\n" % (number_of_variables, number_of_clauses)
    output += create_dimacs_line(lines)
    #print graphs

    mypath = "cnfs"
    file_name = '%s___cnf-%s-%s.txt' % (input_name, number_of_variables, number_of_clauses)
    with open(join(mypath, file_name), 'w') as fh:
        print "writing cnf into %s" % file_name
        fh.write(output)

    file_names = get_file_names(mypath)
    sat_output_file = abspath(join("solutions", file_name))
    for file_name in file_names:
        cmd = "minisat %s %s" % (abspath(join(mypath, file_name)), sat_output_file)
        print "calling command %s" % cmd
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output

    satisfiable = False
    variables = []
    with open(sat_output_file, 'r') as fh:
        satisfiable = "SAT" == fh.readline().strip()
        if satisfiable:
            line = fh.readline().split(" ")
            for el in line:
                variables.append(el)

    for row in matrix_range:
        for col in matrix_range:
            for num in matrix_range:
                mapping = map_to_dimacs(row, col, num)
                if mapping in variables:
                    matrix[row][col] = num + 1
    print "solution"
    print matrix

convert("sudoku1.txt")

