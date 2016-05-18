def search_opt_bdac(swam3_object,coarse_search_array,m3G_en,chip):
    from opt_rx_bdac import opt_rx_bdac as opt_rx_bdac
    from cdr_setup import cdr_setup as cdr_setup
    from STAT_search_opt_bdac import STAT_search_opt_bdac as STAT_search_opt_bdac
    from find import find as find
    from median import median as median
    import numpy
    
    if coarse_search_array == None:
        coarse_search_array = range(15,61,3)
        
    if m3G_en == None:
        m3G_en = 0
        
    link_status = STAT_search_opt_bdac()
    link_status.rx_bdac = opt_rx_bdac(coarse_search_array,swam3_object,1,chip)

    
    for index,item in enumerate(link_status.rx_bdac.bch_err_cnt):
        if link_status.rx_bdac.fd_sync_lost_cnt[index] != 0:
            link_status.rx_bdac.bch_err_cnt[index] = float('nan')
            link_status.rx_bdac.checker_error_counter[index] = float('nan')
       
    for index,item in enumerate(link_status.rx_bdac.sync_to_own_link):
        if link_status.rx_bdac.sync_to_own_link[index] == 1:
            link_status.rx_bdac.bch_err_cnt[index] = float('nan')
            link_status.rx_bdac.checker_error_counter[index] = float('nan')        
    
    if m3G_en:
        if not (False in numpy.isnan(link_status.rx_bdac.checker_error_counter)):
            print 'Error: No RX bdac value found that gives acceptable link'
            return
    else:
        if not (False in numpy.isnan(link_status.rx_bdac.bch_err_cnt)):
            print 'Error: No RX bdac value found that gives acceptable link'
            return        
    
    
           
    if m3G_en:
        min_value = min(link_status.rx_bdac.checker_error_counter)
        M = median(find(link_status.rx_bdac.checker_error_counter,min_value))
    else:
        bch_err_cnt_withnonan = []
        for item in link_status.rx_bdac.bch_err_cnt:
            try:
                int(item)
            except ValueError:
                continue
            else:
                bch_err_cnt_withnonan.append(item)
        min_value = min(bch_err_cnt_withnonan)
        M = median(find(link_status.rx_bdac.bch_err_cnt,min_value))  

    
    
    rx_bdac_search = min(coarse_search_array)+(coarse_search_array[1] - coarse_search_array[0])*(M-1)
    
    
    cdr_setup(swam3_object,-1,chip)
    link_status.rx_bdac_search = rx_bdac_search
    print 'checking optimal RX BDAC values:'
    link_status.rx_bdac = opt_rx_bdac(range(rx_bdac_search-(coarse_search_array[1]-coarse_search_array[0]-1),rx_bdac_search+(coarse_search_array[1]-coarse_search_array[0])), swam3_object,1,chip)   #Python not include upper limit
    return link_status