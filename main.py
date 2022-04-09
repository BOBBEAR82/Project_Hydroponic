import time
import RPi.GPIO as gpio
import signal
import Adafruit_DHT
from picamera import PiCamera

DHT_sensor = Adafruit_DHT.DHT11
gpio_id_DHT = 18

gpio_id_air_pump = 4
gpio_id_growing_light = 27
gpio_id_tant_fan = 17

gpio.setmode(gpio.BCM)
gpio.setup(gpio_id_air_pump, gpio.OUT, initial = gpio.HIGH)
gpio.setup(gpio_id_growing_light, gpio.OUT, initial = gpio.HIGH)
gpio.setup(gpio_id_tant_fan, gpio.OUT, initial = gpio.HIGH)
gpio.setup(22, gpio.OUT, initial = gpio.HIGH)

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        gpio.output(gpio_id_air_pump, gpio.HIGH)
        gpio.output(gpio_id_growing_light, gpio.HIGH)
        gpio.output(gpio_id_tant_fan, gpio.HIGH)
        gpio.output(22, gpio.HIGH)
        gpio.cleanup()
        camera.close()
        exit(1)
        
signal.signal(signal.SIGINT, handler)

#gpio_state = 0
time_start_on = time.time()
time_object = time.localtime()
time_start_off = 0
#print(time_start_on)

gpio.output(gpio_id_air_pump, gpio.LOW)
gpio.output(gpio_id_growing_light, gpio.LOW)

actual_time_hour = time_object.tm_hour
actual_time_min = time_object.tm_min
actual_time_sec = time_object.tm_sec
time_display = str(actual_time_hour) + ':' + str(actual_time_min) + ':' + str(actual_time_sec)

print(('Air pump turn on time:' + '\t' * 2 + '{0};' + '\t' + 'Air pump state:' + '\t' * 2 + '{1}.')
        .format(time_display, ('ON' if gpio.input(gpio_id_air_pump) == 0 else 'OFF')))
print(('Growing light turn on time:' + '\t' + '{0};' + '\t' + 'Growing light state:' + '\t' + '{1}.')
        .format(time_display, ('ON' if gpio.input(gpio_id_growing_light) == 0 else 'OFF')))

DHT_report_enable = 0
DHT_report_enable_old = 0
DHT_report_retry = 0
DHT_report_retry_counter = 0
DHT_report_retry_time_start = 0
DHT_report_complete_time_start = 0

frame = 0
camera = PiCamera()
image_folder = '/home/pi/Pictures/time_lapse_test'
#camera.capture(image_folder + '/time_lapse_test_%05d.jpg' % (frame))
#print('frame number: %04d' % (frame))
#frame += 1
time_camera_last_capture = time.time()
camera_capture_init = 1


while 1:
    time_actual = time.time()
    time_object = time.localtime()
    actual_time_hour = time_object.tm_hour
    actual_time_min = time_object.tm_min
    actual_time_sec = time_object.tm_sec
    time_display = str(actual_time_hour) + ':' + str(actual_time_min) + ':' + str(actual_time_sec)
    
    
    
    if (gpio.input(gpio_id_air_pump) == 0 and time_actual - time_start_on >= 60*30):
        time_start_off = time.time()
        gpio.output(gpio_id_air_pump, gpio.HIGH)
        print(('Air pump turn off time:' + '\t' * 2 + '{0};' + '\t' + 'Air pump state:' + '\t' * 2 + '{1}.')
              .format(time_display, ('ON' if gpio.input(gpio_id_air_pump) == 0 else 'OFF')))
        time_start_on = 0
 
    if (gpio.input(gpio_id_air_pump) == 1 and time_actual - time_start_off >= 60*30):
        time_start_on = time.time()
        gpio.output(gpio_id_air_pump, gpio.LOW)
        print(('Air pump turn on time:' + '\t' * 2 + '{0};' + '\t' + 'Air pump state:' + '\t' * 2 + '{1}.')
              .format(time_display, ('ON' if gpio.input(gpio_id_air_pump) == 0 else 'OFF')))
        time_start_off = 0


        
    if (gpio.input(gpio_id_growing_light) == 0 and (actual_time_hour < 7 or actual_time_hour >= 23)):
        gpio.output(gpio_id_growing_light, gpio.HIGH)
        print(('Growing light turn off time:' + '\t' + '{0};' + '\t' + 'Growing light state:' + '\t' + '{1}.')
              .format(time_display, ('ON' if gpio.input(gpio_id_growing_light) == 0 else 'OFF')))
        
    if (gpio.input(gpio_id_growing_light) == 1 and actual_time_hour >= 7 and actual_time_hour < 23):                  
        gpio.output(gpio_id_growing_light, gpio.LOW)
        #print("Growing light turn on time: {0}; Growing light status {1}".format(time_display, ('ON' if gpio.input(gpio_id_growing_light) == 0 else 'OFF')))
        print(('Growing light turn on time:' + '\t' + '{0};' + '\t' + 'Growing light state:' + '\t' + '{1}.')
              .format(time_display, ('ON' if gpio.input(gpio_id_growing_light) == 0 else 'OFF')))
        

        
    if DHT_report_enable == 0 and (actual_time_min == 0 or actual_time_min == 30) and time_actual - DHT_report_complete_time_start > 60:
        DHT_report_enable = 1
        #print('Debug: enable triggered, time: ', actual_time_sec, time_actual, DHT_report_retry_time_start)
        
    if DHT_report_enable == 1 and (actual_time_min == 1 or actual_time_sec == 31):
        DHT_report_enable = 0
        DHT_report_complete_time_start = time_actual
        #print('Debug: disable triggered, time: ', actual_time_sec)
        
    if (DHT_report_enable == 1 and DHT_report_enable_old == 0) or (DHT_report_enable == 1 and DHT_report_retry == 1 and time_actual - DHT_report_retry_time_start > 3):
        #print('Debug: time: ', time_actual, DHT_report_retry_time_start, '; status:', DHT_report_enable, DHT_report_enable_old, DHT_report_retry)
        humidity, temperature = Adafruit_DHT.read(DHT_sensor, gpio_id_DHT)
        #print("Debug: test: ", humidity, temperature, actual_time_sec)
        if humidity == None or temperature == None:
            DHT_report_retry = 1
            DHT_report_retry_time_start = time_actual
            DHT_report_retry_counter += 1
        else:
            DHT_report_enable = 0
            DHT_report_retry = 0
            #print('Debug: data: ', humidity, temperature, DHT_report_retry_counter, DHT_report_enable, DHT_report_enable_old, DHT_report_retry)
            print(('DHT measure time: ' + '{0},' + '\t' + 'Humidity: ' + '{1} %,' + '\t' + 'Temperature: ' + '{2} degC,' + '\t' * 2 + 'Retry counter: ' + '{3}')
                  .format(time_display, humidity, temperature, DHT_report_retry_counter))
            DHT_report_retry_counter = 0
            DHT_report_complete_time_start = time_actual
            
            
    if DHT_report_enable == 0 and DHT_report_enable_old == 1 and DHT_report_retry != 0:
        print('DHT too many failures!')
        DHT_report_retry_counter = 0
        DHT_report_retry = 0
    
    DHT_report_enable_old = DHT_report_enable
    
    
    if time_actual - time_camera_last_capture >= 60 * 10 or camera_capture_init == 1: 
        camera.capture(image_folder + '/time_lapse_test_%05d.jpg' % (frame))
        print('frame number: %04d' % (frame))
        frame += 1
        time_camera_last_capture = time_actual
        camera_capture_init = 0