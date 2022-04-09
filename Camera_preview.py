#import libraries
from picamera import PiCamera
from time import sleep
import os
#import cv2


#setup and start camera
def capture_image(interval, duration_minute, image_folder):
    
    #define variables
    #interval = 1
    frame = 0
    #duration_min = 10 
    frame_limit = duration_minute * 60 / interval
    
    camera = PiCamera()
    #camera.resolution = (1280, 720)
    camera.start_preview()
    sleep(2)
    
    print('Start capturing images.')

    while frame < frame_limit:
        camera.capture(image_folder + '/time_lapse_test_%05d.jpg' % (frame))
        print('frame number: %04d' % (frame), end = '\r')
        frame += 1
        sleep(interval)

    camera.stop_preview()
    print('Stop capturing images. Total frame: %05d.' % (frame))

def create_video(video_fps, image_folder, video_folder, video_name):
    import cv2
    
    #define variables
    #video_fps = 25
    #image_folder = '/home/pi/Pictures/time_lapse_test' # Use the folder
    #video_name = 'mygeneratedvideo.avi'
    os.chdir(video_folder)
    
    print('Start creating video.')

    images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    images.sort()

    fourcc = cv2.VideoWriter_fourcc(*'DIVX')

    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, fourcc, video_fps, (width, height))

    for image in images:
        print(image)
        video.write(cv2.imread(os.path.join(image_folder,image)))

    cv2.destroyAllWindows()
    video.release()
    
    print('Stop creating video.')

def camera_test():
    camera = PiCamera()
    #camera.resolution = (1280, 720)
    print('Start testing.')
    camera.start_preview()
    #camera.start_preview(fullscreen=False, window = (0,0,640,480))
    sleep(500)
    camera.stop_preview()
    camera.close()
    print('Stop testing.')


#main
    
interval = 20
duration_minute = 120
video_fps = 15
image_folder = '/home/pi/Pictures/time_lapse_test' 
video_folder = "/home/pi/Pictures/time_lapse_test"
video_name = 'mygeneratedvideo_sunset_1.avi'


#camera_test()
capture_image(interval, duration_minute, image_folder)
#create_video(video_fps, image_folder, video_folder, video_name)

#os.system('sudo reboot now')
