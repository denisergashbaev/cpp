from os.path import join


def create_matrix(mypath, graph_name):
    matrix = []
    with open(join(mypath, graph_name), 'r') as fh:
        for idx, line in enumerate(fh):
            row = []
            els = line.split(", ")
            size = len(els)
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
    #mapping = 3 * row + col + 1
    return ("-" if negation else "") + str(mapping)


def convert():
    matrix = create_matrix("sudokus", "sudoku1.txt")
    size = len(matrix)
    lines = []
    matrix_range = range(size)

    #set the assigned variables
    for row in matrix_range:
        for col in matrix_range:
            for num in matrix_range:
                if matrix[row][col] == num:
                    lines.append([map_to_dimacs(row, col, num)])

    #each cell has at least one number assigned
    for row in matrix_range:
        for col in matrix_range:
            line = []
            for num in matrix_range:
                line.append(map_to_dimacs(row, col, num))
            lines.append(line)

    #each cell has at most one number assigned
    for row in matrix_range:
        for col in matrix_range:
            for num0 in matrix_range:
                line = []
                for num1 in range(num0, size):
                    line.append(map_to_dimacs(row, col, num0, negation=True))
                    line.append(map_to_dimacs(row, col, num1, negation=True))
                lines.append(line)

    for num in matrix_range:
        #there is only one cell with each number in a row
        for row in matrix_range:
            line = []
            for col in matrix_range:
                line.append(map_to_dimacs(row, col, num))
            lines.append(line)

        for row in matrix_range:
            for col0 in matrix_range:
                line = []
                for col1 in range(col0, size):
                    line.append(map_to_dimacs(row, col0, num, negation=True))
                    line.append(map_to_dimacs(row, col1, num, negation=True))
                lines.append(line)

        #there is only one cell with each number in a col
        for col in matrix_range:
            line = []
            for row in matrix_range:
                line.append(map_to_dimacs(row, col, num))
            lines.append(line)

        for col in matrix_range:
            for row0 in matrix_range:
                line = []
                for row1 in range(row0, size):
                    line.append(map_to_dimacs(row0, col, num, negation=True))
                    line.append(map_to_dimacs(row1, col, num, negation=True))
                lines.append(line)

        #there is only one cell with each number in a block
        for row in matrix_range:
            line = []
            for col in matrix_range:
                row %= size
                col %= size
                line.append(map_to_dimacs(row, col, num, negation=True))
            lines.append(line)

        for row in matrix_range:
            for col0 in matrix_range:
                line = []
                for col1 in range(col0, size):
                    row %= size
                    col0 %= size
                    col1 %=size
                    line.append(map_to_dimacs(row, col0, num, negation=True))
                    line.append(map_to_dimacs(row, col1, num, negation=True))
                lines.append(line)

    output = create_dimacs_line(lines)
    print output


convert()

