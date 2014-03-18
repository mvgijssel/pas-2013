

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
from util.nao_settings import NaoSettings

class Naocalibration_0(basebehavior.behaviorimplementation.BehaviorImplementation):


    def implementation_init(self):

        pass

    def implementation_update(self):

        if self.m.n_occurs("framerate") > 0:

            # get the framerate
            (recogtime, observation) = self.m.get_last_observation("framerate")

            # set the framerate in the NaoCalibration object
            NaoSettings.set_time_per_frame(observation['seconds_per_frame'])

            if self.debug:
                print "Seconds per frame: " + str(observation['seconds_per_frame'])
