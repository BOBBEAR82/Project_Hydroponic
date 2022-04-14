import time


class CycleTimeCalculator:
    def __init__(self):      
        self.cycle_inteval_max_ms = 0
        self.cycle_inteval_min_ms = 10000
        self.cycle_interval_init_counter = 5
        self.this_cycle_interval_ms = None
        self.this_cycle_start_time_ms = 0
        
    def get_cycle_start_time_ms(self):
        self.this_cycle_start_time_ms = time.time() * 1000
    
    def running(self):
        self.this_cycle_interval_ms = time.time() * 1000 - self.this_cycle_start_time_ms
        
        if self.cycle_interval_init_counter > 1:   ### this if and elif is for skipping the first several cycles, because found that the the first several cycles the interval is usually longer
            self.cycle_interval_init_counter -= 1
        elif self.cycle_interval_init_counter == 1:
            self.cycle_interval_init_counter -= 1
            self.cycle_inteval_max_ms = self.this_cycle_interval_ms
            self.cycle_inteval_max_ms = self.this_cycle_interval_ms
        else:
            if self.this_cycle_interval_ms > self.cycle_inteval_max_ms:
                self.cycle_inteval_max_ms = self.this_cycle_interval_ms
            if self.this_cycle_interval_ms < self.cycle_inteval_min_ms:
                self.cycle_inteval_min_ms = self.this_cycle_interval_ms 
            #print('cycle duration: {0} ms; \t max cycle time: {1} ms; \t min cycle time: {2} ms'.format(self.this_cycle_interval_ms, self.cycle_inteval_max_ms, self.cycle_inteval_min_ms))



class ActualTime:
    def __init__(self):
        self.actual_time_s = 0
        self.actual_time_ms = 0
        self.actual_time_hour = 0
        self.actual_time_min = 0
        self.actual_time_sec = 0
        self.actual_date = ''
        self.time_display = ''
        
    def get_actual_time(self):
        self.actual_time_s = time.time()
        self.actual_time_ms = self.actual_time_s * 1000
        
        time_object = time.localtime()
        
        self.actual_date = str(time_object.tm_year) + '/' + str(time_object.tm_mon) + '/' + str(time_object.tm_mday)
        
        self.actual_time_hour = time_object.tm_hour
        self.actual_time_min = time_object.tm_min
        self.actual_time_sec = time_object.tm_sec
        
        self.time_display = str(self.actual_time_hour) + ':' + str(self.actual_time_min) + ':' + str(self.actual_time_sec)

