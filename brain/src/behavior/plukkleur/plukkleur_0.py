

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import random

import basebehavior.behaviorimplementation
import cv2


class PlukKleur_0(basebehavior.behaviorimplementation.BehaviorImplementation):


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.nao.say("Test: How often do I see the ball?")
        self.timer = 30
        self.nao.complete_behavior("standup")
        self.nao.look_at(0.5,0.75)

    def implementation_update(self):

        # Check for postcondition.
        # It is currently never set, so you'll have to stop the behavior manually by pressing Enter or Ctrl-C in the Terminal.
        # Fixing this to detect any goal scored and then stopping might be one of your improvements for this software.
        if (self.timer < 1):
            self.timer += 1
            if (self.timer%10 == 0):
                print("next test in " + str(int(self.timer/10)) + " seconds.")
            return
        else:
            self.timer = 0

        print("")
        #print("Ik kijk nu of ik een bal zie...")
        #print("")
        (posx,posy) = self.nao.waar_is_bal()
        #if ((posx,posy) == (-999,-999)):
        #    print("Ik zie GEEN bal.")
        #else:
        #    print("Ik zie WEL een bal.")

        #print("")
        #print("Ik kijk nu of ik een hoek zie...")
        #print("")
        #seen = self.nao.zie_hoek()
        #if (seen == True):
        #    print("Ik zie WEL een hoek")
        #else:
        #    print("Ik zie GEEN hoek")

        return
