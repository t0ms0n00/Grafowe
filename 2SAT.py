from dimacs import *
import networkx as nx
from networkx.algorithms.components import strongly_connected_components

def makeGraph():
    (V, F) = loadCNFFormula("sat//simple_sat")
    Graph=nx.DiGraph()
    for i in F:
        u=i[0]
        v=i[1]
        if not Graph.has_node(u):
            Graph.add_node(u)
        if not Graph.has_node(v):
            Graph.add_node(v)
        if not Graph.has_node(-u):
            Graph.add_node(-u)
        if not Graph.has_node(-v):
            Graph.add_node(-v)
        Graph.add_edge(-u,v)
        Graph.add_edge(-v,u)
    return Graph

G=makeGraph()
SCC = strongly_connected_components(G)    # policz silnie spójne składowe grafu G
# wypisz zawartość składowych
t = 0
for S in SCC:
  print("Silnie spojna składowa", t, "zawiera wierzcholki")
  for v in S:
    print("  ",v)
  t += 1