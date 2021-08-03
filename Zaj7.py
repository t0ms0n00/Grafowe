import networkx as nx
from networkx.algorithms.planarity import check_planarity
from networkx.algorithms.flow import maximum_flow
from dimacs import *

# tworzenie grafu
G = nx.Graph()                   # stwórz pusty graf nieskierowany
G.add_node(1)                    # dodaj wierzchołek 1 (wierzchołkami może być cokolwiek haszowalnego)
G.add_nodes_from([2,3])          # dodaj wierzchołki z listy (dowolnego iterowalnego kontenera)
G.remove_node(1)                 # usuń wierchołek 1
G.remove_nodes_from([2,3])       # usuń wierzchołki z listy
G.add_edge(1,2)                  # dodaj krawędź między wierzchołkami 1 i 2
G.add_edges_from([(1,3),(2,3)])  # dodaj krawędzie z listy (iterowalnego kontenera)
G.remove_edge(1,2)               # usuń krawędź
G.remove_edges_from([(1,2),(1,3)])  # usuń krawędzie z listy (iterowalnego kontenera)

# odczytywanie podstawowych informacji o grafie
G.number_of_nodes()              # liczba wierzchołkóœ
G.number_of_edges()              # liczba krawędzi
G.nodes                          # wierzchołki grafu
G.edges                          # krawędzie grafu
G.adj[1]                         # sąsiedzi wierzchołka 1
print("Sasiedzi 3", G[3])                             # sąsiedzi wierzchołka 1
#G[1][2]                         # dostęp do krawędzi {1,2} (można jej dodawać atrybuty)
G.has_node(1)                    # czy istnieje wierzchołek 1?
G.has_edge(1,2)                  # czy istnieje krawędź {1,2}?

def makeGraph():
    (V, L) = loadWeightedGraph("lab7_1\\nonplanar-ex1")
    Graph = nx.Graph()
    Graph.add_nodes_from([i for i in range(1,V)])
    for edge in L:
        Graph.add_edge(edge[0],edge[1])
        Graph.add_edge(edge[1],edge[0])
    return Graph

def makeDirectedGraph():
    (V, L) = loadDirectedWeightedGraph("lab7_2\\flow\\grid5x5")
    Graph=nx.DiGraph()
    Graph.add_nodes_from([i for i in range(1,V)])
    for edge in L:
        Graph.add_edge(edge[0],edge[1])
        Graph[edge[0]][edge[1]]['capacity']=edge[2]
    return Graph

print(check_planarity(makeGraph()))
Graph = makeDirectedGraph()
print(maximum_flow(Graph,1,Graph.number_of_nodes()))