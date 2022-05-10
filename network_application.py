
import copy
import yaml
from common.consts import *
from common.utils import find_level, next_power_of_2, read_scalar_unit
from mapping.cos_mapping import cos_mapping
from mapping.reliability_mapping import reliability_mapping
from mapping.hardware_mapping import hardware_mapping

class network_application :

    def __init__(self, template_path):
        self.dict = {}
        self.app_properties = {} 
        self.app_requirements = {} 
        self.host_properties = {}
        self.host_requirements = {} 
        self.network_properties = {}
        self.network_requirements = {}
        self.error = None
        self.warnings = []
        with open(template_path) as f:
            self.dict = yaml.load(f, Loader=yaml.FullLoader)
            try :
                app = self.dict['topology_template']['node_templates'][list(self.dict['topology_template']['node_templates'])[0]]
                if (app['type'] != 'NetworkApplication') :
                    self.error = ERR_2
                    return
            except :
                self.error = ERR_3
                return
            try :
                self.app_properties = app['properties']
            except : self.warnings.append(WARN_1)
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
            if warn_2 : self.warnings.append(WARN_2)

    def translate_response_time(self) :
        rt = ct = sa = su = la = lu = t = cos = None ; ccu = rps = 1
        rt_cond = ct_cond = lat_cond = t_cond = ccu_cond = rps_cond = None
        if 'compute_time' in self.app_requirements : 
            ct_cond = list(self.app_requirements['compute_time'])[0]
            if ct_cond != 'in_range' :
                ct = read_scalar_unit(self.app_requirements['compute_time'][ct_cond], 's')
            else :
                ct = read_scalar_unit(self.app_requirements['compute_time'][ct_cond][1], 's')
        else :
            self.error = ERR_1
            return
        if 'cos' in self.app_properties : 
            cos = self.app_properties['cos']
        if 'response_time' in self.app_requirements : 
            rt_cond = list(self.app_requirements['response_time'])[0]
            if rt_cond != 'in_range' :
                rt = read_scalar_unit(self.app_requirements['response_time'][rt_cond], 's')
            else :
                rt = read_scalar_unit(self.app_requirements['response_time'][rt_cond][1], 's')
        else :
            if cos != None and cos_mapping[cos]['response_time'] != None : 
                rt = read_scalar_unit(cos_mapping[cos]['response_time'], 's')
            else :
                self.error = ERR_1
                return  
        if ct >= rt : 
            self.error = ERR_9
            return
        if 'latency' in self.network_requirements : 
            lat_cond = list(self.network_requirements['latency'])[0]
            if lat_cond != 'in_range' :
                la = lu = read_scalar_unit(self.network_requirements['latency'][lat_cond], 's') / 2
            else :
                la = lu = read_scalar_unit(self.network_requirements['latency'][lat_cond][1], 's') / 2
            if la + lu >= rt : 
                self.error = ERR_8
                return
            if la + lu + ct >= rt : 
                self.error = ERR_10
                return
        else :
            if cos != None and cos_mapping[cos]['latency'] != None : 
                la = lu = read_scalar_unit(cos_mapping[cos]['latency'], 's') / 2
                if la + lu >= rt or la + lu + ct >= rt : 
                    la = lu = None
        if 'request_size' in self.app_properties : 
            sa = read_scalar_unit(self.app_properties['request_size'], 'B')
        if 'response_size' in self.app_properties : 
            su = read_scalar_unit(self.app_properties['response_size'], 'B')
        if 'concurrent_users' in self.app_requirements : 
            ccu_cond = list(self.app_requirements['concurrent_users'])[0]
            if ccu_cond != 'in_range' :
                ccu = self.app_requirements['concurrent_users'][ccu_cond]
            else : 
                ccu = self.app_requirements['concurrent_users'][ccu_cond][0]
        if 'requests_per_second' in self.app_requirements : 
            rps_cond = list(self.app_requirements['requests_per_second'])[0]
            if rps_cond != 'in_range' :
                rps = self.app_requirements['requests_per_second'][rps_cond]
            else : 
                rps = self.app_requirements['requests_per_second'][rps_cond][0]
        if 'bandwidth' in self.network_requirements : 
            t_cond = list(self.network_requirements['bandwidth'])[0]
            if t_cond != 'in_range' :
                t = read_scalar_unit(self.network_requirements['bandwidth'][t_cond], 'Bps')
            else :
                t = read_scalar_unit(self.network_requirements['bandwidth'][t_cond][0], 'Bps')
        try :
            if la != None and lu != None :
                if t == None :
                    if sa != None and su != None : 
                        t = ((sa + su) / (rt - ct - (la + lu))) * ccu
                    else :
                        if cos != None and cos_mapping[cos]['bandwidth'] != None : 
                            t = read_scalar_unit(cos_mapping[cos]['bandwidth'], 'Bps') * ccu
                        else : 
                            t = NEGLIGIBLE
                            self.warnings.append(WARN_4)
            else :
                if sa == None or su == None :
                    la = lu = (rt - ct) / 2
                    if t == None :
                        if cos != None and cos_mapping[cos]['bandwidth'] != None : 
                            t = read_scalar_unit(cos_mapping[cos]['bandwidth'], 'Bps') * ccu
                        else : 
                            t = NEGLIGIBLE
                            self.warnings.append(WARN_4)
                else :
                    if t == None :
                        t = ((sa + su) / (rt - ct)) * ccu
                        la = lu = NEGLIGIBLE  
                        self.warnings.append(WARN_3)
                    else : 
                        la = lu = (rt - ct - ((sa + su) / (t / ccu))) / 2
        except Exception as e: 
            self.warnings.append(e)
        self.network_requirements['latency'] = { 'less_or_equal' : str(read_scalar_unit(str(la + lu) + ' s', 'ms')) + ' ms' }
        self.network_requirements['bandwidth'] = { 'greater_or_equal' : str(read_scalar_unit(str(t) + ' Bps', 'Mbps')) + ' Mbps' }


    def translate_compute_time(self) :
        ct = ct_cond = inst = mips = mips_cond = None
        if 'compute_time' in self.app_requirements and 'instructs_per_task' in self.app_properties :
            ct_cond = list(self.app_requirements['compute_time'])[0]
            if ct_cond != 'in_range':
                ct = read_scalar_unit(self.app_requirements['compute_time'][ct_cond], 's')
            else : 
                ct = read_scalar_unit(self.app_requirements['compute_time'][ct_cond][1], 's')
            inst = self.app_properties['instructs_per_task'] / 1000000
            mips = inst / ct
            if 'mips' in self.host_requirements : 
                mips_cond = list(self.host_requirements['mips'])[0]
                if mips_cond != 'in_range' :
                    if self.host_requirements['mips'][mips_cond] > mips :
                        mips = self.host_requirements['mips'][mips_cond]
                else :
                    if self.host_requirements['mips'][mips_cond][0] > mips :
                        mips = self.host_requirements['mips'][mips_cond][0]
            self.host_requirements['mips'] = { 'greater_or_equal' : mips }
        else :
            self.error = ERR_13
            return


    def translate_requests_per_second(self) :
        rps = worker_mem = task_time = req_type = ram = cpus = None
        rps_cond = tt_cond = ram_cond = cpus_cond = None
        if 'compute_time' in self.app_requirements and 'requests_per_second' in self.app_requirements :
            tt_cond = list(self.app_requirements['compute_time'])[0]
            if tt_cond != 'in_range' :
                task_time = read_scalar_unit(self.app_requirements['compute_time'][tt_cond], 's')
            else : 
                task_time = read_scalar_unit(self.app_requirements['compute_time'][tt_cond][1], 's')
            rps_cond = list(self.app_requirements['requests_per_second'])[0]
            if rps_cond != 'in_range' :
                rps = self.app_requirements['requests_per_second'][rps_cond]
            else :
                rps = self.app_requirements['requests_per_second'][rps_cond][0]
        else :
            self.error = ERR_11
            return
        if 'request_type' in self.app_properties : 
            req_type = self.app_properties['request_type']
        else :
            if 'cos' in self.app_properties:
                if self.app_properties['cos'] == 'cpu_bound' : 
                    req_type = 'CPU_BOUND'
                else : 
                    req_type = 'MEM_BOUND'
            else :
                self.error = ERR_11
                return           
        if req_type == 'MEM_BOUND' :    
            if 'worker_mem' in self.app_properties :
                worker_mem = read_scalar_unit(self.app_properties['worker_mem'], 'MB')
                ram = rps * worker_mem * task_time
                if 'mem_size' in self.host_requirements :
                    ram_cond = list(self.host_requirements['mem_size'])[0]
                    if ram_cond != 'in_range' :
                        ex_ram = read_scalar_unit(self.host_requirements['mem_size'][ram_cond], 'MB')
                        if  ex_ram > ram :  
                            ram = ex_ram
                    else :
                        ex_ram = read_scalar_unit(self.host_requirements['mem_size'][ram_cond][0], 'MB')
                        if  ex_ram > ram :  
                            ram = ex_ram
                self.host_requirements['mem_size'] = { 'greater_or_equal' : str(ram) + ' MB' }
            else :
                self.error = ERR_11
                return
        else :
            cpus = next_power_of_2(rps * task_time)
            if 'num_cpus' in self.host_requirements :
                cpus_cond = list(self.host_requirements['num_cpus'])[0]
                if cpus_cond != 'in_range' :
                    if self.host_requirements['num_cpus'][cpus_cond] > cpus : 
                        cpus = self.host_requirements['num_cpus'][cpus_cond]
                else : 
                    if self.host_requirements['num_cpus'][cpus_cond][0] > cpus : 
                        cpus = self.host_requirements['num_cpus'][cpus_cond][0]
            self.host_requirements['num_cpus'] = { 'greater_or_equal' : cpus }
        

    def translate_concurrent_users(self) :
        ccu = response_time = click_freq = cpus = None
        ccu_cond = rt_cond = cpus_cond = None
        if 'response_time' in self.app_requirements and 'concurrent_users' in self.app_requirements and 'click_frequency' in self.app_properties :
            rt_cond = list(self.app_requirements['response_time'])[0]
            if rt_cond != 'in_range' :
                response_time = read_scalar_unit(self.app_requirements['response_time'][rt_cond], 's')
            else :
                response_time = read_scalar_unit(self.app_requirements['response_time'][rt_cond][1], 's')
            ccu_cond = list(self.app_requirements['concurrent_users'])[0]
            if ccu_cond != 'in_range' :
                ccu = self.app_requirements['concurrent_users'][ccu_cond]
            else :
                ccu = self.app_requirements['concurrent_users'][ccu_cond][0]
            click_freq = read_scalar_unit(self.app_properties['click_frequency'], 's')
        else :
            self.error = ERR_12
            return
        cpus = next_power_of_2((ccu * response_time) / (60 * click_freq))
        if 'num_cpus' in self.host_requirements :
            cpus_cond = list(self.host_requirements['num_cpus'])[0]
            if cpus_cond != 'in_range' : 
                if self.host_requirements['num_cpus'][cpus_cond] > cpus : 
                    cpus = self.host_requirements['num_cpus'][cpus_cond]
            else :
                if self.host_requirements['num_cpus'][cpus_cond][0] > cpus : 
                    cpus = self.host_requirements['num_cpus'][cpus_cond][0]
        self.host_requirements['num_cpus'] = { 'greater_or_equal' : cpus }


    def translate_reliability(self):
        loss = error = None
        if 'loss_rate' in self.network_requirements :
            loss_cond = list(self.network_requirements['loss_rate'])[0]
            if loss_cond != 'in_range' :
                loss = self.network_requirements['loss_rate'][loss_cond]
            else:
                loss = self.network_requirements['loss_rate'][loss_cond][1]
        if 'error_rate' in self.network_requirements :
            error_cond = list(self.network_requirements['error_rate'])[0]
            if error_cond != 'in_range' :
                error = self.network_requirements['error_rate'][error_cond]
            else:
                error = self.network_requirements['error_rate'][error_cond][1]
        
        if 'reliability' in self.app_requirements :
            if 'equal' not in self.app_requirements['reliability']:
                self.error = ERR_18
                return
            
            loss_map = reliability_mapping[self.app_requirements['reliability']['equal']]['loss_rate']
            """
            loss_map_cond = list(loss_map)[0]
            if loss_map_cond != 'in_range' :
                loss_map = loss_map[loss_map_cond]
            else :
                loss_map = loss_map[loss_map_cond][1]
            """
            if 'loss_rate' not in self.network_requirements : 
                self.network_requirements['loss_rate'] = loss_map
            """
            else :
                if loss_map < loss :
                    self.network_requirements['loss_rate'] = loss_map
            """
            error_map = reliability_mapping[self.app_requirements['reliability']['equal']]['error_rate']
            """
            error_map_cond = list(error_map)[0]
            if error_map_cond != 'in_range' :
                error_map = error_map[error_map_cond]
            else :
                error_map = error_map[error_map_cond][1]
            """
            if 'error_rate' not in self.network_requirements : 
                self.network_requirements['error_rate'] = error_map
            """
            else :
                if error_map < error :
                    self.network_requirements['error_rate'] = error_map
            """
        else :
            if 'loss_rate' in self.network_requirements :
                if 'error_rate' not in self.network_requirements :
                    niv = find_level(reliability_mapping, 'loss_rate', loss)
                    self.network_requirements['error_rate'] = reliability_mapping[niv]['error_rate']
            else :
                if 'error_rate' in self.network_requirements :
                    niv = find_level(reliability_mapping, 'error_rate', error)
                    self.network_requirements['loss_rate'] = reliability_mapping[niv]['loss_rate']
                else :
                    if 'cos' in self.app_properties :
                        if 'loss_rate' in cos_mapping[self.app_properties['cos']] : 
                            self.network_requirements['loss_rate'] = { 'less_or_equal' : cos_mapping[self.app_properties['cos']]['loss_rate'] }
                        if 'error_rate' in cos_mapping[self.app_properties['cos']] : 
                            self.network_requirements['error_rate'] = { 'less_or_equal' : cos_mapping[self.app_properties['cos']]['error_rate'] }
                    else :
                        self.error = ERR_4
                        return
    

    def translate_hardware(self):
        cpus = ram = None
        if 'num_cpus' in self.host_requirements :
            cpus_cond = list(self.host_requirements['num_cpus'])[0]
            if cpus_cond != 'in_range' :
                cpus = self.host_requirements['num_cpus'][cpus_cond]
            else:
                cpus = self.host_requirements['num_cpus'][cpus_cond][0]
        if 'mem_size' in self.host_requirements :
            ram_cond = list(self.host_requirements['mem_size'])[0]
            if ram_cond != 'in_range' :
                ram = self.host_requirements['mem_size'][ram_cond]
            else:
                ram = self.host_requirements['mem_size'][ram_cond][0]

        if 'hardware' in self.app_requirements :
            if 'equal' not in self.app_requirements['hardware']:
                self.error = ERR_18
                return

            cpus_map = hardware_mapping[self.app_requirements['hardware']['equal']]['num_cpus']
            """
            cpus_map_cond = list(cpus_map)[0]
            if cpus_map_cond != 'in_range' :
                cpus_map = cpus_map[cpus_map_cond]
            else :
                cpus_map = cpus_map[cpus_map_cond][0]
            """
            if 'num_cpus' not in self.host_requirements : 
                self.host_requirements['num_cpus'] = cpus_map
            """
            else :
                if cpus_map > cpus :
                    self.host_requirements['num_cpus'] = cpus_map
            """
            ram_map = hardware_mapping[self.app_requirements['hardware']['equal']]['mem_size']
            """
            ram_map_cond = list(ram_map)[0]
            if ram_map_cond != 'in_range' :
                ram_map = ram_map[ram_map_cond]
            else :
                ram_map = ram_map[ram_map_cond][0]
            """
            if 'mem_size' not in self.host_requirements : 
                self.host_requirements['mem_size'] = ram_map
            """
            else:
                if ram_map > ram:
                    self.host_requirements['mem_size'] = ram_map
            """
        else :
            if 'num_cpus' in self.host_requirements :
                if 'mem_size' not in self.host_requirements :
                    niv = find_level(hardware_mapping, 'num_cpus', cpus)
                    self.host_requirements['mem_size'] = hardware_mapping[niv]['mem_size']
            else :
                if 'mem_size' in self.host_requirements :
                    niv = find_level(hardware_mapping, 'mem_size', ram)
                    self.host_requirements['num_cpus'] = hardware_mapping[niv]['num_cpus']
                else :
                    self.error = ERR_5
                    return

