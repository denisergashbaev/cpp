from dircache import listdir
from os.path import isfile, join, abspath
import subprocess
from file_operations.file_operations import get_file_names

import graph_generator
import cnf_converter


def generate_graph():
    for node_count in [5, 10, 20, 40, 80, 200]:
        for edge_count in [1, 2, 3, 10, 15, 30, 50, 100]:
            if node_count > edge_count:
                graph_generator.generate_graph(node_count, edge_count)


def convert_to_cnf():
    mypath = "graphs"
    file_names = get_file_names(mypath)
    for file_name in file_names:
        print "converting %s" % file_name
        cnf_converter.convert_to_cnf(mypath, file_name)


def run_minisat():
    mypath = "cnfs"
    file_names = get_file_names(mypath)
    for file_name in file_names:
        cmd = "minisat %s %s" % (abspath(join(mypath, file_name)), abspath(join("solutions", file_name)))
        print "calling command %s" % cmd
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output = process.communicate()[0]
        print output


generate_graph()
convert_to_cnf()
run_minisat()
