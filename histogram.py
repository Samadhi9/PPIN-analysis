import numpy as np
from scipy.interpolate import make_interp_spline, BSpline
import networkx as nx
import matplotlib.pyplot as plt

proteins = open('4004_in_sub_network100.txt', 'rb')
protein = open('4004_in_sub_network75.txt', 'rb')

rows = proteins.readline()[0:]
graphs = nx.Graph()
edges = nx.read_edgelist(proteins, nodetype=str, data=(('weight', str),))
graphs.add_edges_from(edges.edges())

row = protein.readline()[0:]
graph = nx.Graph()
edges = nx.read_edgelist(protein, nodetype=str, data=(('weight', str),))
graph.add_edges_from(edges.edges())

y1 = np.array(nx.degree_histogram(graphs))
y2 = np.array(nx.degree_histogram(graph))

x = np.arange(29)
x1 = np.arange(23)

xnew = np.linspace(x.min(), x.max(), 300)
spl = make_interp_spline(x, y1, k=2)  # type: BSpline
y_smooth = spl(xnew)

x1new = np.linspace(x1.min(), x1.max(), 300)
spl = make_interp_spline(x1, y2, k=2)  # type: BSpline
y2_smooth = spl(x1new)


plt.figure(figsize=(6, 4))
plt.plot(xnew, y_smooth, label="100")
plt.fill_between(xnew, y_smooth, color='#cccaff', alpha=0.5)
plt.plot(x1new, y2_smooth, color='#ff7e87', label="75")
plt.fill_between(x1new, y2_smooth, color='#ffd2d5', alpha=0.5)
plt.ylabel("Distribution")
plt.xlabel("Degree")
plt.legend()
plt.show()