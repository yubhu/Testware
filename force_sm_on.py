def force_sm_on(swam3_object1,swam3_object2,chip):
    from regwr import regwr as regwr
    regwr('0x14e','0x31',swam3_object1,chip) #rf control
    regwr('0x5f','0xc4',swam3_object1,chip) #wps
    regwr('0x100','0x0f',swam3_object1,chip) #prox
    regwr('0x118','0x0b',swam3_object1,chip) #porsm
    
    if swam3_object2:
        regwr('0x14e','0x31',swam3_object2,chip) #rf control
        regwr('0x5f','0xc4',swam3_object2,chip) #wps
        regwr('0x100','0x0f',swam3_object2,chip) #prox
        regwr('0x118','0x0b',swam3_object2,chip) #porsms  
    