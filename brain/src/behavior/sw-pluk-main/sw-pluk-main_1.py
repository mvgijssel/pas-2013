'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import random

class Sw-pluk-main_1(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.selected_behaviors = [
            ("sw-pluk-findball", "self.seeball == False and self.at_ball == False"),
            ("sw-pluk-approachball", "self.at_ball == False & self.seeball == True"),
        ]

        sound = random.choice(["deploy1.wav","deploy2.wav"])
        self.nao.zeg_dit(sound)

        self.seeball = False
        self.at_ball = False

    def implementation_update(self):

        waarbal = self.nao.waar_is_bal()
        verbal = self.nao.hoe_ver_bal()
        if (waarbal == (-999,-999)):
            if (self.seeball == True):
                sound = random.choice(["target_lost1.wav","target_lost2.wav"])
                self.nao.zeg_dit(sound)
                self.seeball = False
        else:
            if (self.seeball == False):
                sound = random.choice(["target.wav","target2.wav","target3.wav"])
                self.nao.zeg_dit(sound)
                self.seeball = True
        if (verbal <= 0.05):
            if (self.at_ball == False):

                self.at_bal = True
        else:
            if (self.seeball == True):
                self.at_ball = False
