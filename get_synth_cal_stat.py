def get_synth_cal_stat(swam3_object,chip):
    from hex2dec import hex2dec as hex2dec
    from regrd import regrd as regrd
    from extractbits import extractbits as extractbits
    from bin2dec import bin2dec as bin2dec
    from bget import bget as bget
    from LO import LO as LO
    
    x = int(hex2dec(regrd('RF_CTL_72',swam3_object,chip)))
    a = LO()
    a.LO_lock_det = extractbits(x,2,1)
    a.LO_calresethi = extractbits(x,3,1)
    a.LO_calwarnhi = extractbits(x,4,1)
    a.LO_calresetlo = extractbits(x,5,1)
    a.LO_calwarnlo = extractbits(x,6,1)
    a.LO_vconoosc = extractbits(x,7,1)  
    a.synthCalResidual = bin2dec(bget('vco_cal_final_timer_12_08',swam3_object,chip)+bget('vco_cal_final_timer_07_00',swam3_object,chip))
    
    x = bin2dec(bget('lo_dyn_synth_cal_out',swam3_object,chip))
    
    a.LO_calrange = extractbits(x,0,5)
    a.LO_calmode = extractbits(x,5,1)
    a.LO_lockd_rst_n = extractbits(x,6,1)   
    
    x = int(hex2dec(regrd('RF_CAL_10',swam3_object,chip)))
    
    a.vco_cal_done = extractbits(x,4,1)
    a.vco_cal_fail = extractbits(x,5,1)   
    if (a.LO_calresethi==0) and (a.LO_calwarnhi==0) and (a.LO_calresetlo==0) and (a.LO_calwarnlo==0) and (a.LO_vconoosc==0) and (a.LO_calmode==0) and (a.LO_lockd_rst_n==1) and (a.vco_cal_done==1) and (a.vco_cal_fail==0):
        a.bGood = 1
        
    if a.bGood:
        a.synthcal_stat = 'OK: synthcal PASS (LO_lock_det not checked)'
    else:
        a.synthcal_stat = '!!! ERROR: synthcal FAIL !!!'
        
    return a
    