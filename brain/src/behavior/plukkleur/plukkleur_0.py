

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import balherkenning

class PlukKleur_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.nao.say("Let's see if I can find the ball.")
        self.timer = 30
        self.detector = balherkenning.rasterImage()

    def implementation_update(self):

        # Check for postcondition.
        # It is currently never set, so you'll have to stop the behavior manually by pressing Enter or Ctrl-C in the Terminal.
        # Fixing this to detect any goal scored and then stopping might be one of your improvements for this software.
        if (self.timer < 30):
            self.timer += 1
            return
        else:
            self.timer = 0

        (posx,posy) = self.detector.getPos()
        if (posx < 0 and posy < 0):
            self.nao.say("LEFT UP")
        elif (posx >= 0 and posy < 0):
            self.nao.say("RIGHT UP")
        elif (posx < 0 and posy > 0):
            self.nao.say("LEFT DOWN")
        elif (posx < 0 and posy < 0):
            self.nao.say("RIGHT DOWN")
        self.set_finished()
        return



