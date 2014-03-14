

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import random,time

class PlukRGBfindball_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.step = 0

    def implementation_update(self):

        seq = ["up","mid","down","mid","turn"]

        self.step += 1
        if (self.step >= len(seq)):
            self.step = 0

        if (self.nao.is_er_bal() == True):
            self.set_finished()
            self.step = 1
            return

        action = seq[self.step]
        if (action == "turn"):
            self.nao.walk(0,0,1)
        elif (action == "down"):
            self.nao.kijk_lager(30)
        elif (action == "up"):
            self.nao.kijk_hoger(5)
        elif (action == "mid"):
            self.nao.corrigeer_hoofd()

        if (self.nao.is_er_bal() == True):
            self.set_finished()
            self.step = 1
