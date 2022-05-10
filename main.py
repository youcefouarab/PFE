
import argparse, subprocess

from common.consts import APP_PARSE_ERR, DONE, ERR, ERR_16, ERR_17, PUCCINI_TOSCA, WARN
from network_application import network_application
from host_nodes import host_nodes

parser = argparse.ArgumentParser()

parser.add_argument('--app_template', help='YAML file containing TOSCA template describing application requirements')
parser.add_argument('--node_template', help='YAML file containing TOSCA template describing nodes and links')

args = parser.parse_args()

if args.app_template != None : 
    APP_TEMPLATE = args.app_template
else :
    # print(ERR_16)
    APP_TEMPLATE = "tosca/test_app.yaml"

if args.node_template != None : 
    NODE_TEMPLATE = args.node_template
else :
    # print(ERR_17)
    NODE_TEMPLATE = "tosca/test_nodes.yaml"

print("\nValidating your application template...", end="\t")

proc = subprocess.run(
    [PUCCINI_TOSCA, "parse", APP_TEMPLATE],
    stdout=subprocess.DEVNULL, 
    stderr=subprocess.STDOUT
)

if proc.returncode != 0 :
    print()
    subprocess.run([PUCCINI_TOSCA, "parse", APP_TEMPLATE])
    exit(proc.returncode)

print(DONE)

print("Validating your nodes template...", end="\t")

proc = subprocess.run([PUCCINI_TOSCA, "parse", NODE_TEMPLATE],
    stdout=subprocess.DEVNULL, 
    stderr=subprocess.STDOUT
)

if proc.returncode != 0 : 
    print()
    subprocess.run([PUCCINI_TOSCA, "parse", NODE_TEMPLATE])
    exit(proc.returncode)

print(DONE)

print("Parsing application requirements...", end="\t")

net_app = network_application(APP_TEMPLATE)

if net_app.error != None :
    print("\n" + ERR + net_app.error)
    exit()

print(DONE)

for i in range(len(net_app.warnings)) : 
    warn = net_app.warnings.pop(i)
    print(WARN + warn)

print("Parsing node characteristics...", end="\t\t")

nodes = host_nodes(NODE_TEMPLATE)

if nodes.error != None :
    print("\n" + ERR + nodes.error)
    exit()

print(DONE)

for i in range(len(nodes.warnings)) : 
    warn = nodes.warnings.pop(i)
    print(WARN + warn)

print("\nReady to translate requirements? (Y/N):", end=" ")
cont = input()
if cont.upper() != 'Y':
    exit()
print()

if 'response_time' in net_app.app_requirements :
    print("Translating response time...", end="\t\t")

    net_app.translate_response_time()

    if net_app.error != None : 
        print("\n" + ERR + net_app.error)
        exit()
    
    print(DONE)

if 'compute_time' in net_app.app_requirements :
    print("Translating compute time...", end="\t\t")

    net_app.translate_compute_time()

    if net_app.error != None : 
        print("\n" + ERR + net_app.error)
        exit()
    
    print(DONE)

if 'requests_per_second' in net_app.app_requirements :
    print("Translating requests per second...", end="\t")

    net_app.translate_requests_per_second()

    if net_app.error != None : 
        print("\n" + ERR + net_app.error)
        exit()
    
    print(DONE)

if 'concurrent_users' in net_app.app_requirements:
    print("Translating concurrent users...", end="\t\t")

    net_app.translate_concurrent_users()

    if net_app.error != None : 
        print("\n" + ERR + net_app.error)
        exit()
    
    print(DONE)

if 'reliability' in net_app.app_requirements:
    print("Translating reliability...", end="\t\t")

    net_app.translate_reliability()

    if net_app.error != None : 
        print("\n" + ERR + net_app.error)
        exit()
    
    print(DONE)

if 'hardware' in net_app.app_requirements:
    print("Translating hardware...", end="\t\t\t")

    net_app.translate_hardware()

    if net_app.error != None : 
        print("\n" + ERR + net_app.error)
        exit()
    
    print(DONE)

print("\nPrint generated host profile? (Y/N):", end=" ")
cont = input()
if cont.upper() == 'Y':
    def print_req(requirements) :
        for req in list(requirements) :
            print("\033[0;36;40m" + req + "\033[0;37;40m\t", end="")
            if len(req) < 8 : print("\t", end="")
            cond = list(requirements[req])[0] 
            cond_sym = ''
            if cond == 'equal' : cond_sym = '= '
            if cond == 'greater_or_equal' : cond_sym = '>='
            if cond == 'greater_than' : cond_sym = '> '
            if cond == 'less_or_equal' : cond_sym = '<='
            if cond == 'less_than' : cond_sym = '< '
            if cond == 'in_range' : cond_sym = 'in'
            print(cond_sym, "\033[0;32;40m", requirements[req][cond], "\033[0;37;40m")

    print("\n\033[0;33;40mYour application's host should have the following characteristics:\033[0;37;40m")
    print_req(net_app.host_requirements)
    print_req(net_app.network_requirements)

print("\nReady to select a host? (Y/N):", end=" ")
cont = input()
if cont.upper() != 'Y':
    exit()

src = None
while src == None :
    print("\nSelect a source node:\033[0;33;40m", end=" ")
    src = input()
    if src in nodes.nodes :
        src = nodes.nodes.index(src)

node, path = nodes.select_host(src, net_app.host_requirements, net_app.network_requirements)

if node != None and path != None :
    print("\n\033[0;32;40m" + nodes.nodes[node], "\033[0;37;40mis a suitable host through path:\033[0;32;40m", end=' ')
    print("\033[0;33;40m" + nodes.nodes[src], end=' \033[0;37;40m')
    for i in path['path'] :
        if (i != src) : 
            if (i == node) : print('->\033[0;32;40m', nodes.nodes[i], end=' ')
            else : print('->', nodes.nodes[i], end=' ')
else :
    print("\033[0;31;40mNo suitable host was found.")

print("\033[0;37;40m\n")
