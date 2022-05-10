reliability_mapping = {
    'low' : {
        'loss_rate' : { 'in_range' : [0.01, 0.03] }, 
        'error_rate' : { 'in_range' : [0.01, 0.03] }
    },
    'medium' : {
        'loss_rate' : { 'in_range' : [0.0001, 0.01] }, 
        'error_rate' : { 'in_range' : [0.0001, 0.01] }
    },
    'high' : {
        'loss_rate' : { 'in_range' : [0, 0.0001] },
        'error_rate' : { 'in_range' : [0, 0.0001] }
    }
}