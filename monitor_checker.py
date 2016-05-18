def monitor_checker(testtime,swam3_object1,swam3_object2,willPlot,chip):
    from STAT_Monitor import STAT_Monitor as STAT_Monitor
    from checker_status import checker_status as checker_status
    import matplotlib.pyplot as pyplot
    from array_right_division import array_right_division as array_right_division
    from calculate_checker_diff import calculate_checker_diff as calculate_checker_diff
    import time    
    
    if swam3_object2 == None:
        bFullDuplex = False
    else:
        bFullDuplex = True
    
    stat1 = STAT_Monitor()
    stat1.init = checker_status(swam3_object1,chip)
    stat1.fd_bitcnt_last = stat1.init.fd_bitcnt
    stat1.fd_bitcnt_Gb_last = stat1.init.fd_bitcnt_Gb
    stat1.fd_sync_lost_cnt_last = stat1.init.fd_sync_lost_cnt
    stat1.bch_err_cnt_last = stat1.init.bch_err_cnt
    stat1.checker_error_counter_last = stat1.init.checker_error_counter
    com1_t0 = stat1.init.time
    if bFullDuplex:
        stat2 = STAT_Monitor()
        stat2.init = checker_status(swam3_object2,chip)
        com2_t0 = stat2.init.time    
        stat2.fd_bitcnt_last = stat2.init.fd_bitcnt
        stat2.fd_bitcnt_Gb_last = stat2.init.fd_bitcnt_Gb
        stat2.fd_sync_lost_cnt_last = stat2.init.fd_sync_lost_cnt
        stat2.bch_err_cnt_last = stat2.init.bch_err_cnt
        stat2.checker_error_counter_last = stat2.init.checker_error_counter        
    else:
        stat2 = None
    
    while time.time() - com1_t0 < testtime:
        time.sleep(1)
        a = checker_status(swam3_object1,chip)
        if a.time - com1_t0 < testtime:
            stat1.time.append(a.time - com1_t0)
            stat1.fd_bitcnt.append(calculate_checker_diff(stat1.init.fd_bitcnt,a.fd_bitcnt,stat1.fd_bitcnt_last,48,stat1.fd_bitcnt_wrap)[0])
            stat1.fd_bitcnt_wrap = calculate_checker_diff(stat1.init.fd_bitcnt,a.fd_bitcnt,stat1.fd_bitcnt_last,48,stat1.fd_bitcnt_wrap)[1]
            
            stat1.fd_bitcnt_Gb.append(calculate_checker_diff(stat1.init.fd_bitcnt_Gb,a.fd_bitcnt_Gb,stat1.fd_bitcnt_Gb_last,18,stat1.fd_bitcnt_Gb_wrap)[0])
            stat1.fd_bitcnt_Gb_wrap = calculate_checker_diff(stat1.init.fd_bitcnt_Gb,a.fd_bitcnt_Gb,stat1.fd_bitcnt_Gb_last,18,stat1.fd_bitcnt_Gb_wrap)[1]  
            
            stat1.fd_sync_lost_cnt.append(calculate_checker_diff(stat1.init.fd_sync_lost_cnt,a.fd_sync_lost_cnt,stat1.fd_sync_lost_cnt_last,8,stat1.fd_sync_lost_cnt_wrap)[0])
            stat1.fd_sync_lost_cnt_wrap = calculate_checker_diff(stat1.init.fd_sync_lost_cnt,a.fd_sync_lost_cnt,stat1.fd_sync_lost_cnt_last,8,stat1.fd_sync_lost_cnt_wrap)[1]              
            
            stat1.bch_err_cnt.append(calculate_checker_diff(stat1.init.bch_err_cnt,a.bch_err_cnt,stat1.bch_err_cnt_last,24,stat1.bch_err_cnt_wrap)[0])
            stat1.bch_err_cnt_wrap = calculate_checker_diff(stat1.init.bch_err_cnt,a.bch_err_cnt,stat1.bch_err_cnt_last,24,stat1.bch_err_cnt_wrap)[1]            
            
            stat1.checker_error_counter.append(calculate_checker_diff(stat1.init.checker_error_counter,a.checker_error_counter,stat1.checker_error_counter_last,24,stat1.checker_error_counter_wrap)[0])
            stat1.checker_error_counter_wrap = calculate_checker_diff(stat1.init.checker_error_counter,a.checker_error_counter,stat1.checker_error_counter_last,24,stat1.checker_error_counter_wrap)[1]   
            
            stat1.fd_bitcnt_last = a.fd_bitcnt
            stat1.fd_bitcnt_Gb_last = a.fd_bitcnt_Gb
            stat1.fd_sync_lost_cnt_last = a.fd_sync_lost_cnt
            stat1.bch_err_cnt_last = a.bch_err_cnt
            stat1.checker_error_counter_last = a.checker_error_counter  
        if bFullDuplex:
            b = checker_status(swam3_object2,chip)
            if b.time - com2_t0 < testtime:
                stat2.time.append(b.time - com2_t0)
                stat2.fd_bitcnt.append(calculate_checker_diff(stat2.init.fd_bitcnt,b.fd_bitcnt,stat2.fd_bitcnt_last,48,stat2.fd_bitcnt_wrap)[0])
                stat2.fd_bitcnt_wrap = calculate_checker_diff(stat2.init.fd_bitcnt,b.fd_bitcnt,stat2.fd_bitcnt_last,48,stat2.fd_bitcnt_wrap)[1]
                        
                stat2.fd_bitcnt_Gb.append(calculate_checker_diff(stat2.init.fd_bitcnt_Gb,b.fd_bitcnt_Gb,stat2.fd_bitcnt_Gb_last,18,stat2.fd_bitcnt_Gb_wrap)[0])
                stat2.fd_bitcnt_Gb_wrap = calculate_checker_diff(stat2.init.fd_bitcnt_Gb,b.fd_bitcnt_Gb,stat2.fd_bitcnt_Gb_last,18,stat2.fd_bitcnt_Gb_wrap)[1]  
                        
                stat2.fd_sync_lost_cnt.append(calculate_checker_diff(stat2.init.fd_sync_lost_cnt,b.fd_sync_lost_cnt,stat2.fd_sync_lost_cnt_last,8,stat2.fd_sync_lost_cnt_wrap)[0])
                stat2.fd_sync_lost_cnt_wrap = calculate_checker_diff(stat2.init.fd_sync_lost_cnt,b.fd_sync_lost_cnt,stat2.fd_sync_lost_cnt_last,8,stat2.fd_sync_lost_cnt_wrap)[1]              
                        
                stat2.bch_err_cnt.append(calculate_checker_diff(stat2.init.bch_err_cnt,b.bch_err_cnt,stat2.bch_err_cnt_last,24,stat2.bch_err_cnt_wrap)[0])
                stat2.bch_err_cnt_wrap = calculate_checker_diff(stat2.init.bch_err_cnt,b.bch_err_cnt,stat2.bch_err_cnt_last,24,stat2.bch_err_cnt_wrap)[1]            
                        
                stat2.checker_error_counter.append(calculate_checker_diff(stat2.init.checker_error_counter,b.checker_error_counter,stat2.checker_error_counter_last,24,stat2.checker_error_counter_wrap)[0])
                stat2.checker_error_counter_wrap = calculate_checker_diff(stat2.init.checker_error_counter,b.checker_error_counter,stat2.checker_error_counter_last,24,stat2.checker_error_counter_wrap)[1]   
                        
                stat2.fd_bitcnt_last = b.fd_bitcnt
                stat2.fd_bitcnt_Gb_last = b.fd_bitcnt_Gb
                stat2.fd_sync_lost_cnt_last = b.fd_sync_lost_cnt
                stat2.bch_err_cnt_last = b.bch_err_cnt
                stat2.checker_error_counter_last = b.checker_error_counter    
        if willPlot:
            if not bFullDuplex:
                pyplot.subplot(2,2,1)
                stat1_Gbps = array_right_division(stat1.fd_bitcnt_Gb,stat1.time,2**30)
                pyplot.plot(stat1.time,stat1_Gbps)
                pyplot.title('fd_bitcnt [%0.2fGb/s]' % stat1_Gbps[-1])
                pyplot.grid()
                pyplot.show()
                pyplot.subplot(2,2,3)
                pyplot.plot(stat1.time,stat1.fd_sync_lost_cnt)
                pyplot.title('fd_sync_lost_cnt [%0.2f/s]' % (stat1.fd_sync_lost_cnt[-1]/stat1.time[-1]))
                pyplot.grid()
                pyplot.show()
                pyplot.subplot(2,2,2)
                stat1_bcherrps = array_right_division(stat1.bch_err_cnt,stat1.time)
                pyplot.plot(stat1.time,stat1_bcherrps)
                pyplot.title('bch_err_cnt [%f/s]' % stat1_bcherrps[-1])
                pyplot.grid()
                pyplot.show()
                pyplot.subplot(2,2,4)
                stat1_checkererrps = array_right_division(stat1.checker_error_counter,stat1.time)
                pyplot.plot(stat1.time,stat1_checkererrps)
                pyplot.title('checker_error_counter [%0.2f/s]' % stat1_checkererrps[-1])
                pyplot.grid() 
                pyplot.show()
            else:
                pyplot.subplot(2,4,1)
                stat1_Gbps = array_right_division(stat1.fd_bitcnt_Gb,stat1.time)
                pyplot.plot(stat1.time,stat1_Gbps)
                pyplot.title('(M) fd_bitcnt [%0.2fGb/s]' % stat1_Gbps[-1])
                pyplot.grid()
                pyplot.show()
                pyplot.subplot(2,4,5)
                pyplot.plot(stat1.time,stat1.fd_sync_lost_cnt)
                pyplot.title('(M) fd_sync_lost_cnt [%0.2f/s]' % (stat1.fd_sync_lost_cnt[-1]/stat1.time[-1]))
                pyplot.grid()
                pyplot.show()
                pyplot.subplot(2,4,2)
                stat1_bcherrps = array_right_division(stat1.bch_err_cnt,stat1.time)
                pyplot.plot(stat1.time,stat1_bcherrps)
                pyplot.title('(M) bch_err_cnt [%f/s]' % stat1_bcherrps[-1])
                pyplot.grid()
                pyplot.show()
                pyplot.subplot(2,4,6)
                stat1_checkererrps = array_right_division(stat1.checker_error_counter,stat1.time)
                pyplot.plot(stat1.time,stat1_checkererrps)
                pyplot.title('(M) checker_error_counter [%0.2f/s]' % stat1_checkererrps[-1])
                pyplot.grid()
                pyplot.show()
                pyplot.subplot(2,4,3)
                stat2_Gbps = array_right_division(stat2.fd_bitcnt_Gb,stat2.time)
                pyplot.plot(stat2.time,stat2_Gbps)
                pyplot.title('(D) fd_bitcnt [%0.2fGb/s]' % stat2_Gbps[-1])
                pyplot.grid() 
                pyplot.show()
                pyplot.subplot(2,4,7)
                pyplot.plot(stat2.time,stat2.fd_sync_lost_cnt)
                pyplot.title('(D) fd_sync_lost_cnt [%0.2f/s]' % (stat2.fd_sync_lost_cnt[-1]/stat2.time[-1]))
                pyplot.grid()  
                pyplot.show()
                pyplot.subplot(2,4,4)
                stat2_bcherrps = array_right_division(stat2.bch_err_cnt,stat2.time)
                pyplot.plot(stat2.time,stat2_bcherrps)
                pyplot.title('(D) bch_err_cnt [%f/s]' % stat2_bcherrps[-1])
                pyplot.grid() 
                pyplot.show()
                pyplot.subplot(2,4,8)
                stat2_checkererrps = array_right_division(stat2.checker_error_counter,stat2.time)
                pyplot.plot(stat2.time,stat2_checkererrps)
                pyplot.title('(D) checker_error_counter [%0.2f/s]' % stat2_checkererrps[-1])
                pyplot.grid() 
                pyplot.show()
    return stat1,stat2
            
            