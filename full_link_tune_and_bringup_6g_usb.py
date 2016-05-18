def full_link_tune_and_bringup_6g_usb(chip,swam3_object1,swam3_object2,mobile_txp_tar,dock_txp_tar,mobile_coarse_search_array,dock_coarse_search_array,m3G_en=0,coarse_search_cdr_val=5,force_cdr_val=0,detout_en=0):
    from STAT_full_link import STAT_full_link as STAT_full_link
    from enable_prox_detect import enable_prox_detect as enable_prox_detect
    from set_txp_tar_pd2 import set_txp_tar_pd2 as set_txp_tar_pd2
    from bset import bset as bset
    from bget import bget as bget
    import time
    from bin2dec import bin2dec as bin2dec
    from cdr_setup import cdr_setup as cdr_setup
    from regwr import regwr as regwr
    from force_sm_on import force_sm_on as force_sm_on
    from search_opt_bdac import search_opt_bdac as search_opt_bdac
    from median import median as median
    from find import find as find
    from set_biasdac_agc import set_biasdac_agc as set_biasdac_agc
    from bringup_6g_usb import bringup_6g_usb as bringup_6g_usb
    import numpy
    
    link_status = STAT_full_link()
    link_status.mobile_rx_bdac = []
    link_status.dock_rx_bdac = []
    link_status.mobile_prox_failed = 0
    link_status.dock_prox_failed = 0    
    
    if mobile_txp_tar == None:
        mobile_txp_tar = 120
        
    if dock_txp_tar == None:
        dock_txp_tar = 120
        
    if mobile_coarse_search_array == None:
        mobile_coarse_search_array = range(15,61,3)
        
    if dock_coarse_search_array == None:
        dock_coarse_search_array = range(15,61,3)
        
    if m3G_en == None:
        m3G_en = 0
        
    if coarse_search_cdr_val == None:
        coarse_search_cdr_val = 5
        
    if force_cdr_val == None:
        force_cdr_val = 0
        
    if detout_en == None:
        detout_en = 0
        
    hard_reset = 1
    if hard_reset:
        swam3_object1.SendTenCmd('ss_reset',silent='yes')
        swam3_object2.SendTenCmd('ss_reset',silent='yes')
        
    if m3G_en:
        checker_enable = 1
    else:
        checker_enable = 0
        
    m8b10b = 0
    enable_prox_detect(swam3_object1, checker_enable, m8b10b, m3G_en,chip)
    enable_prox_detect(swam3_object2, checker_enable, m8b10b, m3G_en,chip)
    set_txp_tar_pd2(mobile_txp_tar,swam3_object1,chip)
    set_txp_tar_pd2(mobile_txp_tar,swam3_object2,chip)
    
    bset('tx6g_disable_timeout', '1', swam3_object1,chip)
    bset('tx6g_disable_timeout', '1', swam3_object2,chip)
    bset('link_lost_cnt_1', '11111111', swam3_object2,chip)
    bset('link_lost_cnt_0', '11111111', swam3_object2,chip)
    bset('link_lost_cnt_1', '11111111', swam3_object1,chip)
    bset('link_lost_cnt_0', '11111111', swam3_object1,chip)   
    
    bset('prox_rst', '0', swam3_object1,chip)
    bset('prox_rst', '0', swam3_object2,chip)
    time.sleep(1)
    
    print 'checking prox detect'
    
    prox_fail_mobile_side = 1
    prox_fail_dock_side = 1
    
    for i in range(100):
        if int(bin2dec(bget('prox_sm',swam3_object1,chip))) == 7:
            prox_fail_mobile_side = 0
            
    for i in range(100):
        if int(bin2dec(bget('prox_sm',swam3_object2,chip))) == 7:
            prox_fail_dock_side = 0    
            
    if prox_fail_mobile_side == 1:
        print 'Error: prox is failing on the mobile side!'
        link_status.mobile_prox_failed = 1
        
    if prox_fail_dock_side == 1:
        print 'Error: prox is failing on the dock side!'
        link_status.dock_prox_failed = 1    
        
    if prox_fail_mobile_side or prox_fail_dock_side:
        return
    
    print 'prox detect passed'
    
    
    swam3_object1.SendTenCmd('ss_reset',silent='yes')
    swam3_object2.SendTenCmd('ss_reset',silent='yes')
    
    enable_prox_detect(swam3_object1, checker_enable, m8b10b, m3G_en,chip)
    enable_prox_detect(swam3_object2, checker_enable, m8b10b, m3G_en,chip)
    set_txp_tar_pd2(mobile_txp_tar, swam3_object1,chip)
    set_txp_tar_pd2(dock_txp_tar, swam3_object2,chip)
    
    if force_cdr_val:
        cdr_setup(swam3_object1, coarse_search_cdr_val,chip) #force the CDR during the coarse search:
        cdr_setup(swam3_object2, coarse_search_cdr_val,chip) 
        
    bset('prox_byp', '1', swam3_object1,chip)
    bset('prox_byp', '1', swam3_object2,chip)    
    
    bset('tx6g_disable_timeout', '1', swam3_object1,chip)
    bset('tx6g_disable_timeout', '1', swam3_object2,chip)    
    
    if detout_en:
        print 'Enabling the DETOUT pins.'
        bset('cdrbuf_en_detoutbuf','1',swam3_object1,chip)
        bset('cdrbuf_en_detoutbuf','1',swam3_object2,chip) 
        
    print '========= 6. PRBS seed: 0xFD55\n'
    regwr('0xEF','0xFD',swam3_object1,chip)
    regwr('0xEE','0x55',swam3_object1,chip)
    regwr('0xEF','0xFD',swam3_object2,chip)
    regwr('0xEE','0x55',swam3_object2,chip)    
    
    bset('prox_rst', '0', swam3_object1,chip)
    bset('prox_rst', '0', swam3_object2,chip)  
    
    time.sleep(2)
    
    force_sm_on(swam3_object1, swam3_object2,chip)
    
    print 'search for optimum BDAC for mobile:'
    
    mobile_link_status = search_opt_bdac(swam3_object1, mobile_coarse_search_array, m3G_en,chip)
    
    if m3G_en:
        if not (False in numpy.isnan(mobile_link_status.rx_bdac.checker_error_counter)):
            print 'Error: No valid bdac value for Mobile side'
            return
        else:
            min_value = min(mobile_link_status.rx_bdac.checker_error_counter)
            M = int(median(find(mobile_link_status.rx_bdac.checker_error_counter,min_value))) 
    else:
        if not (False in numpy.isnan(mobile_link_status.rx_bdac.bch_err_cnt)):
            print 'Error: No valid bdac value for Mobile side'
            return        
        else:
            min_value = min(mobile_link_status.rx_bdac.bch_err_cnt)
            M = int(median(find(mobile_link_status.rx_bdac.bch_err_cnt,min_value)))    
            
    mobile_opt_bdac = mobile_link_status.rx_bdac_search - 3 + M
    link_status.mobile_rx_bdac = mobile_opt_bdac
    print 'optimum value for Mobile BDAC = %d' % mobile_opt_bdac
    
    
    print 'search for optimum BDAC for dock:'
        
    dock_link_status = search_opt_bdac(swam3_object2, dock_coarse_search_array, m3G_en,chip)
        
    if m3G_en:
        if not (False in numpy.isnan(dock_link_status.rx_bdac.checker_error_counter)):
            print 'Error: No valid bdac value for Dock side'
            return
        else:
            min_value = min(dock_link_status.rx_bdac.checker_error_counter)
            M = int(median(find(dock_link_status.rx_bdac.checker_error_counter,min_value))) 
    else:
        if not (False in numpy.isnan(dock_link_status.rx_bdac.bch_err_cnt)):
            print 'Error: No valid bdac value for Dock side'
            return        
        else:
            min_value = min(dock_link_status.rx_bdac.bch_err_cnt)
            M = int(median(find(dock_link_status.rx_bdac.bch_err_cnt,min_value)))    
                
    dock_opt_bdac = dock_link_status.rx_bdac_search - 3 + M
    link_status.dock_rx_bdac = dock_opt_bdac
    print 'optimum value for Dock BDAC = %d' % dock_opt_bdac    
    
    set_biasdac_agc(mobile_opt_bdac, swam3_object1,chip)
    set_biasdac_agc(dock_opt_bdac, swam3_object2,chip)    
    
    time.sleep(1)
    
    dock_cdr_offset = int(bin2dec(bget('cdrbuf_offsetdac_out', swam3_object2,chip)))
    mobile_cdr_offset = int(bin2dec(bget('cdrbuf_offsetdac_out', swam3_object1,chip)))    
    
    checker_enable = 0
    link_status.last_monitor_checker = bringup_6g_usb(checker_enable, swam3_object1, swam3_object2, link_status.mobile_rx_bdac, link_status.dock_rx_bdac, mobile_txp_tar, dock_txp_tar, m3G_en, 1, mobile_cdr_offset, dock_cdr_offset, force_cdr_val, detout_en,chip) #if we've gone through tuning with 3G, use the values!
            
       
    print 'optimum value for Mobile BDAC = %d' % mobile_opt_bdac
    print 'optimum value for Dock BDAC = %d' % dock_opt_bdac
    print 'mobile cdr offset value = %d' % mobile_cdr_offset
    print 'dock cdr offset value = %d' % dock_cdr_offset
    return link_status


from start_swam3_mobile import start_swam3_mobile as start_swam3_mobile
from start_swam3_dock import start_swam3_dock as start_swam3_dock
import Chip
mobile = start_swam3_mobile('COM10')
dock = start_swam3_dock('COM22')
chip = Chip.Chip(host_port=mobile)
full_link_tune_and_bringup_6g_usb(chip,mobile,dock,120, 120, range(21,56,3), range(21,56,3))