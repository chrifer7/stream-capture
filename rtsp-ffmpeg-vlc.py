import os
import time
import vlc
#import cv2
import numpy as np
from PIL import Image


from subprocess import call


''' GLOBAL VARIABLES '''
delay = 0.012 #.1*4 #delay to screen capture
imgs = [] #frames captured
i_buffer = 0
duration = 10 #
size_buffer = duration * int(1/delay)
player = vlc.MediaPlayer('rtsp://localhost:8554/stream.h264')

def reset_buffer():
    img = []
    i_buffer = 0

#http://www.xavierdupre.fr/blog/2016-03-30_nojs.html
"""
def make_video(images, outvid=None, fps=5, size=None,
               is_color=True, format="XVID"):
"""
"""
    Create a video from a list of images.

    @param      outvid      output video
    @param      images      list of images to use in the video
    @param      fps         frame per second
    @param      size        size of each frame
    @param      is_color    color
    @param      format      see http://www.fourcc.org/codecs.php
    @return                 see http://opencv-python-tutroals.readthedocs.org/en/latest/py_tutorials/py_gui/py_video_display/py_video_display.html

    The function relies on http://opencv-python-tutroals.readthedocs.org/en/latest/.
    By default, the video will have the size of the first image.
    It will resize every image to this size before adding them to the video.
"""
"""
    fourcc = cv2.VideoWriter_fourcc(*format)

    vid = None
    for img in images: 
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = cv2.VideoWriter(outvid, fourcc, float(fps), size, is_color)
            print('Video out: ', outvid)
        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = cv2.resize(img, size)
        vid.write(img)
        print('Writing frame: ', img.shape)
    vid.release()
    return vid
"""

''' MAIN '''

player.play()
total_extra_exec_time = 0

while True:
    time.sleep(delay)

    start_time = time.time()

    #We should wait until the video is loaded and the snapshot returns an non empty object
    if (player.video_take_snapshot(0, 'v_frames/frame'+str(i_buffer)+'.png', 0, 0) == 0): #.snapshot.tmp.png
        #i_img = cv2.imread('v_frames/frame'+str(i_buffer)+'.png')
        i_img = Image.open('v_frames/frame'+str(i_buffer)+'.png')
        i_img = np.array(i_img)

        # We should verify the shape of the snapshot

        if hasattr(i_img, 'shape'):
            imgs.append(i_img) #.snapshot.tmp.png

            height, width, layers = imgs[i_buffer].shape
            print('height: ', str(height), 'width: ', str(width))

            i_buffer = i_buffer + 1
            total_extra_exec_time = total_extra_exec_time + delta_time
            print('size: ', len(imgs), '- i_buff: ', i_buffer)

            if (i_buffer >= size_buffer):
                break

    end_time = time.time()
    delta_time = end_time - start_time

delay = delay + (total_extra_exec_time / i_buffer)
#make_video(imgs, 'v_frames/video_opencv_mjpg.avi', fps= int(1/delay), format='MJPG') # 'MJPG'

#make_video(imgs, 'v_frames/video_opencv_xvid.avi', fps= int(1/delay), format=['X','V','I','D']) #test failed
#make_video(imgs, 'v_frames/video_opencv_fmp4.mp4', fps= int(1/delay), format=['F','M','P','4']) #test failed


#ffmpeg -f image2 -r 23 -i v_frames/frame%1d.png -vcodec mpeg4 -y movie.mp4
call(['ffmpeg', '-f', 'image2', '-r', str(int(1/delay)), '-i', 'v_frames/frame%1d.png',
        '-vcodec', 'mpeg4', '-y', 'v_frames/video_ffmpeg_mpeg4.mp4'])

#call(["ffmpeg", "-i", video_arg, '-ss', start_time, '-vframes', vdata[2],
#                video_path_frames + '/' + video_name + '_frames' + '-%06d.jpg'])

'''
height, width, layers = imgs[i_buffer-1].shape

print('Writing video_test.avi')
video = cv2.VideoWriter('video_test.avi', -1, 1, (width, height))

for j in range(0, i_buffer):
    video.write(imgs[j])
    print('Writing: ', str(j))
    #cv2.startWindowThread()
    #cv2.namedWindow('Preview frames')
    #cv2.imshow('Frame', imgs[j])
    #cv2.waitKey(0)

video.release()
cv2.destroyAllWindows()

'''

#i_buffer = 0
#imgs = []
