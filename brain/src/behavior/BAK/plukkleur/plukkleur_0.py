

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import balherkenning
import util.naovideo as naovideo

class PlukKleur_0(basebehavior.behaviorimplementation.BehaviorImplementation):


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.nao.say("Test Mode Us: Cluuhr vahn bahl.")
        self.timer = 20
        self.detector = balherkenning.RasterImage(naovideo.VideoModule(self.nao.get_robot_ip()))

    def implementation_update(self):

        # Check for postcondition.
        # It is currently never set, so you'll have to stop the behavior manually by pressing Enter or Ctrl-C in the Terminal.
        # Fixing this to detect any goal scored and then stopping might be one of your improvements for this software.
        if (self.timer < 50):
            self.timer += 1
            return
        else:
            self.timer = 0

        (posx,posy) = self.detector.getPos()
        if (posx < 0 and posy < 0):
            self.nao.say("links boven: " + str(posx) + "ix, en " + str(posy) + "eiy")
        elif (posx >= 0 and posy < 0):
            self.nao.say("rechts boven: " + str(posx) + "ix, en " + str(posy) + "eiy")
        elif (posx < 0 and posy > 0):
            self.nao.say("links onder: " + str(posx) + "ix, en " + str(posy) + "eiy")
        elif (posx < 0 and posy < 0):
            self.nao.say("rechts onder: " + str(posx) + "ix, en " + str(posy) + "eiy")
        else:
            self.nao.say("Ik zie de bal niet.")
        return
