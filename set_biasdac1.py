def set_biasdac1(field,val,swam3_object,chip):
    from dec2bin import dec2bin as dec2bin
    from bset import bset as bset
    from bset_str import bset_str as bset_str
    from extractbits import extractbits as extractbits
    from bget import bget as bget
    from bin2dec import bin2dec as bin2dec
    
    # biasdac1<5:0>     : pa4 (cc100)
    # biasdac1<11:6>    : pa5 (cc20)
    # biasdac1<17:12>   : pa6 (cc100)
    # biasdac1<23:18>   : txmix (cg100) - atb_testIcg100
    # biasdac1<29:24>   : lobuf1 (cg100)
    # biasdac1<35:30>   : lobuf2 (cg100)
    # biasdac1<41:36>   : lobuf3 (cc20) - atb_testIcc20
    
    biasdac1 = dec2bin(0,42)   # set default to 0    
    field = field.lower()
    if field == 'biasdac1_override':
        bset(field,dec2bin(val,1),swam3_object,chip)
    elif field == 'pa4':
        biasdac1 = bset_str(biasdac1,0,bget('biasdac1_07_00',swam3_object,chip))
        biasdac1 = bset_str(biasdac1,0,dec2bin(val,6))
        bset('biasdac1_07_00',dec2bin(extractbits(bin2dec(biasdac1),0,8),8),swam3_object,chip)    
    elif field == 'pa5':
        biasdac1 = bset_str(biasdac1,0,bget('biasdac1_07_00',swam3_object,chip))
        biasdac1 = bset_str(biasdac1,8,bget('biasdac1_15_08',swam3_object,chip))
        biasdac1 = bset_str(biasdac1,6,dec2bin(val,6))
        bset('biasdac1_07_00',dec2bin(extractbits(bin2dec(biasdac1),0,8),8),swam3_object,chip)
        bset('biasdac1_15_08',dec2bin(extractbits(bin2dec(biasdac1),8,8),8),swam3_object,chip)   
    elif field == 'pa6':
        biasdac1 = bset_str(biasdac1,8,bget('biasdac1_15_08',swam3_object,chip))
        biasdac1 = bset_str(biasdac1,16,bget('biasdac1_23_16',swam3_object,chip))
        biasdac1 = bset_str(biasdac1,12,dec2bin(val,6))
        bset('biasdac1_15_08',dec2bin(extractbits(bin2dec(biasdac1),8,8),8),swam3_object,chip)
        bset('biasdac1_23_16',dec2bin(extractbits(bin2dec(biasdac1),16,8),8),swam3_object,chip) 
    elif field == 'txmix'+'atb_testicg100' or field == 'atb_testicg100' + 'txmix':
        biasdac1 = bset_str(biasdac1,16,bget('biasdac1_23_16',swam3_object,chip))
        biasdac1 = bset_str(biasdac1,18,dec2bin(val,6))
        bset('biasdac1_23_16',dec2bin(extractbits(bin2dec(biasdac1),16,8),8),swam3_object,chip)   
    elif field == 'lobuf1':
        biasdac1 = bset_str(biasdac1,24,bget('biasdac1_31_24',swam3_object,chip))
        biasdac1 = bset_str(biasdac1,24,dec2bin(val,6))
        bset('biasdac1_31_24',dec2bin(extractbits(bin2dec(biasdac1),24,8),8),swam3_object,chip)    
    elif field == 'lobuf2':
        biasdac1 = bset_str(biasdac1,24,bget('biasdac1_31_24',swam3_object,chip))
        biasdac1 = bset_str(biasdac1,32,bget('biasdac1_39_32',swam3_object,chip))
        biasdac1 = bset_str(biasdac1,30,dec2bin(val,6))
        bset('biasdac1_31_24',dec2bin(extractbits(bin2dec(biasdac1),24,8),8),swam3_object,chip)
        bset('biasdac1_39_32',dec2bin(extractbits(bin2dec(biasdac1),32,8),8),swam3_object,chip) 
    elif field == 'lobuf3'+'atb_testicc20' or field == 'atb_testicc20'+'lobuf3':
        biasdac1 = bset_str(biasdac1,32,bget('biasdac1_39_32',swam3_object,chip))
        biasdac1 = bset_str(biasdac1,40,bget('biasdac1_41_40',swam3_object,chip))
        biasdac1 = bset_str(biasdac1,36,dec2bin(val,6))
        bset('biasdac1_39_32',dec2bin(extractbits(bin2dec(biasdac1),32,8),8),swam3_object,chip)
        bset('biasdac1_41_40',dec2bin(extractbits(bin2dec(biasdac1),40,2),2),swam3_object,chip) 
    else:
        print 'Incorrect field name:%s' %field
    