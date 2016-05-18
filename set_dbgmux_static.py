def set_dbgmux_static(swam3_object,chip):
    "SET_DBGMUX_STATIC enables all debug mux pins and sets them to 0"
    from set_dbgmux import set_dbgmux as set_dbgmux
    set_dbgmux(swam3_object,chip,176,176,176,176,176) # selection 176 is static 0
    