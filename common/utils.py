


def read_scalar_unit(str, required_unit) :
    
    scalar = unit = ''
    
    for t in str :
        if t.isdigit() or t == '.' : scalar += t
        elif len(scalar) > 0 : break
    scalar = float(scalar)
    
    for t in str :
        if t.isalpha() : unit += t
        elif len(unit) > 0 : break

    if unit == 'd' : scalar *= 24 * 60 * 60
    if unit == 'h' : scalar *= 60 * 60
    if unit == 'm' : scalar *= 60
    if unit == 'ms' : scalar /= 1000
    if unit == 'us' : scalar /= (1000 * 1000)
    if unit == 'ns' : scalar /= (1000 * 1000 * 1000)

    if unit == 'kHz' : scalar *= 1000
    if unit == 'MHz' : scalar *= 1000 * 1000
    if unit == 'GHz' : scalar *= 1000 * 1000 * 1000

    if unit == 'kB' or unit == 'KBps' : scalar *= 1000
    if unit == 'KiB' or unit == 'KiBps' : scalar *= 1024
    if unit == 'MB' or unit == 'MBps' : scalar *= 1000 * 1000
    if unit == 'MiB' or unit == 'MiBps' : scalar *= 1024 * 1024
    if unit == 'GB' or unit == 'GBps' : scalar *= 1000 * 1000 * 1000
    if unit == 'GiB' or unit == 'GiBps' : scalar *= 1024 * 1024 * 1024
    if unit == 'TB' or unit == 'TBps' : scalar *= 1000 * 1000 * 1000 * 1000
    if unit == 'TiB' or unit == 'TiBps' : scalar *= 1024 * 1024 * 1024 * 1024

    if unit == 'bps' : scalar /= 8
    if unit == 'Kbps' : scalar *= 1000 / 8
    if unit == 'Kibps' : scalar *= 1024 / 8
    if unit == 'Mbps' : scalar *= 1000 * 1000 / 8
    if unit == 'Mibps' : scalar *= 1024 * 1024 / 8
    if unit == 'Gbps' : scalar *= 1000 * 1000 * 1000 / 8
    if unit == 'Gibps' : scalar *= 1024 * 1024 * 1024 / 8
    if unit == 'Tbps' : scalar *= 1000 * 1000 * 1000 * 1000 / 8
    if unit == 'Tibps' : scalar *= 1024 * 1024 * 1024 * 1024 / 8

    if required_unit == 'd' : return scalar / (24 * 60 * 60)
    if required_unit == 'h' : return scalar / (60 * 60)
    if required_unit == 'm' : return scalar / (60)
    if required_unit == 'ms' : return scalar * 1000
    if required_unit == 'us' : return scalar * 1000 * 1000
    if required_unit == 'ns' : return scalar * 1000 * 1000 * 1000
 
    if required_unit == 'kHz' : return scalar / 1000
    if required_unit == 'MHz' : return scalar / (1000 * 1000)
    if required_unit == 'GHz' : return scalar / (1000 * 1000 * 1000)

    if required_unit == 'kB' or required_unit == 'KBps' : return scalar / 1000
    if required_unit == 'KiB' or required_unit == 'KiBps' : return scalar / 1024
    if required_unit == 'MB' or required_unit == 'MBps' : return scalar / (1000 * 1000)
    if required_unit == 'MiB' or required_unit == 'MiBps' : return scalar / (1024 * 1024)
    if required_unit == 'GB' or required_unit == 'GBps' : return scalar / (1000 * 1000 * 1000)
    if required_unit == 'GiB' or required_unit == 'GiBps' : return scalar / (1024 * 1024 * 1024)
    if required_unit == 'TB' or required_unit == 'TBps' : return scalar / (1000 * 1000 * 1000 * 1000)
    if required_unit == 'TiB' or required_unit == 'TiBps' : return scalar / (1024 * 1024 * 1024 * 1024)   

    if required_unit == 'bps' : return scalar * 8
    if required_unit == 'Kbps' : return scalar / (1000 / 8)
    if required_unit == 'Kibps' : return scalar / (1024 / 8)
    if required_unit == 'Mbps' : return scalar / (1000 * 1000 / 8)
    if required_unit == 'Mibps' : return scalar / (1024 * 1024 / 8)
    if required_unit == 'Gbps' : return scalar / (1000 * 1000 * 1000 / 8)
    if required_unit == 'Gibps' : return scalar / (1024 * 1024 * 1024 / 8)
    if required_unit == 'Tbps' : return scalar / (1000 * 1000 * 1000 * 1000 / 8)
    if required_unit == 'Tibps' : return scalar / (1024 * 1024 * 1024 * 1024 / 8)

    return scalar


def check_condition(requirement, capability) :
    # TODO check conditions equal greater_than greater_or_equal less_than less_or_equal in_range
    check = False
    if 'equal' in requirement : 
        pass 
    if 'greater_than' in requirement :  
        pass 
    if 'greater_or_equal' in requirement :  
        pass 
    if 'less_than' in requirement :  
        pass 
    if 'less_or_equal' in requirement :  
        pass 
    if 'in_range' in requirement :  
        pass 
    return check


def next_power_of_2(x):  
    return 1 if x == 0 else 2**(x - 1).bit_length()
