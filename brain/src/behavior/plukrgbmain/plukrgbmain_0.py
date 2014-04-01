

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation
import random
import time


class PlukRGBmain_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!

    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.prev_fall_time = 0

        self.plukrgbfindball = self.ab.plukrgbfindball({}) # kijk waar de bal is
        self.plukrgbapproachball = self.ab.plukrgbapproachball({}) # loop naar de bal
        self.plukrgbfindgoal = self.ab.plukrgbfindgoal({}) # kijk waar het doel is
        self.plukrgballigngoal = self.ab.plukrgballigngoal({}) # krijg bal tussen jou en doel
        self.plukrgbscoregoal = self.ab.plukrgbscoregoal({}) # ren vooruit, hopen dat de bal mee komt.

        self.selected_behaviors = [
            ("plukrgbfindball", "self.finding_ball == True and self.approaching_ball == False"),
            ("plukrgbapproachball", "self.approaching_ball == True and self.finding_ball == False and self.allign_goal == False"),
            ("plukrgbfindgoal", "self.finding_goal == True and self.allign_goal == False and self.finding_ball == False"),
            ("plukrgballigngoal", "self.allign_goal == True and self.finding_goal == False and self.scoring_ball == False"),
            ("plukrgbscoregoal", "self.scoring_ball == True and self.allign_goal == False")
        ]

        # om te zorgen dat de camera niet steeds zichzelf blijft aanpassen
        self.nao.setup_camera_parameters()

        self.nao.set_do_nothing_on_stop(True) # The Nao will still be enslaved
        sound = random.choice(["deploy1.wav","deploy2.wav"])
        self.nao.zeg_dit(sound)

        self.nao.complete_behavior("standup")
        self.m.add_item('last_done',time.time()-5,{})

        self.finding_ball = True
        self.approaching_ball = False
        self.finding_goal = False
        self.scoring_ball = False
        self.allign_goal = False

        # CONFIGURE THIS AT THE START OF THE MATCH
        self.target_goal = "blue"  # "blue" or "yellow"

        # for sounds
        self.at_ball = False
        self.ball_seen = False
        self.goal_seen = False

        self.last_done = time.time()

    def allOff(self):
        self.finding_ball = False
        self.approaching_ball = False
        self.finding_goal = False
        self.scoring_ball = False
        self.allign_goal = False

    def checkallOff(self):
        if (self.finding_ball == False):
            if (self.approaching_ball == False):
                if (self.finding_goal == False):
                    if (self.scoring_ball == False):
                        if (self.allign_goal == False):
                            return True
        return False

    def activate(self,name):
        print("activating " + str(name))
        self.allOff()
        if (name == "finding_ball"):
            self.finding_ball = True
            self.plukrgbfindball = self.ab.plukrgbfindball({}) # kijk waar de bal is
        elif (name == "approaching_ball"):
            self.approaching_ball = True
            self.plukrgbapproachball = self.ab.plukrgbapproachball({}) # loop naar de bal
        elif (name == "finding_goal"):
            self.finding_ball = True
            self.plukrgbfindball = self.ab.plukrgbfindball({})
            #self.finding_goal = True
            #self.plukrgbfindgoal = self.ab.plukrgbfindgoal({}) # kijk waar het doel is
        elif (name == "scoring_ball"):
            self.finding_ball = True
            self.plukrgbfindball = self.ab.plukrgbfindball({})
            #self.scoring_ball = True
            #self.plukrgbscoregoal = self.ab.plukrgbscoregoal({}) # ren vooruit, hopen dat de bal mee komt.
        elif (name == "allign_goal"):
            self.finding_ball = True
            self.plukrgbfindball = self.ab.plukrgbfindball({})
            #self.allign_goal = True
            #self.plukrgballigngoal = self.ab.plukrgballigngoal({}) # krijg bal tussen jou en doel
        else:
            print("error in \"activate\", misspelled? -> " + str(name))

    def get_done(self):
        (last,value) = self.m.get_last_observation("last_done")
        if (last > self.last_done):
            self.last_done = last
            return True
        else:
            return False

    def implementation_update(self):

        waar = self.nao.waar_is_bal() # update zichzelf 5 keer per seconde?

        if (self.checkallOff() == True):
            self.finding_ball = True

        ranIdle = random.randint(1,100)
        if (ranIdle == 5): # 1x per 10 seconden?
            sound = random.choice(["idle.wav","idle2.wav","idle3.wav","idle4.wav","idle5.wav"])
            self.nao.zeg_dit(sound)

        if (self.m.n_occurs('naoHasFallen') > 0):
            (recogtime, observation) = self.m.get_last_observation('naoHasFallen')
            if (recogtime > self.prev_fall_time):
                # I fell
                sound = random.choice(["alarm.wav"])
                self.nao.zeg_dit(sound)
                time.sleep(0.3)
                self.nao.zeg_dit(sound)
                time.sleep(0.3)
                self.nao.zeg_dit(sound)
                time.sleep(0.3)
                self.nao.zeg_dit(sound)
                time.sleep(0.3)
                self.nao.zeg_dit(sound)
                time.sleep(0.3)
                self.nao.zeg_dit(sound)
                time.sleep(0.3) # play alarm for a while
                sound = random.choice(["hate1.wav","hate2.wav","hate3.wav"])
                self.nao.complete_behavior("standup")
                self.nao.zeg_dit(sound)
                self.prev_fall_time = recogtime
                self.reset()
                return

        if (self.finding_ball == True):
            print("main: finding ball")
            if (self.get_done() == True):
                self.plukrgbfindball.set_finished()
                self.activate("approaching_ball")

        elif (self.approaching_ball == True):
            print("main: approaching ball")
            if (self.get_done() == True):
                self.plukrgbapproachball.set_finished()
                if (self.nao.is_er_bal() == True):
                    self.activate("finding_ball")
                    #self.activate("finding_goal")
                else:
                    # let's start back from the top
                    self.reset()

        elif (self.finding_goal == True):
            print("main: finding goal")
            if (self.get_done() == True):
                self.plukrgbfindgoal.set_finished()
                self.activate("allign_goal")

        elif (self.allign_goal == True):
            print("main: alligning to goal")
            if (self.get_done() == True):
                self.plukrgballigngoal.set_finished()
                if (self.nao.check_goal() == True):
                    self.nao.kijk_lager(30)
                    self.activate("scoring_ball")
                else:
                    self.reset()


        elif (self.scoring_ball == True):
            print("main: scoring goal")
            if (self.get_done() == True):
                self.plukrgbscoregoal.set_finished()
                self.reset()

        else:
            print("not doing anything...")

    def reset(self):
        self.goal_seen = False
        self.ball_seen = False
        self.activate("finding_ball")