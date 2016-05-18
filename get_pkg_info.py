def get_pkg_info(swam3_object,chip):
    from bget import bget as bget
    from regrd import regrd as regrd
    from hex2dec import hex2dec as hex2dec
    from bin2dec import bin2dec as bin2dec
    
    pkg_id = int(bin2dec(bget('dfp_pkg_id',swam3_object,chip)))
    
    # register 0, bit 0 is inverted pkg_type
    pkg_type = 1-(int(hex2dec(regrd('0x0',swam3_object,chip)))%2) 
    return pkg_id*2 + pkg_type