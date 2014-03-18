

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import random

class PlukRGBapproachball_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.laatst = None

    def implementation_update(self):


        (posx,posy) = self.nao.waar_is_bal()
        print("x: " + str(posx) + ", y: " + str(posy))
        if (abs(posx) <= 0.3 and abs(posy) <= 0.1):
            # ligt in het midden van blikveld: loop er naar toe
            print("ik zie de bal. Ik loop er naar toe.")
            # rekent afstand uit, en loopt dan een stuk van die afstand vooruit
            dist = abs(self.nao.hoe_ver_bal() * 10)
            sound = random.choice(["search1.wav","search2.wav"])
            self.nao.zeg_dit(sound)
            self.nao.walk(float(dist * 0.2),0,0)
            self.laatst = "midden"
            return
        else:
            if (posx == -999 or posy == -999):
                # er is geen bal, fuck die shit.
                if (self.laatst == None):
                    print("Help! Ik ben de bal kwijt en zit nu in een loop!")
                    self.nao.kijk_lager(random.randint(-5,5))
                    self.nao.walk(0,0,random.randint(-1,1)/10)
                elif (self.laatst == "links"):
                    self.nao.walk(0,0,-0.15)
                elif (self.laatst == "rechts"):
                    self.nao.walk(0,0,0.15)
                elif (self.laatst == "boven"):
                    self.nao.kijk_lager(5)
                elif (self.laatst == "onder"):
                    self.nao.kijk_hoger(5)
                self.laatst = "midden"
                return
            elif (posx < -0.3):
                if (posy < -0.1):
                    print ("Ik zie de bal links boven.")
                    dist = abs(posy)
                    self.nao.kijk_hoger(dist)
                    self.laatst = "boven"
                elif (posy > 0.1):
                    print ("Ik zie de bal links onder.")
                    dist = abs(posy)
                    self.nao.kijk_lager(dist)
                    self.laatst = "onder"
                else:
                    print("Ik zie de bal precies links.")
                    self.nao.walk(0,0,0.25)
                    self.laatst = "links"
            elif (posx >= 0.3):
                if (posy < -0.1):
                    print ("Ik zie de bal rechts boven.")
                    dist = abs(posy)
                    self.nao.kijk_hoger(dist)
                    self.laatst = "boven"
                elif (posy > 0.1):
                    print ("Ik zie de bal rechts onder.")
                    dist = abs(posy)
                    self.nao.kijk_lager(dist)
                    self.laatst = "onder"
                else:
                    print("Ik zie de bal precies rechts.")
                    self.nao.walk(0,0,-0.25)
                    self.laatst = "rechts"
            elif (posx > -0.3 and posx < 0.3 and posy < 0):
                print("ik zie de bal een eindje verderop.")
                dist = abs(posy)
                self.nao.kijk_hoger(dist)
                self.laatst = "boven"