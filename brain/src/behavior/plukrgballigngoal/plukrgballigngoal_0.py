

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import time


class Plukrgballigngoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)

    def set_done(self):
        self.m.add_item('last_done',time.time(),{})

    def implementation_update(self):

            seen = self.nao.waar_goal()
            if (seen != None):
                if (seen > 0.3):
                    self.nao.walk(0.1,0.1,-0.25)
                elif (seen > 0.3):
                    self.nao.walk(0.1,-0.1,0.25)
                else:
                    self.set_done()
            else:
                self.set_done()




