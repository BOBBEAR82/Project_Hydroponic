import time
import RPi.GPIO as gpio
import signal
import Adafruit_DHT
from picamera import PiCamera
from tkinter import *

from test_air_pump import *
from test_growing_light import *
from test_DHT import *
from test_cycle_time_cal import *
from test_camera import *
from test_GUI import *


air_pump = AirPump()
growing_light = GrowingLight()
dht = DHT()

gpio_id_DHT = 18
gpio_id_air_pump = 4
gpio_id_growing_light = 27
#gpio_id_tant_fan = 17

gpio.setmode(gpio.BCM)
air_pump.init(gpio_id_air_pump)
growing_light.init(gpio_id_growing_light)

#gpio.setup(gpio_id_tant_fan, gpio.OUT, initial = gpio.HIGH)
#gpio.setup(22, gpio.OUT, initial = gpio.HIGH)

def handler(signum, frame):
    res = input("Ctrl-c was pressed. Do you really want to exit? y/n ")
    if res == 'y':
        gpio.output(air_pump.gpio_id, gpio.HIGH)
        gpio.output(growing_light.gpio_id, gpio.HIGH)
        #gpio.output(gpio_id_tant_fan, gpio.HIGH)
        #gpio.output(22, gpio.HIGH)
        gpio.cleanup()
        camera.kill()
        exit(1)
        
signal.signal(signal.SIGINT, handler)


air_pump.first_start(time.time())
growing_light.first_start()

actual_time = ActualTime()
actual_time.get_actual_time()


print(('Air pump turn on time:' + '\t' * 2 + '{0};' + '\t' + 'Air pump state:' + '\t' * 2 + '{1}.')
        .format(actual_time.time_display, ('ON' if air_pump.get_gpio_state() == 0 else 'OFF')))
print(('Growing light turn on time:' + '\t' + '{0};' + '\t' + 'Growing light state:' + '\t' + '{1}.')
        .format(actual_time.time_display, ('ON' if growing_light.get_gpio_state() == 0 else 'OFF')))

dht.init(gpio_id_DHT)


camera = Camera()
image_folder = '/home/pi_with_screen/Pictures/time_lapse_test'


cycle_time_cal = CycleTimeCalculator()


root = GUI()
root.init()



while 1:
    cycle_time_cal.get_cycle_start_time_ms()    
    actual_time.get_actual_time()
        
   
    air_pump.running(actual_time.actual_time_s, actual_time.time_display)  
    
    growing_light.running(actual_time.actual_time_s, actual_time.actual_time_hour, actual_time.time_display)
   
    dht.running(actual_time.actual_time_s, actual_time.actual_time_min, actual_time.time_display)
    
    camera.running(actual_time.actual_time_s, image_folder)
       
        
    #GUI display
    root.running(air_pump.get_gpio_state(), growing_light.get_gpio_state(), dht.humidity, dht.temperature)

    
    cycle_time_cal.running()    