from urllib.request import urlopen
import cv2
import numpy as np
import time

# Replace the URL with your own IPwebcam shot.jpg IP:port

class Moble_capture:
    def __init__(self,url):
        self.url=url + '/shot.jpg'
    def get_image(self,size =(640,480)):
        imgResp = urlopen(self.url)

        # Numpy to convert into a array
        imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
        image = cv2.imdecode(imgNp,-1)

        return  cv2.resize(image,size)


