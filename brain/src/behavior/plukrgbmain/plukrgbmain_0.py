

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

        self.plukrgbfindball = self.ab.plukrgbfindball({})
        self.plukrgbapproachball = self.ab.plukrgbapproachball({})
        self.plukrgbfindgoal = self.ab.plukrgbfindgoal({})
        self.plukrgballigngoal = self.ab.plukrgballigngoal({})
        self.plukrgbscoregoal = self.ab.plukrgbscoregoal({})

        self.selected_behaviors = [
            ("plukrgbfindball", "self.finding_ball == True"),
            ("plukrgbapproachball", "self.approaching_ball == True"),
            ("plukrgbfindgoal", "self.finding_goal == True"),
            ("plukrgballigngoal", "self.allign_goal == True"),
            ("plukrgbscoregoal", "self.scoring_ball == True")
        ]

        self.nao.set_do_nothing_on_stop(True) # The Nao will still be enslaved
        sound = random.choice(["deploy1.wav","deploy2.wav"])
        self.nao.zeg_dit(sound)

        self.nao.complete_behavior("standup")

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

    def implementation_update(self):

        ranIdle = random.randint(1,100)
        if (ranIdle == 5): # 1x per 10 seconden?
            sound = random.choice(["idle.wav","idle2.wav","idle3.wav","idle4.wav"])
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
                self.nao.complete_behavior("standup")
                sound = random.choice(["hate1.wav","hate2.wav","hate3.wav"])
                self.nao.zeg_dit(sound)
                self.prev_fall_time = recogtime
                return

        print("updating...")

        waarbal = self.nao.is_er_bal()
        waargoal = self.nao.waar_goal()
        if (waarbal == True):
            verbal = self.nao.hoe_ver_bal()
        else:
            # is er geen bal? dan niet checken hoe dichtbij bal is.
            verbal = 999


        if (self.finding_ball == True):
            if (waarbal == False):
                # Hey, where did you go?
                print("I do not see the ball.")
                if (self.ball_seen == True):
                    sound = random.choice(["target_lost1.wav","target_lost2.wav"])
                    self.nao.zeg_dit(sound)
                    self.ball_seen = False
            elif (waarbal == True):
                # There you are!
                print("I have found the ball. Now going to approach the ball.")
                if (self.ball_seen == False):
                    sound = random.choice(["target.wav","target2.wav","target3.wav"])
                    self.nao.zeg_dit(sound)
                    self.ball_seen = True
                self.finding_ball = False
                self.approaching_ball = True
        if (self.approaching_ball == True and verbal <= 0.05):
                # ik ben bij de bal!
                print("I am now at the ball. Now looking for goal. TEST: Nope, gaat gewoon weer zoeken.")
                sound = random.choice(["ready.wav"])
                self.nao.zeg_dit(sound)
                self.approaching_ball = False
                #self.finding_goal = True
                self.finding_ball = True
        elif (self.approaching_ball == True):
                # ik zie de bal, maar ik ben er niet
                print("I see the ball, but I am not at the ball.")
        if (self.finding_goal == True):
            if (waargoal != -999):
                (naam,x) = self.nao.check_goal()
                if (naam == "blue goal"):
                    print("I see the blue goal.")
                    if (self.target_goal == "blue"):
                        print("I am now alligning to the goal.")
                        self.finding_goal = False
                        self.allign_goal = True
                elif (naam == "yellow goal"):
                    print("I see the yellow goal.")
                    if (self.target_goal == "yellow"):
                        print("I am now alligning to the goal.")
                elif (naam == "blue-side corner"):
                    print("I see the corner on the blue side.")
                elif (naam == "yellow-side corner"):
                    print("I see the corner on the yellow side.")
                self.finding_goal = False
            else:
                print("I do not see the goal or a corner.")