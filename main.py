import random
from graph.graph import UnDirectedGraph

import itertools

def create_random_graph(num_vertices, num_edges):
    graph = UnDirectedGraph()
    for i in range(num_vertices):
        graph.add_vertex(i)
    added = 0
    while added < num_edges:
        vertex1 = random.randint(0, num_vertices - 1)
        vertex2 = random.randint(0, num_vertices - 1)
        if not graph.edge_exists(vertex1, vertex2):
            graph.add_edge(vertex1, vertex2)
            added += 1

    return graph

def check_graph_color_valid(g: UnDirectedGraph, color: dict):
    for vertex in g.get_vertices():
        for neighbor in g.adj(vertex):
            if color[vertex] == color[neighbor]:
                return False
    return True

def color_backtracking(g: UnDirectedGraph, k):
    colors = [-1] * len(g.get_vertices())  # Inicializamos los colores como no asignados (-1)
    success, solution = backtracking_aux(g, k, 0, colors)
    return solution if success else None

def backtracking_aux(g: UnDirectedGraph, k, i, colors):
    # Si hemos coloreado todos los vértices, encontramos una solución
    if i == len(g.get_vertices()):
        return True, colors

    # Intentamos asignar un color de 0 a k-1 al vértice actual
    for color in range(k):
        colors[i] = color
        valid = backtrack_valid(g, i, colors, color)
        if valid:
            success, solution = backtracking_aux(g, k, i + 1, colors)
            if success:
                return True, solution
        colors[i] = -1  # Deshacemos la asignación si no es solución

    return False, colors

def backtrack_valid(g: UnDirectedGraph, i, colors, color):
    for neighbor in g.adj(i):
        if colors[neighbor] == color:
            return False
    return True

if __name__ == '__main__':
    G1 = create_random_graph(10, 15)
    G1.print_graph()
    
    # Método de fuerza bruta con itertools
    color = {}
    vertex_list = list(G1.get_vertices())
    for num_colors in range(2, len(G1.get_vertices()) + 1):
        print(f"Trying {num_colors} colors with brute force")
        stop = False
        for p in itertools.product(range(num_colors), repeat=len(vertex_list)):
            for i in range(len(vertex_list)):
                color[vertex_list[i]] = p[i]
            if check_graph_color_valid(G1, color):
                print("Brute force valid coloring found:", color)
                G1.print_graph()
                print(f"Found a valid coloring with {num_colors} colors using brute force.")
                stop = True
                break
        if stop:
            break

    # Método de backtracking
    for num_colors in range(2, len(G1.get_vertices()) + 1):
        print(f"Trying {num_colors} colors with backtracking")
        backtracking_result = color_backtracking(G1, num_colors)
        if backtracking_result:
            print("Backtracking valid coloring found:", backtracking_result)
            G1.print_graph()
            print(f"Found a valid coloring with {num_colors} colors using backtracking.")
            break
