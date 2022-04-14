import RPi.GPIO as gpio


class AirPump:
    def __init__(self, gpio_id = 4):
        self.gpio_id = gpio_id
        self.last_on_time = 0
        self.last_off_time = 0
        self.gpio_state = 1
        
        gpio.setup(self.gpio_id, gpio.OUT, initial = gpio.HIGH)        
        
    def first_start(self, time_actual):    ### for initial, turn the air pump off for 30 mins, this is to separate the tent fan and air pump tuning on at the same time to lower peak power consumption 
        gpio.output(self.gpio_id, gpio.HIGH)
        self.last_off_time = time_actual
        
    def get_gpio_state(self):
        self.gpio_state = gpio.input(self.gpio_id)
        return self.gpio_state
        
    def running(self, time_actual, time_display):
        if (self.get_gpio_state() == 0 and time_actual - self.last_on_time >= 60*30):   ### turn on for 30 mins
            self.last_off_time = time_actual
            gpio.output(self.gpio_id, gpio.HIGH)
            print(('Air pump turn off time:' + '\t' * 2 + '{0};' + '\t' + 'Air pump state:' + '\t' * 2 + '{1}.')
                  .format(time_display, ('ON' if self.get_gpio_state() == 0 else 'OFF')))
            self.last_on_time = 0
 
        if (self.get_gpio_state() == 1 and time_actual - self.last_off_time >= 60*30):   ### turn off for 30 mins
            self.last_on_time = time_actual
            gpio.output(self.gpio_id, gpio.LOW)
            print(('Air pump turn on time:' + '\t' * 2 + '{0};' + '\t' + 'Air pump state:' + '\t' * 2 + '{1}.')
                  .format(time_display, ('ON' if self.get_gpio_state() == 0 else 'OFF')))
            self.last_off_time = 0
