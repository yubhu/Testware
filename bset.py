def bset(field_name,new_field_bits,swam3_object,chip):
    "Sets the field_name value to the new_field_bits value"
    import re
    pattern = re.compile(r'[^01]')
    if pattern.search(new_field_bits):
        print 'Error, there should no characters other than 0 or 1!'
        return None
    import lookup_field
    reg_address_0x,reg_bit_first,reg_bit_second = lookup_field.lookup_field(field_name,chip)
    bit_start = 8 - max(reg_bit_first,reg_bit_second)  #Here '8' is the register length
    bit_stop = 8 - min(reg_bit_first,reg_bit_second)
    field_length = 1 + bit_stop - bit_start
    if len(new_field_bits)!=field_length:
        print 'number of bits not match!'
        return None
    import call_i2c_dbgrd
    if swam3_object==None:
        reg_val = call_i2c_dbgrd.call_i2c_dbgrd(reg_address_0x,chip.host_port) #in '0xab' mode
    else:
        reg_val = call_i2c_dbgrd.call_i2c_dbgrd(reg_address_0x,swam3_object) #in '0xab' mode
    import hex2bin
    reg_val_bin = hex2bin.hex2bin(reg_val)  #result in '01010101' mode
    reg_val_bin_list = list(reg_val_bin)
    reg_val_bin_list[bit_start-1:bit_stop] = list(new_field_bits)
    reg_val_bin_new = ''.join(reg_val_bin_list) #result in '01010101' mode
    import bin2hex
    reg_val_towrite = bin2hex.bin2hex(reg_val_bin_new) #result in '0xab' mode
    import call_i2c_dbgwr
    if swam3_object==None:
        call_i2c_dbgwr.call_i2c_dbgwr(reg_address_0x,reg_val_towrite,chip.host_port)
    else:
        call_i2c_dbgwr.call_i2c_dbgwr(reg_address_0x,reg_val_towrite,swam3_object)