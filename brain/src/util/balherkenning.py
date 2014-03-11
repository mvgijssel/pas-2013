# geschreven voor Paul-Luuk Profijt, 10-2-2014, voor Practicum Autonome Systemen aan de RuG

import pygame,random
import util.vidmemreader
import Image
import cv2
import cv
from pygame.locals import *
import time

window = 0
screen = None
imgsize = 200
imgheight = 0

yellow = (255,255,0)
blue = (0,0,255)
green = (0,255,0)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
colors = [yellow,blue,green,red,white,black]

pygame.init()


#
# hoe te gebruiken: een andere module kan dit typen:
# import util.balherkenning
# detector = balherkenning.rasterImage()
# (posx,posy) = detector.getPos()
#



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
        # waardes voor rood herkennen trainen
        self.std_minwaarde = 200 # moet minimaal zoveel van de kleur aanwezig zijn <0,255>, om zwart uit te schakelen
        self.std_factor = 0.9 # er moet minimaal "factor" keer zoveel "kleur" zijn als andere kleuren samen
        self.std_maxwaarde = 140 # de andere kleuren mogen maximaal deze waarde hebben, om wit uit te schakelen
        self.p_minwaarde = 0.5
        self.p_factor = 0.5
        self.p_maxwaarde = 0.5

    def get_new_image(self):
        img = self.vid.get_image()
        return img

    def getCorner(self):
        oldpic = self.get_new_image()
        oldpic = pygame.image.fromstring(oldpic.tostring(),(oldpic.width,oldpic.height),"RGB")
        W = oldpic.get_width()
        H = oldpic.get_height()
        yellow = (255,255,0)
        blue = (0,0,255)

        pic = []
        for i in range(0,W):
            pic.append([])
            for j in range(0,H):
                col = oldpic.get_at((i,j))
                r = col.b
                g = col.g
                b = col.r
                if (r > 150):
                    r = 255
                else:
                    r = 0
                if (g > 150):
                    g = 255
                else:
                    g = 0
                if (b > 150):
                    b = 255
                else:
                    b = 0
                pic[i].append((r,g,b))

        newpic = []
        num = 0
        for i in range(0,len(pic)-2,2):
            newpic.append([])
            for j in range(0,len(pic[i])-2,2):
                (r1,g1,b1) = pic[i][j]
                (r2,g2,b2) = pic[i+1][j]
                (r3,g3,b3) = pic[i][j+1]
                (r4,g4,b4) = pic[i+1][j+1]
                r = int((r1 + r2 + r3 + r4) / 4)
                g = int((g1 + g2 + g3 + g4) / 4)
                b = int((b1 + b2 + b3 + b4) / 4)
                color = (r,g,b)
                newpic[num].append(color)
            num += 1

        power_y = 0
        (x_y,y_y) = (0,0)
        power_b = 0
        (x_b,y_b) = (0,0)
        for i in range(0,len(newpic)-2,2):
            for j in range(0,len(newpic[i])-2,2):
                (r1,g1,b1) = newpic[i][j]
                (r2,g2,b2) = newpic[i+1][j]
                (r3,g3,b3) = newpic[i][j+1]
                (r4,g4,b4) = newpic[i+1][j+1]
                r = int((r1 + r2 + r3 + r4) / 4)
                g = int((g1 + g2 + g3 + g4) / 4)
                b = int((b1 + b2 + b3 + b4) / 4)
                if (r > 150 and g > 150 and b < 100):
                    (r,g,b) = yellow
                    newpower = int((r + g) / 2)
                    if (newpower > power_y):
                        power_y = newpower
                        (x_y,y_y) = (i,j)
                elif (r < 100 and g < 100 and b > 150):
                    (r,g,b) = blue
                    newpower = b
                    if (newpower > power_b):
                        power_b = newpower
                        (x_b,y_b) = (i,j)

        if (y_y < y_b):
            # yellow above blue
            if (power_y > 200 and power_b > 200):
                # blue and yellow strong enough
                return True
        return False

        pos_y_x = int(x_y / len(newpic)) * imgsize
        pos_y_y = int(y_y / len(newpic[0])) * imgheight
        pos_b_x = int(x_b / len(newpic)) * imgsize
        pos_b_y = int(y_b / len(newpic[0])) * imgheight
        for i in range(0,imgsize):
            screen.set_at((i,pos_y_y),yellow)
            screen.set_at((i,pos_b_y),blue)
            screen.set_at((i,pos_y_y-1),yellow)
            screen.set_at((i,pos_b_y-1),blue)
            screen.set_at((i,pos_y_y+1),yellow)
            screen.set_at((i,pos_b_y+1),blue)
        for i in range(0,imgheight):
            screen.set_at((pos_y_x,i),yellow)
            screen.set_at((pos_b_x,i),blue)
            screen.set_at((pos_y_x-1,i),yellow)
            screen.set_at((pos_b_x-1,i),blue)
            screen.set_at((pos_y_x+1,i),yellow)
            screen.set_at((pos_b_x+1,i),blue)
        pygame.display.flip()


    def getPos(self):
        init_window()
        color = self.color
        oldpic = self.get_new_image()
        oldpic = pygame.image.fromstring(oldpic.tostring(),(oldpic.width,oldpic.height),"RGB")
        W = oldpic.get_width()
        H = oldpic.get_height()
        W2 = screen.get_width()
        Scale = float(float(W2 * 100) / float(W * 100))
        W = W2
        H = H * Scale
        W = int(W)
        H = int(H)
        imgheight = H
        oldpic = pygame.transform.scale(oldpic,(W,H))

        #print("color detection - redscaling")

        #self.p_maxwaarde = float(random.randint(9,20))/float(10)
        #self.p_minwaarde = float(random.randint(5,11))/float(10)
        #self.p_factor = float(random.randint(4,6))/float(10)

        self.p_maxwaarde = 0.88 #* float((random.randint(80,130))/float(100))
        self.p_minwaarde = 0.77 #* float((random.randint(80,130))/float(100))
        self.p_factor = 0.52 #* (float(random.randint(80,130))/float(100))

        print("maxwaarde: " + str(self.p_maxwaarde))
        print("minwaarde: " + str(self.p_minwaarde))
        print("factor: " + str(self.p_factor))

        redpic = pygame.transform.scale(oldpic,(W,H))
        for i in range(0,W):
            for j in range(0,H):
                col = oldpic.get_at((i,j))
                r = col.b
                g = col.g
                b = col.r
                minwaarde = self.std_minwaarde * self.p_minwaarde # moet minimaal zoveel van de kleur aanwezig zijn <0,255>, om zwart uit te schakelen
                factor = self.std_factor * self.p_factor # er moet minimaal "factor" keer zoveel "kleur" zijn als andere kleuren samen
                maxwaarde = self.std_maxwaarde * self.p_maxwaarde # de andere kleuren mogen maximaal deze waarde hebben, om wit uit te schakelen
                if (color == "red"):
                    if (r > (b+g)*factor and r > minwaarde and g < maxwaarde and b < maxwaarde):
                        if (bestColor(col) == red):
                            redpic.set_at((i,j),(min(max(r-(b+g)/2,0),255),0,0))
                    else:
                        redpic.set_at((i,j),(0,0,0))
                if (color == "blue"):
                    if (b > (r+g)*factor and b > minwaarde and r < maxwaarde and g < maxwaarde):
                        redpic.set_at((i,j),(min(max(b-(r+g)/2,0),255),0,0))
                    else:
                        redpic.set_at((i,j),(0,0,0))
                if (color == "green"):
                    if (g > (b+r)*factor and g > minwaarde and r < maxwaarde and b < maxwaarde):
                        redpic.set_at((i,j),(min(max(g-(b+r)/2,0),255),0,0))
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

        #print("color detection - finding hotspot")
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

        pointUpLeft_x = (leftX + midX) / 2
        pointUpLeft_y = (upY + midY) / 2
        pointUpRight_x = (rightX + midX) / 2
        pointUpRight_y = (upY + midY) / 2
        pointDownLeft_x = (leftX + midX) / 2
        pointDownLeft_y = (upY + midY) / 2
        pointDownRight_x = (rightX + midX) / 2
        pointDownRight_y = (upY + midY) / 2

        wincolor = oldpic.get_at((midX,midY))
        wincolor1 = oldpic.get_at((pointUpLeft_x,pointUpLeft_y))
        wincolor2 = oldpic.get_at((pointUpRight_x,pointUpRight_y))
        wincolor3 = oldpic.get_at((pointDownLeft_x,pointDownLeft_y))
        wincolor4 = oldpic.get_at((pointDownRight_x,pointDownRight_y))
        wincolor5 = oldpic.get_at((rightX-1,upY+1))
        wincolor6 = oldpic.get_at((leftX+1,upY+1))
        wincolor7 = oldpic.get_at((rightX-1,downY-1))
        wincolor8 = oldpic.get_at((leftX+1,downY-1))
        wins = [wincolor,wincolor1,wincolor2,wincolor3,wincolor4,wincolor5,wincolor6,wincolor7,wincolor8]
            
        for i in range(leftX,rightX):
            for j in range(upY,downY):
                r = oldpic.get_at((i,j)).r
                oldpic.set_at((i,j),(r,50,0))

        for i in range(0,redpic.get_width()):
            oldpic.set_at((i,midY),(255,255,255))
        for j in range(0,redpic.get_height()):
            oldpic.set_at((midX,j),(255,255,255))

        found_red = False
        for win in wins:
            best = bestColor(win)
            if (best == red):
                print("----I'm quite certain this is the red ball.----")
                found_red = True
                break
        if (found_red == False):
            print("----This might actually not be the red ball.----")
            return (-999,-999)

        redpic.set_colorkey((0,0,0))
        screen.blit(oldpic,(0,0))
        screen.blit(redpic,(0,0))
        pygame.display.flip()

        return ((float(float(midX) / float(W))-0.5)*2,(float(float(midY) / float(H))-0.5)*2)

def getDist(defined,actual):
    (b1,g1,r1,a) = actual
    (r2,g2,b2) = defined
    distR = abs(r1 - r2)
    distB = abs(b1 - b2)
    distG = abs(g1 - g2)
    totalDist = (distR + distB + distG)/3
    return totalDist

def bestColor(actual):
    closest = 999
    best = None
    for color in colors:
        newdist = getDist(color,actual)
        if (newdist < closest):
            closest = newdist
            best = color
    return best