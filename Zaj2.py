from dimacs import *
from math import inf

class Vertex:
    def __init__(self, number):
        self.number = number
        self.neighbours = []
        self.res = []


def actualGState(G):
    print("Obecny wyglad grafu")
    for i in range(len(G)):
        print("Wierzcholek: ", G[i].number, " (sasiad,przepustowosc,aktualny przeplyw)= ", G[i].neighbours)


def actualResState(G):
    print("Obecny wyglad sieci residualnej")
    for i in range(len(G)):
        print("Wierzcholek: ", G[i].number, " (sasiad,krawedz res)= ", G[i].res)


def buildResidual(G):
    for i in range(len(G)):
        G[i].res.clear()
    for i in range(len(G)):
        for j in G[i].neighbours:
            if j[2] == 0:  # nie ma przeplywu
                G[i].res.append([j[0], j[1]])
            else:  # jest przeplyw
                if j[1] - j[2] > 0: G[i].res.append([j[0], j[1] - j[2]])
                G[j[0] - 1].res.append([i + 1, j[2]])


def BFS(G, s, visited, parent):
    q = []
    visited[s - 1] = True
    q.append(s)
    while len(q) > 0:
        u = q.pop(0)
        for v in G[u - 1].res:
            if not visited[v[0] - 1]:
                visited[v[0] - 1] = True
                parent[v[0] - 1] = u
                q.append(v[0])


def DFS(G, s, t, visited, parent):
    visited[s - 1] = True
    for u in G[s - 1].res:
        if not visited[u[0] - 1]:
            parent[u[0] - 1] = s
            DFS(G, u[0], t, visited, parent)


def findEdge(G, s, t):
    for l in range(len(G[s - 1].neighbours)):
        if G[s - 1].neighbours[l][0] == t: return (True, l)
    return (False, -1)


def getResVal(G, begin, end):
    for l in range(len(G[begin - 1].res)):
        if G[begin - 1].res[l][0] == end: return G[begin - 1].res[l][1]
    return -1


def buildGraph(G, v, s, t):
    G.clear()
    for i in range(v):
        G.append(Vertex(i + 1))
    for (x, y, c) in L:  # przeglądaj krawędzie z listy
        # print("krawedz miedzy", x, "i", y, "o wadze", c)  # wypisuj
        if (y == s or x == t):
            G[y - 1].neighbours.append([x, c, 0])
        elif (x==s or y==t):
            G[x - 1].neighbours.append([y, c, 0])
        else:
            G[x - 1].neighbours.append([y, c, 0])
            G[y - 1].neighbours.append([x, c, 0])


def Ford_Fulkerson(G, s, t):
    score = 0
    while True:
        buildResidual(G)
        # actualGState(G)
        # actualResState(G)
        visited = [False] * len(G)
        parent = [0] * len(G)
        x = inf
        #BFS(G, s, visited, parent)
        DFS(G, s, t, visited, parent)
        # print(parent)
        u = t
        while not u == s:
            element = getResVal(G, parent[u - 1], u)
            # print("Krawedz ", parent[u-1]," ",u," wartosc ", element)
            if element == -1:
                x = 0
                break
            if element < x: x = element
            u = parent[u - 1]
        if x == 0: break
        # print("Wartosc sciezki: ", x)
        score += x
        v = t
        while not v == s:
            begin = parent[v - 1]
            (find, pos) = findEdge(G, begin, v)
            if find:
                G[begin - 1].neighbours[pos][2] += x
            else:
                (tmp, posrev) = findEdge(G, v, begin)
                G[v - 1].neighbours[posrev][2] -= x
            v = parent[v - 1]
    return score


(V, L) = loadDirectedWeightedGraph("clique5")

# ----------------------------------------------------------------------------------
# Ford-Fulkerson
#G = []

#for i in range(V):
#   G.append(Vertex(i + 1))

#for (x, y, c) in L:  # przeglądaj krawędzie z listy
#print("krawedz miedzy", x, "i", y, "o wadze", c)  # wypisuj
#    G[x - 1].neighbours.append([y, c, 0])

#actualGState(G)

#print(Ford_Fulkerson(G, 1, V))

# ----------------------------------------------------------------------------------
# Spójność krawędziowa

G = []

mincut = inf

for i in range(2, V + 1):
    buildGraph(G, V, 1, i)
    # actualGState(G)
    cut = Ford_Fulkerson(G, 1, i)
    if cut < mincut: mincut = cut

print(mincut)

# ----------------------------------------------------------------------------------
# Ściągawka indeksów
# neighbours[i][...]
# 0 - koniec krawedzi skierowanej
# 1 - przepustowosc krawedzi
# 2 - aktualny przeplyw
# res[i][...]
# 0 - koniec krawedzi skierowanej
# 1 - wartosc sciezki w sieci
