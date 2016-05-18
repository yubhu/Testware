def get_agc_dc_offset(swam3_object,chip):
    from bin2dec import bin2dec as bin2dec
    from bget import bget as bget
    
    return int(bin2dec(bget('agc_dc_offset_09_08',swam3_object,chip)+bget('agc_dc_offset_07_00',swam3_object,chip)))