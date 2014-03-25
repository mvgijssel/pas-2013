

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import random,time

class PlukRGBapproachball_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)

    def set_done(self):
        self.m.add_item('last_done',time.time(),{})

    def implementation_update(self):

        time.sleep(0.4) # wait some time so we can target the ball.

        (posx,posy) = self.nao.waar_is_bal()
        print("x: " + str(posx) + ", y: " + str(posy))
        if (abs(posx) <= 0.1 and abs(posy) <= 0.1):
            # ligt in het midden van blikveld: loop er naar toe
            print("approach bal: ik zie de bal. Ik loop er naar toe.")
            # rekent afstand uit, en loopt dan een stuk van die afstand vooruit
            dist = abs(self.nao.hoe_ver_bal() * 10)
            sound = random.choice(["search1.wav","search2.wav"])
            self.nao.zeg_dit(sound)
            self.nao.walk(float(dist * 0.2),0,0)
            self.nao.kijk_lager(30)
            return
        else:
            if (posx == -999 or posy == -999):
                print("approach bal: kan de bal niet meer vinden.")
                # er is geen bal, fuck die shit.
                self.set_done()
                return
            elif (posx < -0.1):
                if (posy < 0):
                    print ("approach bal: Ik zie de bal links boven.")
                    dist = abs(posy * 2)
                    dist = max(dist,3)
                    self.nao.kijk_hoger(dist)
                    self.nao.walk(0.1,0,0.35)
                elif (posy > 0):
                    print ("approach bal: Ik zie de bal links onder.")
                    dist = abs(posy * 2)
                    dist = max(dist,3)
                    if (self.nao.kijkt_laagst() == True):
                        self.set_done()
                        return
                    else:
                        self.nao.kijk_lager(dist)
                else:
                    print("approach bal: Ik zie de bal precies links.")
                    self.nao.walk(0,0,0.35)
            elif (posx > 0.1):
                if (posy < 0):
                    print ("approach bal: Ik zie de bal rechts boven.")
                    dist = abs(posy * 2)
                    dist = max(dist,3)
                    self.nao.kijk_hoger(dist)
                    self.nao.walk(0.1,0,-0.35)
                elif (posy > 0):
                    print ("approach bal: Ik zie de bal rechts onder.")
                    dist = abs(posy * 2)
                    dist = max(dist,3)
                    if (self.nao.kijkt_laagst() == True):
                        self.set_done()
                        return
                    else:
                        self.nao.kijk_lager(dist)
                else:
                    print("approach bal: Ik zie de bal precies rechts.")
                    self.nao.walk(0,0,-0.35)
            elif (posy < 0):
                print("approach bal: ik zie de bal een eindje verderop.")
                dist = abs(self.nao.hoe_ver_bal())
                dist = max(dist,0.1)
                #self.nao.kijk_hoger(dist)
                self.nao.walk(float(dist * 0.2),0,0)
            elif (posy > 0):
                print("approach bal: ik zie de bal vlak voor me.")
                if (self.nao.kijkt_laagst() == True):
                    self.set_done()
                    return
                else:
                    self.nao.walk(0.15,0,0)
            else:
                print("approach bal: niks?              ERROR ERROR ERROR")