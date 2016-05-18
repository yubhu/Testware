def bin2hex(bin_string):
    "Change '00110011' like string to '0x33' like string"
    import re
    pattern = re.compile(r'[^01]')
    if pattern.search(bin_string):
        return None
    sum_dec = 0
    if len(bin_string)==1:
        return hex(int(bin_string[0]))
    for index in range(len(bin_string)-1):
        sum_dec = (sum_dec + int(bin_string[index]))*2
    sum_dec = sum_dec + int(bin_string[index+1])
    return hex(sum_dec)