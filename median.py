def median(input_list):
    inside_list = input_list[:]
    inside_list.sort()
    length = len(inside_list)
    if length%2==1:
        return inside_list[length/2]
    else:
        middle_low = inside_list[length/2-1]
        middle_high = inside_list[length/2]
        return (middle_low+middle_high)/2
