import time
import RPi.GPIO as gpio
import signal
#import Adafruit_DHT
#from picamera import PiCamera
from tkinter import *


##########################################################
# import other files which defines classes and functions
##########################################################
from test_air_pump import *
from test_growing_light import *
from test_DHT import *
from test_cycle_time_cal import *
from test_camera import *
from test_GUI import *
from test_pd_excel import *
from test_tent_fan import *


##########################################################
# hander to confirm terminating the program and perfrom actions before shuttding down
##########################################################
def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        gpio.output(air_pump.gpio_id, gpio.HIGH)
        gpio.output(growing_light.gpio_id, gpio.HIGH)
        gpio.output(gpio_id_tant_fan, gpio.HIGH)
        #gpio.output(22, gpio.HIGH)
        gpio.cleanup()
        camera.kill()
        df.write_to_excel()
        exit(1)
        
signal.signal(signal.SIGINT, handler)

##########################################################
# create class instance which depend on GPIOs, define the GPIO IDs, initiate GPIOs
##########################################################
gpio_id_air_pump = 4
gpio_id_growing_light = 27
gpio_id_tant_fan = 17
gpio_id_DHT = 18

gpio.setmode(gpio.BCM)

air_pump = AirPump(gpio_id_air_pump)
growing_light = GrowingLight(gpio_id_growing_light)
tent_fan = TentFan(gpio_id_tant_fan)
dht = DHT(gpio_id_DHT)

#gpio.setup(22, gpio.OUT, initial = gpio.HIGH)

air_pump.first_start(time.time())
tent_fan.first_start(time.time())
growing_light.first_start()


##########################################################
# create class instance for actual time
##########################################################
actual_time = ActualTime()
actual_time.get_actual_time()


##########################################################
# print the initial condition of GPIO related items
##########################################################
print(('Air pump turn on time:' + '\t' * 2 + '{0};' + '\t' + 'Air pump state:' + '\t' * 2 + '{1}.')
        .format(actual_time.time_display, ('ON' if air_pump.get_gpio_state() == 0 else 'OFF')))
print(('Tent fan turn on time:' + '\t' * 2 + '{0};' + '\t' + 'Tent fan state:' + '\t' * 2 + '{1}.')
        .format(actual_time.time_display, ('ON' if tent_fan.get_gpio_state() == 0 else 'OFF')))
print(('Growing light turn on time:' + '\t' + '{0};' + '\t' + 'Growing light state:' + '\t' + '{1}.')
        .format(actual_time.time_display, ('ON' if growing_light.get_gpio_state() == 0 else 'OFF')))


##########################################################
# create class instance for camera, get the starting frame number
##########################################################
camera = Camera()
image_folder = '/home/pi_with_screen/Pictures/time_lapse_test'
camera.set_start_frame(image_folder + '/')


##########################################################
# create class instance for calcuating cycle time
##########################################################
cycle_time_cal = CycleTimeCalculator()


##########################################################
# create class instance for GUI and initiate it
##########################################################
root = GUI()


##########################################################
# create class instance for pandas dataframe to log the data
##########################################################
df = Df()


##########################################################
# main loop
##########################################################
while 1:
    ##########################################################
    # get actual time at the beginning of a cycle 
    ##########################################################
    cycle_time_cal.get_cycle_start_time_ms()    
    actual_time.get_actual_time()
        

    ##########################################################
    # update all items
    ##########################################################
    air_pump.running(actual_time.actual_time_s, actual_time.time_display)    
    tent_fan.running(actual_time.actual_time_s, actual_time.time_display)      
    growing_light.running(actual_time.actual_time_s, actual_time.actual_time_hour, actual_time.time_display)   
    dht.running(actual_time.actual_time_s, actual_time.actual_time_min, actual_time.time_display)    
    camera.running(actual_time.actual_time_s, image_folder, 10)
       

    ##########################################################
    # update GUI display
    ##########################################################
    root.running(actual_time.actual_time_s,
                air_pump.get_gpio_state(),
                tent_fan.get_gpio_state(),
                growing_light.get_gpio_state(),
                dht.humidity,
                dht.temperature,
                dht.is_updated,
                cycle_time_cal.cycle_inteval_max_ms,
                cycle_time_cal.cycle_inteval_min_ms)


    ##########################################################
    # add all new data to dataframe
    ##########################################################    
    df.add_data(actual_time.actual_time_s, actual_time.actual_date, actual_time.actual_time_hour, actual_time.actual_time_min, actual_time.actual_time_sec,
                ('ON' if air_pump.gpio_state == 0 else 'OFF'),
                ('ON' if tent_fan.gpio_state == 0 else 'OFF'),
                ('ON' if growing_light.gpio_state == 0 else 'OFF'),
                dht.humidity, dht.temperature, camera.frame,
                cycle_time_cal.cycle_inteval_max_ms, cycle_time_cal.cycle_inteval_min_ms
                )
    
    
    ##########################################################
    # update cycle time interval
    ##########################################################    
    cycle_time_cal.running()