def bringup_6g_usb(checker_enable, swam3_object1, swam3_object2, mobile_rx_bdac, dock_rx_bdac, mobile_txp_tar, dock_txp_tar, m3G_en, m3G_use_tune_values, mobile_cdr_thresh, dock_cdr_thresh, force_cdr_thresh, detout_en,chip):
    from enable_prox_detect import enable_prox_detect as enable_prox_detect
    from set_txp_tar_pd2 import set_txp_tar_pd2 as set_txp_tar_pd2
    from set_biasdac_agc import set_biasdac_agc as set_biasdac_agc
    from cdr_setup import cdr_setup as cdr_setup
    from bset import bset as bset
    from regwr import regwr as regwr
    import time
    from get_sync_to_own_link_status import get_sync_to_own_link_status as get_sync_to_own_link_status
    from monitor_checker import monitor_checker as monitor_checker
    
    if mobile_txp_tar == None:
        mobile_txp_tar = 120
        
    if dock_txp_tar == None:
        dock_txp_tar = 120
        
    if m3G_en == None:
        m3G_en = 0
        
    if m3G_use_tune_values == None:
        m3G_use_tune_values = 0
        
    if mobile_cdr_thresh == None:
        mobile_cdr_thresh = 10
        
    if dock_cdr_thresh == None:
        dock_cdr_thresh = 10
        
    if force_cdr_thresh == None:
        force_cdr_thresh = 0
        
    if detout_en == None:
        detout_en = 0
        
    m8b10b = 0
    swam3_object1.SendTenCmd('ss_reset',silent='yes')
    swam3_object2.SendTenCmd('ss_reset',silent='yes')    
    
    enable_prox_detect(swam3_object1, checker_enable, m8b10b, m3G_en,chip)
    enable_prox_detect(swam3_object2, checker_enable, m8b10b, m3G_en,chip)
    set_txp_tar_pd2(mobile_txp_tar, swam3_object1,chip)
    set_txp_tar_pd2(dock_txp_tar, swam3_object2,chip) 
    
    if m3G_en == 0 or m3G_use_tune_values:
        set_biasdac_agc(mobile_rx_bdac, swam3_object1,chip)
        set_biasdac_agc(dock_rx_bdac, swam3_object2,chip)

    
    if force_cdr_thresh:
        cdr_setup(swam3_object2, dock_cdr_thresh,chip)
        cdr_setup(swam3_object1, mobile_cdr_thresh,chip)

    
    if detout_en:
        # enable the CDR DETOUT pins
        print'Enabling the DETOUT pins.'
        bset('cdrbuf_en_detoutbuf','1',swam3_object1,chip)
        bset('cdrbuf_en_detoutbuf','1',swam3_object2,chip)

    
    #reduce the mobile sleep timer:
    regwr('0x200', '0xa', swam3_object1,chip)
    
    #release prox from reset:
    bset('prox_rst', '0', swam3_object1,chip)
    bset('prox_rst', '0', swam3_object2,chip)
    
    time.sleep(2)
    get_sync_to_own_link_status(swam3_object2,chip)
    get_sync_to_own_link_status(swam3_object1,chip)
    link_status = monitor_checker(15, swam3_object1, swam3_object2,1,chip)  
    return link_status
