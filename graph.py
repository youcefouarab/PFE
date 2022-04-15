
from collections import defaultdict

class graph:

    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def select_host_bfs(self, s):
        visited = [False] * (max(self.graph) + 1)
        queue = []
        queue.append(s)
        visited[s] = True 
        while queue:
            s = queue.pop(0)
            if s != 0 and self.check_host_requirements():
                if self.check_link_requirements():
                    print("Node ", s, " is a possible host")
                    return s
            for i in self.graph[s]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
    
    def check_host_requirements(self):
        check = False
        # TODO check host requirements
        return check

    def check_link_requirements(self):
        check = False
        # TODO check link requirements
        return check