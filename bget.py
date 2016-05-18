def bget(field_name,swam3_object,chip):
    "Returns the bits from the field_name"
    import lookup_field
    reg_addr_0x,reg_bit_first,reg_bit_second = lookup_field.lookup_field(field_name,chip)
    bit_start = 8 - max(reg_bit_first,reg_bit_second)  #Here '8' is the register length
    bit_stop = 8 - min(reg_bit_first,reg_bit_second)
    import call_i2c_dbgrd
    reg_val = call_i2c_dbgrd.call_i2c_dbgrd(reg_addr_0x,swam3_object) #in '0xab' mode
    import hex2bin
    reg_val_bin = hex2bin.hex2bin(reg_val)  #result in '01010101' mode
    return reg_val_bin[bit_start-1:bit_stop]