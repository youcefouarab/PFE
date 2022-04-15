from collections import defaultdict
from collections import deque

class graph:
    def min_distance(self,dist,queue):
        minimum = float("Inf")
        min_index = -1
        for i in range(len(dist)):
            if dist[i] < minimum and i in queue:
                minimum = dist[i]
                min_index = i
        return min_index
    def get_path(self, parent, j, path = []):
        if parent[j] == -1 :
            path.append(j)
            return
        self.get_path(parent , parent[j], path)
        path.append(j)
        return path
    def dijkstra(self, graph, src):
        row = len(graph)
        col = len(graph[0])
        dist = [float("Inf")] * row
        parent = [-1] * row
        dist[src] = 0
        queue = []
        for i in range(row):
            queue.append(i)
        while queue:
            u = self.min_distance(dist,queue)  
            queue.remove(u)
            for i in range(col):
                if graph[u][i] and i in queue:
                    if dist[u] + graph[u][i] < dist[i]:
                        dist[i] = dist[u] + graph[u][i]
                        parent[i] = u
        return dist, parent

class DFS: 
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)
    def print_all_paths_util(self, u, d, visited, path):
        visited[u]= True
        path.append(u)
        if u == d:
            print (path)
        else:
            for i in self.graph[u]:
                if visited[i]== False:
                    self.print_all_paths_util(i, d, visited, path)
        path.pop()
        visited[u]= False
    def print_all_paths(self, s, d):
        visited =[False]*(self.V)
        path = []
        self.print_all_paths_util(s, d, visited, path)

class BFS:
    def __init__(self, vertices):
        self.V = vertices
        self.graph = defaultdict(list)
    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)
    def bfs_explore(self, s):
        visited = [False] * (max(self.graph) + 1)
        queue = []
        queue.append(s)
        visited[s] = True 
        while queue:
            s = queue.pop(0)
            print (s, end = " ")
            for i in self.graph[s]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
    def print_path(self, path):
        size = len(path)
        for i in range(size):
            print(path[i], end = " ")
        print()
    def find_paths(self, src: int, dst: int) -> None:
        q = deque()
        path = []
        path.append(src)
        q.append(path.copy())
        while q:
            path = q.popleft()
            last = path[len(path) - 1]
            if last == dst:
                self.print_path(path)
            for i in range(len(self.graph[last])):
                if self.graph[last][i] not in path:
                    newpath = path.copy()
                    newpath.append(self.graph[last][i])
                    q.append(newpath)


"""
g = graph()
 
my_graph = [
    [ 0, 14, 25, 15,  3,  0,  0,  0],
    [14,  0, 15,  0, 10,  0, 20, 10],
    [25, 15,  0,  4,  0, 15, 25, 30],
    [15,  0,  4,  0, 10,  0,  0,  0],
    [ 3, 10,  0, 10,  0,  0,  0,  0],
    [ 0,  0, 15,  0,  0,  0,  0,  0],
    [ 0, 20, 25,  0,  0,  0,  0,  5],
    [ 0, 10, 30,  0,  0,  0,  5,  0],
]

source = 0
 
dist, parent = g.dijkstra(my_graph, source)
print(dist)

sat = [i for i in range(len(dist)) if dist[i] < 20]
print(sat)

g = DFS(4)
g.add_edge(0, 1)
g.add_edge(0, 2)
g.add_edge(0, 3)
g.add_edge(2, 1)
g.add_edge(1, 3)
  
s = 2 ; d = 3
print ("Following are all different paths from % d to % d :" %(s, d))
g.print_all_paths(s, d)
"""