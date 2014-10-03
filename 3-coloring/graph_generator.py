from Crypto.Random.random import randint


def create_graph_line(lines):
    output = ""
    for line in lines:
        output += " ".join(line)
        if not output:
            output += " "
        output += "-1\n"
    return output


def generate_graph(node_count, edge_count):
    print "generating graph (node_count=%s, edge_count=%s)" % (node_count, edge_count)
    graph = [[i == j for i in range(node_count)] for j in range(node_count)]
    graph_length = range(len(graph))
    node_connections = {}
    for node in graph_length:
        node_connections[node] = 0

    for i in graph_length:
        while node_connections[i] < edge_count:
            free_nodes = []
            for node in graph_length:
                if node != i and node_connections[node] < edge_count:
                    free_nodes.append(node)
            if not free_nodes:
                break
            connected_to = free_nodes[randint(0, len(free_nodes) - 1)]
            graph[i][connected_to] = True
            graph[connected_to][i] = True

            node_connections[i] += 1
            node_connections[connected_to] += 1
            #print "connecting %s and %s" % (i, connected_to)

    lines = []
    for i in graph_length:
        line = []
        for j in range(len(graph[i])):
            if i != j and graph[i][j]:
                line.append(str(j))
        lines.append(line)

    output = str(node_count) + "\n"
    output += create_graph_line(lines)
    with open("graphs/graph-%s-%s" % (node_count, edge_count), 'w') as fh:
        fh.write(output)
