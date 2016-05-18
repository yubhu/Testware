def set1V0voltage(voltage,swam3_object):
    from dec2hex import dec2hex as dec2hex
    upperPossibleVoltage = 1.208
    lowerPossibleVoltage = 0.851
    step = (upperPossibleVoltage-lowerPossibleVoltage)/256
    if voltage < upperPossibleVoltage and voltage > lowerPossibleVoltage:
        dac_steps = round((upperPossibleVoltage-voltage)/step)
        hex_value = dec2hex(dac_steps,2)
        upperNibble = hex_value[-2]
        lowerNibble = hex_value[-1]
        i2c_cmd = 'i2c_dac1v0_wr 0x0%s 0x%s0' %(upperNibble,lowerNibble)
        swam3_object.SendTenCmd(i2c_cmd,silent='yes')
        print 'The 1V0 DUT has been set to: %f' %voltage
    else:
        print 'Voltage must be between 1.208V and 0.851V'