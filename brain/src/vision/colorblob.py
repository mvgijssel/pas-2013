#!/usr/bin/python

import time
import memory
import pickle
import sys
import configparse
import os
import logging
import cv2
import numpy

import util.nullhandler
import util.loggingextra
import util.vidmemreader
import util.naovideo
import util.sendsocket

import SocketServer
import shutil

from abstractvisionmodule import AbstractVisionModule

logging.getLogger('Borg.Brain.Vision.Colorblob').addHandler(util.nullhandler.NullHandler())


class Colorblob(AbstractVisionModule):

    def __init__(self, host, port, source):
        self.DEBUG = True 
        self.SHOW = True
        self.logger = logging.getLogger("Borg.Brain.Vision.Colorblob")
        super(Colorblob, self).__init__(host, port)
        self.source = [source]
        self.vid_mem_reader = util.vidmemreader.VidMemReader(self.source)
        self.get_new_image()
        self.blobs = self.load_colors()
    
    def train(self):
        print "train"
        
    def run(self):
        while True:
            #Frame rate +/- 30HZ
            time.sleep(0.03)
            self.update()
            #Get new image and add blur to it
            image = self.blur_image(self.get_new_image(), 5)
            #Convert BGR to HSV
            imageHSV = self.convert_to_HSV(image)
            #Detect blobs in image
            self.detect_blobs(imageHSV)

            #For debuging
            if self.DEBUG:
                cv2.imshow("Image", image)
                cv2.imshow("ImageHSV", imageHSV)
                cv2.waitKey(1)

    def load_colors(self):
        directory = os.path.abspath(os.environ['BORG'] + '/brain/data/colorblob_new')

        if not os.path.exists(directory):
            print "Unknown directory"
            return {'Green': {'upper': [81, 204, 255], 'lower': [31, 43, 0]},'Yellow' : {'upper' : [33, 255, 255], 'lower': [0, 6, 255]}}
	
        f = open(directory + '/Colors', 'r')
        print "Data"
        colors = f.read()
        f.close()
        return eval(colors)

    def get_new_image(self):
        """ Get new image from video shared memory """
        img = self.vid_mem_reader.get_latest_image()[0]
        #return resized image
        return self.resize_image(numpy.asarray(img[:,:]))

    def resize_image(self, image):
        ''' Resize the original image '''
        return cv2.resize(image, (160,120))        
            
    def blur_image(self, image, value):
        #Add blur
        return cv2.blur(image, (value,value))

    def convert_to_HSV(self, image):
        #Convert from BGR to HSV
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    def detect_blobs(self, image):
        #Try to detects blobs in observation
        for blob in self.blobs:
            #Get the upper and lower HSV values. [H, S, V]
            lower = numpy.asarray(self.blobs[blob]['lower'], dtype=numpy.uint8)
            upper = numpy.asarray(self.blobs[blob]['upper'], dtype=numpy.uint8)

            #Get colorblobs
            self.get_colorblobs(image, lower, upper, blob)

    def get_colorblobs(self, image, lower, upper, name):
        #Get the mask on the image
        mask = cv2.inRange(image, lower, upper)

        #Debug code
        if self.DEBUG:
            cv2.imshow(name, cv2.bitwise_and(image, image, mask = mask))
            cv2.waitKey(1)


        #Find contours from the mask
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        #If there are no observations
        if len(contours) == 0:
            return

        #Create a list with the observations.
        obs = []
        for contour in contours:
            x, y, width, height = cv2.boundingRect(contour) 
            #Ignore observation: size < 20
            if (width * height) > 20:               
                obs.append({'x' : x, 'y' : y, 'width' : width, 'height' : height, 'size' : (width * height)})

        if self.DEBUG:
            print name
            print obs

        self.add_property('name', name)
        self.add_property('blobs', obs)
        self.store_observation()

def usage():
    print "You should add the configuration options on the command line.\n"
    print "Usage: ", sys.argv[0], " host=<controller_host> port=<controller_port> preview=<True>\n"
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        exit()

    sec = "colorblob" #section in config_dict
    args = sys.argv[1:]
    config_dict = configparse.parse_args_to_param_dict(args, sec)

    controller_ip = config_dict.get_option(sec, "host")
    controller_port = config_dict.get_option(sec, "port")
    video_source = config_dict.get_option(sec, "video_source")
    sect = config_dict.get_section(sec)
    print sect

    if not (controller_ip and controller_port):
        usage()
        exit()

    logging.getLogger('Borg.Brain').addHandler(util.loggingextra.ScreenOutput())
    logging.getLogger('Borg.Brain').setLevel(logging.DEBUG)

    #Create module and connect to visioncontroller.
    colorblob = Colorblob(controller_ip, controller_port, source = video_source)
    colorblob.connect()
    #colorblob.set_socket_verbose(True, True)
    if (colorblob.is_connected()):
        colorblob.run()

