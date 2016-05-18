def set_dbgmux(swam3_object,chip,gpi=None,gpo=None,ledo=None,scl=None,sda=None):
    "Sets individual pins to the debug mux. GPI,GPO,LEDO,SCL,SDA are the mux selection in decimal. Leave parameter as empty to leave unchanged"
    from hex2dec import hex2dec as hex2dec
    from regwr import regwr as regwr
    from regrd import regrd as regrd
    enable = int(hex2dec(regrd('dbg_ctl_6',swam3_object,chip)))
    if gpi!=None:
        regwr('dbg_CTL_1',hex(gpi),swam3_object,chip)
        enable = enable|1
    if gpo!=None:
        regwr('dbg_CTL_2',hex(gpo),swam3_object,chip)
        enable = enable|2
    if ledo!=None:
        regwr('dbg_CTL_3',hex(ledo),swam3_object,chip)
        enable = enable|4
    if scl!=None:
        regwr('dbg_CTL_4',hex(scl),swam3_object,chip)
        enable = enable|8
    if sda!=None:
        regwr('dbg_CTL_5',hex(sda),swam3_object,chip)
        enable = enable|16
    regwr('dbg_CTL_6',hex(enable),swam3_object,chip)
        
    
        
        
    