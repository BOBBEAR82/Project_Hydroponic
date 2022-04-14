import RPi.GPIO as gpio
import Adafruit_DHT

class DHT:
    def __init__(self, gpio_id = 18):
        self.gpio_id = gpio_id
        self.DHT_sensor = Adafruit_DHT.DHT11
        
        self.humidity = None
        self.temperature = None
        
        self.last_on_time = 0
        self.last_off_time = 0
        
        self.report_enable = 0
        self.report_enable_old = 0
        self.report_retry = 0   ### the DHT read function fails a lot and return None value, so the retry flag and counter is used to allow retry until returning good data
        self.report_retry_counter = 0
        self.report_retry_time_start = 0   ### record the time of last retry, because need to wait at least 2s between two read command 
        self.report_complete_time_start = 0   ### record the time of last successful update, used to calculate when to start next measurement
        self.is_updated = 0   ### used by GUI to update the plot
        
    def running(self, time_actual, minute_actual, time_display):
        self.is_updated = 0
        #if self.report_enable == 0 and (minute_actual == 0 or minute_actual == 30) and time_actual - self.report_complete_time_start > 60:
        if self.report_enable == 0 and time_actual - self.report_complete_time_start > 10:   ### enable the read command after a specific interval after last successful read
            self.report_enable = 1
            #print('Debug: enable triggered, time: ', actual_time_sec, time_actual, self.report_retry_time_start)
            
        if self.report_enable == 1 and self.report_retry_counter > 50:  ### disable the read command if too many failures happen
            self.report_enable = 0
            self.report_complete_time_start = time_actual
            #print('Debug: disable triggered, time: ', actual_time_sec)
            
        if (self.report_enable == 1 and self.report_enable_old == 0) or \
                    (self.report_enable == 1 and self.report_retry == 1 and time_actual - self.report_retry_time_start > 2):   ### command read if enable change to 1 or retry conditon is met
            #print('Debug: time: ', time_actual, DHT_report_retry_time_start, '; status:', DHT_report_enable, DHT_report_enable_old, DHT_report_retry)
            self.humidity, self.temperature = Adafruit_DHT.read(self.DHT_sensor, self.gpio_id)
            #print("Debug: test: ", humidity, temperature, actual_time_sec)
            if self.humidity == None or self.temperature == None:    ### if either humidity or temperature return is None, set allow retry
                self.report_retry = 1
                self.report_retry_time_start = time_actual
                self.report_retry_counter += 1
            else:   ### otherwise update the value and reset the flags and retry counter 
                self.report_enable = 0
                self.report_retry = 0
                #print('Debug: data: ', humidity, temperature, DHT_report_retry_counter, DHT_report_enable, DHT_report_enable_old, DHT_report_retry)
                print(('DHT measure time: ' + '{0},' + '\t' + 'Humidity: ' + '{1} %,' + '\t' + 'Temperature: ' + '{2} degC,' + '\t' * 2 + 'Retry counter: ' + '{3}')
                      .format(time_display, self.humidity, self.temperature, self.report_retry_counter))
                self.report_retry_counter = 0
                self.report_complete_time_start = time_actual
                self.is_updated = 1  
                
        if self.report_enable == 0 and self.report_enable_old == 1 and self.report_retry != 0:
            print('DHT too many failures! Retry counter: {}'.format(self.report_retry_counter))
            self.report_retry_counter = 0
            self.report_retry = 0
        
        self.report_enable_old = self.report_enable
