

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import random

import basebehavior.behaviorimplementation
from behavior.plukkleur import balherkenning
import cv2
import util.naovideo as naovideo


class PlukKleur_0(basebehavior.behaviorimplementation.BehaviorImplementation):


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.nao.say("Test Mode Us: Sook bahl.")
        self.timer = 20
        self.detector = balherkenning.RasterImage(naovideo.VideoModule(self.nao.get_robot_ip()))
        self.nao.complete_behavior("standup")
        self.nao.look_at(0.5,0.75)


    def implementation_update(self):

        # Check for postcondition.
        # It is currently never set, so you'll have to stop the behavior manually by pressing Enter or Ctrl-C in the Terminal.
        # Fixing this to detect any goal scored and then stopping might be one of your improvements for this software.
        if (self.timer < 5):
            self.timer += 1
            return
        else:
            self.timer = 0

        (posx,posy) = self.detector.getPos()
        HEAD_YAW, HEAD_PITCH = self.nao.get_angles(['HeadYaw', 'HeadPitch'], False)
        # yaw = horizontaal draaien hoofd, pitch = verticaal draaien hoofd
        # gemeten: bij een head angle van "0.75", is het onderste stipje op 35 cm afstand, en het bovenste stipje op 130 cm

        # afstand (cm) = tan(hoek) * 45cm

        if (posx == -999 or posy == -999):
            #self.nao.say("Ik zie de bal niet.")
            print("Ik zie geen bal.")
            self.nao.walk(0,0,1)
        elif (posx < -0.5):
            print ("Ik zie de bal links boven.")
            #self.nao.say("links boven: " + str(posx) + "ix, en " + str(posy) + "eiy")
            self.nao.walk(0.1,0,0.1)
        elif (posx >= 0.5):
            print ("Ik zie de bal rechts boven.")
            #self.nao.say("rechts boven: " + str(posx) + "ix, en " + str(posy) + "eiy")
            self.nao.walk(0.1,0,-0.1)
        elif (posx > -0.5 and posx < .5 and posy > 0):
            # uitrekenen hoe ver
            print("ik zie de bal vlak voor me.")
            # vooruit lopen
            self.nao.walk(0.3,0,0)
        elif (posx > -0.5 and posx < 0.5 and posy < 0):
            print("ik zie de bal een eindje verderop.")
            self.nao.walk(0.5,0,0)
        return
