import basebehavior.behaviorimplementation

import time
import random


class FindBall_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will move the head around untill the ball is in fov or all angles were tried.'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):
        self.__nao = self.body.nao(0)
        self.__nao.say("Lets find the ball our way!")
        self.__start_time = time.time()

        #Make sure the robot is standing and looks horizontal:
        self.__nao.start_behavior("standup")
        self.__nao.look_horizontal()

        #Possible states (WALK or TURN):
        self.__state = "WALK"
        self.__last_recogtime = time.time()

    def implementation_update(self):
        haha = false #self.__nao.m.ball = false?????)
        if not haha:
            #niet voor zijn neus, kijk bij voeten
            self.get_proxy("motion").setStiffnesses("Head", 1.0)
            self.__nao.look_down()
        if not haha:
            #niet bij voeten kijk naar linkslaag1
            self.get_proxy("motion").setStiffnesses("Head", 1.0)
            self.__nao.setAngles('HeadYaw',25 * almath.TO_RAD,0.5, radians=TRUE)
        if not haha:
            #niet op links1 kijk op linkslaag2
            self.get_proxy("motion").setStiffnesses("Head", 1.0)
            self.__nao.setAngles('HeadYaw',25 * almath.TO_RAD,0.5, radians=TRUE)
        if not haha:
            #niet op links1 kijk op linkshoog2
            self.get_proxy("motion").setStiffnesses("Head", 1.0)
            self.__nao.setAngles('HeadPitch',0 * almath.TO_RAD,1.0, radians=TRUE)
        if not haha:
            #niet op links1 kijk op linkshoog1
            self.get_proxy("motion").setStiffnesses("Head", 1.0)
            self.__nao.setAngles('HeadYaw',-25 * almath.TO_RAD,0.5, radians=TRUE)
        if not haha:
            #niet op links1 kijk op rechtshoog1
            self.get_proxy("motion").setStiffnesses("Head", 1.0)
            self.__nao.setAngles('HeadYaw',-50 * almath.TO_RAD,0.5, radians=TRUE)
        if not haha:
            #niet op links1 kijk op rechtshoog2
            self.get_proxy("motion").setStiffnesses("Head", 1.0)
            self.__nao.setAngles('HeadYaw',-25 * almath.TO_RAD,0.5, radians=TRUE)
        if not haha:
            #niet op links1 kijk op rechtslaag2
            self.get_proxy("motion").setStiffnesses("Head", 1.0)
            self.__nao.setAngles('HeadPitch', 25 * almath.TO_RAD,1.0, radians=TRUE)
        if not haha:
            #niet bij voeten kijk naar rechtslaag1
            self.get_proxy("motion").setStiffnesses("Head", 1.0)
            self.__nao.setAngles('HeadYaw',25 * almath.TO_RAD,0.5, radians=TRUE)
        # Turn around in a certain direction unless you see the ball.
        # In that case, turn towards it until you have it fairly central in the Field of Vision.
        #if (time.time() - self.__start_time) > 10:
        #    if self.__state == "TURN":
        #        if not self.__nao.isWalking():
        #            self.__state = "WALK"
        #            self.__nao.walkNav(random.random() * 10, 0, 0)
        #    elif self.__state == "WALK":
        #        if not self.__nao.isWalking():
        #            self.__state = "TURN"
        #            self.__nao.walkNav(0, 0, random.random() * 2 - 1, 0.1)

        #Try to see if there is a ball in sight:
        #if (self.m.n_occurs("combined_red") > 0):

            #(recogtime, observation) = self.m.get_last_observation("combined_red")

           # obs = observation['sorted_contours'][0]     # 0 Corresponds to the largest blob in the list

           # if not obs == None and recogtime > self.__last_recogtime:
              #  print "red: x=%d, y=%d, size=%f" % (obs['x'], obs['y'], obs['surface'])
             #   self.__last_recogtime = recogtime
                #Ball is found if the detected ball is big enough (thus filtering noise):
             #   if obs['surface'] > 40:
              #      self.__nao.say("I see the ball!")
                    # Once the ball is properly found, use: self.m.add_item('ball_found',time.time(),{}) to finish this behavior.
              #      self.m.add_item('ball_found',time.time(),{})
