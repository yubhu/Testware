def calculate_checker_diff(initial_val, curr_val, last_val, numBits, wrap_in):
    max_result = float('nan')
    wrap = wrap_in
    if wrap == 1:
        wrap_result = curr_val - last_val
        if wrap_result < 0:
            result = max_result
            wrap = wrap + 1
        else:
            result = (2**numBits-1 - initial_val) + curr_val
    elif wrap>1:
        result = max_result
    else:
        wrap_result = curr_val - last_val
        if wrap_result <0:
            wrap = 1
            result = (2**numBits-1 - initial_val) + curr_val
        else:
            result = curr_val - initial_val
    return result,wrap