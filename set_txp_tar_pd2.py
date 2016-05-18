def set_txp_tar_pd2(x,swam3_object,chip):
    from extractbits import extractbits as extractbits
    from dec2bin import dec2bin as dec2bin
    from bset import bset as bset
    bset('txp_tar_pd2_1',dec2bin(extractbits(x,8,2),2),swam3_object,chip)    # [9:8]
    bset('txp_tar_pd2_0',dec2bin(extractbits(x,0,8),8),swam3_object,chip)    # [7:0]    