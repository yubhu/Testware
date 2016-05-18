def set_bdacs_lna2345(bdac_2,bdac_3,bdac_4,bdac_5,swam3_object,chip):
    # override the state machine and hold the state before writing
    from dec2bin import dec2bin as dec2bin
    from bin2dec import bin2dec as bin2dec
    from dec2hex import dec2hex as dec2hex
    from bset import bset as bset
    from regwr import regwr as regwr
    bset('bias_agcstrobe_override','1',swam3_object,chip) # override functional strobe path
    bset('bias_agcstrobe','0',swam3_object,chip) # hold the previous values
    bset('biasdac_agc_override','1',swam3_object,chip) # use the manual setting
    bin_2 = dec2bin(bdac_2,6)
    bin_3 = dec2bin(bdac_3,6)
    bin_4 = dec2bin(bdac_4,6)
    bin_5 = dec2bin(bdac_5,6)
    bdac_all = bin_5 + bin_4 + bin_3 + bin_2
    # now break it up into 8 bit chunks and write it back
    regwr('RF_CTL_53',dec2hex(bin2dec(bdac_all[0:8]),2),swam3_object,chip)
    regwr('RF_CTL_52',dec2hex(bin2dec(bdac_all[8:16]),2),swam3_object,chip)
    regwr('RF_CTL_51',dec2hex(bin2dec(bdac_all[16:24]),2),swam3_object,chip)
    # strobe the new BDAC values in
    bset('bias_agcstrobe','1',swam3_object,chip)
    