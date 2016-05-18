def start_swam3_mobile(mobile_comport,mobileComPort='40100',logfile='log_mobile.txt'):
    "define mobile_swam3 object and dock_swam3 object and return them."
    import adapter_swam3
    mobile_swam3 = adapter_swam3.Adapter(mobileComPort,mobile_comport,logfile)
    return mobile_swam3

