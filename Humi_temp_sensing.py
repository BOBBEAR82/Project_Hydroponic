import Adafruit_DHT
import time

DHT_sensor = Adafruit_DHT.DHT11
gpio_id_DHT = 18

DHT_report_enable = 0
DHT_report_enable_old = 0
DHT_report_retry = 0
DHT_report_retry_counter = 0
DHT_report_retry_time_start = 0
DHT_report_complete_time_start = 0
 
while 1:
    time_actual = time.time()
    time_object = time.localtime()
    actual_time_hour = time_object.tm_hour
    actual_time_min = time_object.tm_min
    actual_time_sec = time_object.tm_sec
    time_display = str(actual_time_hour) + ':' + str(actual_time_min) + ':' + str(actual_time_sec)
                   
         
    if DHT_report_enable == 0 and (actual_time_sec == 0 or actual_time_sec == 30) and time_actual - DHT_report_complete_time_start > 1:
        DHT_report_enable = 1
        print('Debug: enable triggered, time: ', actual_time_sec, time_actual, DHT_report_retry_time_start)
        
    if DHT_report_enable == 1 and (actual_time_sec == 15 or actual_time_sec == 45):
        DHT_report_enable = 0
        DHT_report_complete_time_start = time_actual
        print('Debug: disable triggered, time: ', actual_time_sec)
        
    if (DHT_report_enable == 1 and DHT_report_enable_old == 0) or (DHT_report_enable == 1 and DHT_report_retry == 1 and time_actual - DHT_report_retry_time_start > 3):
        print('Debug: time: ', time_actual, DHT_report_retry_time_start, '; status:', DHT_report_enable, DHT_report_enable_old, DHT_report_retry)
        humidity, temperature = Adafruit_DHT.read(DHT_sensor, gpio_id_DHT)
        print("Debug: test: ", humidity, temperature, actual_time_sec)
        if humidity == None or temperature == None:
            DHT_report_retry = 1
            DHT_report_retry_time_start = time_actual
            DHT_report_retry_counter += 1
        else:
            DHT_report_enable = 0
            DHT_report_retry = 0
            print('Debug: data: ', humidity, temperature, DHT_report_retry_counter, DHT_report_enable, DHT_report_enable_old, DHT_report_retry)
            print(('DHT measure time: ' + '{0},' + '\t' + 'Humidity: ' + '{1} %,' + '\t' + 'Temperature: ' + '{2} degC,' + '\t' * 2 + 'Retry counter: ' + '{3}')
                  .format(time_display, humidity, temperature, DHT_report_retry_counter))
            DHT_report_retry_counter = 0
            DHT_report_complete_time_start = time_actual
            
            
    if DHT_report_enable == 0 and DHT_report_enable_old == 1 and DHT_report_retry != 0:
        print('DHT too many failure!')
        DHT_report_retry_counter = 0
        DHT_report_retry = 0
    
    DHT_report_enable_old = DHT_report_enable
