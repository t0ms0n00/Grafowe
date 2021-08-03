from queue import PriorityQueue
from math import inf
from dimacs import *

(V,L) = loadWeightedGraph( "rand20_100" )        # wczytaj graf

G=[[]]*V
for i in range(V):
    G[i]=[0]*V

for (x,y,c) in L:                        # przeglądaj krawędzie z listy
    print( "krawedz miedzy", x, "i", y,"o wadze", c )   # wypisuj
    G[x-1][y-1]=c
    G[y-1][x-1]=c

def Dijkstra(G, s, t):
    q = PriorityQueue()
    d = [-1] * len(G[s])
    used = [False] * len(G[s])
    d[s] = inf
    q.put((-d[s], s))
    while not q.empty():
        v = q.get()[1]
        if not used[v]:
            used[v] = True
            for u in range(len(G[v])):  # przeglad sasiadow
                if not G[v][u] == 0:
                    if d[v] <= G[v][u]:
                        d[u] = max(d[v], d[u])
                    else:
                        d[u] = max(G[v][u], d[u])
                    if not used[u]: q.put((-d[u], u))
    return d[t]

print(Dijkstra(G,0,1))