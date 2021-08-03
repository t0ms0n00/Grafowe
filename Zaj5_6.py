from dimacs import *


class Node:
    def __init__(self, idx):
        self.idx = idx
        self.out = set()  # zbiór sąsiadów
        self.RN = set()
        self.parent = 0

    def connect_to(self, v):
        self.out.add(v)


def LexBFS(G):
    visited = []
    list = []
    a = set()
    for i in range(1, len(G)): a.add(i)
    list.append(a)
    while len(visited) < len(G) - 1:
        v = list[len(list) - 1].pop()
        if v == set(): continue
        visited.append(v)
        i = 0
        while i < len(list):
            j = 0
            s = list[i]
            x = s & G[v].out  # sasiedzi, przeciecie zbiorow
            y = s - x  # niesasiedzi
            if len(x) > 0:
                list.insert(i + 1, x)
                j += 1
            if len(y) > 0:
                list.insert(i + 1, y)
                j += 1
            list.remove(s)
            i += j
        # print(list)

        l = set()
        p = []
        for u in visited:
            l.add(u)
            p.append(u)
        G[v].RN = (l & G[v].out)
        found = False
        while len(p) > 0 and not found:
            if {p[-1]} & G[v].RN == set():
                p.pop(-1)
            else:
                found = True
        if found: G[v].parent = p[-1]
    return visited


def checkLexBFS(G, vs):
    n = len(G)
    pi = [None] * n
    for i, v in enumerate(vs):
        pi[v] = i

    for i in range(n - 1):
        for j in range(i + 1, n - 1):
            Ni = G[vs[i]].out
            Nj = G[vs[j]].out

            verts = [pi[v] for v in Nj - Ni if pi[v] < i]
            if verts:
                viable = [pi[v] for v in Ni - Nj]
                if not viable or min(verts) <= min(viable):
                    return False
    return True


def PEO(G):
    q = LexBFS(G)
    peo = True
    for v in q[1:]:
        if peo == False: break
        if not G[v].RN - {G[v].parent} <= G[G[v].parent].RN: peo = False
    return peo


# Zadanie 1:

def czyPrzekatniowy(G):
    return PEO(G)


# Zadanie 2:

def najwiekszaKlika(G):
    m = 0
    q = LexBFS(G)
    for v in q:
        s = len(G[v].RN) + 1
        if s > m: m = s
    return m


# Zadanie 3:

def kolorowanie(G):
    color = [0] * len(G)
    V = LexBFS(G)
    for v in V:
        used = {color[u] for u in G[v].out}
        c = 1
        while c in used: c += 1
        color[v] = c
    print(color)
    return max(color)


# Zadanie 4:

def pokrycie(G):        # do poprawy
    I = set()
    V = LexBFS(G)
    for v in V:
        N = G[v].out
        if I & N == set(): I.add(v)
    F = {u for u in range(1,len(G))}
    return len(F-I)

(V, L) = loadWeightedGraph("pokrycie\\nonplanar-ex1")

G = [None] + [Node(i) for i in range(1, V + 1)]  # żeby móc indeksować numerem wierzchołka

for (u, v, _) in L:
    G[u].connect_to(v)
    G[v].connect_to(u)

# print(LexBFS(G))
# print(checkLexBFS(G, LexBFS(G)))
# print(G[3].RN)
# print(G[3].parent)
print(pokrycie(G))
