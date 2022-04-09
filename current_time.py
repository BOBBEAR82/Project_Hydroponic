# from datetime import datetime
# 
# now = datetime.now()
# 
# current_time = now.strftime("%H:%M:%S")
# print("Current Time =", current_time)


import time

while 1:
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(current_time)
    time.sleep(2)
