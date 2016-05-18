def txbb_filter_max(swam3_object,chip):
    from bset import bset as bset
    from dec2bin import dec2bin as dec2bin
    bset('txbb_cap1_cal',dec2bin(0,6),swam3_object,chip)
    bset('txbb_cap2_cal',dec2bin(0,6),swam3_object,chip)
    bset('txbb_cap3_cal',dec2bin(0,6),swam3_object,chip)
    bset('txbb_cap1_cal_override','1',swam3_object,chip)
    bset('txbb_cap2_cal_override','1',swam3_object,chip)
    bset('txbb_cap2_cal_override','1',swam3_object,chip)   