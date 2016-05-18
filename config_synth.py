def config_synth(tst1,swam3_object,chip):
    "CONFIG_SYNTH - function to force synthesizer to a variety of alternate states that may have a bearing on the observed level of 12MHz disturbance to transmit signal"
    from bset import bset as bset
    from extractbits import extractbits as extractbits
    from bin2dec import bin2dec as bin2dec
    from bget import bget as bget
    from dec2bin import dec2bin as dec2bin
    bset('lo_dyn_pll_en_07_00', '11111111',swam3_object,chip)
    bset('lo_dyn_pll_en_15_08','00001111',swam3_object,chip)
    bset('lo_dyn_pll_en_override','1',swam3_object,chip)
    synthCalCode = extractbits(bin2dec(bget('lo_dyn_synth_cal_out',swam3_object,chip)),0,5)
    synthCalMode = synthCalCode + 32
    if tst1 ==1:
        bset('lo_dyn_pll_en_07_00', '11111101',swam3_object,chip)
        bset('lo_dyn_pll_en_15_08','00001111',swam3_object,chip)
        bset('lo_dyn_pll_en_override','1',swam3_object,chip)
        bset('lo_dyn_n_div_override', '0',swam3_object,chip)
        bset('lo_dyn_synth_cal_override', '0', swam3_object,chip)
    if tst1 ==2:
        bset('lo_dyn_pll_en_07_00', '11111101',swam3_object,chip) # disable vco_cal_clk
        bset('lo_dyn_pll_en_15_08','00001111',swam3_object,chip)
        bset('lo_dyn_pll_en_override','1',swam3_object,chip)
        bset('lo_dyn_n_div_07_00',dec2bin(69,8),swam3_object,chip) # switch to 6mhz ref clk
        bset('lo_dyn_n_div_15_08',dec2bin(6,8),swam3_object,chip)
        bset('lo_dyn_n_div_override', '1',swam3_object,chip)
        bset('lo_dyn_synth_cal',dec2bin(synthCalCode, 8),swam3_object,chip)
        bset('lo_dyn_synth_cal_override', '1', swam3_object,chip)
    if tst1 == 3:
        bset('lo_dyn_pll_en_07_00', '11111001',swam3_object,chip)  # disable vco_cal_clk, cp_en
        bset('lo_dyn_pll_en_15_08','00001111',swam3_object,chip)
        bset('lo_dyn_pll_en_override','1',swam3_object,chip)
        bset('lo_dyn_n_div_07_00',dec2bin(69,8),swam3_object,chip) # switch to 6mhz ref clk
        bset('lo_dyn_n_div_15_08',dec2bin(6,8),swam3_object,chip)
        bset('lo_dyn_n_div_override', '1',swam3_object,chip)
        bset('lo_dyn_synth_cal',dec2bin(synthCalMode, 8),swam3_object,chip)
        bset('lo_dyn_synth_cal_override', '1', swam3_object,chip)
    if tst1 == 4:
        bset('lo_dyn_pll_en_07_00', '11111001',swam3_object,chip)  # disable vco_cal_clk, cp_en
        bset('lo_dyn_pll_en_15_08','00000111',swam3_object,chip)  # disable psca_buf
        bset('lo_dyn_pll_en_override','1',swam3_object,chip)
        bset('lo_dyn_n_div_07_00',dec2bin(69,8),swam3_object,chip) # switch to 6mhz ref clk
        bset('lo_dyn_n_div_15_08',dec2bin(6,8),swam3_object,chip) 
        bset('lo_dyn_n_div_override', '1',swam3_object,chip)
        bset('lo_dyn_synth_cal',dec2bin(synthCalMode, 8),swam3_object,chip)
        bset('lo_dyn_synth_cal_override', '1', swam3_object,chip)  
    if tst1 == 5:
        bset('lo_dyn_pll_en_07_00', '11011001',swam3_object,chip) # disable vco_cal_clk, cp_en, pfd
        bset('lo_dyn_pll_en_15_08','00000111',swam3_object,chip)  # disable psca_buf
        bset('lo_dyn_pll_en_override','1',swam3_object,chip)
        bset('lo_dyn_n_div_07_00',dec2bin(69,8),swam3_object,chip) # switch to 6mhz ref clk
        bset('lo_dyn_n_div_15_08',dec2bin(6,8),swam3_object,chip)
        bset('lo_dyn_n_div_override', '1',swam3_object,chip)
        bset('lo_dyn_synth_cal',dec2bin(synthCalMode, 8),swam3_object,chip)
        bset('lo_dyn_synth_cal_override', '1', swam3_object,chip)    
    if tst1 == 6:
        bset('lo_dyn_pll_en_07_00', '11011000',swam3_object,chip) # disable vco_cal_clk, cp_en, pfd, ref_clk_en
        bset('lo_dyn_pll_en_15_08','00000111',swam3_object,chip)  # disable psca_buf
        bset('lo_dyn_pll_en_override','1',swam3_object,chip)
        bset('lo_dyn_n_div_07_00',dec2bin(69,8),swam3_object,chip) # switch to 6mhz ref clk
        bset('lo_dyn_n_div_15_08',dec2bin(6,8),swam3_object,chip)
        bset('lo_dyn_n_div_override', '1',swam3_object,chip)
        bset('lo_dyn_synth_cal',dec2bin(synthCalMode, 8),swam3_object,chip)
        bset('lo_dyn_synth_cal_override', '1', swam3_object,chip)  
    if tst1 == 7:
        bset('lo_dyn_pll_en_07_00', '11111101',swam3_object,chip)  # disable vco_cal_clk
        bset('lo_dyn_pll_en_15_08','00001111',swam3_object,chip)
        bset('lo_dyn_pll_en_override','1',swam3_object,chip)
        bset('lo_dyn_n_div_07_00',dec2bin(69,8),swam3_object,chip) # switch to 6mhz ref clk
        bset('lo_dyn_n_div_15_08',dec2bin(6,8),swam3_object,chip)
        bset('lo_dyn_n_div_override', '1',swam3_object,chip)
        bset('lo_dyn_synth_cal',dec2bin(synthCalMode, 8),swam3_object,chip) 
        bset('lo_dyn_synth_cal_override', '0', swam3_object,chip) # don't override cal value  
    if tst1 == 8:
        bset('lo_dyn_pll_en_07_00', '11011001',swam3_object,chip)  # disable vco_cal_clk, cp_en, pfd
        bset('lo_dyn_pll_en_15_08','00001111',swam3_object,chip)
        bset('lo_dyn_pll_en_override','1',swam3_object,chip)
        bset('lo_dyn_n_div_07_00',dec2bin(69,8),swam3_object,chip) # switch to 6mhz ref clk
        bset('lo_dyn_n_div_15_08',dec2bin(6,8),swam3_object,chip)
        bset('lo_dyn_n_div_override', '1',swam3_object,chip)
        bset('lo_dyn_synth_cal',dec2bin(synthCalMode, 8),swam3_object,chip)
        bset('lo_dyn_synth_cal_override', '1', swam3_object,chip)     
    if tst1 == 9:
        bset('lo_dyn_pll_en_07_00', '11111101',swam3_object,chip)
        bset('lo_dyn_pll_en_15_08','00001111',swam3_object,chip)
        bset('lo_dyn_pll_en_override','1',swam3_object,chip)
        bset('lo_dyn_n_div_override', '0',swam3_object,chip)
        bset('lo_dyn_synth_cal_override', '0', swam3_object,chip)
        bset('lo_dyn_pll_cfg', '01001100',swam3_object,chip)
        bset('lo_dyn_pll_cfg_override', '1', swam3_object,chip)   
    if tst1 == 10:
        bset('lo_dyn_pll_en_07_00', '11111101',swam3_object,chip)
        bset('lo_dyn_pll_en_15_08','00001111',swam3_object,chip)
        bset('lo_dyn_pll_en_override','1',swam3_object,chip)
        bset('lo_dyn_n_div_override', '0',swam3_object,chip)
        bset('lo_dyn_synth_cal_override', '0', swam3_object,chip)
        bset('lo_dyn_pll_cfg', '01001000',swam3_object,chip) # reduce charge pump current
        bset('lo_dyn_pll_cfg_override', '1', swam3_object,chip)
    if tst1 == 11:
        bset('lo_dyn_pll_en_07_00', '11111101',swam3_object,chip)  # disable vco_cal_clk
        bset('lo_dyn_pll_en_15_08','00001111',swam3_object,chip)
        bset('lo_dyn_pll_en_override','1',swam3_object,chip)
        bset('lo_dyn_n_div_07_00',dec2bin(139,8),swam3_object,chip) # switch to 3MHz ref clk
        bset('lo_dyn_n_div_15_08',dec2bin(14,8),swam3_object,chip)
        bset('lo_dyn_n_div_override', '1',swam3_object,chip)
        bset('lo_dyn_synth_cal',dec2bin(synthCalCode, 8),swam3_object,chip)
        bset('lo_dyn_synth_cal_override', '1', swam3_object,chip)        
                  
        
    
    
    