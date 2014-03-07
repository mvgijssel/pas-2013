

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation


class plukfindball_1(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)

    def implementation_update(self):

        choice = random.choice(["turn left","turn right","turn right","look down","look down","look up"])
        if (choice == "turn left"):
            self.nao.corrigeer_hoofd()
            self.nao.walk(0,0,1)
        elif (choice == "turn right"):
            self.nao.corrigeer_hoofd()
            self.nao.walk(0,0,-1)
        elif (choice == "look down"):
            self.nao.kijk_lager()
        elif (choice == "look up"):
            self.nao.kijk_hoger()

        if (self.nao.is_er_bal() == True):
            self.set_finished()
