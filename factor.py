def factor(dec_input):
    import math
    dec_input = int(dec_input)
    elem = []
    prime_factor = []
    for i in range(2,dec_input+1):
        if dec_input%i==0:
            elem.append(i)
    for item in elem:
        if item>=2:
            if item==2:
                prime_factor.append(item)
                continue
            if item%2 ==0 and item>2:
                continue
            for i in range(3,int(math.sqrt(item))+1):
                if item%i==0:
                    break
            else:
                prime_factor.append(item)
    return prime_factor

