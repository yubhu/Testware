def full_link_bringup_6g(checker_enable=0,mobile_object=None,dock_object=None,chip=None,hard_reset=1,fec_main_mode=0,mcm_board=0):
    from regwr import regwr as regwr
    from enable_prox_detect import enable_prox_detect as enable_prox_detect
    from set_biasdac_agc import set_biasdac_agc as set_biasdac_agc
    from cdr_setup import cdr_setup as cdr_setup
    from bset import bset as bset
    from set_agc_tar_ed import set_agc_tar_ed as set_agc_tar_ed
    from config_synth import config_synth as config_synth
    from set_dbgmux_static import set_dbgmux_static as set_dbgmux_static
    from check_sm import check_sm as check_sm
    from monitor_checker import monitor_checker as monitor_checker
    from extractbits import extractbits as extractbits
    from bin2dec import bin2dec as bin2dec
    from bget import bget as bget
    from txbb_filter_max import txbb_filter_max as txbb_filter_max
    from set_txp_tar_pd2 import set_txp_tar_pd2 as set_txp_tar_pd2
    fec_main_demo_board = 0
    i2c_tunneling_testing = 0
    if hard_reset:
        mobile_object.SendTenCmd('ss_reset')
        dock_object.SendTenCmd('ss_reset')
    # enable I2C writes
    regwr('0x76','0x1',mobile_object,chip)
    regwr('0x76','0x1',dock_object,chip)
    
    enable_prox_detect(mobile_object, checker_enable, 0,chip)
    enable_prox_detect(dock_object, checker_enable, 0,chip)   
    
    if fec_main_mode:
        set_biasdac_agc(27,mobile_object,chip)
        set_biasdac_agc(33,dock_object,chip)
        cdr_setup(mobile_object, chip,10)
        cdr_setup(dock_object, chip,0)    
    else:
        if checker_enable:
            set_biasdac_agc(57,mobile_object,chip)
            set_biasdac_agc(57,dock_object,chip)
            cdr_setup(mobile_object, chip,20)
            cdr_setup(dock_object, chip,10)  
        else:
            set_biasdac_agc(23,mobile_object,chip)
            set_biasdac_agc(26,dock_object,chip)
            cdr_setup(mobile_object, chip,27)
            cdr_setup(dock_object, chip,27)      
            
    if fec_main_demo_board:
        set_biasdac_agc(26,mobile_object,chip)
        set_biasdac_agc(30,dock_object,chip)
        cdr_setup(mobile_object, chip,32)
        cdr_setup(dock_object, chip,32)   
        bset('wlink_force_on', '1', mobile_object,chip) # the demo board isn't running USB, so don't allow to go to sleep.  
        bset('wlink_force_on', '1', dock_object,chip)
        
    if mcm_board:
        set_biasdac_agc(58,mobile_object,chip)
        set_biasdac_agc(62,dock_object,chip)
        cdr_setup(mobile_object,chip,32)
        cdr_setup(dock_object,chip,32) 
        bset('wlink_force_on', '1', mobile_object,chip) #the demo board isn't running USB, so don't allow to go to sleep.  
        bset('wlink_force_on', '1', dock_object,chip)
        txbb_filter_max(dock_object,chip)
        txbb_filter_max(mobile_object,chip)
        set_txp_tar_pd2(140, mobile_object,chip)
        set_txp_tar_pd2(140, dock_object,chip)        
               
    
    # run synth in open loop     
    config_synth(3,mobile_object,chip)
    config_synth(3,dock_object,chip) 
    
    # enable the CDR DETOUT pins
    bset('cdrbuf_en_detoutbuf','1',mobile_object,chip)
    bset('cdrbuf_en_detoutbuf','1',dock_object,chip)    
    
    # put the prox SM into reset (this will reset all of the state machines:
    bset('prox_rst', '1', mobile_object,chip)
    bset('prox_rst', '1', dock_object,chip)            
    
    print 'Turning off all digital I/O'
    # hold all digital I/O static
    set_dbgmux_static(dock_object,chip)
    set_dbgmux_static(mobile_object,chip)    
    
    # CDR equalizer settings:
    bset('reg_cdr_eq_ctl', '00100000', mobile_object,chip)
    bset('reg_cdr_eq_ctl', '00100000', dock_object,chip)  
    
    if fec_main_mode:
        bset('frm_structure', '01', mobile_object,chip)
        bset('frm_structure', '01', dock_object,chip)
    else:
        bset('frm_structure', '10', mobile_object,chip)
        bset('frm_structure', '10', dock_object,chip)
    
    bset('prox_rst', '0', mobile_object,chip)
    bset('prox_rst', '0', dock_object,chip)   
    
    # readback VCO cal code
    print 'Mobile VCO cal: %d\n' % extractbits(bin2dec(bget('lo_dyn_synth_cal_out',mobile_object,chip)),0,5)
    print 'Dock VCO cal: %d\n' % extractbits(bin2dec(bget('lo_dyn_synth_cal_out',dock_object,chip)),0,5)
        
    # readback sleep osc cal code
    print 'Mobile sleeposc cal: %d\n' % int(bin2dec(bget('sleeposc_code_out',mobile_object,chip)))
    print 'Dock sleeposc cal: %d\n' % int(bin2dec(bget('sleeposc_code_out',dock_object,chip)))    
    
    print '--- Checking Mobile SMs ---'
    check_sm(mobile_object,chip)
    print '--- Checking Dock SMs ---'
    check_sm(dock_object,chip)   
    
    monitor_checker(10, mobile_object, dock_object,chip)
    
    
from start_swam3_mobile import start_swam3_mobile as start_swam3_mobile
from start_swam3_dock import start_swam3_dock as start_swam3_dock
import Chip
chip = Chip.Chip()
mobile = start_swam3_mobile('COM10')
dock = start_swam3_dock('COM14')
full_link_bringup_6g(1,mobile,dock,chip,mcm_board=1)