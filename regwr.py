def regwr(register,value_0x,swam3_object,chip):
    "This function takes the argument (register_name, value_0x, swam3_object)"
    import lookup_address
    from call_i2c_dbgwr import call_i2c_dbgwr as call_i2c_dbgwr
    if '0x' in register:
        address_0x = register
    else:
        address_0x = lookup_address.lookup_address(register,chip)
    call_i2c_dbgwr(address_0x,value_0x,swam3_object)