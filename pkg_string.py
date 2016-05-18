def pkg_string(pkg_type):
    if pkg_type == 0:
        return '6210A'
    elif pkg_type == 1:
        return '6211A'
    elif pkg_type == 2:
        return '6212A'
    elif pkg_type == 3:
        return '6213A'
    elif pkg_type == 4:
        return '6210B'
    elif pkg_type == 5:
        return '6211B'
    elif pkg_type == 6:
        return '6212B'
    elif pkg_type == 7:
        return '6213B'
    elif pkg_type == 8:
        return '6210C'
    elif pkg_type == 9:
        return '6211C'
    elif pkg_type == 10:
        return '6212C'
    elif pkg_type == 11:
        return '6213C'
    else:
        return 'unrecognized package'