

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import os
import time

from util.naovideo import VideoModule
from util.nao_settings import NaoSettings

class SillyWalkers_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    # this implementation should not define an __init__ !!!
        

    def implementation_init(self):

        # get the nao reference
        self.nao = self.body.nao(0)

        # get the ball object
        self.ball = NaoSettings.BALL_OBJECT

        # when the nao is done, don't do anything. Don't sit down
        self.nao.set_do_nothing_on_stop(True)

        # is a hack, should be an external behaviour which stands up when nao isn't standing
        # self.nao.complete_behavior("standup")

        # instantiate the behaviours, acts as a reset
        self.instantiate_behaviours()

        # define all the beheviours with start conditions
        # self.selected_behaviors = [
        #     ("naocalibration", "True"),
        #     ("objectdetector", "True"),
        #     ("findball", "True"),
        #     ("aligntorso", "self.findball.is_finished()"),
        #     ("approachball", "self.aligntorso.is_finished()")
        # ]

        self.selected_behaviors = [
            ("naocalibration", "True"),
            ("objectdetector", "True"),
            ("headfollowball", "True")
        ]

        self.restart_time = time.time()


    def implementation_update(self):

        # if the approach ball fails
        if self.approachball.is_failed():

            # restart findball, aligntorso, approachball
            self.findball = self.ab.findball({'debug': True})
            self.aligntorso = self.ab.aligntorso({'debug': True})
            self.approachball = self.ab.approachball({'debug', True})


    def instantiate_behaviours(self):

        # set the debug flag
        self.debug = True

        # NEED BEHAVIOUR FOR STANDING BACK UP

        # DO WE NEED TO MANUALLE STOP THE RUNNING BEHAVIOURS STILL RUNNING?

        #define list of sub-behavior here
        self.naocalibration = self.ab.naocalibration({'debug': True})
        self.objectdetector = self.ab.objectdetector({'debug': False})
        self.findball = self.ab.findball({'debug': True})

        # follow the ball the the head
        self.headfollowball = self.ab.headfollowball({'debug': True})

        # the calling of self.ab.aligntorso({'debug': False}) creates a new instance, and restarts a behaviour
        self.aligntorso = self.ab.aligntorso({'debug': True})
        self.approachball = self.ab.approachball({'debug', True})
