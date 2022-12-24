import time

import graphviz


def timeit(fun):
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"Running {fun.__name__}...")
        result = fun(*args, **kwargs)
        end = time.time()
        print(f'{fun.__name__} time: {end - start:.3f} s')
        return result

    return wrapper


class FNFMaker:
    def __init__(self, alphabet, dependence_fun=None):
        self.alphabet = alphabet
        self.dependence_fun = dependence_fun

        self.dependencies = None

    def get_dependencies(self):
        if self.dependencies is None:
            dependencies = set()

            for c1 in self.alphabet:
                for c2 in self.alphabet:
                    if self.dependence_fun(c1, c2):
                        dependencies.add((c1, c2))

            self.dependencies = dependencies

        return self.dependencies

    def build_graph(self, word):
        n = len(word)

        dependencies = self.get_dependencies()

        G = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                G[i][j] = 1 if (word[i], word[j]) in dependencies else 0

        G = self._transitive_reduction(G)

        return G

    def draw_graph(self, G, word):
        graph = graphviz.Digraph()

        for i, label in enumerate(word):
            graph.node(str(i), label=str(label))

        for i in range(len(G)):
            for j in range(len(G[i])):
                if G[i][j]:
                    graph.edge(str(i), str(j))

        graph.render('graph', view=True)

    def getFNF(self, G, word):
        shortest_paths = self._longest_path_dag(G)
        FNF = [set() for _ in range(max(shortest_paths) + 1)]
        for i, char in zip(shortest_paths, word):
            FNF[i].add(char)
        return FNF

    @staticmethod
    def _transitive_closure(adj):
        n = len(adj)
        closure = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                closure[i][j] = adj[i][j]

        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if adj[i][k] and adj[k][j]:
                        closure[i][j] = 1
        return closure

    @staticmethod
    def _transitive_reduction(adj):
        closure = FNFMaker._transitive_closure(adj)

        n = len(adj)
        for i in range(n):
            for j in range(n):
                if adj[i][j] == 1:
                    for k in range(n):
                        if k == i or k == j:
                            continue
                        if adj[k][j] == 1 and closure[i][k] == 1:
                            adj[i][j] = 0
                            break
        return adj

    @staticmethod
    def _longest_path_dag(adj_mat):
        n = len(adj_mat)
        distances = [float('-inf')] * n

        sources = [i for i in range(n) if sum(adj_mat[j][i] for j in range(n)) == 0]
        for u in sources:
            distances[u] = 0

        for u in range(n):
            for v in range(n):
                if adj_mat[u][v] > 0:  # there is an edge from u to v
                    distances[v] = max(distances[v], distances[u] + adj_mat[u][v])

        return distances
