from picamera import PiCamera
import os


class Camera:
    def __init__(self):
        self.frame = 0
        self.camera = PiCamera()
        self.time_last_capture = 0
        self.is_first_capture = 1
        
    def running(self, time_actual, image_folder):
        if time_actual - self.time_last_capture >= 60*1 or self.is_first_capture == 1: 
            self.camera.capture(image_folder + '/time_lapse_test_%05d.jpg' % (self.frame))
            print('frame number: %05d' % (self.frame))
            self.frame += 1
            self.time_last_capture = time_actual
            self.is_first_capture = 0
            
    def set_start_frame(self,image_folder):
        arr = []
        for (root, dirs, file) in os.walk(image_folder):
            #print(root)
            #print(dirs)
            arr_root = root
            for val in file:
                if ".jpg" in val:
                    arr.append(val)
            break
        arr.sort()
        
        if arr != []:
            #print(arr[-1][-9:-4])

            last_frame_num = list(arr[-1][-9:-4])
            for i in range(len(last_frame_num)):
                if len(last_frame_num) > 1 and last_frame_num[0] == '0':
                    last_frame_num.pop(0)
                elif len(last_frame_num) == 1 and last_frame_num[0] == '0':
                    last_frame_num = '0'
                    break
                else:
                    break

            self.frame = int(''.join(last_frame_num)) + 1
    
    
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