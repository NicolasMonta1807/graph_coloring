import random
from graph.graph import UnDirectedGraph

import itertools
import time
import pandas as pd
import matplotlib.pyplot as plt

def cross_product_solve(G1: UnDirectedGraph):
    # Brute force using itertools cross product
    color = {}
    vertex_list = list(G1.get_vertices())
    for num_colors in range(2, len(G1.get_vertices()) + 1):
        print(f"Trying {num_colors} colors with brute force")
        stop = False
        for p in itertools.product(range(num_colors), repeat=len(vertex_list)):
            for i in range(len(vertex_list)):
                color[vertex_list[i]] = p[i]
            if check_graph_color_valid(G1, color):  # Llama a la función con el diccionario de colores
                print("Brute force valid coloring found:", color)
                print(f"Found a valid coloring with {num_colors} colors using brute force.")
                return num_colors
        if stop:
            break
        
def backtrack_solve(G1: UnDirectedGraph):
    # Backtracking
    for num_colors in range(2, len(G1.get_vertices()) + 1):
        print(f"Trying {num_colors} colors with backtracking")
        backtracking_result = color_backtracking(G1, num_colors)
        if backtracking_result:
            print("Backtracking valid coloring found:", backtracking_result)
            print(f"Found a valid coloring with {num_colors} colors using backtracking.")
            return num_colors
    return None

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

def run_tests():
    results = []
    graph_sizes = [(5, 10), (8, 14), (10, 18), (12, 22), (15, 25)]

    for nodes, edges in graph_sizes:
        G = create_random_graph(nodes, edges)
        G.print_graph()
        
        # Fuerza bruta
        start_time = time.time()
        num_colors_brute = cross_product_solve(G)
        brute_time = time.time() - start_time

        # Backtracking
        start_time = time.time()
        num_colors_backtrack = backtrack_solve(G)
        backtrack_time = time.time() - start_time

        # Guardar resultados
        results.append({
            "Nodes": nodes,
            "Edges": edges,
            "Colors (Brute Force)": num_colors_brute,
            "Time (Brute Force)": brute_time,
            "Colors (Backtracking)": num_colors_backtrack,
            "Time (Backtracking)": backtrack_time
        })

    df = pd.DataFrame(results)
    print(df)

    plt.plot(df["Nodes"], df["Time (Brute Force)"], label="Brute Force", marker="o")
    plt.plot(df["Nodes"], df["Time (Backtracking)"], label="Backtracking", marker="o")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Execution Time (s)")
    plt.title("Execution Time Comparison")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == '__main__':
    run_tests()
    