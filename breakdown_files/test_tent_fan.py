import RPi.GPIO as gpio


class TentFan:
    def __init__(self):
        self.gpio_id = 0
        self.last_on_time = 0
        self.last_off_time = 0
        self.gpio_state = 1
        
    def init(self, gpio_id = 17):
        self.gpio_id = gpio_id
        gpio.setup(self.gpio_id, gpio.OUT, initial = gpio.HIGH)
        
    def first_start(self, time_actual):
        gpio.output(self.gpio_id, gpio.LOW)
        self.last_on_time = time_actual
        
    def get_gpio_state(self):
        self.gpio_state = gpio.input(self.gpio_id)
        return self.gpio_state
        
    def running(self, time_actual, time_display):
        if (self.get_gpio_state() == 0 and time_actual - self.last_on_time >= 60*30):
            self.last_off_time = time_actual
            gpio.output(self.gpio_id, gpio.HIGH)
            print(('Tent fan turn off time:' + '\t' * 2 + '{0};' + '\t' + 'Tent fan state:' + '\t' * 2 + '{1}.')
                  .format(time_display, ('ON' if self.get_gpio_state() == 0 else 'OFF')))
            self.last_on_time = 0
 
        if (self.get_gpio_state() == 1 and time_actual - self.last_off_time >= 60*10):
            self.last_on_time = time_actual
            gpio.output(self.gpio_id, gpio.LOW)
            print(('Tent fan turn on time:' + '\t' * 2 + '{0};' + '\t' + 'Tent fan state:' + '\t' * 2 + '{1}.')
                  .format(time_display, ('ON' if self.get_gpio_state() == 0 else 'OFF')))
            self.last_off_time = 0
