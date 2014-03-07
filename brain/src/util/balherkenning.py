# geschreven voor Paul-Luuk Profijt, 10-2-2014, voor Practicum Autonome Systemen aan de RuG

import pygame,random
import util.vidmemreader
import Image
import cv2
import cv
from pygame.locals import *

pygame.init()


#
# hoe te gebruiken: een andere module kan dit typen:
# import util.balherkenning
# detector = balherkenning.rasterImage()
# (posx,posy) = detector.getPos()
#

window = 0
screen = None
imgsize = 200

def init_window():
    global window,screen,imgsize
    if (window == 0):
        screen = pygame.display.set_mode((imgsize,imgsize))
        pygame.display.set_caption("Nao Balherkennning")
        window = 1

class RasterImage:

    def __init__(self,source,color="red"):
        self.vid = source # must be a naovideo class
        self.color = color

    def get_new_image(self):
        img = self.vid.get_image()
        return img

    def getPos(self):
        init_window()
        color = self.color
        oldpic = self.get_new_image()
        oldpic = pygame.image.fromstring(oldpic.tostring(),(oldpic.width,oldpic.height),"RGB")
        W = oldpic.get_width()
        H = oldpic.get_height()
        W2 = imgsize
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
                minwaarde = 100 # moet minimaal zoveel van de kleur aanwezig zijn <0,255>, om zwart uit te schakelen
                factor = 0.9 # er moet minimaal "factor" keer zoveel "kleur" zijn als andere kleuren samen
                maxwaarde = 300 # de andere kleuren samen mogen maximaal deze waarde hebben, om wit uit te schakelen
                if (color == "red"):
                    if (r > (b+g)*factor and r > minwaarde and (g+b) < maxwaarde):
                        redpic.set_at((i,j),(r-(b+g)/2,0,0))
                    else:
                        redpic.set_at((i,j),(0,0,0))
                if (color == "blue"):
                    if (b > (r+g)*factor and b > minwaarde and (r+g) < maxwaarde):
                        redpic.set_at((i,j),(b-(r+g)/2,0,0))
                    else:
                        redpic.set_at((i,j),(0,0,0))
                if (color == "green"):
                    if (g > (b+r)*factor and g > minwaarde and (r+b) < maxwaarde):
                        redpic.set_at((i,j),(g-(b+r)/2,0,0))
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
            highest = 0
            if (max(max(upleft,upright),max(downleft,downright)) == 0):
                # if we did not find any pixes at all, do not "rezoom", just zoom in
                if (crude == 0):
                    screen.blit(oldpic,(0,0))
                    pygame.display.flip()
                    return (-999,-999)
                else:
                    pass
            elif (upleft >= upright and upleft >= downleft and upleft >= downright):
                # if we find most pixel up-left, rezoom up-left
                leftX = leftX
                rightX = midX
                upY = upY
                downY = midY
                highest = upleft
            elif (upright >= downleft and upright >= downright):
                # etc, upright
                leftX = midX
                rightX = rightX
                upY = upY
                downY = midY
                highest = upright
            elif (downleft >= downright):
                # etc, downleft
                leftX = leftX
                rightX = midX
                upY = midY
                downY = downY
                highest = downleft
            elif (downright >= downleft):
                # etc, downright
                leftX = midX
                rightX = rightX
                upY = midY
                downY = downY
                highest = downright
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

        # stuur foto naar window met naam "balhekenner"
        #cv2.namedWindow("Balherkenner")
        #cv2.moveWindow("Balherkenner",100,100)
        #cv_image = pygame.surfarray.array2d(redpic)
        #cv2.imshow("Balherkenner", cv_image)
        #cv2.waitKey(10)

        redpic.set_colorkey((0,0,0))
        screen.blit(oldpic,(0,0))
        screen.blit(redpic,(0,0))
        pygame.display.flip()

        diffX = abs(rightX - leftX)
        diffY = abs(upY - downY)
        area = diffX * diffY
        maxima = area*255
        real = highest/area
        percent = int(float(max(1,real))/float(maxima)*100)
        print("I am this sure that that is the ball: " + str(percent) + "%" + "(power = " + str(real) + ")")
        if (percent < 25):
            print("So I'm probably wrong?")
        else:
            print("So I'm probably right?")
        #pygame.image.save(oldpic,"testpic.png")

        return ((float(float(midX) / float(W))-0.5)*2,(float(float(midY) / float(H))-0.5)*2)