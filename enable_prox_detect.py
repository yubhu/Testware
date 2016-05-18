def enable_prox_detect(swam3_object,checker_enable,m8b10b,m3G_en,chip):
    from get_chip_revision import get_chip_revision as get_chip_revision
    from regwr import regwr as regwr
    from bset import bset as bset
    from set_pll1_bypass import set_pll1_bypass as set_pll1_bypass
    from txbb_filter_max import txbb_filter_max as txbb_filter_max
    chiprev = get_chip_revision(swam3_object,chip)
    regwr('0x76', '0x1', swam3_object,chip) # allow register writes
    regwr('0x214', '0x1', swam3_object,chip)
    regwr('0x75', '0x64', swam3_object,chip) # put prox detect into reset
    if chiprev <2:
        regwr('0xcd','0x04',swam3_object,chip) # LED0 bugfix
        regwr('0xcd','0x05',swam3_object,chip) # LEDO usermode
    if checker_enable:
        if chiprev >=2:
            bset('disable_sync_to_own_link','0',swam3_object,chip) # this doesn't seem to be working
    
    #Bypass PLL1 and power it down; correct error in register default for PLL2 bias type.
    bset('reg_p1_ctl_1','01000000',swam3_object,chip)
    bset('reg_cdr_pll_vcocal','1000',swam3_object,chip)
    bset('reg_p1_pdb','0',swam3_object,chip)
    # bset('reg_cdr_pll_icpcnt','00010');        
    
    # increase 6G timeout, TX at startup (because 6G link isn't working) 
    regwr('0x11e','0xff',swam3_object,chip)
    regwr('0x11b','0xff',swam3_object,chip)
    # increase amount of time we wait after sync lost
    regwr('0x119','0xff',swam3_object,chip)
    regwr('0x11a','0xff',swam3_object,chip)
    
    #equalizer setting from Mark:
    bset('reg_cdr_eq_ctl', '00100000', swam3_object,chip)        
    
    # disable tx6g timeout
    if chiprev<2:
        if m8b10b:
            bset('tx6g_disable_timeout','1',swam3_object,chip)
    regwr('0x20c','0x70',swam3_object,chip) # allow main domain to switch, force i2c on
    regwr('0x20b','0x01',swam3_object,chip) # disable I2C tuneling wakeup
    regwr('0x201','0x0', swam3_object,chip)
    # Dock side fix for prox detect low power (fixed in Rev2)
    if chiprev<2:
        regwr('0x202', '0xff', swam3_object,chip)
        regwr('0x206', '0x00', swam3_object,chip)
        regwr('0x207', '0x00', swam3_object,chip)
    # disable sleep, w2, w3
    if chiprev<2:
        bset('wlink_sleep_en', '0', swam3_object,chip) # this enables sleep -- polarity is reversed
    bset('wlink_w2_en', '0', swam3_object,chip)
    bset('wlink_w3_en', '0', swam3_object,chip)
    bset('wlink_sleep_en', '0', swam3_object,chip)
    if checker_enable:
        if m8b10b or m3G_en:
            # set to prbs
            bset('generator_sel', '00', swam3_object,chip)
            bset('pat_mode_sel', '010', swam3_object,chip)
            bset('duration_sel', '1', swam3_object,chip)
            bset('pattern_test_en', '1', swam3_object,chip)
            bset('fixed_pattern_31_24', '01111000', swam3_object,chip)
            bset('fixed_pattern_23_16', '01010110', swam3_object,chip)
            bset('fixed_pattern_15_08', '00110100', swam3_object,chip)
            bset('fixed_pattern_07_00', '00010010', swam3_object,chip)
        else:
            regwr('0x1e','0x3a',swam3_object,chip) # PRBS pattern, infinite length, before FEC
            regwr('0x2a','0x00',swam3_object,chip) # set first match threshold
            regwr('0x2b','0x0f',swam3_object,chip)
    
    if chiprev>=2:
        if m3G_en:
            bset('frm_structure', '11', swam3_object,chip)
            bset('dpll_control_dec_zn', '010', swam3_object,chip)            
            
    # enable the CDR
    if chiprev<2:
        bset('reg_cdr_pmode','0',swam3_object,chip)
    
    if chiprev>=2:
        bset('disable_led_modulation', '1', swam3_object,chip)
        bset('bitslp_enable', '1', swam3_object,chip); #enable the bitslip fix
        # bset('sync_new_mode', '1', comPort); %enable new 8b10b mode lock
        set_pll1_bypass(1,swam3_object,chip) #bypass PLL
        txbb_filter_max(swam3_object,chip)        
       
    # enable the CDR threshold tracking
    bset('offst_tracking_en_override', '0', swam3_object,chip)
    bset('cdrbuf_test_reserved', '100', swam3_object,chip)
        