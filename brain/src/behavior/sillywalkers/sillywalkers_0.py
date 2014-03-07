

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

        #define list of sub-behavior here
        self.findball = self.ab.findball({})
        self.objectdetector = self.ab.objectdetector({})

        self.selected_behaviors = [
            ("objectdetector", "True"),
            ("findball", "True"),
        ]

        # when the nao is done, don't do anything. Don't sit down
        self.nao.set_do_nothing_on_stop(True)

        self.restart_time = time.time()

        #Select Nao to use:
        self.nao = self.body.nao(0)
        self.nao.say("Lets play soccer!")

        # idea:
        # - one behaviour which walks towards whatever is in the center of the screen
        # - another behaviour which centers the field of view while rotating the head
        # - rotate the nao based on the rotation of the head to correct the course it is walking



    def implementation_update(self):




        pass





