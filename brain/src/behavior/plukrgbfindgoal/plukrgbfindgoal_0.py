

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation


class Plukrgbfindgoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.nao.look_horizontal()

    def set_done(self):
        self.m.add_item('last_done',time.time(),{})

    def implementation_update(self):

        if (self.nao.is_er_bal() == True):
            self.set_done()
            return

        # draai rondjes om de bal, tot je de goal hebt gevonden.
        self.nao.walk(0,0.1,-0.25)
        seen = self.nao.waar_goal()



