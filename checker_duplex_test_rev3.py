def checker_duplex_test_rev3(chip,swam3_object1,swam3_object2,txptar_tx=None,agctar=None,set_rxbdac=None,tx_rxbdac=None,rx_rxbdac=None,restrim_offset=None,txptar_rx=None):
    from regwr import regwr as regwr
    from bset import bset as bset
    from bget import bget as bget
    from set_txp_tar_pd2 import set_txp_tar_pd2 as set_txp_tar_pd2
    from set_agc_tar_ed import set_agc_tar_ed as set_agc_tar_ed
    from set_biasdac_agc import set_biasdac_agc as set_biasdac_agc
    import time
    from set_biasdac1 import set_biasdac1 as set_biasdac1
    from dec2bin import dec2bin as dec2bin
    from force_sm_on import force_sm_on as force_sm_on
    from get_chip_revision import get_chip_revision as get_chip_revision
    from get_pkg_info import get_pkg_info as get_pkg_info
    from pkg_string import pkg_string as pkg_string
    from check_sm import check_sm as check_sm
    from get_synth_cal_stat import get_synth_cal_stat as get_synth_cal_stat
    from get_restrim_out import get_restrim_out as get_restrim_out
    from get_txp_idx import get_txp_idx as get_txp_idx
    from get_txp_tar_pd2 import get_txp_tar_pd2 as get_txp_tar_pd2
    from get_txp_dc_offset import get_txp_dc_offset as get_txp_dc_offset
    from get_agc_idx import get_agc_idx as get_agc_idx
    from get_agc_tar_ed import get_agc_tar_ed as get_agc_tar_ed
    from get_agc_dc_offset import get_agc_dc_offset as get_agc_dc_offset
    from extractbits import extractbits as extractbits
    from bin2dec import bin2dec as bin2dec
    
    if txptar_tx == None:
        txptar_tx = 174
        
    if agctar == None:
        agctar = 227
        
    if set_rxbdac == None:
        set_rxbdac = 0
        
    if tx_rxbdac == None:
        tx_rxbdac = 21
        
    if rx_rxbdac == None:
        rx_rxbdac = 34
        
    if restrim_offset == None:
        restrim_offset_2s_comp = 8
    else:
        if restrim_offset <0:
            restrim_offset_2s_comp = 32 + restrim_offset
        else:
            restrim_offset_2s_comp = restrim_offset
            
    if txptar_rx == None:
        txptar_rx = txptar_tx
        
    swam3_object1.SendTenCmd('ss_reset',silent='yes')
    swam3_object2.SendTenCmd('ss_reset',silent='yes')
    #allow I2C register writes
    regwr('0x76','0x1',swam3_object1,chip)        
    regwr('0x76','0x1',swam3_object2,chip) 
    regwr('0x214','0x1',swam3_object1,chip) 
    regwr('0x214','0x1',swam3_object2,chip) 
    #put prox detect into reset
    bset('prox_rst', '1', swam3_object1,chip)
    bset('prox_rst', '1', swam3_object2,chip)
    
    '''
    dont allow wakeup from I2C pins
    these have to be in this order for the prox detect lockup workaround
    '''
    bset('regs_i2c_dbg_active_count_23_16', '00000000', swam3_object1, chip)
    bset('regs_i2c_dbg_wakeup', '0', swam3_object1, chip)
    bset('regs_i2c_dbg_active_count_23_16', '00000000', swam3_object2, chip)
    bset('regs_i2c_dbg_wakeup', '0', swam3_object2, chip)
    
    #disable remote I2C access, messes up with prox detect
    bset('remote_access_clr', '1', swam3_object1, chip)
    bset('remote_access_clr', '1', swam3_object2, chip)
    
    bset('disable_sync_to_own_link', '0', swam3_object1, chip)
    bset('disable_sync_to_own_link', '0', swam3_object2, chip)  
    
    #allow main domain to switch, force i2c on
    regwr('0x20c', '0x70', swam3_object1,chip)
    regwr('0x20c', '0x70', swam3_object2,chip)
    
    #PRBS pattern-checker settings
    regwr('0x1e','0x3a',swam3_object1,chip) # PRBS pattern, infinite length, before FEC 
    regwr('0x1e','0x3a',swam3_object2,chip)
    regwr('0x2a','0x00',swam3_object1,chip) # set first match threshold
    regwr('0x2a','0x00',swam3_object2,chip)
    regwr('0x2b','0x0f',swam3_object1,chip)
    regwr('0x2b','0x0f',swam3_object2,chip) 
    
    #enable the CDR DETOUT pins
    bset('cdrbuf_en_detoutbuf','1',swam3_object1,chip)
    bset('cdrbuf_en_detoutbuf','1',swam3_object2,chip)   
    
    # Change TXP target
    set_txp_tar_pd2(txptar_tx,swam3_object1,chip)
    set_txp_tar_pd2(txptar_rx,swam3_object2,chip)   
    
    # Change AGC target
    set_agc_tar_ed(agctar,swam3_object1,chip)
    set_agc_tar_ed(agctar,swam3_object2,chip)  
    
    # Fix AGC BDAC
    if set_rxbdac == 1:
        set_biasdac_agc(tx_rxbdac,swam3_object1,chip)
        set_biasdac_agc(rx_rxbdac,swam3_object2,chip)   
        
    #Program restrim offset
    bset('restrim_offset',dec2bin(restrim_offset_2s_comp,5),swam3_object1,chip)
    bset('restrim_offset',dec2bin(restrim_offset_2s_comp,5),swam3_object2,chip)    
    
    '''    
    brians thing to not allow the link to come up fully -- it will be stuck in TRY6G and hence it will also never be torn down.
    '''
    bset('tx6g_disable_timeout','1',swam3_object1,chip)
    bset('tx6g_disable_timeout','1',swam3_object2,chip)
    bset('fd_bitslp_thres_pre_sync','000',swam3_object1,chip)
    bset('fd_bitslp_thres_pre_sync','000',swam3_object2,chip)   
    
    # increase LO power for Rev3 (target is -3.5dBm)
    bset('bias_x2_30G_to_60g_itrim','11',swam3_object1,chip)
    set_biasdac1('lobuf1',51,swam3_object1,chip)
    set_biasdac1('lobuf2',51,swam3_object1,chip)
    bset('bias_x2_30G_to_60g_itrim','11',swam3_object2,chip)
    set_biasdac1('lobuf1',51,swam3_object2,chip)
    set_biasdac1('lobuf2',51,swam3_object2,chip)
    
    #re-run calibrations once PROX is released from reset
    bset('clr_startup_cals_done', '1', swam3_object1,chip)
    bset('clr_startup_cals_done', '0', swam3_object1,chip)
    bset('clr_startup_cals_done', '1', swam3_object2,chip)
    bset('clr_startup_cals_done', '0', swam3_object2,chip)    
    
    bset('agc_ki','000',swam3_object2,chip)
    
    bset('prox_byp', '1', swam3_object1,chip) #bypass prox detect so that DC offset calibrations are run
    bset('prox_byp', '1', swam3_object2,chip)
    
    #put prox detect out of reset
    bset('prox_rst', '0', swam3_object1,chip)
    bset('prox_rst', '0', swam3_object2,chip)
    
    time.sleep(2)
    
    # fix state machine states for uninterrupted operation
    force_sm_on (swam3_object1, swam3_object2,chip)    
    
    '''    
    brians thing to not allow the link to come up fully -- it will be stuck in TRY6G and hence it will also never be torn down.
    '''
    bset('fd_bitslp_thres_pre_sync','001',swam3_object2,chip)
    bset('fd_bitslp_thres_pre_sync','001',swam3_object1,chip)
    
    # display the chip revision info
    tx_chiprev = get_chip_revision(swam3_object1,chip)
    rx_chiprev = get_chip_revision(swam3_object2,chip)
    print 'TX die revision: %0.1f\n' %tx_chiprev
    print 'RX die revision: %0.1f\n' %rx_chiprev    
    
    # display the package info
    print 'TX connected to: %s\n' %pkg_string(get_pkg_info(swam3_object1,chip))
    print 'RX connected to: %s\n' %pkg_string(get_pkg_info(swam3_object2,chip))  
    
    # readback VCO cal code
    print 'TX default VCO cal: %d\n' %extractbits(bin2dec(bget('lo_dyn_synth_cal_out',swam3_object1,chip)),0,5)
    print 'RX default VCO cal: %d\n' %extractbits(bin2dec(bget('lo_dyn_synth_cal_out',swam3_object2,chip)),0,5) 
    
    # readback sleep osc cal code
    print 'TX sleeposc cal: %d\n' %int(bin2dec(bget('sleeposc_code_out',swam3_object1,chip)))
    print 'RX sleeposc cal: %d\n' %int(bin2dec(bget('sleeposc_code_out',swam3_object2,chip)))   
    
    print '--- Checking TX SMs ---'
    check_sm(swam3_object1,chip)
    print '--- Checking RX SMs ---'
    check_sm(swam3_object2,chip)  
    
    print 'TX VCO cal: %d\n' %extractbits(bin2dec(bget('lo_dyn_synth_cal_out',swam3_object1,chip)),0,5)
    a = get_synth_cal_stat(swam3_object1,chip)
    print '%s\n' %a.synthcal_stat
    if not a.bGood:
        print a
    print 'RX VCO cal: %d\n' %extractbits(bin2dec(bget('lo_dyn_synth_cal_out',swam3_object2,chip)),0,5)
    a = get_synth_cal_stat(swam3_object2,chip)
    print '%s\n' %a.synthcal_stat
    if not a.bGood:
        print a    
        
    rxFilterCal = int(bin2dec(bget('txbb_osc_cal_out',swam3_object2,chip)))
    txFilterCal = int(bin2dec(bget('txbb_osc_cal_out',swam3_object1,chip)))
    rxLOR = int(bin2dec(bget('lor_bbdac_out',swam3_object2,chip)))
    txLOR = int(bin2dec(bget('lor_bbdac_out',swam3_object1,chip)))
        
    print 'TX filter cal %d\n' %txFilterCal
    print 'RX filter cal %d\n' %rxFilterCal
    print 'TX LOR %d\n' %txLOR
    print 'RX LOR %d\n' %rxLOR    
    
    a = get_restrim_out(swam3_object1,chip)
    b = get_restrim_out(swam3_object2,chip)
    
    print 'TX Restrim: cal_done=%d, fail=%d, restrim_reg=%d, restrim_gm=%d, temp_reg=%d, temp_ofs_reg=%d\n' %(a.restrim_cal_done,a.restrim_fail,a.restrim_reg,a.restrim_gm,a.temp_reg,a.temp_ofs_reg)
    print 'RX Restrim: cal_done=%d, fail=%d, restrim_reg=%d, restrim_gm=%d, temp_reg=%d, temp_ofs_reg=%d\n' %(b.restrim_cal_done,b.restrim_fail,b.restrim_reg,b.restrim_gm,b.temp_reg,b.temp_ofs_reg)
    
    print 'txComPort => rxComPort\n'
    print '    TX values: '
    txp_idx,txLOR,a.pa1,a.pa2,a.pa3,txbb = get_txp_idx(swam3_object1,chip) 
    print '  BB=%2d,  PA1=%2d,  PA2=%2d,  PA3=%2d' %(txbb,a.pa1,a.pa2,a.pa3)
    print ', IDX=%2d (TXP_TAR_PD2=%3d, TXP_DC_OFFSET=%d, LOR=%d)\n' %(txp_idx,get_txp_tar_pd2(swam3_object1,chip),get_txp_dc_offset(swam3_object1,chip), txLOR)
    
    print '    RX values: '
    agc_idx,lna2,lna3,lna4,lna5,lna6,lna1 = get_agc_idx(swam3_object2,chip)
    x=int(bin2dec(bget('cdrbuf_offsetdac_out',swam3_object2,chip)))
    print 'LNA2=%2d, LNA3=%2d, LNA4=%2d, LNA5=%2d, LNA6=%2d, LNA1=%2d' %(lna2,lna3,lna4,lna5,lna6,lna1)
    print ', IDX=%2d, CDRBUF_OFFSETDAC_OUT=%2d (AGC_TAR_ED= %3d, AGC_DC_OFFSET=%d)\n' %(agc_idx,x,get_agc_tar_ed(swam3_object2,chip),get_agc_dc_offset(swam3_object2,chip))    
    
    print 'rxComPort => txComPort\n'
    print '    TX values: '
    txp_idx,txLOR,a.pa1,a.pa2,a.pa3,txbb = get_txp_idx(swam3_object2,chip)
    print '  BB=%2d,  PA1=%2d,  PA2=%2d,  PA3=%2d' %(txbb,a.pa1,a.pa2,a.pa3)
    print ', IDX=%2d (TXP_TAR_PD2=%3d, TXP_DC_OFFSET=%d, LOR=%d)\n' %(txp_idx,get_txp_tar_pd2(swam3_object1,chip),get_txp_dc_offset(swam3_object1,chip), txLOR)
    
    print '    RX values: '
    agc_idx,lna2,lna3,lna4,lna5,lna6,lna1 = get_agc_idx(swam3_object1,chip)
    x=int(bin2dec(bget('cdrbuf_offsetdac_out',swam3_object1,chip)))
    print 'LNA2=%2d, LNA3=%2d, LNA4=%2d, LNA5=%2d, LNA6=%2d, LNA1=%2d' %(lna2,lna3,lna4,lna5,lna6,lna1)
    print ', IDX=%2d, CDRBUF_OFFSETDAC_OUT=%2d (AGC_TAR_ED= %3d, AGC_DC_OFFSET=%d)\n' %(agc_idx,x,get_agc_tar_ed(swam3_object1,chip),get_agc_dc_offset(swam3_object1,chip))    
    
    
from start_swam3_mobile import start_swam3_mobile as start_swam3_mobile
from start_swam3_dock import start_swam3_dock as start_swam3_dock
import Chip
mobile = start_swam3_mobile('COM4')
dock = start_swam3_dock('COM3')
chip = Chip.Chip(host_port=mobile)
checker_duplex_test_rev3(chip,mobile,dock)