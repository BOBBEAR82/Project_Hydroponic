import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(4, gpio.OUT, initial = gpio.HIGH)
gpio.setup(17, gpio.OUT, initial = gpio.HIGH)
gpio.setup(27, gpio.OUT, initial = gpio.HIGH)
gpio.setup(22, gpio.OUT, initial = gpio.HIGH)

counter = 0

while counter < 2: 
    gpio.output(4, gpio.LOW)
    time.sleep(3)
    gpio.output(4, gpio.HIGH)
    time.sleep(1)
    
    gpio.output(17, gpio.LOW)
    time.sleep(3)
    gpio.output(17, gpio.HIGH)
    time.sleep(1)
    
    gpio.output(27, gpio.LOW)
    time.sleep(3)
    gpio.output(27, gpio.HIGH)
    time.sleep(1)
    
    gpio.output(22, gpio.LOW)
    time.sleep(3)
    gpio.output(22, gpio.HIGH)
    time.sleep(1)
    
    counter += 1

#time.sleep(5)
    
gpio.cleanup()