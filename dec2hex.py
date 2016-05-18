def dec2hex(dec_string,nbits=1):
    "Change '33' like string to '0x21' like string"
    dec = int(dec_string)
    hex_initial = hex(dec)
    hex_string = hex_initial[2:]
    if len(hex_string)>=nbits:
        return hex_initial
    else:
        return '0x' + hex_string.zfill(nbits)