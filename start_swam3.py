def start_swam3(mobile_comport,dock_comport,mobileComPort='40100',dockComPort='40200',logfile='log.txt'):
    "define mobile_swam3 object and dock_swam3 object and return them."
    import adapter_swam3
    mobile_swam3 = adapter_swam3.Adapter(mobileComPort,mobile_comport,logfile)
    dock_swam3 = adapter_swam3.Adapter(dockComPort,dock_comport,logfile)
    return mobile_swam3,dock_swam3

