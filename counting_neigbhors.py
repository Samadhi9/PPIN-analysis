import networkx as nx

proteins = open('sub_network75.txt', 'rb')
output_file = open('node_degree.txt', 'w')
output_file.write("protein degree\n")

rows = proteins.readline()[0:]
graph = nx.Graph()
edges = nx.read_edgelist(proteins, nodetype=str, data=(('weight', str),))
graph.add_edges_from(edges.edges())


seeds = open('gene.txt', 'r').read()
contents =[]
for node in graph:
    if node in seeds:
        gene1 = node.strip().lower()
        contents.append(gene1)
        # counting neighbours
        degree = graph.degree[node]
        degree1 = str(degree)

        list1 = [node, degree1]
        row1 = ' '.join(list1)
        output_file.write("%s\n" % row1)

    else:
        continue
