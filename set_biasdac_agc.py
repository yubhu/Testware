def set_biasdac_agc(bdac_val,swam3_object,chip):
    from set_bdacs_lna2345 import set_bdacs_lna2345 as set_bdacs_lna2345
    set_bdacs_lna2345(bdac_val,bdac_val,bdac_val,bdac_val,swam3_object,chip)