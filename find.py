def find(input_list,value):
    index_list = []
    for index,item in enumerate(input_list):
        if item == value:
            index_list.append(index+1)  #because Matlab starts from 1 while python starts from 0
    return index_list