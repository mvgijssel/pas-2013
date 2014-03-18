

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import random

import basebehavior.behaviorimplementation
import cv2


class PlukKleur_0(basebehavior.behaviorimplementation.BehaviorImplementation):


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.nao.say("Test: Pluk's Find Ball")
        self.timer = 30
        self.nao.complete_behavior("standup")
        self.nao.look_horizontal()

        self.nao.set_do_nothing_on_stop(True) # The Nao will still be enslaved

        self.plukrgbfindball = self.ab.plukrgbfindball({}) # kijk waar de bal is
        self.selected_behaviors = [
            ("plukrgbfindball", "self.found == False")
        ]

        self.found = False

    def implementation_update(self):

        (posx,posy) = self.nao.waar_is_bal()
        if (self.found == False and posx != -999 and posy != -999):
            print("bal gevonden: stoppen met zoeken")
            sound = random.choice(["target.wav","target2.wav","target3.wav"])
            self.nao.zeg_dit(sound)
            self.found = True
            self.plukrgbfindball.set_finished()
        elif (self.found == True and (posx == -999 or posy == -999)):
            print("bal kwijt: verder gaan met zoeken")
            sound = random.choice(["target_lost1.wav","target_lost2.wav"])
            self.nao.zeg_dit(sound)
            self.found = False
            self.plukrgbfindball = self.ab.plukrgbfindball({})


        return
