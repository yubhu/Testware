def regrd(register,swam3_object,chip):
    "This function takes the argument (register_name,swam3_object)"
    import lookup_address
    from call_i2c_dbgrd import call_i2c_dbgrd as call_i2c_dbgrd
    if '0x' in register:
        address_0x = register
    else:
        address_0x = lookup_address.lookup_address(register,chip)
    value_0x = call_i2c_dbgrd(address_0x,swam3_object)
    return value_0x