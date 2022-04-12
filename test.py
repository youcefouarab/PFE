
from common.utils import read_scalar_unit
from network_application import network_application

TEMPLATE_PATH = 'tosca/test.yaml'
net_app = network_application(TEMPLATE_PATH)

net_app.translate_response_time()
print(read_scalar_unit(str(net_app.requirements['latency']) + 's', 'ms'))
print(read_scalar_unit(str(net_app.requirements['bandwidth']) + 'Bps', 'MBps'))
