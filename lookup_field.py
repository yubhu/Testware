def lookup_field(field_name,chip):
    "Accept field_name and return its register address in '0x' pattern and if its field bit is in a range, return its highest bit positon and lowest bit position"
    if not field_name:
        print "Error! Please input filed name"
        return
    name_upper = field_name.upper()
    #import Chip
    #chip = Chip.Chip()
    if name_upper not in chip.fields:
        print "filed name: %s not in fields!" % name_upper
        return None
    address_0x = chip.fields[name_upper][0]
    field_bits = chip.fields[name_upper][1]
    if ':' in field_bits:
        bit_first = field_bits[0]
        bit_second = field_bits[2]
    else:
        bit_first = field_bits[0]
        bit_second = field_bits[0]
    bit_first = int(bit_first)
    bit_second = int(bit_second)
    return address_0x,bit_first,bit_second
    