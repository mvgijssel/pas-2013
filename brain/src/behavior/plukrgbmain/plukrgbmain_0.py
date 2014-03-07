

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import random
import time
class PlukRGBmain_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.prev_fall_time = 0

        self.plukrgbfindball = self.ab.plukrgbfindball({})
        self.plukrgbapproachball = self.ab.plukrgbapproachball({})

        self.selected_behaviors = [
            ("plukrgbfindball", "self.seeball == False and self.at_ball == False"),
            ("plukrgbapproachball", "self.seeball == True and self.at_ball == False")
        ]

        self.nao.set_do_nothing_on_stop(True) # The Nao will still be enslaved
        sound = random.choice(["deploy1.wav","deploy2.wav"])
        self.nao.zeg_dit(sound)

        self.nao.complete_behavior("standup")

        self.seeball = False
        self.at_ball = False

    def implementation_update(self):

        ranIdle = random.randint(1,300)
        if (ranIdle == 5): # 1x per 30 seconde?
            sound = random.choice(["idle.wav","idle2.wav","idle3.wav","idle4.wav"])
            self.nao.zeg_dit(sound)

        if (self.m.n_occurs('naoHasFallen') > 0):
            (recogtime, observation) = self.m.get_last_observation('naoHasFallen')
            if (recogtime > self.prev_fall_time):
                # I fell
                sound = random.choice(["alarm.wav"])
                self.nao.zeg_dit(sound)
                time.sleep(0.1)
                self.nao.zeg_dit(sound)
                time.sleep(0.1)
                self.nao.zeg_dit(sound)
                time.sleep(0.1)
                self.nao.zeg_dit(sound)
                time.sleep(0.1)
                self.nao.zeg_dit(sound)
                time.sleep(0.1)
                self.nao.zeg_dit(sound)
                time.sleep(0.1)
                self.nao.complete_behavior("standup")
                sound = random.choice(["hate1.wav","hate2.wav","hate3.wav"])
                self.nao.zeg_dit(sound)
                self.prev_fall_time = recogtime
                return

        print("updating...")
        waarbal = self.nao.is_er_bal()
        if (waarbal == True):
            verbal = self.nao.hoe_ver_bal()
        else:
            verbal = 999
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