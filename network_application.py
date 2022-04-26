
import yaml
from common.consts import *
from common.utils import next_power_of_2, read_scalar_unit
from mapping.cos_mapping import cos_mapping
from mapping.reliability_mapping import reliability_mapping
from mapping.hardware_mapping import hardware_mapping

class network_application :

    def __init__(self, template_path):
        self.app_properties = {} 
        self.app_requirements = {} 
        self.host_properties = {}
        self.host_requirements = {} 
        self.network_requirements = {}
        self.network_requirements = {}
        with open(template_path) as f:
            dict = yaml.load(f, Loader=yaml.FullLoader)
            try :
                app = dict['topology_template']['node_templates'][list(dict['topology_template']['node_templates'])[0]]
                if (app['type'] != 'NetworkApplication') :
                    print(ERR_2)
                    return
            except :
                print(ERR_3)
                return
            try :
                self.app_properties = app['properties']
            except : print(WARN_1)
            warn_2 = False
            try :
                for req in app['requirements'] :
                    r = list(req)[0]
                    try :
                        for prop in req[list(req)[0]]['node_filter']['properties'] :
                            try :
                                if r == 'application' : self.app_requirements = {**self.app_requirements, **prop}
                                if r == 'host' : self.host_properties = {**self.host_properties, **prop}
                                if r == 'network' : self.network_properties = {**self.network_properties, **prop}
                            except : warn_2 = True
                    except : warn_2 = True
                    try :
                        for cap in req[list(req)[0]]['node_filter']['capabilities'] :
                            try :
                                for prop in cap[list(cap)[0]]['properties'] :
                                    try :
                                        if r == 'application' : self.app_requirements = {**self.app_requirements, **prop}
                                        if r == 'host' : self.host_requirements = {**self.host_requirements, **prop}
                                        if r == 'network' : self.network_requirements = {**self.network_requirements, **prop}
                                    except : warn_2 = True
                            except : warn_2 = True
                    except : warn_2 = True 
            except : warn_2 = True
            if warn_2 : print(WARN_2)

    def translate_response_time(self) :
        rt = ct = sa = su = la = lu = t = cos = None
        if 'cos' in self.app_properties : cos = self.app_properties['cos']
        if 'compute_time' in self.app_requirements : ct = read_scalar_unit(self.app_requirements['compute_time'][list(self.app_requirements['compute_time'])[0]], 's')
        else :
            print(ERR_1)
            return
        if 'response_time' in self.app_requirements : rt = read_scalar_unit(self.app_requirements['response_time'][list(self.app_requirements['response_time'])[0]], 's')
        else :
            if cos != None and cos_mapping[cos]['response_time'] != None : rt = read_scalar_unit(cos_mapping[cos]['response_time'], 's')
            else :
                print(ERR_1)
                return  
        if ct >= rt : 
            print(ERR_9)
            return
        if 'latency' in self.network_requirements : 
            la = lu = read_scalar_unit(self.network_requirements['latency'][list(self.network_requirements['latency'])[0]], 's') / 2
            if la + lu >= rt : 
                print(ERR_8)
                return
            if la + lu + ct >= rt : 
                print(ERR_10)
                return
        else :
            if cos != None and cos_mapping[cos]['latency'] != None : 
                la = lu = read_scalar_unit(cos_mapping[cos]['latency'], 's') / 2
                if la + lu >= rt or la + lu + ct >= rt : la = lu = None
        if 'request_size' in self.app_properties : sa = read_scalar_unit(self.app_properties['request_size'], 'B')
        if 'response_size' in self.app_properties : su = read_scalar_unit(self.app_properties['response_size'], 'B')
        if 'bandwidth' in self.network_requirements : t = read_scalar_unit(self.network_requirements['bandwidth'][list(self.network_requirements['bandwidth'])[0]], 'Bps') 
        if 'ccu' in self.network_requirements : ccu = self.network_requirements['concurrent_users'][list(self.network_requirements['concurrent_users'])[0]]
        else : ccu = 1
        try :
            if la != None and lu != None :
                if t == None :
                    if sa != None and su != None : t = ((sa + su) / (rt - ct - (la + lu))) * ccu
                    else :
                        if cos != None and cos_mapping[cos]['bandwidth'] != None : t = read_scalar_unit(cos_mapping[cos]['bandwidth'], 'Bps') * ccu
                        else : t = NEGLIGIBLE
            else :
                if sa == None or su == None :
                    la = lu = (rt - ct) / 2
                    if t == None :
                        if cos != None and cos_mapping[cos]['bandwidth'] != None : t = read_scalar_unit(cos_mapping[cos]['bandwidth'], 'Bps') * ccu
                        else : t = NEGLIGIBLE
                else :
                    if t == None :
                        t = ((sa + su) / (rt - ct)) * ccu 
                        la = lu = NEGLIGIBLE  
                    else : la = lu = (rt - ct - ((sa + su) / (t / ccu))) / 2 # hmmm...
        except Exception as e: print(e)

        # TODO add condition

        self.network_requirements['latency'] = la + lu
        self.network_requirements['bandwidth'] = t
        if la == NEGLIGIBLE : print(WARN_3)
        if t == NEGLIGIBLE : print(WARN_4)
    
    def translate_requests_per_second(self) :
        rps = worker_mem = task_time = req_type = ram = cpus = None
        if 'compute_time' in self.app_requirements and 'requests_per_second' in self.app_requirements :
            task_time = read_scalar_unit(self.app_requirements['compute_time'][list(self.app_requirements['compute_time'])[0]], 's')
            rps = self.app_requirements['requests_per_second']
            if 'request_type' in self.app_properties : req_type = self.app_properties['request_type']
            else :
                if 'cos' in self.app_properties:
                    if self.app_properties['cos'] == 'cpu_bound' : req_type = 'CPU_BOUND'
                    else : req_type = 'MEM_BOUND'
                else :
                    print(ERR_11)
                    return
        else :
            print(ERR_11)
            return           
        if req_type == 'MEM_BOUND' :    
            if 'worker_mem' in self.app_properties :
                worker_mem = read_scalar_unit(self.app_properties['worker_mem'], 'MB')
                ram = rps * worker_mem * task_time
                if 'mem_size' not in self.host_requirements or ('mem_size' in self.host_requirements and ram > read_scalar_unit(self.host_requirements['mem_size'][list(self.host_requirements['mem_size'])[0]], 'MB') ) : self.host_requirements['mem_size'] = ram
            else :
                print(ERR_11)
                return
        else :
            cpus = next_power_of_2(rps * task_time)
            if 'num_cpus' not in self.host_requirements or ('num_cpus' in self.host_requirements and cpus > self.host_requirements['num_cpus'][list(self.host_requirements['num_cpus'])[0]]) : self.host_requirements['num_cpus'] = cpus
        
    def translate_concurrent_users(self) :
        ccu = response_time = click_freq = None
        if 'response_time' in self.app_requirements and 'concurrent_users' in self.app_requirements and 'click_frequency' in self.app_properties :
            response_time = read_scalar_unit(self.app_requirements['response_time'][list(self.app_requirements['response_time'])[0]], 's')
            click_freq = read_scalar_unit(self.app_properties['click_frequency'], 's')
            ccu = self.app_requirements['concurrent_users'][list(self.app_requirements['concurrent_users'])[0]]
        else :
            print(ERR_12)
            return
        cpus = next_power_of_2((ccu * response_time) / (60 * click_freq))
        if 'num_cpus' not in self.host_requirements or ('num_cpus' in self.host_requirements and cpus > self.host_requirements['num_cpus'][list(self.host_requirements['num_cpus'])[0]]) : self.host_requirements['num_cpus'] = cpus

    def translate_reliability(self):
        loss = error = None
        if 'reliability' in self.app_requirements :
            if 'loss_rate' not in self.network_requirements : loss = reliability_mapping[self.app_requirements['reliability']]['loss_rate']
            if 'error_rate' not in self.network_requirements : error = reliability_mapping[self.app_requirements['reliability']]['error_rate']
        else :
            if 'loss_rate' in self.network_requirements :
                if 'error_rate' not in self.network_requirements :
                    # trouver niveau
                    niv = ''
                    error = reliability_mapping[niv]['error_rate']
            else :
                if 'error_rate' in self.network_requirements :
                    # trouver niveau
                    niv = ''
                    loss = reliability_mapping[niv]['loss_rate']
                else :
                    if 'cos' in self.app_properties :
                        if 'loss_rate' in cos_mapping[self.app_properties['cos']] : loss = cos_mapping[self.app_properties['cos']]['loss_rate']
                        if 'error_rate' in cos_mapping[self.app_properties['cos']] : error = cos_mapping[self.app_properties['cos']]['error_rate']
                    else :
                        print(ERR_4)
                        return
        self.network_requirements['loss_rate'] = loss
        self.network_requirements['error_rate'] = error
    
    def translate_hardware(self):
        cpus = ram = None
        if 'hardware' in self.app_requirements :
            if 'num_cpus' not in self.host_requirements : cpus = hardware_mapping[self.app_requirements['hardware']]['num_cpus']
            if 'mem_size' not in self.host_requirements : ram = hardware_mapping[self.app_requirements['hardware']]['mem_size']
        else :
            if 'num_cpus' in self.host_requirements :
                if 'mem_size' not in self.host_requirements :
                    # trouver niveau
                    niv = ''
                    ram = hardware_mapping[niv]['mem_size']
            else :
                if 'mem_size' in self.host_requirements :
                    # trouver niveau
                    niv = ''
                    cpus = hardware_mapping[niv]['num_cpus']
                else :
                    print(ERR_4)
                    return
        self.host_requirements['num_cpus'] = cpus
        self.host_requirements['mem_size'] = ram

    def translate_compute_time(self) :
        ct = inst = mips = None
        if 'compute_time' in self.app_requirements and 'instructs_per_request' in self.app_properties :
            ct = read_scalar_unit(self.app_requirements['compute_time'][list(self.app_requirements['compute_time'])[0]], 's')
            inst = self.app_properties['instructs_per_request'] / 1000000
            mips = inst / ct
            if 'mips' not in self.host_requirements or ('mips' in self.host_requirements and mips > self.host_requirements['mips'][list(self.host_requirements['mips'])[0]]) : self.host_requirements['mips'] = mips
        else :
            print(ERR_13)
            return
