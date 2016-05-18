def dec2bin(dec_input,nbits=8):
    "str = dec2bin(d) returns the binary representation of d as a string. d must be a nonnegative integer. If d is greater than 2^52, dec2bin might not return an exact representation of d.str = dec2bin(d,n) produces a binary representation with at least n bits."
    bin_list = []
    dec_input = int(dec_input)
    while dec_input >0:
        remain = dec_input%2
        bin_list.append(str(remain))
        dec_input = dec_input/2
    bin_list.reverse()
    if len(bin_list)>=nbits:
        return ''.join(bin_list)
    else:
        bin_str = ''.join(bin_list)
        bin_str = bin_str.zfill(nbits)
        return bin_str
        
    
        