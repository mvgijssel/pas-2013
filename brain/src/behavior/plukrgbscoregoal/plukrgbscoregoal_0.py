

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation


class Plukrgbscoregoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)

    def implementation_update(self):

        # just run forward
        self.nao.kijk_lager(30)
        self.nao.walk(0.25,0,0)
        self.set_finished()

