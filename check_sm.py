def check_sm(swam3_object,chip):
    from RET import RET as RET
    from hex2dec import hex2dec as hex2dec
    from regrd import regrd as regrd
    from extractbits import extractbits as extractbits
    r = RET()
    
    addr = '0x76'
    data = hex2dec(regrd(addr,swam3_object,chip))
    state = extractbits(data,4,4)
    print "Addr: %s   Val: 0x%s State:  %d --> " % (addr,data,state)
    if state==7:
        print "OK!! Prox SM in linkdet (0x7)"
    else:
        print "ERROR!! Prox SM not in linkdet (0x7)"
    r.prox_state = state
    
    addr = '0x60'
    data = hex2dec(regrd(addr,swam3_object,chip))
    state = extractbits(data,1,3)
    print "Addr: %s   Val: 0x%s State:  %d --> " % (addr,data,state)
    if state==0:
        print "OK!! WPS SM in W0"
    else:
        print "ERROR!! WPS SM not in W0"
    r.wps_state = state 
    
    addr = '0xd6'
    data = hex2dec(regrd(addr,swam3_object,chip))
    state = extractbits(data,0,8)
    print "Addr: %s   Val: 0x%s State:  %d --> " % (addr,data,state)
    if state==5:
        print "OK!! PORSM in IDLE6G (0x5)"
    else:
        print "ERROR!! PORSM not in IDLE6G (0x5)"
    r.por_state = state    
    
    addr = '0x154'
    data = hex2dec(regrd(addr,swam3_object,chip))
    state = extractbits(data,0,8)
    print "Addr: %s   Val: 0x%s State:  %d --> " % (addr,data,state)
    if state==24:
        print "OK!! RF CTRL SM in 0x18"
    else:
        print "ERROR!! RF CTRL SM not in 0x18"
    r.rf_state = state  
    return r
    
    