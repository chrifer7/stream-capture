import cv2, platform
import numpy as np
#import urllib
import urllib.request
import os

cam2 = "http://localhost:8080/stream.mjpeg"

#stream=urllib.urlopen(cam2)
stream=urllib.request.urlopen(cam2)
bytes=''
while True:
    # to read mjpeg frame -
    bytes+=str(stream.read(1024))
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')
    jpg = None
    print(bytes)
    print(a)
    print(b)
    if a!=-1 and b!=-1:
        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
    frame = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),cv2.CV_LOAD_IMAGE_COLOR)
    # we now have frame stored in frame.

    cv2.imshow('cam2',frame)

    # Press 'q' to quit 
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
