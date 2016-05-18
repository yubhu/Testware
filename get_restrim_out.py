def get_restrim_out(swam3_object,chip):
    from bin2dec import bin2dec as bin2dec
    from bget import bget as bget
    from extractbits import extractbits as extractbits
    from RESTRIM import RESTRIM as RESTRIM
    
    restrim = RESTRIM()
    a = bin2dec(bget('restrim_out_09_08',swam3_object,chip)+bget('restrim_out_07_00',swam3_object,chip))
    a_reg = extractbits(a,0,5)
    a_gm = extractbits(a,5,5)   
    
    if a_reg>15:
        restrim.restrim_reg = a_reg-32
    else:
        restrim.restrim_reg = a_reg
        
    if a_gm>15:
        restrim.restrim_gm = a_gm-32
    else:
        restrim.restrim_gm = a_gm
        
    a = int(bin2dec(bget('restrim_offset',swam3_object,chip)))
  
    if a>15:
        restrim.restrim_offset = a-32
    else:
        restrim.restrim_offset = a   
        
    restrim.bypass_restrim = int(bin2dec(bget('bypass_restrim',swam3_object,chip)))
    restrim.restrim_cal_done = int(bin2dec(bget('restrim_cal_done',swam3_object,chip)))
    restrim.restrim_fail = int(bin2dec(bget('restrim_fail',swam3_object,chip)))
    restrim.temp_reg = int(bin2dec(bget('temp_reg_09_08',swam3_object,chip)+bget('temp_reg_07_00',swam3_object,chip)))
    restrim.temp_ofs_reg = int(bin2dec(bget('temp_ofs_reg_09_08',swam3_object,chip)+bget('temp_ofs_reg_07_00',swam3_object,chip)))
    return restrim