

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import balherkenning
import random
import util.naovideo as naovideo

class PlukKleur_0(basebehavior.behaviorimplementation.BehaviorImplementation):


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.nao.say("Test Mode Us: Cluuhr vahn bahl.")
        self.timer = 20
        self.detector = balherkenning.RasterImage(naovideo.VideoModule(self.nao.get_robot_ip()))
        self.nao.complete_behavior("standup")
        self.nao.look_at(0.5,0.75)


    def implementation_update(self):

        # Check for postcondition.
        # It is currently never set, so you'll have to stop the behavior manually by pressing Enter or Ctrl-C in the Terminal.
        # Fixing this to detect any goal scored and then stopping might be one of your improvements for this software.
        if (self.timer < 2):
            self.timer += 1
            return
        else:
            self.timer = 0

        (posx,posy) = self.detector.getPos()
        HEAD_YAW, HEAD_PITCH = self.nao.get_angles(['HeadYaw', 'HeadPitch'], False)
        # yaw = horizontaal draaien hoofd, pitch = verticaal draaien hoofd
        # gemeten: bij een head angle van "0.75", is het onderste stipje op 35 cm afstand, en het bovenste stipje op 130 cm



        if (posx == -999 or posy == -999):
            #self.nao.say("Ik zie de bal niet.")
            self.nao.walk(0,0,random.randint(-1,1)/2)
        elif (posx < -0.5):
            #self.nao.say("links boven: " + str(posx) + "ix, en " + str(posy) + "eiy")
            self.nao.walk(0.1,0,0.1)
        elif (posx >= 0.5):
            #self.nao.say("rechts boven: " + str(posx) + "ix, en " + str(posy) + "eiy")
            self.nao.walk(0.1,0,-0.1)
        elif (posx > -0.5 and posx < .5 and posy > 0):
            # uitrekenen hoe ver

            # vooruit lopen
            self.nao.walk(0.5,0,0)
        elif (posx > -0.5 and posx < 0.5 and posy < 0):
            self.nao.walk(0.5,0,0)
        return
