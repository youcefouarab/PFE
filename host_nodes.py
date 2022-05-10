
from collections import deque
import yaml

from common.consts import *
from common.utils import check_condition
from common.graph import graph

class host_nodes :

    def __init__(self, template_path):
        self.nodes = []
        self.properties = [] 
        self.capabilities = []
        self.links = []
        self.warnings = []
        self.error = None
        with open(template_path) as f:
            dict = yaml.load(f, Loader=yaml.FullLoader)
            try :
                l = list(dict['topology_template']['node_templates'])
                warn_6 = warn_5 = False
                for i in range(len(l)) :
                    node = dict['topology_template']['node_templates'][l[i]]
                    if node['type'] == 'NetworkNode' :
                        self.nodes.append(l[i])
                        self.properties.append({})
                        self.capabilities.append({})
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
                if warn_5 : self.warnings.append(WARN_5)
                if warn_6 : self.warnings.append(WARN_6)
            except : 
                self.error = ERR_15
                return
            self.graph = graph(len(self.nodes))
            try :
                warn_7 = False
                for i in range(len(l)) :
                    node = dict['topology_template']['node_templates'][l[i]]
                    if node['type'] == 'Link' :
                        node_1 = node_2 = None
                        try : node_1 = node['requirements'][0]['link']
                        except : pass
                        try : node_2 = node['requirements'][1]['link']
                        except : pass
                        c = {}
                        try : 
                            for cap in list(node['capabilities']) : c = {**c, **node['capabilities'][cap]['properties']}
                        except : warn_7 = True
                        self.graph.add_edge(self.nodes.index(node_1), self.nodes.index(node_2), c)
                if warn_7 : self.warnings.append(WARN_7)
            except : 
                self.error = ERR_15
                return
            

    def select_host(self, src, host_requirements, network_requirements):
        s = src
        visited = [False] * (max(self.graph.graph) + 1)
        queue = deque()
        queue.append(s)
        visited[s] = True 
        while queue:
            s = queue.popleft()
            if s != src and len(self.capabilities[s]) > 0 and self.check_host_requirements(host_requirements, self.capabilities[s]):
                path = self.graph.find_path(src, s, network_requirements)
                if path != None :
                    return s, path
            for i in self.graph.graph[s]:
                if visited[i] == False:
                    queue.append(i)
                    visited[i] = True
        return None, None
    

    def check_host_requirements(self, requirements, capabilities):
        for req in list(requirements) :
            if req in capabilities :
                if not check_condition(requirements[req], capabilities[req]) : return False
            else :
                return False
        return True
