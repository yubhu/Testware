def call_i2c_dbgrd(address_0x,swam3_object):
    "This function does the actual job of sending 'i2c_dbgrd 0x..' to swam3 and returns the read out value as 'xx'"
    if '0x' in address_0x:
        i2c_cmd = 'i2c_dbgrd %s' % address_0x
    else:
        print "Invalid address or value!"
        return None    
    read_data = swam3_object.SendTenCmd(i2c_cmd,silent='yes')
    if 'Invalid' in read_data:
        print 'Error when read register!'
        return None
    import re
    pattern = re.compile(r'SS Reg. 0x([0-9a-f]+)=0x([0-9a-f]+)')
    result = pattern.search(read_data)
    return '0x'+result.group(2)