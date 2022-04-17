
from collections import deque
from pkg_resources import require
import yaml

from common.consts import *
from common.utils import check_condition
from graph import graph

class host_nodes :

    def __init__(self, template_path):
        self.nodes = [] ; self.properties = [] ; self.capabilities = []
        self.links = [] 
        self.graph = graph()
        with open(template_path) as f:
            dict = yaml.load(f, Loader=yaml.FullLoader)
            try :
                l = list(dict['topology_template']['node_templates'])
                warn_6 = warn_5 = False
                for i in range(len(l)) :
                    node = dict['topology_template']['node_templates'][l[i]]
                    if node['type'] == 'HostNode' :   
                        self.nodes.append(l[i])
                        p = {}
                        try : p = node['properties']
                        except : warn_5 = True
                        finally: self.properties.append(p)
                        c = {}
                        try : 
                            for cap in list(node['capabilities']) : c = {**c, **node['capabilities'][cap]['properties']}
                        except : warn_6 = True
                        finally: self.capabilities.append(c) 
                    if node['type'] == 'NetworkNode' :
                        self.nodes.append(l[i])
                        self.properties.append({})
                        self.capabilities.append({})
                if warn_5 : print(WARN_5)
                if warn_6 : print(WARN_6)
            except: print(ERR_15)

            try :
                for i in range(len(l)) :
                    node = dict['topology_template']['node_templates'][l[i]]
                    if node['type'] == 'Link' :
                        self.links.append(l[i])
                        node_1 = node['requirements'][0][list(node['requirements'][0])[0]]
                        node_2 = node['requirements'][1][list(node['requirements'][1])[0]]
                        self.graph.add_edge(self.nodes.index(node_1), self.nodes.index(node_2))
            except: print(ERR_15)
    
    def select_host_bfs(self, src, requirements):
        s = src
        visited = [False] * (max(self.graph.graph) + 1)
        queue = deque()
        queue.append(s)
        visited[s] = True 
        while queue:
            s = queue.popleft()
            if s != src and len(self.capabilities[s]) > 0 and self.check_host_requirements(requirements, self.capabilities[s]):
                print("Node ", s, " is a possible host")
                """
                paths = self.graph.find_paths(src, s)
                for path in paths :
                    if self.check_network_requirements():
                        print("Node ", s, " is a possible host")
                        return s
                """
            for i in self.graph.graph[s]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
    
    def check_host_requirements(self, requirements, capabilities):
        for req in list(requirements) :
            if req in capabilities :
                if not check_condition(requirements[req], capabilities[req]) : return False
            else :
                return False
        return True

    def check_network_requirements(self, requirements, path):
        check = False
        # TODO check link requirements
        return check


nodes = host_nodes('tosca/test_nodes.yaml')

host_requirements = {
    'mem_size' : { 'in_range' : [ '6 GB', '8 GB' ] },
    'availability' : { 'greater_or_equal' : 0.80 }
}

nodes.select_host_bfs(0, host_requirements)

host_requirements = {
    'mem_size' : { 'in_range' : [ '4 GB', '8 GB' ] },
    'availability' : { 'greater_or_equal' : 0.80 },
    'num_cpus' : { 'in_range' : [ 4, 8 ] }
}

nodes.select_host_bfs(0, host_requirements)