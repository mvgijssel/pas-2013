# geschreven voor Paul-Luuk Profijt, 10-2-2014, voor Practicum Autonome Systemen aan de RuG

import pygame,random
import util.vidmemreader
import Image
import cv2.cv as cv
import cv2
from pygame.locals import *

pygame.init()


#
# hoe te gebruiken: een andere module kan dit typen:
# import balherkenning
# detector = balherkenning.rasterImage()
# (posx,posy) = detector.getPos()
#

class RasterImage:

    def __init__(self,source,color="red"):
        self.vid = source # must be a naovideo class
        self.color = color

    def get_new_image(self):
        img = self.vid.get_image()
        return img
    
    def getPos(self):
        color = self.color
        oldpic = self.get_new_image()
        ImgArr = oldpic[6]
        #oldpic2 = Image.fromstring("RGB",(oldpic.size),oldpic)
        oldpic = pygame.image.fromstring(oldpic.tostring(),(oldpic.width,oldpic.height),"RGB")
        W = oldpic.get_width()
        H = oldpic.get_height()

        print("color detection - redscaling")
        redpic = pygame.transform.scale(oldpic,(W,H))
        for i in range(0,W):
            for j in range(0,H):
                col = oldpic.get_at((i,j))
                r = col.r
                g = col.g
                b = col.b
                if (color == "red"):
                    if (r > (b+g)*0.9):
                        redpic.set_at((i,j),(r,0,0))
                    else:
                        redpic.set_at((i,j),(0,0,0))
                if (color == "blue"):
                    if (b > (r+g)*0.9):
                        redpic.set_at((i,j),(b,0,0))
                    else:
                        redpic.set_at((i,j),(0,0,0))
                if (color == "green"):
                    if (g > (b+r)*0.9):
                        redpic.set_at((i,j),(g,0,0))
                    else:
                        redpic.set_at((i,j),(0,0,0))
        self.pic_ball = redpic

        leftX = 0
        rightX = W
        upY = 0
        downY = H

        midX = (leftX + rightX) / 2
        midY = (upY + downY) / 2

        upleft = 0
        upright = 0
        downleft = 0
        downright = 0

        crude = 4

        print("color detection - finding hotspot")
        while(crude >= 1):
            for i in range(0,redpic.get_width(),crude):
                for j in range(0,redpic.get_height(),crude):
                    r = redpic.get_at((i,j)).r
                    if (r > 0):
                        if (i < midX and j < midY):
                            upleft += r
                        elif (i > midX and j < midY):
                            upright += r
                        elif (i < midX):
                            downleft += r
                        else:
                            downright += r
            crude -= 1
            if (max(max(upleft,upright),max(downleft,downright)) == 0):
                # if we did not find any pixes at all, do not "rezoom", just zoom in
                if (crude == 0):
                    return (-999,-999)
                else:
                    pass
            elif (upleft >= upright and upleft >= downleft and upleft >= downright):
                # if we find most pixel up-left, rezoom up-left
                leftX = leftX
                rightX = midX
                upY = upY
                downY = midY
            elif (upright >= downleft and upright >= downright):
                # etc, upright
                leftX = midX
                rightX = rightX
                upY = upY
                downY = midY
            elif (downleft >= downright):
                # etc, downleft
                leftX = leftX
                rightX = midX
                upY = midY
                downY = downY
            elif (downright >= downleft):
                # etc, downright
                leftX = midX
                rightX = rightX
                upY = midY
                downY = downY
            else:
                # dit zou niet moeten kunnen
                print("error: no color detection")

            midX = (leftX + rightX) / 2
            midY = (upY + downY) / 2
            upleft = 0
            upright = 0
            downleft = 0
            downright = 0

        cv2.namedWindow("Bal herkenner")
        cv2.moveWindow("Bal herkenner",100,100)
        cv2.imshow("Bal herkenner", redpic)
        cv2.waitKey(1)
            
        for i in range(leftX,rightX):
            for j in range(upY,downY):
                r = redpic.get_at((i,j)).r
                redpic.set_at((i,j),(r,50,0))

        for i in range(0,redpic.get_width()):
            redpic.set_at((i,midY),(255,255,255))
        for j in range(0,redpic.get_height()):
            redpic.set_at((midX,j),(255,255,255))
        return (midX-W/2,midY-H/2)

# this was for testing, debugging
#
#    def printMe(self,name):
#        pygame.image.save(self.pic_ball,name)
#
#for num in range(1,10):
#    pic_of_head = pygame.image.load("sc" + str(num) + ".png")
#    raster = rasterImage(pic_of_head)
#    raster.printMe("sc" + str(num) + "-find.png")
