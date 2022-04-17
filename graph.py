
from collections import defaultdict, deque

class graph:

    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def bfs_explore(self, s, nodes):
        visited = [False] * (max(self.graph) + 1)
        queue = []
        queue.append(s)
        visited[s] = True 
        while queue:
            s = queue.pop(0)
            print (nodes[s], end = " ")
            for i in self.graph[s]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True

    def print_path(self, path):
        size = len(path)
        for i in range(size):
            print(path[i], end = " ")
        print()
        
    def find_paths(self, src, dst):
        q = deque()
        paths = []
        path = []
        path.append(src)
        q.append(path.copy())
        while q:
            path = q.popleft()
            last = path[len(path) - 1]
            if last == dst:
                self.print_path(path)
                paths.append(path)
            for i in range(len(self.graph[last])):
                if self.graph[last][i] not in path:
                    newpath = path.copy()
                    newpath.append(self.graph[last][i])
                    q.append(newpath)
        return paths

    