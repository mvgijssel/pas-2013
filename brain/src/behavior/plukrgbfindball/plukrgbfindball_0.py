

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import random

class PlukRGBfindball_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.step = 0

        # verwijder vanaf hier
        self.__start_time = time.time()

        #Make sure the robot is standing and looks horizontal:
        self.__nao.look_horizontal()

        #Possible states (WALK or TURN):
        self.__state = "WALK"
        self.__last_recogtime = time.time()
        # tot hier

    def implementation_update(self):

        # verwijder vanaf hier
        if (time.time() - self.__start_time) > 10:
            if self.__state == "TURN":
                if not self.__nao.isWalking():
                    self.__state = "WALK"
                    self.__nao.walkNav(random.random() * 10, 0, 0)
            elif self.__state == "WALK":
                if not self.__nao.isWalking():
                    self.__state = "TURN"
                    self.__nao.walkNav(0, 0, random.random() * 2 - 1, 0.1)



        return
        # tot hier

        seq = ["up","mid","down","turn"]

        self.step += 1
        if (self.step >= len(seq)):
            self.step = 0

        action = seq[self.step]
        if (action == "turn"):
            self.nao.walk(0,0,1)
        elif (action == "down"):
            self.nao.kijk_lager(30)
        elif (action == "up"):
            self.nao.kijk_hoger(30)
        elif (action == "mid"):
            self.nao.corrigeer_hoofd()

        if (self.nao.is_er_bal() == True):
            self.set_finished()
