

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import time

class PlukRGBfindball_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.step = 0

    def set_done(self):
        self.m.add_item('last_done',time.time(),{})

    def implementation_update(self):

        if (self.nao.is_er_bal() == True):
            self.set_done()
            return

        seq = ["wait","up","wait","mid","wait","down","wait","turn"]

        self.step += 1
        if (self.step >= len(seq)):
            self.step = 0

        action = seq[self.step]
        print("findball: action = " + str(action))
        if (action == "turn"):
            self.nao.walk(0,0,0.5)
        elif (action == "down"):
            self.nao.look_horizontal()
            self.nao.kijk_lager(7)
        elif (action == "up"):
            self.nao.look_horizontal()
            self.nao.kijk_hoger(5)
        elif (action == "mid"):
            self.nao.look_horizontal()
        elif (action == "wait"):
            time.sleep(1)
