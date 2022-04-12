from tkinter import *
import datetime
import matplotlib

matplotlib.use('TkAgg')

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk



class GUI(Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Hydroponic System Data")
        self.geometry("600x500")
        self.configure(bg = 'white')
        
        self.humidity_index = Label(self, text= "Humidity: ", font=("sans-serif", 10), fg= "red", bg= "white")
        self.temperature_index = Label(self, text= "Temperature: ", font=("sans-serif", 10), fg= "blue", bg= "white")
        self.growing_light_index = Label(self, text= "Growing Light Status: ", font=("sans-serif", 10), fg= "green", bg= "white")
        self.air_pump_index = Label(self, text= "Air Pump Status: ", font=("sans-serif", 10), fg= "black", bg= "white")
        self.cycle_time_max_index = Label(self, text= "Cycle Time Max: ", font=("sans-serif", 10), fg= "blue", bg= "white")
        self.cycle_time_min_index = Label(self, text= "Cycle Time Min: ", font=("sans-serif", 10), fg= "blue", bg= "white")
        
        self.humidity_display = Label(self, text= "", font=("sans-serif", 10), fg= "red", bg= "white")
        self.temperature_display = Label(self, text= "", font=("sans-serif", 10), fg= "blue", bg= "white")
        self.growing_light_display = Label(self, text= "", font=("sans-serif", 10), fg= "green", bg= "white")
        self.air_pump_display = Label(self, text= "", font=("sans-serif", 10), fg= "black", bg= "white")
        self.cycle_time_max_display = Label(self, text= "", font=("sans-serif", 10), fg= "blue", bg= "white")
        self.cycle_time_min_display = Label(self, text= "", font=("sans-serif", 10), fg= "blue", bg= "white")
        
        #below is to define the plot 
        self.DHT_time = []
        self.DHT_humidity = []
        self.DHT_temperature = []
        
        
        figure = Figure(figsize=(6, 3), dpi=100)
        self.canvas = FigureCanvasTkAgg(figure, self)
        self.ax_humidity = figure.add_subplot(111)
        self.ax_temperature = self.ax_humidity.twinx()
        self.reset_plot(0, 0)
        self.canvas.get_tk_widget().grid(row = 7, column = 0, columnspan = 2)

        
    def init(self):
        self.humidity_index.grid(row = 0, column = 0, sticky = 'w')
        self.temperature_index.grid(row = 1, column = 0, sticky = 'w')
        self.growing_light_index.grid(row = 2, column = 0, sticky = 'w')
        self.air_pump_index.grid(row = 3, column = 0, sticky = 'w')
        self.cycle_time_max_index.grid(row = 4, column = 0, sticky = 'w')
        self.cycle_time_min_index.grid(row = 5, column = 0, sticky = 'w')
        
        self.humidity_display.grid(row = 0, column = 1, sticky = 'w')
        self.temperature_display.grid(row = 1, column = 1, sticky = 'w')
        self.growing_light_display.grid(row = 2, column = 1, sticky = 'w')
        self.air_pump_display.grid(row = 3, column = 1, sticky = 'w')
        self.cycle_time_max_display.grid(row = 4, column = 1, sticky = 'w')
        self.cycle_time_min_display.grid(row = 5, column = 1, sticky = 'w')
        
    def reset_plot(self, first_data, data_len):
        #self.axes.set_ylim([-10, 10])
#         if data_len >= 20:
#             self.axes.set_xlim([first_data, first_data + 20])
#         else: 
#             self.axes.set_xlim([0, 20])
        self.ax_humidity.cla()
        self.ax_temperature.cla()
        self.ax_humidity.grid()
        self.ax_humidity.set_title('Humidity and Temperature Curve')
        self.ax_humidity.set_ylabel('Humidity')
        self.ax_temperature.set_ylabel('Temperature')
        self.ax_humidity.set_ylim([10, 80])
        self.ax_temperature.set_ylim([15, 35])
              
    def running(self, air_pump_gpio_state, growing_light_gpio_state, humidity, temperature, is_DHT_updated, cycle_time_max, cycle_time_min):
        self.air_pump_display.config(text= 'ON' if air_pump_gpio_state == 0 else 'OFF')
        
        self.growing_light_display.config(text = 'ON' if growing_light_gpio_state == 0 else 'OFF')
        
        self.cycle_time_max_display.config(text= str(cycle_time_max) + " ms")
        self.cycle_time_min_display.config(text= str(cycle_time_min) + " ms")
        
        if humidity != None and temperature != None:
            self.humidity_display.config(text= str(humidity) + " %")
            self.temperature_display.config(text= str(temperature) + " degC")
            
        if is_DHT_updated == 1:
            self.DHT_time.append(datetime.datetime.now())
            self.DHT_humidity.append(humidity)
            self.DHT_temperature.append(temperature)
        
            if len(self.DHT_time) > 40:
                self.DHT_time.pop(0)
                self.DHT_humidity.pop(0)
                self.DHT_temperature.pop(0)
            #self.ax_humidity.cla()
            self.reset_plot(self.DHT_time[0], len(self.DHT_time))
            temp1, = self.ax_humidity.plot(self.DHT_time, self.DHT_humidity, color="blue", marker="o", label='Humidity')
            temp2, = self.ax_temperature.plot(self.DHT_time, self.DHT_temperature, color="red", marker="o", label='Temperature')
            self.ax_humidity.legend(handles=[temp1, temp2])
            
            self.canvas.draw()
            
        self.update()


# if __name__ == "__main__":
#     root = GUI()
#     root.init()
#     root.running(0, 1, 14, 32)
    
    #root.mainloop()


