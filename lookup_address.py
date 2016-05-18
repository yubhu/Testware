def lookup_address(register,chip):
    "Accepts register input like '0x68' or 'CDR_CTL_12' and return register address"
    if not register:
        print "Error! Please input register name"
        return
    #import Chip
    #chip = Chip.Chip()
    if '0x' in register or '0X' in register:
        return register
    else:
        register_upper = register.upper()
        if register_upper not in chip.addresses:
            print "register: %s not found!" % register_upper
            return
        else:
            return chip.addresses[register_upper]
            