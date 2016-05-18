def array_right_division(list_a,list_b,factor=1):
    list_result = []
    if len(list_a) != len(list_b):
        print 'two list length not equal!'
        return
    for index in range(len(list_a)):
        list_result.append(list_a[index]/factor/list_b[index])
    return list_result
        
    