
from common.utils import read_scalar_unit
from host_nodes import host_nodes
from network_application import network_application

TEMPLATE_PATH = 'tosca/test_app.yaml'
#net_app = network_application(TEMPLATE_PATH)

#print(net_app.app_properties)
#print(net_app.app_requirements)
#print(net_app.host_properties)
#print(net_app.host_requirements)
#print(net_app.network_requirements)

#net_app.translate_response_time()
#print(read_scalar_unit(str(net_app.requirements['latency']) + 's', 'ms'))
#print(read_scalar_unit(str(net_app.requirements['bandwidth']) + 'Bps', 'MBps'))


nodes = host_nodes('tosca/test_nodes.yaml')
print(nodes.nodes)
#print(nodes.properties)
#print(nodes.capabilities)

print(nodes.graph.graph)
print(nodes.graph.weights)