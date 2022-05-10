hardware_mapping = {
    'very_low' : {
        'num_cpus' : { 'equal' : 1 },
        'mem_size' : { 'in_range' : ['0 GB', '1 GB']  }
    },
    'low' : {
        'num_cpus' : { 'equal' : 2 },
        'mem_size' : { 'in_range' : ['1 GB', '2 GB']  }
    },
    'medium' : {
        'num_cpus' : { 'equal' : 4 },
        'mem_size' : { 'in_range' : ['2 GB', '4 GB']  }
    },
    'high' : {
        'num_cpus' : { 'equal' : 8 },
        'mem_size' : { 'in_range' : ['4 GB', '8 GB']  }
    },
    'very_high' : {
        'num_cpus' : { 'equal' : 16 },
        'mem_size' : { 'in_range' : ['8 GB', '16 GB']  }
    },
    'unlimited' : {
        'num_cpus' : { 'greater_than' : 16 },
        'mem_size' : { 'greater_than' : '16 GB'  }
    }
}