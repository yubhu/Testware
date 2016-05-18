def call_i2c_dbgwr(address_0x,value_0x,swam3_object):
    "This function does the actual job of sending 'i2c_dbgwr 0x.. 0x..' to swam3"
    if '0x' in address_0x and '0x' in value_0x:
        i2c_cmd = 'i2c_dbgwr %s %s' %(address_0x,value_0x)
    else:
        print "Invalid address or value!"
        return None
    swam3_object.SendTenCmd(i2c_cmd,silent='yes')
    