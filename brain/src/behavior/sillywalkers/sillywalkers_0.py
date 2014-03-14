

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

        # when the nao is done, don't do anything. Don't sit down
        self.nao.set_do_nothing_on_stop(True)

        #define list of sub-behavior here
        self.findball = self.ab.findball({})
        self.objectdetector = self.ab.objectdetector({})
        self.naocalibration = self.ab.naocalibration({})

        self.selected_behaviors = [
            ("naocalibration", "True"),
            ("objectdetector", "True"),
            ("findball", "True")
        ]

        self.restart_time = time.time()



    def implementation_update(self):

        pass

        # 1 is for the camera id
        # print "Framerate: " + str(self.nao.get_proxy('video').getFrameRate(1))

        # print "trying to get an image"

        # is a blocking operation
        # img = self.naovideo.get_image()

        # print "the image: " + str(img)








