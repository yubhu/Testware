def get_sync_to_own_link_status(swam3_object,chip):
    from bin2dec import bin2dec as bin2dec
    from bget import bget as bget
    from factor import factor as factor
    
    local_chip_id = bin2dec(bget('tx_wlm_r5', swam3_object,chip))
    local_pkg_type_register = bin2dec(bget('tx_wlm_r0', swam3_object,chip))  
   
    
    if (factor(local_pkg_type_register)[0]-2):
        local_pkg_type = 1
    else:
        local_pkg_type = 0

    
    remote_chip_id = bin2dec(bget('remote_slingshot_d_chip_id', swam3_object, chip))
    remote_pkg_type_register = bin2dec(bget('remote_wireless_stat', swam3_object, chip))  

    
    if (factor(remote_pkg_type_register)[0]-2):
        remote_pkg_type = 1
    else:
        remote_pkg_type = 0

        
    if local_pkg_type == remote_pkg_type and local_chip_id == remote_chip_id:
        sync_to_own_link = 1
        print 'Link is self-coupling.'
    else:
        sync_to_own_link = 0
    return sync_to_own_link