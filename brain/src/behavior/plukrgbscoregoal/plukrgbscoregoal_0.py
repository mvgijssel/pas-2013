

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import time


class Plukrgbscoregoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)

    def set_done(self):
        self.m.add_item('last_done',time.time(),{})

    def implementation_update(self):

        if (self.nao.is_er_bal() == False):
            self.set_done()
            return

        # just run forward
        self.nao.walk(0.25,0,0)

