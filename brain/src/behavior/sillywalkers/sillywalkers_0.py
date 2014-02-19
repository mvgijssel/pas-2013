

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import os

class SillyWalkers_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    # this implementation should not define an __init__ !!!
        

    def implementation_init(self):

        # constructor
       
        # somevar is passed to the config_sillywalkers
        # print self.somevar; 
        
        # self.eval_file = os.getcwd() + '/behavior/sillywalkers/eval_code.py';

        print 'init!'

        pass

    def implementation_update(self):

        # update function at 10Hz

        #execfile(self.eval_file)

        # you can do things here that are low-level, not consisting of other behaviors

        # in this function you can check what behaviors have failed or finished
        # and do possibly other things when something has failed
        pass



