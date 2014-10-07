from os.path import join
from dimacs.dimacs import encode
from file_operations.file_operations import write_cnf


def map_to_dimacs(i, j, negation=False):
    mapping = "x" + str(i) + str(j)
    mapping = 3 * i + j + 1
    return ("-" if negation else "") + str(mapping)


def convert_to_cnf(mypath, graph_name):
    number_of_colors = 3
    with open(join(mypath, graph_name), 'r') as fh:
        number_of_nodes = int(fh.readline())
        connections = {}
        for node_index, line in enumerate(fh):
            line = line.strip()
            if line == '\n':
                continue
            if node_index not in connections:
                connections[node_index] = []
            els = line.split(" ")
            for el_index, el in enumerate(els):
                # last element (probably -1 or "\n")
                if el_index == len(els) - 1:
                    continue
                connections[node_index].append(int(el))
                #print connections

    lines = []

    #a node must have at least one color: x00 v x01 v x02
    for node in range(number_of_nodes):
        lines.append([map_to_dimacs(node, color) for color in range(number_of_colors)])

    #a node can not have more than one color: -(x00 ^ x01) ...
    for node in range(number_of_nodes):
        for color0 in range(number_of_colors):
            for color1 in range(color0 + 1, number_of_colors):
                lines.append([map_to_dimacs(node, color0, True), map_to_dimacs(node, color1, True)])

    print connections
    ##one color can not be shared among two adjacent nodes: -(x01 ^ x11) ...
    for color in range(number_of_colors):
        for node0 in range(number_of_nodes):
            for node1 in connections[node0]:
                lines.append([map_to_dimacs(node0, color, True), map_to_dimacs(node1, color, True)])

    number_of_vars = number_of_nodes * number_of_colors
    number_of_clauses = len(lines)

    output = encode(number_of_vars, number_of_clauses, lines)
    cnf_file_name, cnf_full_file_name = write_cnf("cnfs", graph_name, output, number_of_vars, number_of_clauses)

    return cnf_file_name, cnf_full_file_name