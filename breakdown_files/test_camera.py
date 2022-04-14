from picamera import PiCamera
import os


class Camera:
    def __init__(self):
        self.frame = 0
        self.camera = PiCamera()
        self.time_last_capture = 0
        self.is_first_capture = 1
        
    def running(self, time_actual, image_folder, capture_interval_min = 10):
        if time_actual - self.time_last_capture >= 60 * capture_interval_min or self.is_first_capture == 1: 
            self.camera.capture(image_folder + '/time_lapse_test_%05d.jpg' % (self.frame))
            print('frame number: %05d' % (self.frame))
            self.frame += 1
            self.time_last_capture = time_actual
            self.is_first_capture = 0
            
    ##########################################################
    # when the program is restarted, get the last frame id of existing pictures, and continue increment the frame ID
    ##########################################################    
    def set_start_frame(self,image_folder):
        arr = []
        for (root, dirs, file) in os.walk(image_folder):
            #print(root)
            #print(dirs)
            arr_root = root
            for val in file:
                if ".jpg" in val:
                    arr.append(val)
            break     ### only check the root folder. if there are multiple sub folders in the root folder, skip them
        arr.sort()
        
        if arr != []:   ### only if there are already some picture files in the folder
            #print(arr[-1][-9:-4])
            last_frame_num = arr[-1][-9:-4]
            self.frame = int(last_frame_num) + 1
    
    
    def kill(self):
        self.camera.close()


# 
# frame = 0
# camera = PiCamera()
# image_folder = '/home/pi_with_screen/Pictures/time_lapse_test'
# #camera.capture(image_folder + '/time_lapse_test_%05d.jpg' % (frame))
# #print('frame number: %04d' % (frame))
# #frame += 1
# time_camera_last_capture = time.time()
# camera_capture_init = 1
# 
# 
# if time_actual - time_camera_last_capture >= 60 * 10 or camera_capture_init == 1: 
#         camera.capture(image_folder + '/time_lapse_test_%05d.jpg' % (frame))
#         print('frame number: %04d' % (frame))
#         frame += 1
#         time_camera_last_capture = time_actual
#         camera_capture_init = 0