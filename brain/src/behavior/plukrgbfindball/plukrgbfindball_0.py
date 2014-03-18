

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
        self.nao.look_horizontal()

    def implementation_update(self):

        seq = ["mid","wait","mid","wait","down","wait","turn"]

        self.step += 1
        if (self.step >= len(seq)):
            self.step = 0

        action = seq[self.step]
        if (action == "turn"):
            self.nao.walk(0,0,0.5)
        elif (action == "down"):
            self.nao.kijk_lager(30)
        elif (action == "up"):
            self.nao.kijk_hoger(10)
        elif (action == "mid"):
            self.nao.look_horizontal()
            self.nao.kijk_hoger(5)
        elif (action == "wait"):
            time.sleep(0.25)

        if (self.nao.is_er_bal() == True):
            self.set_finished()
            self.step = 0
