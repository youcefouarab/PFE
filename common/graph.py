
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
        jitter = latency = 0
        loss_rate = error_rate = 1
        bandwidth = math.inf
        for i in range(1, len(path)) :
            dst = path[i]
            if 'bandwidth' in self.weights[src][dst] : 
                bandwidth = min(bandwidth, read_scalar_unit(self.weights[src][dst]['bandwidth'], 'Mbps'))
            if 'latency' in self.weights[src][dst] : 
                latency += read_scalar_unit(self.weights[src][dst]['latency'], 'ms')
            if 'jitter' in self.weights[src][dst] : 
                jitter = max(jitter, read_scalar_unit(self.weights[src][dst]['jitter'], 'ms'))
            if 'loss_rate' in self.weights[src][dst] : 
                loss_rate *= (1 - self.weights[src][dst]['loss_rate'])
            if 'error_rate' in self.weights[src][dst] : 
                error_rate *= (1 - self.weights[src][dst]['error_rate'])
            src = dst
        return {
            'bandwidth' : str(bandwidth) + ' Mbps', 
            'latency' : str(latency) + ' ms', 
            'jitter' : str(jitter) + 'ms',
            'loss_rate' : 1 - loss_rate,
            'error_rate' : 1 - error_rate
        }
