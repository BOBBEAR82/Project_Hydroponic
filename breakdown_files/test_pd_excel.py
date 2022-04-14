import pandas as pd

class Df:
    def __init__(self):
        ##########################################################
        # define what data needs to be saved in dataframe
        ##########################################################
        self.df = pd.DataFrame(columns=['Date', 
                           'Hour', 
                           'Minute', 
                           'Second', 
                           'Air Pump Status',
                            'Tent Fan Status',
                           'Growing Linght Status', 
                           'Humitidiy', 
                           'Temperature', 
                           'Photo Frame', 
                           'Max Cycle Time',
                           'MinCycle Time'])
        
        ##########################################################
        # record the time of last writing data to dataframe
        ##########################################################        
        self.last_write_time = 0
        
    def add_data(self, actual_time, date, hour, minute, second, air_pump, tent_fan,
                 growing_light, humidity, temperature, photo_frame, max_cycle_time, min_cycle_time):
        ##########################################################
        # define the frequence of writing data to the data frame, unit is second
        ########################################################## 
        if actual_time - self.last_write_time >= 60 * 1:
            self.df.loc[len(self.df.Date)] = [date, hour, minute, second, air_pump, tent_fan, growing_light, humidity, temperature, photo_frame, max_cycle_time, min_cycle_time]
            self.last_write_time = actual_time
    
    def write_to_excel(self):
        ##########################################################
        # export the dataframe to csv file at when terminating the programe
        ########################################################## 
        self.df.to_csv('/home/pi_with_screen/Documents/export_dataframe.csv', index = False, header = True)
        
#         with pd.ExcelWriter('/home/pi_with_screen/Documents/export_dataframe.xlsx',
#                     mode='a') as writer:  
#             self.df.to_excel(writer, sheet_name = str(self.df.at[self.df.shape[0] - 1, 'Date']), engine="openpyxl", index = False, header=True)
