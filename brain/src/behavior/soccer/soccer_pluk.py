import basebehavior.behaviorimplementation

import time
import balherkenning

class Soccer_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''The core soccer behavior for PAS.'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        #Select Nao to use:
        self.nao = self.body.nao(0)
        self.nao.say("Let's see if I can find the ball.")
        self.timer = 30
        self.detector = balherkenning.rasterImage()
        

    def implementation_update(self):

        # Check for postcondition.
        # It is currently never set, so you'll have to stop the behavior manually by pressing Enter or Ctrl-C in the Terminal.
        # Fixing this to detect any goal scored and then stopping might be one of your improvements for this software.
        if (timer < 30):
            timer += 1
            return
        else:
            timer = 0

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
