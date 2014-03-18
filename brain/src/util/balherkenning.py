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

yellow = (0.5,0.5,0)
blue = (0,0,1)
darkblue = (0.16,0.16,0.68)
green = (0,1,0)
red = (1,0,0)
pink = (0.46,0.27,0.27)
white = (0.33,0.33,0.33)
black = (0.0,0.0,0.0)
greybrown = (0.37,0.32,0.32)
darkgreen = (0.21,0.65,0.15)
lightpink = (0.39,0.31,0.31)
yellow2 = (0.42,0.42,0.14)

colors = [yellow,blue,green,red,white,black,greybrown,pink,darkgreen,lightpink,darkblue,yellow2]
reds = [red,pink,lightpink]
blues = [blue,darkblue]
yellows = [yellow,yellow2]

pygame.init()


#
# hoe te gebruiken: een andere module kan dit typen:
# import util.balherkenning
# detector = balherkenning.rasterImage()
# (posx,posy) = detector.getPos()
#

lastreturn_goal = (-999,-999)
lastreturn_ball = (-999,-999)
lastreturn_goal_time = time.time()-5
lastreturn_ball_time = time.time()-5
time_buffer = 0 #hoeveel seconden hij een beeld bewaart

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

    def getGoal(self):
        global lastreturn_goal,lastreturn_goal_time
        now = time.time()
        if (lastreturn_goal_time >= now-time_buffer):
            return lastreturn_goal
        oldpic = self.get_new_image()
        oldpic = pygame.image.fromstring(oldpic.tostring(),(oldpic.width,oldpic.height),"RGB")
        W = oldpic.get_width()
        H = oldpic.get_height()
        simplegrid = []
        num_blocks = 25 # in hoeveel blokjes het beeld wordt verdeelt
        for i in range(0,W,int(W/num_blocks)):
            simplegrid.append([])
            for j in range(0,H,int(H/num_blocks)):
                col = oldpic.get_at((i,j))
                simplegrid[len(simplegrid)-1].append((col,(i,j)))

        found_blue = []
        found_yellow = []
        lowest_blue = 999
        highest_blue = -1
        lowest_yellow = 999
        highest_yellow = -1

        middle_blue = 0
        middle_yellow = 0

        MIN_NUM = 5 # minimum number of pixels of a color to be found
        for i in simplegrid:
            num_blue = 0
            num_yellow = 0
            low_blue = 999
            high_blue = -1
            low_yellow = 999
            high_yellow = -1
            for j in i:
                (col,(x,y)) = j
                col = bestColor(col)
                if (yellows.count(col) > 0):
                    num_yellow += 1
                    if (y < low_yellow):
                        low_yellow = y
                    if (y > high_yellow):
                        high_yellow = y
                elif (blues.count(col) > 0):
                    num_blue += 1
                    if (y < low_blue):
                        low_blue = y
                    if (y > high_blue):
                        high_blue = y
            if (num_blue > MIN_NUM):
                found_blue.append((x,low_blue,high_blue))
            if (num_yellow > MIN_NUM):
                found_yellow.append((x,low_yellow,high_yellow))

        if (len(found_blue) > 0):
            for temp in found_blue:
                (x,ymin,ymax) = temp
                if (ymin < lowest_blue):
                    lowest_blue = ymin
                if (ymax > highest_blue):
                    highest_blue = ymax
                middle_blue += x
        if (len(found_yellow) > 0):
            for temp in found_yellow:
                (x,ymin,ymax) = temp
                if (ymin < lowest_yellow):
                    lowest_yellow = ymin
                if (ymax > highest_yellow):
                    highest_yellow = ymax
                middle_yellow += x

        if (len(found_blue) > 0):
            middle_blue = middle_blue / len(found_blue)
        if (len(found_yellow) > 0):
            middle_yellow = middle_yellow / len(found_yellow)


        toreturn = None
        if (len(found_blue) > 0 and len(found_yellow) > 0 and highest_blue < lowest_yellow):
            # found blue and yellow, blue above yellow
            toreturn = ("yellow-side corner",middle_yellow)
        elif (len(found_blue) > 0 and len(found_yellow) > 0 and highest_yellow < lowest_blue):
            # found blue and yellow, yellow above blue
           toreturn = ("blue-side corner",middle_blue)
        elif (len(found_blue) > 0):
            # found blue
           toreturn = ("blue goal",middle_blue)
        elif (len(found_yellow) > 0):
            # found blue
           toreturn = ("yellow goal",middle_yellow)

        lastreturn_goal = toreturn
        lastreturn_goal_time = time.time()
        return toreturn


    def getPos(self):
        global lastreturn_ball,lastreturn_ball_time
        now = time.time()
        if (lastreturn_ball_time >= now-time_buffer):
            return lastreturn_ball
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
                #oldpic.set_at((i,j),bestColor(col))
                if (color == "red"):
                    if (r > (b+g)*factor and r > minwaarde and g < maxwaarde and b < maxwaarde):
                        if (reds.count(bestColor(col)) > 0):
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
                    lastreturn_ball = (-999,-999)
                    lastreturn_ball_time = time.time()
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

        #wincolor = oldpic.get_at((midX,midY))
        #wincolor1 = oldpic.get_at((pointUpLeft_x,pointUpLeft_y))
        #wincolor2 = oldpic.get_at((pointUpRight_x,pointUpRight_y))
        #wincolor3 = oldpic.get_at((pointDownLeft_x,pointDownLeft_y))
        #wincolor4 = oldpic.get_at((pointDownRight_x,pointDownRight_y))
        #wincolor5 = oldpic.get_at((rightX-1,upY+1))
        #wincolor6 = oldpic.get_at((leftX+1,upY+1))
        #wincolor7 = oldpic.get_at((rightX-1,downY-1))
        #wincolor8 = oldpic.get_at((leftX+1,downY-1))
        #wins = [wincolor,wincolor1,wincolor2,wincolor3,wincolor4,wincolor5,wincolor6,wincolor7,wincolor8]

        wins = []
        for i in range(leftX,rightX,2):
            for j in range(upY,downY,2):
                wins.append(oldpic.get_at((i,j)))
            
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
            if (reds.count(best) > 0):
                print("----I'm quite certain this is the red ball.----")
                found_red = True
                break
        if (found_red == False):
            print("----This might actually not be the red ball. Maybe its "+ str(best) + ".----")
            screen.blit(oldpic,(0,0))
            pygame.display.flip()
            lastreturn_ball = (-999,-999)
            lastreturn_ball_time = time.time()
            return (-999,-999)

        redpic.set_colorkey((0,0,0))
        screen.blit(oldpic,(0,0))
        screen.blit(redpic,(0,0))
        pygame.display.flip()

        toreturn = ((float(float(midX) / float(W))-0.5)*2,(float(float(midY) / float(H))-0.5)*2)
        lastreturn_ball = toreturn
        lastreturn_ball_time = time.time()
        return toreturn

def getDist(defined,actual):
    (b1,g1,r1,a) = actual
    total = b1 + g1 + r1
    b1 = float(b1) / float(max(1,total))
    g1 = float(g1) / float(max(1,total))
    r1 = float(r1) / float(max(1,total))
    (r2,g2,b2) = defined
    distR = abs(float(r1) - float(r2))
    distB = abs(float(b1) - float(b2))
    distG = abs(float(g1) - float(g2))
    totalDist = float(distR + distB + distG)/3.0
    return totalDist

def getDists(defined,actual):
    (b1,g1,r1,a) = actual
    total = b1 + g1 + r1
    b1 = b1 / max(1,total)
    g1 = g1 / max(1,total)
    r1 = r1 / max(1,total)
    (r2,g2,b2) = defined
    distR = abs(float(r1) - float(r2))
    distB = abs(float(b1) - float(b2))
    distG = abs(float(g1) - float(g2))
    return (distR,distG,distB)

def bestColor(actual):
    closest = 999
    best = None
    for color in colors:
        newdist = getDist(color,actual)
        if (newdist < closest):
            closest = newdist
            best = color
    return best