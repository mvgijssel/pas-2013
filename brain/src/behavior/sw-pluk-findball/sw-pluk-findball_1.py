

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation


class Sw-pluk-findball_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        #define list of sub-behavior here
        pass

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
