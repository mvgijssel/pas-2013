

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import time,math


class Plukrgballigngoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.seen_angle = -999
        self.start_time = time.time()

    def set_done(self):
        self.m.add_item('last_done',time.time(),{})

    def implementation_update(self):

        print("We zijn bij alligngoal aangekomen")

        print(time.time())
        print(self.start_time)

        if (time.time() > self.start_time + 5):
            print("TimeTimeTime")
            #self.set_done()
            #return

        # als we hier aankomen, dan is er de volgende situatie:
        # het doel is in ons blikveld: waar we naar kijken
        # de bal ligt (vlak?) voor ons
        # we moeten de bal tussen ons en het doel krijgen

            seen = self.nao.waar_goal()
            if (seen != None and self.seen_angle == -999):
                print("Ja, hij is hier gekomen")
                (yaw,pitch) = self.nao.get_yaw_pitch() # yaw is horizontaal draaien, van 120 (links) tot -120 (rechts)
                self.seen_angle = yaw
            else:
                if (abs(self.seen_angle) < 20): # dit is nog ongeveer binnen het huidige blikveld
                    print("allign goal: I am now alligned to the goal")
                    self.set_done()
                elif (self.seen_angle > 0):
                    # toen ik de bal zag, was die links van mij
                    print("allign goal: The goal is to my left.")
                    self.nao.walk(0,0.15,0)
                    self.nao.walk(0.15,0,0)
                    self.nao.walk(0,0,math.radians(-90))
                    self.set_done()
                elif (self.seen_angle < 0):
                    # toen ik de bal zag, was die rechts van mij
                    print("allign goal: The goal is to my right.")
                    self.nao.walk(0,-0.15,0)
                    self.nao.walk(0.15,0,0)
                    self.nao.walk(0,0,math.radians(90))
                    self.set_done()
                else:
                    print("allign goal: nothing?            ERROR ERROR ERROR")




