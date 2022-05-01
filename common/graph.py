
from collections import defaultdict, deque
import math

from common.utils import check_condition, read_scalar_unit

class graph:

    def __init__(self, num_of_vertices):
        self.graph = defaultdict(list)
        self.weights = [[None for i in range(num_of_vertices)] for j in range(num_of_vertices)]

    def add_edge(self, u, v, c):
        self.graph[u].append(v)
        self.graph[v].append(u)
        self.weights[u][v] = c
        self.weights[v][u] = c
        
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
                paths.append({'path':path,'weight':self.path_weight(path)})
            for i in range(len(self.graph[last])):
                if self.graph[last][i] not in path:
                    newpath = path.copy()
                    newpath.append(self.graph[last][i])
                    q.append(newpath)
        return paths

    def find_path(self, src, dst, req):
        q = deque()
        path = []
        path.append(src)
        q.append(path.copy())
        while q:
            path = q.popleft()
            last = path[len(path) - 1]
            if last == dst:
                p = {'path':path,'weight':self.path_weight(path)}
                if self.check_network_requirements(req, p):
                    return p
            for i in range(len(self.graph[last])):
                if self.graph[last][i] not in path:
                    newpath = path.copy()
                    newpath.append(self.graph[last][i])
                    q.append(newpath)
        return None

    def check_network_requirements(self, requirements, path):
        for req in list(requirements) :
            if req in path['weight'] :
                if not check_condition(requirements[req], path['weight'][req]) : return False
            else :
                return False
        return True

    def path_weight(self, path) :
        src = path[0]
        latency = 0
        loss_rate = error_rate = 0
        bandwidth = jitter = math.inf
        # WE COULD ALSO CHECK SERIAL AVAILABILITY HERE !!!
        for i in range(1, len(path)) :
            dst = path[i]
            if 'bandwidth' in self.weights[src][dst] : 
                bandwidth = min(bandwidth, read_scalar_unit(self.weights[src][dst]['bandwidth'], 'bps'))
            if 'latency' in self.weights[src][dst] : 
                latency += read_scalar_unit(self.weights[src][dst]['latency'], 'ms')
            if 'jitter' in self.weights[src][dst] : 
                pass
            if 'loss_rate' in self.weights[src][dst] : 
                pass
            if 'error_rate' in self.weights[src][dst] : 
                pass
            src = dst
        return {'latency':str(latency)+' ms'}


"""
g = graph(5)
g.add_edge(0, 1, { 'latency' : '11 ms' })
g.add_edge(0, 3, { 'latency' : '12 ms' })
g.add_edge(1, 4, { 'latency' : '13 ms' })
g.add_edge(2, 4, { 'latency' : '14 ms' })
g.add_edge(3, 4, { 'latency' : '15 ms' })

# {0: [1, 3], 1: [0, 4], 3: [0, 4], 4: [1, 2, 3], 2: [4]}

nodes = ['host_1', 'host_2', 'host_3', 'router_a', 'router_b']

print(g.path_weight([0, 1, 4, 2]))
"""