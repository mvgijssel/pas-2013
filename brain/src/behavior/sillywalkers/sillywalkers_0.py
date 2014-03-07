

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import os
import time

class SillyWalkers_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    # this implementation should not define an __init__ !!!
        

    def implementation_init(self):

        # get the nao reference
        self.nao = self.body.nao(0)

        # when the nao is done, don't do anything. Don't sit down
        self.nao.set_do_nothing_on_stop(True)

        #define list of sub-behavior here
        self.findball = self.ab.findball({})
        self.objectdetector = self.ab.objectdetector({})

        self.selected_behaviors = [
            ("objectdetector", "True"),
            ("findball", "True"),
        ]

        self.restart_time = time.time()



    def implementation_update(self):




        pass





