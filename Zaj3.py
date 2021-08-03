from dimacs import *
from queue import PriorityQueue
from math import inf

class Node:
    def __init__(self):
        self.edges = {}  # słownik  mapujący wierzchołki do których są krawędzie na ich wagi
        self.active = True  # informacja czy rozpatrujemy dany wierzchołek
        self.merged = []

    def addEdge(self, to, weight):
        self.edges[to] = self.edges.get(to, 0) + weight  # dodaj krawędź do zadanego wierzchołka
        # o zadanej wadze; a jeśli taka krawędź
        # istnieje, to dodaj do niej wagę

    def delEdge(self, to):
        del self.edges[to]  # usuń krawędź do zadanego wierzchołka

    def getEdgeValue(self, to):
        return self.edges[to]


def printGraph(G):
    for i in range(len(G)):
        if G[i].active:
            print("Wierzcholek ", i + 1, " krawędzie do ")
            for e in G[i].edges:
                if G[e - 1].active:
                    print(e, " o wadze ", G[i].edges[e])
    print()

def mergeVertices(G, x, y):
    for v in G[y - 1].edges:
        if not v == x and G[v - 1].active:
            G[x - 1].addEdge(v, G[y - 1].getEdgeValue(v))  # dodaj krawedz do x dla kazdego sasiada y
            G[v - 1].addEdge(x, G[y - 1].getEdgeValue(v))
    G[y - 1].active = False
    G[x - 1].merged.extend(G[y - 1].merged)
    G[x - 1].merged.append(y)


def countActive(G):       # aktualna liczba wierzchołków aktywnych
    counter = 0
    for i in range(len(G)):
        if G[i].active: counter += 1
    return counter


def minimumCutPhase(G):
    a = 1  # dowolny wierzcholek może to zawsze być wierzchołek numer 1 (lub 0 po przenumerowaniu)
    S = []  # lista wierzchołków
    sumToS = [0] * len(G)   # aktualna suma do zbioru S
    used = [False] * len(G)
    q = PriorityQueue()
    q.put((0, a))
    while not len(S) == countActive(G):
        v = q.get()[1]      # tylko nr wierzcholka potrzebny
        if used[v - 1]: continue
        S.append(v)
        used[v - 1] = True
        for i in G[v - 1].edges:
            if G[i-1].active and  not used[i - 1]: sumToS[i - 1] += G[v - 1].getEdgeValue(i)
            q.put((-sumToS[i - 1], i))
    s = S[-1]
    t = S[-2]
    potential_score=0
    for edge in G[s-1].edges:
        if G[edge-1].active:
            potential_score+=G[s-1].edges.get(edge)
    #print("Scalam ",s," do ",t)
    #print()
    mergeVertices(G,t,s)
    #print("WYNIK POTENCJALNY: ",potential_score)
    return (potential_score,s)

def Stoer_Wagner(G):
    score=inf
    pot_cut=[]
    while countActive(G)>1:
    #    printGraph(G)
        pot_score=minimumCutPhase(G)
        if pot_score[0]<score:
            score=pot_score[0]
            pot_cut=pot_score[1]
    G[pot_cut - 1].merged.append(pot_cut)
    print("Odcięta składowa: ",G[pot_cut-1].merged)
    return score


(V, L) = loadWeightedGraph("clique5")  # wczytaj graf
# for (x,y,c) in L:                        # przeglądaj krawędzie z listy
# print( "krawedz miedzy", x, "i", y,"o wadze", c )   # wypisuj

G = [Node() for i in range(V)]

for (x, y, c) in L:
    G[x - 1].addEdge(y, c)
    G[y - 1].addEdge(x, c)


print("Spójność krawędziowa: ",Stoer_Wagner(G))