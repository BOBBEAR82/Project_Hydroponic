import RPi.GPIO as gpio


class GrowingLight:
    def __init__(self):
        self.gpio_id = 0
        self.last_on_time = 0
        self.last_off_time = 0
        self.turn_on_hour = 7
        self.turn_off_hour = 23
        self.gpio_state = 1
        
    def init(self, gpio_id = 27):
        self.gpio_id = gpio_id
        gpio.setup(self.gpio_id, gpio.OUT, initial = gpio.HIGH)
        
    def first_start(self, time_actual = 0):
        gpio.output(self.gpio_id, gpio.LOW)
        self.last_on_time = time_actual
        
    def get_gpio_state(self):
        self.gpio_state = gpio.input(self.gpio_id)
        return self.gpio_state
        
    def running(self, time_actual, hour_actual, time_display):
        if self.get_gpio_state() == 0 and (hour_actual < self.turn_on_hour or hour_actual >= self.turn_off_hour):
            gpio.output(self.gpio_id, gpio.HIGH)
            self.last_off_time = time_actual
            print(('Growing light turn off time:' + '\t' + '{0};' + '\t' + 'Growing light state:' + '\t' + '{1}.')
                  .format(time_display, ('ON' if self.get_gpio_state() == 0 else 'OFF')))
            self.last_on_time = 0
 
        if self.get_gpio_state() == 1 and (hour_actual >= self.turn_on_hour and hour_actual < self.turn_off_hour):
            gpio.output(self.gpio_id, gpio.LOW)
            self.last_on_time = time_actual
            print(('Growing light turn on time:' + '\t' + '{0};' + '\t' + 'Growing light state:' + '\t' + '{1}.')
                  .format(time_display, ('ON' if self.get_gpio_state() == 0 else 'OFF')))
            self.last_off_time = 0

