from picamera import PiCamera


class Camera:
    def __init__(self):
        self.frame = 0
        self.camera = PiCamera()
        self.time_last_capture = 0
        self.is_first_capture = 1
        
    def running(self, time_actual, image_folder):
        if time_actual - self.time_last_capture >= 60*1 or self.is_first_capture == 1: 
            self.camera.capture(image_folder + '/time_lapse_test_%05d.jpg' % (self.frame))
            print('frame number: %04d' % (self.frame))
            self.frame += 1
            self.time_last_capture = time_actual
            self.is_first_capture = 0
            
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