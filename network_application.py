
import yaml
from common.consts import *
from common.utils import next_power_of_2, read_scalar_unit
from mapping.cos_mapping import cos_mapping
from mapping.reliability_mapping import reliability_mapping
from mapping.hardware_mapping import hardware_mapping

class network_application :

    def __init__(self, template_path):
        self.app = self.properties = self.requirements = {}
        with open(template_path) as f:
            dict = yaml.load(f, Loader=yaml.FullLoader)
            try :
                self.app = dict['topology_template']['node_templates'][list(dict['topology_template']['node_templates'])[0]]
                if (self.app['type'] != 'NetworkApplication') :
                    print(ERR_2)
                    return
            except :
                print(ERR_3)
                return
            try :
                self.properties = self.app['properties']
            except : print(WARN_1)
            warn_2 = False
            try :
                for req in self.app['requirements'] :
                    try :
                        for cap in req[list(req)[0]]['node_filter']['capabilities'] :
                            try :
                                for prop in cap[list(cap)[0]]['properties'] :
                                    try :
                                        self.requirements = {**self.requirements, **prop}
                                    except : warn_2 = True
                            except : warn_2 = True
                    except : warn_2 = True
                    try :
                        for prop in req[list(req)[0]]['node_filter']['properties'] :
                            try :
                                self.requirements = {**self.requirements, **prop}
                            except : warn_2 = True
                    except : warn_2 = True
            except : warn_2 = True
            if warn_2 : print(WARN_2)

    def translate_response_time(self) :
        rt = ct = sa = su = la = lu = t = cos = None
        if 'cos' in self.properties : cos = self.properties['cos']
        if 'compute_time' in self.requirements : ct = read_scalar_unit(self.requirements['compute_time'][list(self.requirements['compute_time'])[0]], 's')
        else :
            print(ERR_1)
            return
        if 'response_time' in self.requirements : rt = read_scalar_unit(self.requirements['response_time'][list(self.requirements['response_time'])[0]], 's')
        else :
            if cos != None and cos_mapping[cos]['response_time'] != None : rt = read_scalar_unit(cos_mapping[cos]['response_time'], 's')
            else :
                print(ERR_1)
                return  
        if ct >= rt : 
            print(ERR_9)
            return
        if 'latency' in self.requirements : 
            la = lu = read_scalar_unit(self.requirements['latency'][list(self.requirements['latency'])[0]], 's') / 2
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
        if 'request_size' in self.properties : sa = read_scalar_unit(self.properties['request_size'], 'B')
        if 'response_size' in self.properties : su = read_scalar_unit(self.properties['response_size'], 'B')
        if 'bandwidth' in self.requirements : t = read_scalar_unit(self.requirements['bandwidth'][list(self.requirements['bandwidth'])[0]], 'Bps') 
        if 'ccu' in self.requirements : ccu = self.requirements['concurrent_users'][list(self.requirements['concurrent_users'])[0]]
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
        self.requirements['latency'] = la + lu
        self.requirements['bandwidth'] = t
        if la == NEGLIGIBLE : print(WARN_3)
        if t == NEGLIGIBLE : print(WARN_4)
    
    def translate_requests_per_second(self) :
        rps = worker_mem = task_time = req_type = ram = cpus = None
        if 'compute_time' in self.requirements and 'requests_per_second' in self.requirements :
            task_time = read_scalar_unit(self.requirements['compute_time'][list(self.requirements['compute_time'])[0]], 's')
            rps = self.requirements['requests_per_second']
            if 'request_type' in self.properties : req_type = self.properties['request_type']
            else :
                if 'cos' in self.properties:
                    if self.properties['cos'] == 'cpu_bound' : req_type = 'CPU_BOUND'
                    else : req_type = 'MEM_BOUND'
                else :
                    print(ERR_11)
                    return
        else :
            print(ERR_11)
            return           
        if req_type == 'MEM_BOUND' :    
            if 'worker_mem' in self.properties :
                worker_mem = read_scalar_unit(self.properties['worker_mem'], 'MB')
                ram = rps * worker_mem * task_time
                if 'mem_size' not in self.requirements or ('mem_size' in self.requirements and ram > read_scalar_unit(self.requirements['mem_size'][list(self.requirements['mem_size'])[0]], 'MB') ) : self.requirements['mem_size'] = ram
            else :
                print(ERR_11)
                return
        else :
            cpus = next_power_of_2(rps * task_time)
            if 'num_cpus' not in self.requirements or ('num_cpus' in self.requirements and cpus > self.requirements['num_cpus'][list(self.requirements['num_cpus'])[0]]) : self.requirements['num_cpus'] = cpus
        
    def translate_concurrent_users(self) :
        ccu = response_time = click_freq = None
        if 'response_time' in self.requirements and 'concurrent_users' in self.requirements and 'click_frequency' in self.properties :
            response_time = read_scalar_unit(self.requirements['response_time'][list(self.requirements['response_time'])[0]], 's')
            click_freq = read_scalar_unit(self.properties['click_frequency'], 's')
            ccu = self.requirements['concurrent_users'][list(self.requirements['concurrent_users'])[0]]
        else :
            print(ERR_12)
            return
        cpus = next_power_of_2((ccu * response_time) / (60 * click_freq))
        if 'num_cpus' not in self.requirements or ('num_cpus' in self.requirements and cpus > self.requirements['num_cpus'][list(self.requirements['num_cpus'])[0]]) : self.requirements['num_cpus'] = cpus

    def translate_reliability(self):
        loss = error = None
        if 'reliability' in self.requirements :
            if 'loss_rate' not in self.requirements : loss = reliability_mapping[self.requirements['reliability']]['loss_rate']
            if 'error_rate' not in self.requirements : error = reliability_mapping[self.requirements['reliability']]['error_rate']
        else :
            if 'loss_rate' in self.requirements :
                if 'error_rate' not in self.requirements :
                    # trouver niveau
                    niv = ''
                    error = reliability_mapping[niv]['error_rate']
            else :
                if 'error_rate' in self.requirements :
                    niv = ''
                    loss = reliability_mapping[niv]['loss_rate']
                else :
                    if 'cos' in self.properties :
                        loss = cos_mapping[self.properties['cos']]['loss_rate']
                        error = cos_mapping[self.properties['cos']]['error_rate']
                    else :
                        print(ERR_4)
                        return
        self.requirements['loss_rate'] = loss
        self.requirements['error_rate'] = error
    
    def translate_hardware(self):
        cpus = ram = None
        if 'hardware' in self.requirements :
            if 'num_cpus' not in self.requirements : cpus = hardware_mapping[self.requirements['hardware']]['num_cpus']
            if 'mem_size' not in self.requirements : ram = hardware_mapping[self.requirements['hardware']]['mem_size']
        else :
            if 'num_cpus' in self.requirements :
                if 'mem_size' not in self.requirements :
                    # trouver niveau
                    niv = ''
                    ram = hardware_mapping[niv]['mem_size']
            else :
                if 'mem_size' in self.requirements :
                    niv = ''
                    cpus = hardware_mapping[niv]['num_cpus']
                else :
                    print(ERR_4)
                    return
        self.requirements['num_cpus'] = cpus
        self.requirements['mem_size'] = ram

    def translate_compute_time(self) :
        ct = inst = mips = None
        if 'compute_time' in self.requirements and 'instructs_per_request' in self.properties :
            ct = read_scalar_unit(self.requirements['compute_time'][list(self.requirements['compute_time'])[0]], 's')
            inst = self.properties['instructs_per_request'] / 1000000
            mips = inst / ct
            if 'mips' not in self.requirements or ('mips' in self.requirements and mips > self.requirements['mips'][list(self.requirements['mips'])[0]]) : self.requirements['mips'] = mips
        else :
            print(ERR_13)
            return
