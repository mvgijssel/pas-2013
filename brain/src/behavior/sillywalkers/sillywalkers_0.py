

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import os
import time

from util.naovideo import VideoModule
from util.nao_calibration import NaoCalibration

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

        # self.selected_behaviors = [
        #     ("objectdetector", "True"),
        #     ("findball", "True"),
        # ]

        self.selected_behaviors = [
            ("objectdetector", "True"),
        ]

        self.restart_time = time.time()


        self.naovideo = VideoModule(self.nao.get_robot_ip())



    def implementation_update(self):

        pass

        # 1 is for the camera id
        # print "Framerate: " + str(self.nao.get_proxy('video').getFrameRate(1))

        # print "trying to get an image"

        # is a blocking operation
        # img = self.naovideo.get_image()

        # print "the image: " + str(img)








