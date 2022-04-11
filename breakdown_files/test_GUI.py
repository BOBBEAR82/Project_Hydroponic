from tkinter import *


class GUI(Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Hydroponic System Data")
        self.geometry("600x400")
        
        self.humidity_display = Label(self, text= "Humidity: ", font=("sans-serif", 30), fg= "red")
        self.temperature_display= Label(self, text= "Temperature: ", font=("sans-serif", 30), fg= "blue")
        self.growing_light_display = Label(self, text= "Growing light status: ", font=("sans-serif", 30), fg= "green")
        self.air_pump_display = Label(self, text= "Air pump status: ", font=("sans-serif", 30), fg= "black")

        
    def init(self):
        self.humidity_display.grid(row = 0, column = 0)
        self.temperature_display.grid(row = 1, column = 0)
        self.growing_light_display.grid(row = 2, column = 0)
        self.air_pump_display.grid(row = 3, column = 0)
              
    def running(self, air_pump_gpio_state, growing_light_gpio_state, humidity, temperature):
        self.air_pump_display.config(text= "Air pump status: \t" + ('ON' if air_pump_gpio_state == 0 else 'OFF'))
        
        self.growing_light_display.config(text= "Growing light status: \t" + ('ON' if growing_light_gpio_state == 0 else 'OFF'))
        
        if humidity != None and temperature != None:
            self.humidity_display.config(text= "Humidity: \t" + str(humidity) + " %")
            self.temperature_display.config(text= "Temperature: \t" + str(temperature) + " degC")
        self.update()


# if __name__ == "__main__":
#     root = GUI()
#     root.init()
#     root.running(0, 1, 14, 32)
    
    #root.mainloop()


