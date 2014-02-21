

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import os

class SillyWalkers_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    # this implementation should not define an __init__ !!!
        

    def implementation_init(self):

        # get the nao reference
        # get the nao reference
        nao = self.body.nao(0)

        # say something
        nao.say('Dikke shine')

        # idea:
        # - one behaviour which walks towards whatever is in the center of the screen
        # - another behaviour which centers the field of view while rotating the head
        # - rotate the nao based on the rotation of the head to correct the course it is walking


    def implementation_update(self):

        print 'running'

        # update function at 10Hz

        #execfile(self.eval_file)

        # you can do things here that are low-level, not consisting of other behaviors

        # in this function you can check what behaviors have failed or finished
        # and do possibly other things when something has failed

        pass





