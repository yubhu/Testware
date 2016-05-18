def get_agc_tar_ed(swam3_object,chip):
    from bin2dec import bin2dec as bin2dec
    from bget import bget as bget
    
    return int(bin2dec(bget('agc_tar_ed_1',swam3_object,chip)+bget('agc_tar_ed_0',swam3_object,chip)))