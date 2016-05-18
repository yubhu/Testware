def get_chip_revision(swam3_object,chip):
    from hex2dec import hex2dec as hex2dec
    from regrd import regrd as regrd
    from extractbits import extractbits as extractbits
    chipid = extractbits(hex2dec(regrd('slingshot_d_chip_id',swam3_object,chip)),0,5)
    chip_id = {16:0.0,17:1.0,18:1.1,19:2.0,20:2.1,21:3.0}
    if chipid in chip_id:
        return chip_id[chipid]
    else:
        return None