class STAT_Monitor(object):
    def __init__(self):
        self.init = None
        self.fd_bitcnt_wrap = 0
        self.fd_bitcnt_Gb_wrap = 0
        self.fd_sync_lost_cnt_wrap = 0
        self.bch_err_cnt_wrap = 0
        self.checker_error_counter_wrap = 0
        self.fd_bitcnt_last = 0
        self.fd_bitcnt_Gb_last = 0
        self.fd_sync_lost_cnt_last = 0
        self.bch_err_cnt_last = 0
        self.checker_error_counter_last = 0
        self.time = []
        self.fd_bitcnt = []
        self.fd_bitcnt_Gb = []
        self.fd_sync_lost_cnt = []
        self.bch_err_cnt = []
        self.checker_error_counter = []        