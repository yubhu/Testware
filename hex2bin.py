def hex2bin(hex_string):
    "Change '0x33' like string to '00110011' like string"
    hex_todo = hex_string[2:]
    import re
    pattern = re.compile(r'[^0-9a-fA-F]')
    hex_dict = {'a':10,'b':11,'c':12,'d':13,'e':14,'f':15,'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}
    sum_dec = 0
    if pattern.search(hex_todo):
        return None
    if len(hex_todo)==1:
        if hex_todo[0] in hex_dict:
            return bin(hex_dict[hex_todo[0]])[2:].zfill(8)
        else:
            return bin(int(hex_todo[0]))[2:].zfill(8)
    for index in range(len(hex_todo)-1):
        if hex_todo[index] in hex_dict:
            item_processed = hex_dict[hex_todo[index]]
        else:
            item_processed = int(hex_todo[index])
        sum_dec = (sum_dec + item_processed)*16
    if hex_todo[index+1] in hex_dict:
        item_processed = hex_dict[hex_todo[index+1]]
    else:
        item_processed = int(hex_todo[index+1])
    sum_total = sum_dec + item_processed
    sum_bin = bin(sum_total)[2:]
    sum_bin = sum_bin.zfill(8)
    return sum_bin

    