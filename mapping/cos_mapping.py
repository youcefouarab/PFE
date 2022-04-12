cos_mapping = {
    'best_effort' : {
        'response_time' : '6 s',
        'latency' : '300 ms',
        'jitter' : None,
        'bandwidth' : '16 Kbps',
        'loss_rate' : 0.0,
        'error_rate' : 0.0,
        'env' : 'cloud',
        'hardware' : 'low',
        'scalability' : 'high'
    },
    'cpu_bound' : {
        'response_time' : None,
        'latency' : None,
        'jitter' : None,
        'bandwidth' : None,
        'loss_rate' : 0.0,
        'error_rate' : 0.0,
        'env' : 'any',
        'hardware' : 'high',
        'scalability' : 'low'
    },
    'streaming_audio' : {
        'response_time' : '6 s',
        'latency' : '150 ms',
        'jitter' : '50 ms',
        'bandwidth' : '448 Kbps',
        'loss_rate' : 0.01,
        'error_rate' : 0.01,
        'env' : 'any',
        'hardware' : 'medium',
        'scalability' : 'high'
    },
    'streaming_video' : {
        'response_time' : '6 s',
        'latency' : '150 ms',
        'jitter' : '50 ms',
        'bandwidth' : '5 Mbps',
        'loss_rate' : 0.02,
        'error_rate' : 0.02,
        'env' : 'any',
        'hardware' : 'medium',
        'scalability' : 'high'
    },
    'realtime' : {
        'response_time' : None,
        'latency' : '50 ms',
        'jitter' : '50 ms',
        'bandwidth' : '5 Mbps',
        'loss_rate' : 0.0,
        'error_rate' : 0.0,
        'env' : 'any',
        'hardware' : 'medium',
        'scalability' : 'high'
    },
    'interactive' : {
        'response_time' : None,
        'latency' : '150 ms',
        'jitter' : '50 ms',
        'bandwidth' : '5 Mbps',
        'loss_rate' : 0.0,
        'error_rate' : 0.0,
        'env' : 'any',
        'hardware' : 'medium',
        'scalability' : 'high'
    },
    'conversational' : {
        'response_time' : None,
        'latency' : '250 ms',
        'jitter' : '50 ms',
        'bandwidth' : '2 Mbps',
        'loss_rate' : 0.03,
        'error_rate' : 0.03,
        'env' : 'any',
        'hardware' : 'medium',
        'scalability' : 'high'
    },
    'mission_critical' : {
        'response_time' : None,
        'latency' : '20 ms',
        'jitter' : '1 ms',
        'bandwidth' : None,
        'loss_rate' : 0.0,
        'error_rate' : 0.0,
        'env' : 'any',
        'hardware' : 'high',
        'scalability' : 'high'
    }
}