def cdr_setup(swam3_object,offsetdac,chip):
    if offsetdac <0:
        offsetdac = 0
    elif offsetdac >63:
        offsetdac = 63
    from bset import bset as bset
    from dec2bin import dec2bin as dec2bin
    # force the power state of the CDR to NORMAL - not necessary anymore?
    # cdr_force_normal(comPort);
    
    # The following fields are relevant to this topic.
    
    # CDR_BUF_5	GENERAL	cdr_para_init_s0	5:0	101010	W	07E3
    # CDR_BUF_2	GENERAL	cdr_thresh_offst_polarity	6	0	W	07E0
    # RF_CTL_23	RFOVERRIDE	cdrbuf_offsetdac	7:2	011111	W	078F
    # RF_CTL_14	RFOVERRIDE	cdrbuf_offsetdac_override	3	0	W	0786
    # RF_CTL_20	RFOVERRIDE	cdrbuf_strobe	2	0	W	078C
    # RF_CTL_12	RFOVERRIDE	cdrbuf_strobe_override	2	0	W	0784
    
    # CDR_BUF_2	GENERAL	offst_tracking_en	4	0	W	07E0
    # CDR_BUF_2	GENERAL	offst_tracking_en_override	5	1	W	07E0    
    # """If you write cdrbuf_offsetdac_override to 1 (and to remove any doubt, cdrbuf_strobe to 1 and cdrbuf_strobe_override to 1) then offset DAC will be forced to midscale 011111.The number 41 originates from cdr_para_init_s0. To enable the tracking loop, setoffst_tracking_en to 1 and possibly cdr_thresh_offst_polarity to 1. But I would not personally choose to try the tracking loop yet. """
    if offsetdac==-1:
        bset('cdrbuf_strobe_override', '0', swam3_object,chip)
        bset('cdrbuf_offsetdac_override', '0', swam3_object,chip)
    else:
        bset('cdrbuf_strobe','1',swam3_object,chip) # latches non-transparent
        bset('cdrbuf_strobe_override','1',swam3_object,chip) # override functional strobe path
        bset('cdrbuf_offsetdac',dec2bin(offsetdac,6),swam3_object,chip) # set the new value
        bset('cdrbuf_offsetdac_override','1',swam3_object,chip)          # use the manual setting
        bset('cdrbuf_strobe','0',swam3_object,chip)                     # latch in new value
        bset('cdrbuf_strobe','1',swam3_object,chip)                      # latches non-transparent.
        # fix the EQ common mode voltage def
        bset('reg_cdr_eq_ctl_aux','11',swam3_object,chip)