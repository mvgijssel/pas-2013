

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import random

class Sw-pluk-approachball_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        #define list of sub-behavior here
        pass

    def implementation_update(self):


        (posx,posy) = self.nao.waar_is_bal()
        print("x: " + str(posx) + ", y: " + str(posy))
        if (abs(posx) <= 0.3 and abs(posy) <= 0.1):
            # ligt in het midden van blikveld: loop er naar toe
            print("ik zie de bal. Ik loop er naar toe.")
            # rekent afstand uit, en loopt dan een stuk van die afstand vooruit
            dist = abs(self.nao.hoe_ver_bal() * 10)
            sound = random.choice(["search1.wav","search2.wav"])
            self.nao.say("Searching",sound)
            self.nao.walk(float(dist * 0.2),0,0)
        else:
            if (posx == -999 or posy == -999):
                #self.nao.say("Ik zie de bal niet.")
                print("Ik zie de bal niet. Ik zoek verder.")
                self.nao.zoek_bal()
            elif (posx < -0.3):
                if (posy < -0.1):
                    print ("Ik zie de bal links boven.")
                    self.nao.kijk_hoger()
                elif (posy > 0.1):
                    print ("Ik zie de bal links onder.")
                    self.nao.kijk_lager()
                else:
                    print("Ik zie de bal precies links.")
                self.nao.walk(0,0,0.25)
            elif (posx >= 0.3):
                if (posy < -0.1):
                    print ("Ik zie de bal rechts boven.")
                    self.nao.kijk_hoger()
                elif (posy > 0.1):
                    print ("Ik zie de bal rechts onder.")
                    self.nao.kijk_lager()
                else:
                    print("Ik zie de bal precies rechts.")
                self.nao.walk(0,0,-0.25)
            elif (posx > -0.3 and posx < .3 and posy > 0):
                print("ik zie de bal vlak voor me.")
                self.nao.kijk_lager()
                dist = self.nao.hoe_ver_bal()
                if (dist <= 0.05):
                    # 5 cm of minder verderop
                    print("de bal ligt op minder dan 5 cm, I loop er tegen aan.")
                    self.nao.walk(0.5,0,0)
            elif (posx > -0.3 and posx < 0.3 and posy < 0):
                print("ik zie de bal een eindje verderop.")
                self.nao.kijk_hoger()