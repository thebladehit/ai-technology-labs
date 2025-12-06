import matplotlib.pyplot as plt
import random
import copy

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

## Remove random edge
def remove_random_edge(graph: dict):
    copy_graph = copy.deepcopy(graph)
    edges = []
    for u, neighbors in copy_graph.items():
        for v in neighbors:
            if (v, u) not in edges:
                edges.append((u, v))
    
    if not edges:
        return None
    
    u, v = random.choice(edges)

    if v in copy_graph[u]:
        copy_graph[u].remove(v)
    if u in copy_graph[v]:
        copy_graph[v].remove(u)

    return copy_graph

def remove_random_edges(graph: dict, count: int, rowCount: int, colCount: int):
    if count > (rowCount * colCount - 1):
        raise ValueError("You can't delete this count of edges")
    
    graph_copy = copy.deepcopy(graph)
    i = 0
    attempts = 0
    
    while i < count: 
        while True:
            new_graph = remove_random_edge(graph_copy)
            attempts += 1
            if not new_graph:
                graph_copy = copy.deepcopy(graph)
                i = -1
                break
            if is_connected_dfs(new_graph):
                graph_copy = copy.deepcopy(new_graph)
                break
            if attempts > 10:
                graph_copy = copy.deepcopy(graph)
                i = -1
                break

        i += 1
    return graph_copy

# Agent logic
class Agent:
    def __init__(self, graph, start, goal):
        self.graph = graph
        self.cur_pos = start
        self.goal = goal
        self.stack = []
        # Knowledge base
        self.knowledge_base = {
            'visited': set(),
            'self_graph': dict(),
        }
        self.path = [ start ]
        self.full_path = [ start ]

    def tell_knowledge_base_roads(self, road, possible: list):
        if road in self.knowledge_base['visited']:
            return
        
        self.knowledge_base['self_graph'].setdefault(self.cur_pos, [])
        if road not in self.knowledge_base['self_graph'][self.cur_pos]:
            self.knowledge_base['self_graph'][self.cur_pos].append(road)

        if road not in self.knowledge_base['self_graph']:
            self.knowledge_base['self_graph'][road] = possible

    def tell_knowledge_base_visited(self, visited):
        self.knowledge_base['visited'].add(visited)
    
    def ask_next_move(self):
        roads = self.knowledge_base['self_graph'][self.cur_pos]
        for road in roads:
            if road == self.goal:
                return road
            if road in self.knowledge_base['visited']:
                continue
            next_roads = self.knowledge_base['self_graph'][road]
            if len(next_roads) == 0:
                continue
            for next_road in next_roads:
                if next_road in self.knowledge_base['visited']:
                    continue
                return road
        return None
            
    def read_sign(self, road):
        neigbours = self.graph.get(road, [])
        return neigbours

    def move_to_goal(self):
        while self.cur_pos != self.goal:
            self.tell_knowledge_base_visited(self.cur_pos)
            print(self.cur_pos)
            self.stack.append(self.cur_pos)
            roads = self.graph.get(self.cur_pos, [])

            for road in roads:
                # print(self.cur_pos)
                road_sign = self.read_sign(road)
                self.tell_knowledge_base_roads(road, road_sign)
            
            next_vertex = self.ask_next_move()
            if (next_vertex == None and len(self.stack) == 0):
                print('Unable to find path to goal')
                return [self.path, self.full_path]
            elif (next_vertex == None):
                self.stack.pop()
                next_vertex = self.stack.pop()
            self.path.append(next_vertex)
            self.cur_pos = next_vertex
        
        return [self.path, self.full_path]
        
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

def draw_visited_vertices(vertices: list):
    for [x, y] in vertices:
        plt.scatter(x, y, color="orange", s=150, edgecolors="black", zorder=3)


def draw_path(graph: dict, rowSize: int, colSize: int, path: list, title: str, color: str):
    visited_vertices = []
    for [x, y] in path:
        plt.figure(figsize=(colSize, rowSize))
        draw_edges(graph)
        draw_vertices(graph)
        draw_visited_vertices(visited_vertices)
        plt.scatter(x, y, color=color, s=150, edgecolors="black", zorder=3)
        plt.axis("equal")
        plt.gca().invert_yaxis()
        plt.axis("off")
        plt.title(title)
        plt.show()
        visited_vertices.append((x, y))
        
# Wrapper
def setup_lab(rowCount: int = 5, colCount: int = 5, edgeToDelCount: int = 5):
    graph = generate_grid_graph(rowCount, colCount)
    print(graph)
    draw_graph(graph, rowCount, colCount)
    graph = remove_random_edges(graph, edgeToDelCount, rowCount, colCount)
    draw_graph(graph, rowCount, colCount)

    agent = Agent(graph, (0, 0), (3, 4))
    [path, full_path] = agent.move_to_goal()
    print('path = ', path)
    # draw_path(graph, rowCount, colCount, full_path, 'Full path', 'yellow')
    draw_path(graph, rowCount, colCount, path, 'Path', 'green')

setup_lab(5, 5, 10)