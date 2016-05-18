def get_txp_dc_offset(swam3_object,chip):
    from bin2dec import bin2dec as bin2dec
    from bget import bget as bget
    
    return int(bin2dec(bget('txp_dc_offset_09_08',swam3_object,chip)+bget('txp_dc_offset_07_00',swam3_object,chip)))