import numpy

def translate_response_time(rt, ct, sa = None, su = None, la = None, lu = None) :
    # si le débit est négligeable
    # retourner la latence maximale
    if sa == None and su == None :
        return rt - ct
    # si la latence est négligeable
    # retourner le débit minimal
    if la == None and lu == None :
        return (sa + su) / (rt - ct)
    # si aucun n'est négligeable
    # fixer la latence maximale
    # retourner le débit minimal
    return (sa + su) / (rt - ct - (la + lu))

def calculate_response_time() :
    pass

def translate_compute_time(ct, mi) :
    # retourner le mips
    return mi / ct

def calculate_compute_time(i, cpi, f) :
    # retourner le temps d'exécution
    return i * cpi * (1 / f)

def calculate_availability(mtbf, mttr) :
    # retourner la disponibilité
    return mtbf / (mtbf + mttr)

def calculate_mtbsi(mtbf, mttr) :
    # retourner mtbsi
    return mtbf + mttr

def calculate_serial_availability(a) :
    # retourner la disponibilité en série
    return numpy.prod(a)

def calculate_parallel_availability(a) :
    # retourner la disponibilité parallèle
    res = [1] * len(a)
    res = res - a
    return numpy.prod(res)

def translate_rps(rps, task_time, worker_mem = None) :
    # si requêtes liées à la mémoire
    # retourner la taille de ram
    if worker_mem != None :
        return rps * worker_mem * task_time
    # si requêtes liées au cpu
    # retourner le nombre de coeurs
    else :
        return rps * task_time

def translate_ccu(ccu, response_time, click_freq) :
    # retourner le nombre de coeurs
    return (ccu * response_time) / (60 * click_freq)