
def read_scalar_unit(su, required_unit) :
     
    if not isinstance(su, str) : 
        raise Exception("Type must be scalar-unit.")
    
    scalar = unit = ''

    for t in su :
        if t.isdigit() or t == '.' : scalar += t
        elif len(scalar) > 0 : break
    
    if scalar == '' : raise Exception("Type must be scalar-unit.")
    
    scalar = float(scalar)
    
    for t in su :
        if t.isalpha() : unit += t
        elif len(unit) > 0 : break

    if unit == 'd' : scalar *= 24 * 60 * 60
    elif unit == 'h' : scalar *= 60 * 60
    elif unit == 'm' : scalar *= 60
    elif unit == 'ms' : scalar /= 1000
    elif unit == 'us' : scalar /= (1000 * 1000)
    elif unit == 'ns' : scalar /= (1000 * 1000 * 1000)

    elif unit == 'kHz' : scalar *= 1000
    elif unit == 'MHz' : scalar *= 1000 * 1000
    elif unit == 'GHz' : scalar *= 1000 * 1000 * 1000

    elif unit == 'kB' or unit == 'kBps' : scalar *= 1000
    elif unit == 'KiB' or unit == 'KiBps' : scalar *= 1024
    elif unit == 'MB' or unit == 'MBps' : scalar *= 1000 * 1000
    elif unit == 'MiB' or unit == 'MiBps' : scalar *= 1024 * 1024
    elif unit == 'GB' or unit == 'GBps' : scalar *= 1000 * 1000 * 1000
    elif unit == 'GiB' or unit == 'GiBps' : scalar *= 1024 * 1024 * 1024
    elif unit == 'TB' or unit == 'TBps' : scalar *= 1000 * 1000 * 1000 * 1000
    elif unit == 'TiB' or unit == 'TiBps' : scalar *= 1024 * 1024 * 1024 * 1024

    elif unit == 'bps' : scalar /= 8
    elif unit == 'Kbps' or unit == 'kbps' : scalar *= 1000 / 8
    elif unit == 'Kibps' or unit == 'kibps' : scalar *= 1024 / 8
    elif unit == 'Mbps' : scalar *= 1000 * 1000 / 8
    elif unit == 'Mibps' : scalar *= 1024 * 1024 / 8
    elif unit == 'Gbps' : scalar *= 1000 * 1000 * 1000 / 8
    elif unit == 'Gibps' : scalar *= 1024 * 1024 * 1024 / 8
    elif unit == 'Tbps' : scalar *= 1000 * 1000 * 1000 * 1000 / 8
    elif unit == 'Tibps' : scalar *= 1024 * 1024 * 1024 * 1024 / 8

    elif unit != 's' and unit != 'Hz' and unit != 'B' and unit != 'Bps': 
        raise Exception("Unrecognized unit " + unit)

    if required_unit == 'd' : return scalar / (24 * 60 * 60)
    elif required_unit == 'h' : return scalar / (60 * 60)
    elif required_unit == 'm' : return scalar / (60)
    elif required_unit == 'ms' : return scalar * 1000
    elif required_unit == 'us' : return scalar * 1000 * 1000
    elif required_unit == 'ns' : return scalar * 1000 * 1000 * 1000
 
    elif required_unit == 'kHz' : return scalar / 1000
    elif required_unit == 'MHz' : return scalar / (1000 * 1000)
    elif required_unit == 'GHz' : return scalar / (1000 * 1000 * 1000)

    elif required_unit == 'kB' or required_unit == 'KBps' : return scalar / 1000
    elif required_unit == 'KiB' or required_unit == 'KiBps' : return scalar / 1024
    elif required_unit == 'MB' or required_unit == 'MBps' : return scalar / (1000 * 1000)
    elif required_unit == 'MiB' or required_unit == 'MiBps' : return scalar / (1024 * 1024)
    elif required_unit == 'GB' or required_unit == 'GBps' : return scalar / (1000 * 1000 * 1000)
    elif required_unit == 'GiB' or required_unit == 'GiBps' : return scalar / (1024 * 1024 * 1024)
    elif required_unit == 'TB' or required_unit == 'TBps' : return scalar / (1000 * 1000 * 1000 * 1000)
    elif required_unit == 'TiB' or required_unit == 'TiBps' : return scalar / (1024 * 1024 * 1024 * 1024)   

    elif required_unit == 'bps' : return scalar * 8
    elif required_unit == 'Kbps' : return scalar / (1000 / 8)
    elif required_unit == 'Kibps' : return scalar / (1024 / 8)
    elif required_unit == 'Mbps' : return scalar / (1000 * 1000 / 8)
    elif required_unit == 'Mibps' : return scalar / (1024 * 1024 / 8)
    elif required_unit == 'Gbps' : return scalar / (1000 * 1000 * 1000 / 8)
    elif required_unit == 'Gibps' : return scalar / (1024 * 1024 * 1024 / 8)
    elif required_unit == 'Tbps' : return scalar / (1000 * 1000 * 1000 * 1000 / 8)
    elif required_unit == 'Tibps' : return scalar / (1024 * 1024 * 1024 * 1024 / 8)

    elif required_unit != 's' and required_unit != 'Hz' and required_unit != 'B' and required_unit != 'Bps': 
        raise Exception("Unrecognized unit " + required_unit)

    return scalar


def check_condition(requirement, capability) :
    
    unit = ''
    if isinstance(capability, str) :
        for t in capability :
            if t.isalpha() : unit += t
            elif len(unit) > 0 : break
        cap = read_scalar_unit(capability, unit)
    else :
        cap = capability

    condition = list(requirement)[0]
    req = requirement[condition]
    req_1 = req_2 = None
    
    if isinstance(req, list) :
        if isinstance(req[0], str) :
            req_1 = read_scalar_unit(req[0], unit)
            req_2 = read_scalar_unit(req[1], unit)
        else :
            req_1 = req[0]
            req_2 = req[1]
    else : 
        if isinstance(req, str) :
            req = read_scalar_unit(req, unit)

    if 'equal' in requirement :
        if cap == req : return True
    if 'greater_than' in requirement :
        if cap > req : return True
    if 'greater_or_equal' in requirement :
        if cap >= req: return True
    if 'less_than' in requirement :
        if cap < req : return True
    if 'less_or_equal' in requirement :
        if cap <= req : return True
    if 'in_range' in requirement :
        if cap >= req_1 and cap <= req_2 : return True
    
    return False


def find_level(dict, key, value) :
    for niv in list(dict) :
        if check_condition(dict[niv][key], value) :
            return niv


def next_power_of_2(x): 
    num = round(x) 
    if num < x : num += 1 
    return 1 if num == 0 else 2**(num - 1).bit_length()

