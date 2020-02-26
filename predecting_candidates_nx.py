import networkx as nx

proteins = open('replaced_data.txt', 'rb')
output_file = open('prediction_score_nx.txt', 'w')
output_file.write("protein prediction_score\n")

#set of seeds
seeds = open('gene.txt', 'r')
seed = []
for line in seeds:
    seed.append(line.strip())
set1 = set(seed)

seeds.close()

#graph
rows = proteins.readline()[0:]
graph = nx.Graph()
edges = nx.read_edgelist(proteins, nodetype=str, data=(('weight', str),))
graph.add_edges_from(edges.edges())

#nunmber of seeds
tot_f = len(seed)
#number of nodes
tot_n = len(graph.nodes)

#calculation
seeds = open('gene.txt', 'r').read()
for node in graph:
    if node in seeds:
        continue
    else:
        #counting neighbours
        nu = graph.degree[node]
        #counting seed neighbours
        set2 = set(graph.neighbors(node))
        nfu = len(set1.intersection(set2))
        nfu = float(nfu)


        #calculating prediction score
        ef = tot_f * nu / float(tot_n)
        try:
            prediction_score = (nfu - ef) ** 2 / float(ef)
        except ZeroDivisionError:
            prediction_score = 0
        prediction_scores = str(prediction_score)
        #print(prediction_score)

       #output
        list1 = [node, prediction_scores]
        row1 = ' '.join(list1)
        output_file.write("%s\n" % row1)

