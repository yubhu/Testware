def get_txp_tar_pd2(swam3_object,chip):
    from bin2dec import bin2dec as bin2dec
    from bget import bget as bget
    
    return int(bin2dec(bget('txp_tar_pd2_1',swam3_object,chip)+bget('txp_tar_pd2_0',swam3_object,chip)))