def set_pll1_bypass(bEnable,swam3_object,chip):
    from get_chip_revision import get_chip_revision as get_chip_revision
    from bset import bset as bset
    if get_chip_revision(swam3_object,chip)>=2:
        if bEnable:
            # enable PLL1 bypass mode
            # selection mux (between crystal clock and PLL1 output) and also reconfigures PLL2 predivider
            bset('reg_p1_ctl_1','01000000',swam3_object,chip)
                    
            # disable PLL1
            bset('reg_p1_pdb','0',swam3_object,chip)
                    
            # bias tuning to align settings with those assumed in simulation
            # likely not essential, since we know PLL2 functions in cascade mode with the default value.
            bset('reg_cdr_pll_vcocal','1000',swam3_object,chip)  
        else:
            # enable PLL1
            bset('reg_p1_pdb','1',swam3_object,chip)
                   
            # disable PLL1 bypass mode
            # selection mux (between crystal clock and PLL1 output) and also reconfigures PLL2 predivider
            bset('reg_p1_ctl_1','00000000',swam3_object,chip)
                   
            # bias tuning - set to POR default
            bset('reg_cdr_pll_vcocal','0000',swam3_object,chip)  
        return True
    else:
        print 'WARNING: rev2 required for PLL1 bypass'
        return False
    