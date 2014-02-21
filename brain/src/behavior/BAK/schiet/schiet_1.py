
import basebehavior.behaviorimplementation
import time

nao = True

class Schiet_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        #define list of sub-behavior here
        self.start_time = time.time()
        self.nao = self.body.nao(0)
        if nao: self.nao.start_behavior("rag_kickball5")

    def implementation_update(self):

        #you can do things here that are low-level, not consisting of other behaviors

        #in this function you can check what behaviors have failed or finished
        #and do possibly other things when something has failed
        if (time.time() - self.start_time) > 4:
            self.nao.say("ain. nuhl.")
            self.m.add_item('subsume_stopped',time.time(),{'reason':'Hopefully I kicked the ball.'})

