

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation


class Plukrgballigngoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)

    def implementation_update(self):

        # draai rondjes om de bal, tot je de goal hebt gevonden.
        (posx,posy) = self.nao.waar_is_bal()
        if (posx == -999 or posy == -999):
            self.nao.kijk_lager(5)
            self.nao.walk(-0.1,0,0)
        elif (posy > 0):
            self.nao.walk(0.1,0,0)
        elif (posy < 0):
            self.nao.kijk_hoger(5)
            seen = self.nao.waar_goal()
            if (seen != None):
                if (seen > 0):
                    self.nao.walk(0,-0.1,-0.25)
                else:
                    self.nao.walk(0,0.1,0.25)




