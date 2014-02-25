# geschreven voor Paul-Luuk Profijt, 10-2-2014, voor Practicum Autonome Systemen aan de RuG

import pygame,random
import util.vidmemreader
import Image
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
        oldpic = pygame.image.fromstring(oldpic.tostring(),(oldpic.width,oldpic.height),"RGB")
        W = oldpic.get_width()
        H = oldpic.get_height()
        W2 = 100
        Scale = float(float(W2 * 100) / float(W * 100))
        W = W2
        H = H * Scale
        W = int(W)
        H = int(H)
        oldpic = pygame.transform.scale(oldpic,(W,H))

        print("color detection - redscaling")
        redpic = pygame.transform.scale(oldpic,(W,H))
        for i in range(0,W):
            for j in range(0,H):
                col = oldpic.get_at((i,j))
                r = col.b
                g = col.g
                b = col.r
                if (color == "red"):
                    if (r > (b+g)*1.1):
                        redpic.set_at((i,j),(r,0,0))
                    else:
                        redpic.set_at((i,j),(0,0,0))
                if (color == "blue"):
                    if (b > (r+g)*1.1):
                        redpic.set_at((i,j),(b,0,0))
                    else:
                        redpic.set_at((i,j),(0,0,0))
                if (color == "green"):
                    if (g > (b+r)*1.1):
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
            
        for i in range(leftX,rightX):
            for j in range(upY,downY):
                r = oldpic.get_at((i,j)).r
                oldpic.set_at((i,j),(r,50,0))

        for i in range(0,redpic.get_width()):
            oldpic.set_at((i,midY),(255,255,255))
        for j in range(0,redpic.get_height()):
            oldpic.set_at((midX,j),(255,255,255))

        pygame.image.save(oldpic,"testpic.png")

        return (float((midX-W/2))/(W/2),float((midY-H/2))/(H/2))