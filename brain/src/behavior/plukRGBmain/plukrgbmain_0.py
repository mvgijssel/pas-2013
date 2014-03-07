

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import random

class PlukRGBmain_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)

        self.plukRGBfindball = self.ab.plukRGBfindball({})
        self.plukRGBapproachball = self.ab.plukRGBapproachball({})

        self.selected_behaviors = [
            ("plukRGBfindball", "self.seeball == False and self.at_ball == False"),
            ("plukRGBapproachball", "self.at_ball == False & self.seeball == True"),
        ]

        self.nao.set_do_nothing_on_stop(True) # The Nao will still be enslaved
        sound = random.choice(["deploy1.wav","deploy2.wav"])
        self.nao.zeg_dit(sound)

        self.seeball = False
        self.at_ball = False

    def implementation_update(self):

        if (self.m.n_occurs('naoHasFallen') > 0):
            (recogtime, observation) = self.m.get_last_observation('naoHasFallen')
            if (recogtime > self.prev_fall_time):
                # I fell
                sound = random.choice(["hate1.wav","hate2.wav","hate3.wav"])
                self.nao.zeg_dit(sound)
                self.prev_fall_time = recogtime
                self.nao.complete_behavior("standup")
                return

        waarbal = self.nao.is_er_bal()
        verbal = self.nao.hoe_ver_bal()
        if (waarbal == False):
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