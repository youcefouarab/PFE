
import yaml

from common.consts import *
from graph import graph

class host_nodes :

    def __init__(self, template_path):
        self.names = [] ; self.properties = [] ; self.capabilities = []
        self.graph = graph()
        with open(template_path) as f:
            dict = yaml.load(f, Loader=yaml.FullLoader)
            try :
                l = list(dict['topology_template']['node_templates'])
                warn_6 = warn_5 = False
                for i in range(len(l)) :
                    node = dict['topology_template']['node_templates'][l[i]]
                    if node['type'] == 'HostNode' :   
                        self.names.append(l[i])
                        p = {}
                        try : p = node['properties']
                        except : warn_5 = True
                        finally: self.properties.append(p)
                        c = {}
                        try : 
                            for cap in list(node['capabilities']) : c = {**c, **node['capabilities'][cap]['properties']}
                        except : warn_6 = True
                        finally: self.capabilities.append(c) 
                if warn_5 : print(WARN_5)
                if warn_6 : print(WARN_6)
            except: print(ERR_15)
            # TODO extract links and their capabilities and generate graph
