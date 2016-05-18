def datapath_restart_rx(swam3_object,chip):
    from regwr import regwr as regwr
    regwr('0x6f','0x4a',swam3_object,chip) #clr frame detect, bch decoder, clear error count.
    
    regwr('0x70','0x06',swam3_object,chip) #clear splitter, pattern gen
    
    regwr('0x70','0x00',swam3_object,chip)   # clr_splitter=0
    
    regwr('0x6f','0x40',swam3_object,chip)   # clr_bch_decoder=0
    
    regwr('0x6f','0x00',swam3_object,chip)   # clr_frame_detect=0    