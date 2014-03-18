import cv2
import cv
import numpy
from pprint import pprint

w = 500
h = 500
no_of_bits = cv2.IPL_DEPTH_8U
channels = 3

image = cv.CreateImage((w, h), no_of_bits, channels)

#print image.data

#cv2.ShowImage('WindowName',image)

#cv2.imshow('window name', numpy.asarray(image[:, :]))
#cv2.waitKey(0)
#cv2.destroyAllWindows()


print numpy.count_nonzero(image[:, :])

#print image
