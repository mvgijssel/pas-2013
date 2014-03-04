

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import random

import basebehavior.behaviorimplementation
import cv2


class PlukKleur_0(basebehavior.behaviorimplementation.BehaviorImplementation):


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.nao.say("Test Mode Us: Sook bahl.")
        self.timer = 20
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

        (posx,posy) = self.nao.waar_is_bal()
        print("x: " + str(posx) + ", y: " + str(posy))
        if (abs(posx) <= 0.3 and abs(posy) <= 0.1):
            # ligt in het midden van blikveld: loop er naar toe
            print("ik zie de bal. Ik loop er naar toe.")
            self.nao.loop_naar_bal()
        else:
            if (posx == -999 or posy == -999):
                #self.nao.say("Ik zie de bal niet.")
                print("Ik zie de bal niet. Ik zoek verder.")
                self.nao.zoek_bal()
            elif (posx < -0.3):
                print ("Ik zie de bal links boven.")
                self.nao.walk(0,0,0.25)
            elif (posx >= 0.3):
                print ("Ik zie de bal rechts boven.")
                self.nao.walk(0,0,-0.25)
            elif (posx > -0.3 and posx < .3 and posy > 0):
                print("ik zie de bal vlak voor me.")
                self.nao.kijk_lager()
                dist = self.nao.hoe_ver_bal()
                if (dist <= 0.05):
                    # 5 cm of minder verderop
                    print("de bal ligt op minder dan 5 cm, I loop er tegen aan.")
                    self.nao.walk(0.5,0,0)
            elif (posx > -0.3 and posx < 0.3 and posy < 0):
                print("ik zie de bal een eindje verderop.")
                self.nao.kijk_hoger()
        return
