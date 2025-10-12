neighborhood_coords = [[0, -1], [1, 0], [0, 1], [-1, 0]]

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

graph = generate_grid_graph(5, 5)
print(graph)