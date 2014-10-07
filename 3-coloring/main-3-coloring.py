from os.path import join, exists
from file_operations.file_operations import get_file_names, clean_directories, call_sat_solver, read_sat_output

import graph_generator
import cnf_converter

graph_paths = "graphs"
cnfs_path = "cnfs"
solutions_path = "solutions"
graph_settings_map = {}


def generate_graphs():
    for node_count in [5, 10, 20, 40, 80, 200]:
        for edge_count in [1, 2, 3, 10, 15, 30, 50, 100]:
            if node_count > edge_count:
                graph_file_name = graph_generator.generate_graph(node_count, edge_count)
                graph_settings_map[graph_file_name] = {"node_count": node_count, "edge_count": edge_count}

clean_directories([graph_paths, cnfs_path, solutions_path])
generate_graphs()

file_names = get_file_names(graph_paths)
file_names.sort()
for file_name in file_names:
    cnf_file_name, cnf_full_file_name = cnf_converter.convert_to_cnf(graph_paths, file_name)
    output, sat_output_full_file_name = call_sat_solver(solutions_path, cnf_file_name, cnf_full_file_name)
    satisfiable, variables = read_sat_output(sat_output_full_file_name)
    f = join(solutions_path, "summary")
    mode = 'a' if exists(f) else 'w'
    with open(f, mode) as fh:
        if file_name in graph_settings_map:
            tmp_map = graph_settings_map[file_name]
            fh.write(str(tmp_map["node_count"]) + " " + str(tmp_map["edge_count"]) + " " + str(satisfiable) + "\n")




