def set_agc_tar_ed(x,swam3_object,chip):
    "Sets the AGC target for IDLE_6G mode"
    from dec2bin import dec2bin as dec2bin
    from bset import bset as bset
    from extractbits import extractbits as extractbits
    bset('agc_tar_ed_1',dec2bin(extractbits(x,8,2),2),swam3_object,chip)    # [9:8]
    bset('agc_tar_ed_0',dec2bin(extractbits(x,0,8),8),swam3_object,chip)    # [7:0]    
    