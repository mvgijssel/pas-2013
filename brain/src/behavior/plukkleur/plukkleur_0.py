

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
            ("plukrgbfindball", "self.nao.is_er_bal() == False")
        ]

    def implementation_update(self):

        # Check for postcondition.
        # It is currently never set, so you'll have to stop the behavior manually by pressing Enter or Ctrl-C in the Terminal.
        # Fixing this to detect any goal scored and then stopping might be one of your improvements for this software.
        if (self.timer > 0):
            self.timer -= 1
            if (self.timer%10 == 0):
                print("next test in " + str(int(self.timer/10)) + " seconds.")
            return
        else:
            self.timer = 30

        print("")

        (posx,posy) = self.nao.waar_is_bal()
        if (self.found == False and posx != -999 and posy != -999):
            self.nao.say("found it!")
            self.found = True
        else:
            self.found = False

        print("")


        return
