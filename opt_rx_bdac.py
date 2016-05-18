def opt_rx_bdac(rx_bdac,swam3_object,reset_between_searches,chip):
    from datapath_restart_rx import datapath_restart_rx as datapath_restart_rx
    from set_biasdac_agc import set_biasdac_agc as set_biasdac_agc
    from get_sync_to_own_link_status import get_sync_to_own_link_status as get_sync_to_own_link_status
    from bin2dec import bin2dec as bin2dec
    from bget import bget as bget
    from monitor_checker import monitor_checker as monitor_checker
    import matplotlib.pyplot as pyplot
    from force_sm_on import force_sm_on as force_sm_on
    from STAT_opt_rx_bdac import STAT_opt_rx_bdac as STAT_opt_rx_bdac
    
    bch_err_cnt = [float('nan')]*len(rx_bdac)
    checker_error_counter = [float('nan')]*len(rx_bdac)
    fd_sync_lost_cnt = [float('nan')]*len(rx_bdac)
    sync_to_own_link = [float('nan')]*len(rx_bdac)
    cdr_offset = [float('nan')]*len(rx_bdac)
    
    if reset_between_searches:
        force_sm_on(swam3_object,None,chip)
    
    print 'RX BDAC = '
    for index,item in enumerate(rx_bdac):
        if reset_between_searches:
            datapath_restart_rx(swam3_object,chip)
        print '%d ..' % rx_bdac[index]
        set_biasdac_agc(rx_bdac[index],swam3_object,chip)
        sync_to_own_link[index] = get_sync_to_own_link_status(swam3_object,chip)
        cdr_offset[index] = int(bin2dec(bget('cdrbuf_offsetdac_out',swam3_object,chip)))
        print 'biasdac_agc=%d, cdr_offset=%d\n' % (rx_bdac[index],cdr_offset[index])
        stat1 = monitor_checker(10,swam3_object,None,1,chip)[0]
        pyplot.close()
        x = (stat1.bch_err_cnt[-1]-stat1.bch_err_cnt[0])/(stat1.time[-1]-stat1.time[0])
        if x>=0 and x<=10**6:
            bch_err_cnt[index] = x
        x = (stat1.checker_error_counter[-1]-stat1.checker_error_counter[0])/(stat1.time[-1]-stat1.time[0])
        if x>=0 and x<=10**4:
            checker_error_counter[index] = x
        x = (stat1.fd_sync_lost_cnt[-1] - stat1.fd_sync_lost_cnt[0])/(stat1.time[-1]-stat1.time[0])
        if x>=0:
            fd_sync_lost_cnt[index] = x
        pyplot.subplot(2,1,1)
        pyplot.plot(rx_bdac,bch_err_cnt)
        pyplot.title('bch_err_cnt')
        pyplot.ylabel('err/sec')
        pyplot.grid()
        pyplot.subplot(2,1,2)
        pyplot.plot(rx_bdac,checker_error_counter)
        pyplot.title('checker_error_counter')
        pyplot.ylabel('err/sec')
        pyplot.xlabel('RX BDAC')
        pyplot.grid()    
        
    print '\n'
    data = STAT_opt_rx_bdac()
    data.rx_bdac = rx_bdac
    data.bch_err_cnt = bch_err_cnt
    data.checker_error_counter = checker_error_counter
    data.fd_sync_lost_cnt = fd_sync_lost_cnt
    data.sync_to_own_link = sync_to_own_link
    data.cdr_offset = cdr_offset   
    
    min_index = checker_error_counter.index(min(checker_error_counter))
    data.rx_bdac_opt = rx_bdac[min_index]
    data.bch_err_cnt_opt = bch_err_cnt[min_index]
    data.checker_error_counter_opt = checker_error_counter[min_index]
    data.cdr_offset_opt = cdr_offset[min_index]  
    
    print 'Setting RX BDAC = %d\n' % data.rx_bdac_opt
    set_biasdac_agc(data.rx_bdac_opt,swam3_object,chip)
    return data
    
        
    
    
    