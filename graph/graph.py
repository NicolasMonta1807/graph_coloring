class UnDirectedGraph:
    def __init__(self):
        self.graph = {}

    def get_vertices(self):
        return self.graph.keys()

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, vertex1, vertex2):
        if vertex1 == vertex2:
            return
        if vertex1 in self.graph:
            self.graph[vertex1].append(vertex2)
        else:
            self.graph[vertex1] = [vertex2]

        if vertex2 in self.graph:
            self.graph[vertex2].append(vertex1)
        else:
            self.graph[vertex2] = [vertex1]

    def print_graph(self):
        for vertex in self.graph:
            print(vertex, end=": ")
            for edge in self.graph[vertex]:
                print(edge, end=" ")
            print()

    def adj(self, vertex):
        return self.graph[vertex]

    def edge_exists(self, vertex1, vertex2):
        if vertex1 == vertex2:
            return True
        return vertex2 in self.graph[vertex1]
