def extractbits(x,base,count):
    op1 = int(x)/pow(2,base)
    op2 = pow(2,count)
    return op1%op2
    