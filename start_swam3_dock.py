def start_swam3_dock(dock_comport,dockComPort='40200',logfile='log_dock.txt'):
    "define mobile_swam3 object and dock_swam3 object and return them."
    import adapter_swam3
    dock_swam3 = adapter_swam3.Adapter(dockComPort,dock_comport,logfile)
    return dock_swam3