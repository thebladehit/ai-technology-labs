import matplotlib.pyplot as plt

neighborhood_coords = [[0, -1], [1, 0], [0, 1], [-1, 0]]

# Core logic
## Generate Graph
def get_vertex_neighborhood(x: int, y: int, maxX: int, maxY: int):
    neighborhood_vertices_coords = []
    for dx, dy in neighborhood_coords:
        nx = x + dx
        ny = y + dy
        if nx < 0 or nx >= maxX:
            continue
        if ny < 0 or ny >= maxY:
            continue
        neighborhood_vertices_coords.append((nx, ny))
    return neighborhood_vertices_coords


def generate_grid_graph(rowCount: int, colCount: int):
    graph = {}
    for y in range(0, rowCount):
        for x in range(0, colCount):
            graph[(x, y)] = get_vertex_neighborhood(x, y, colCount, rowCount)
    return graph

## is_connected graph
def is_connected_dfs(graph: dict):
    vertecies = set(graph.keys())
    if not vertecies:
        return True
    
    start = next(iter(vertecies))
    visited = set()

    def dfs(v):
        visited.add(v)
        for w in graph.get(v, []):
            if w not in visited:
                dfs(w)

    dfs(start)
    return visited == vertecies


# Draw logic
def draw_edges(graph: dict):
    drawn_edges = set()
    for vertex, neighbors in graph.items():
        x1, y1 = vertex
        for neighbor in neighbors:
            edge = tuple(sorted([vertex, neighbor]))
            if edge not in drawn_edges:
                x2, y2 = neighbor
                plt.plot([x1, x2], [y1, y2], color="gray", linewidth=2)
                drawn_edges.add(edge)

def draw_vertices(graph: dict):
    for vertex in graph.keys():
        x, y = vertex
        plt.scatter(x, y, color="skyblue", s=150, edgecolors="black", zorder=3)
        plt.text(x, y + 0.2, f"{vertex}", ha="center", fontsize=8)

def draw_graph(graph: dict, rowSize: int, colSize: int):
    plt.figure(figsize=(colSize, rowSize))
    draw_edges(graph)
    draw_vertices(graph)
    plt.axis("equal")
    plt.gca().invert_yaxis()
    plt.axis("off")
    plt.title("Візуалізація графа (дороги)")
    plt.show()


graph = generate_grid_graph(5, 5)
print(graph)

print(is_connected_dfs(graph))

draw_graph(graph, 5, 5)