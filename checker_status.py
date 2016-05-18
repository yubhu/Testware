def checker_status(swam3_object,chip):
    "Returns the checker results for 1. fd_bitcnt 2. fd_bitcnt_Gb 3. fd_sync_lost_cnt 4. bch_err_cnt 5. checker_error_counter"
    # Read Bit-Counters, Statistics, etc (GOOD TO PUT IN A SEPARATE ROUTINE THAT CAN BE INVOKED MANUALLY)
    # -->   `REGWR_US(8'h6F, 8'h10); // Freeze I2C_FD_BITCNT; the internal counter goes unabated
    # 1.	`REGRD_DS(8'h6A, value); FD_BITCNT[07:00]=value;
    # 2.	`REGRD_DS(8'h69, value); FD_BITCNT[15:08]=value;
    # 3.	`REGRD_DS(8'h68, value); FD_BITCNT[23:16]=value;
    # 4.	`REGRD_DS(8'h67, value); FD_BITCNT[31:24]=value;
    # 5.	`REGRD_DS(8'h66, value); FD_BITCNT[39:32]=value;
    # 6.	`REGRD_DS(8'h65, value); FD_BITCNT[47:40]=value;
    # -->   `REGWR_US(8'h6F, 8'h00); // Unfreeze I2C_FD_BITCNT 
    # 7.	`REGRD_DS(8'h6B, value); FD_SYNC_LOST_CNT[7:0]=value;
    # 8.	`REGRD_DS(8'h73, value); BCH_ERR_CNT[07:00]=value;
    # 9.	`REGRD_DS(8'h72, value); BCH_ERR_CNT[15:08]=value;
    # 10.	`REGRD_DS(8'h71, value); BCH_ERR_CNT[23:16]=value;
    # 11.	`REGRD_DS(8'h31, value); CHECKER_ERROR_COUNTER[07:00]=value;
    # 12.	`REGRD_DS(8'h30, value); CHECKER_ERROR_COUNTER[15:08]=value;
    # 13.	`REGRD_DS(8'h2F, value); CHECKER_ERROR_COUNTER[23:16]=value;    
    from get_chip_revision import get_chip_revision as get_chip_revision
    from bset import bset as bset
    import time
    from bin2dec import bin2dec as bin2dec
    from dec2bin import dec2bin as dec2bin
    from hex2dec import hex2dec as hex2dec
    from regrd import regrd as regrd
    from regwr import regwr as regwr
    from STAT_checker_status import STAT_checker_status as STAT_checker_status
    captureCounters = regrd('SLINGSHOT32',swam3_object,chip)
    captureCounters = hex2dec(captureCounters)
    captureCounters = hex(int(captureCounters)|4) 
    # record the clock time immediately before the register write
    # Don't use a bset because of variability in the read response time
    # The field does not need to be cleared, it is self clearing
    # by hardware.    
    time.sleep(0.01)
    stat = STAT_checker_status()
    stat.time = time.time()
    regwr('SLINGSHOT32',captureCounters,swam3_object,chip)
    #chiprev = get_chip_revision(swam3_object,chip)
    #bset('capture_counters','1',swam3_object,chip) 
    #bset('capture_counters','0',swam3_object,chip)     
    stat.fd_bitcnt = int(bin2dec(dec2bin(hex2dec(regrd('FD_BITCNT_47_40',swam3_object,chip)),8) + dec2bin(hex2dec(regrd('FD_BITCNT_39_32',swam3_object,chip)),8) + dec2bin(hex2dec(regrd('FD_BITCNT_31_24',swam3_object,chip)),8) + dec2bin(hex2dec(regrd('FD_BITCNT_23_16',swam3_object,chip)),8) + dec2bin(hex2dec(regrd('FD_BITCNT_15_08',swam3_object,chip)),8) + dec2bin(hex2dec(regrd('FD_BITCNT_07_00',swam3_object,chip)),8)))
    
    stat.fd_bitcnt_Gb = int(stat.fd_bitcnt)/pow(2,30)
    
    stat.fd_sync_lost_cnt = int(hex2dec(regrd('FD_SYNC_LOST_CNT',swam3_object,chip)))
    
    stat.bch_err_cnt = int(bin2dec(dec2bin(hex2dec(regrd('BCH_ERR_CNT_23_16',swam3_object,chip)),8) + dec2bin(hex2dec(regrd('BCH_ERR_CNT_15_08',swam3_object,chip)),8) + dec2bin(hex2dec(regrd('BCH_ERR_CNT_07_00',swam3_object,chip)),8)))
    
    stat.checker_error_counter = int(bin2dec(dec2bin(hex2dec(regrd('CHECKER_ERROR_COUNTER_23_16',swam3_object,chip)),8) + dec2bin(hex2dec(regrd('CHECKER_ERROR_COUNTER_15_08',swam3_object,chip)),8) + dec2bin(hex2dec(regrd('CHECKER_ERROR_COUNTER_07_00',swam3_object,chip)),8)))
    
    return stat