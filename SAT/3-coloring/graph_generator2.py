from Crypto.Random.random import randint
from os.path import join
import subprocess


def create_graph_line(lines):
    output = ""
    for line in lines:
        output += " ".join(line) + " -1\n"
    return output.strip()


def generate_graph(node_count, edge_count):
    seed = 10
    print "generating graph (node_count=%s, edge_count=%s, seed=%s)" % (node_count, edge_count, seed)

    graph_file_name = "graph-%s-%s-%s" % (node_count, edge_count, seed)

    cmd = "./Graph_rnd_generator.o %s %s %s" % (node_count, edge_count, seed)
    print "calling command %s" % cmd
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print "output: \n" + output
    with open(join("graphs", graph_file_name), 'w') as fh:
        fh.write(output)
    return graph_file_name