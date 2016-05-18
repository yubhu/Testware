def bset_str(oldbinstr,index,binstr):
    n = len(oldbinstr)
    m = len(binstr)
    return oldbinstr[:(n-(index+m))] + binstr + oldbinstr[n-index:]
    