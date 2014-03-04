
import basebehavior.behaviorimplementation

import time
import random
import almath


class FindBall_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will move the head around until the ball is in fov or all angles have been checked.'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):
        self.__nao = self.body.nao(0)
        self.__nao.say("Lets find the ball our way!")
        self.__start_time = time.time()

        #Make sure the robot is standing and looks horizontal:
        self.__nao.start_behavior("standup")
        # self.__nao.look_horizontal()

        #Possible states (WALK or TURN):
        self.__state = "WALK"
        self.__last_recogtime = time.time()

    def implementation_update(self):
        # (recogtime, observation) = m.getLastObservation('ball')
        # observation.is_found

        #We check every position we determined to see if the ball is there
        #We use a timer to see when Nao should perform this action to make sure he doesn't perform them at the same time
        #HeadYaw moves the head from right to left, HeadPitch from up to down.
        #The second value (behind the joint) is how many radians it should move in the selected direction.
        #The third value means how fast it should move.

        (recogtime, observation) = self.m.get_last_observation('ball')



        if (time.time() - self.__start_time) > 4 and time.time() - self.__start_time < 8:
            (recogtime, observation) = self.m.get_last_observation('ball')
            if not observation['is_found']:
                #niet voor zijn neus, kijk bij voeten
                self.__nao.get_proxy("motion").setStiffnesses("Head", 1.0)
                self.__nao.look_down()
                print("beneden")
            else:
                print("Gevonden!!")
        if (time.time() - self.__start_time) > 8 and time.time() - self.__start_time < 12:
            (recogtime, observation) = self.m.get_last_observation('ball')
            if not observation['is_found']:
                #niet bij voeten kijk naar linkslaag1
                self.__nao.get_proxy("motion").setStiffnesses("Head", 1.0)
                self.__nao.set_angles('HeadYaw', 45 * almath.TO_RAD, 0.4, radians=True)
                print("linkslaag1")
            else:
                print("Gevonden!!")
        if (time.time() - self.__start_time) > 12 and time.time() - self.__start_time < 16:
            (recogtime, observation) = self.m.get_last_observation('ball')
            if not observation['is_found']:
                #niet op links1 kijk op linkslaag2
                self.__nao.get_proxy("motion").setStiffnesses("Head", 1.0)
                self.__nao.set_angles('HeadYaw', 119 * almath.TO_RAD, 0.4, radians=True)
                print("linkslaag2")
            else:
                print("Gevonden!!")
        if (time.time() - self.__start_time) > 16 and time.time() - self.__start_time < 20:
            (recogtime, observation) = self.m.get_last_observation('ball')
            if not observation['is_found']:
                #niet op links1 kijk op linkshoog2
                self.__nao.get_proxy("motion").setStiffnesses("Head", 1.0)
                self.__nao.set_angles('HeadPitch', 0 * almath.TO_RAD, 0.4, radians=True)
                print("linkshoog2")
            else:
                print("Gevonden!!")
        if (time.time() - self.__start_time) > 20 and time.time() - self.__start_time < 24:
            (recogtime, observation) = self.m.get_last_observation('ball')
            if not observation['is_found']:
                #niet op links1 kijk op linkshoog1
                self.__nao.get_proxy("motion").setStiffnesses("Head", 1.0)
                self.__nao.set_angles('HeadYaw', 45 * almath.TO_RAD, 0.4, radians=True)
                print("linkshoog1")
            else:
                print("Gevonden!!")
        if (time.time() - self.__start_time) > 24 and time.time() - self.__start_time < 28:
            (recogtime, observation) = self.m.get_last_observation('ball')
            if not observation['is_found']:
                #niet op links1 kijk op rechtshoog1
                self.__nao.get_proxy("motion").setStiffnesses("Head", 1.0)
                self.__nao.set_angles('HeadYaw', -45 * almath.TO_RAD, 0.4, radians=True)
                print("rechtshoog1")
            else:
                print("Gevonden!!")
        if (time.time() - self.__start_time) > 28 and time.time() - self.__start_time < 32:
            (recogtime, observation) = self.m.get_last_observation('ball')
            if not observation['is_found']:
                #niet op links1 kijk op rechtshoog2
                self.__nao.get_proxy("motion").setStiffnesses("Head", 1.0)
                self.__nao.set_angles('HeadYaw', -119 * almath.TO_RAD, 0.4, radians=True)
                print("rechtshoog2")
            else:
                print("Gevonden!!")
        if (time.time() - self.__start_time) > 32 and time.time() - self.__start_time < 36:
            (recogtime, observation) = self.m.get_last_observation('ball')
            if not observation['is_found']:
                #niet op links1 kijk op rechtslaag2
                self.__nao.get_proxy("motion").setStiffnesses("Head", 1.0)
                self.__nao.set_angles('HeadPitch', 25 * almath.TO_RAD, 0.4, radians=True)
                print("rechtslaag2")
            else:
                print("Gevonden!!")
        if (time.time() - self.__start_time) > 36 and time.time() - self.__start_time < 40:
            (recogtime, observation) = self.m.get_last_observation('ball')
            if not observation['is_found']:
                #niet bij voeten kijk naar rechtslaag1
                self.__nao.get_proxy("motion").setStiffnesses("Head", 1.0)
                self.__nao.set_angles('HeadYaw', -45 * almath.TO_RAD, 0.4, radians=True)
                print("rechtslaag1")
            else:
                print("Gevonden!!")



        if (time.time() - self.__start_time) > 40 and time.time() - self.__start_time < 44:
            (recogtime, observation) = self.m.get_last_observation('ball')
            if not observation['is_found']:
                self.__nao.set_angles('HeadYaw', 0 * almath.TO_RAD, 0.4, radians=True)
                self.__nao.set_angles('HeadPitch', 0 * almath.TO_RAD, 0.4, radians=True)
                if self.__state == "TURN":
                    if not self.__nao.isWalking():
                        self.__state = "WALK"
                        self.__nao.walkNav(random.random() * 10, 0, 0)
                elif self.__state == "WALK":
                    if not self.__nao.isWalking():
                        self.__state = "TURN"
                        self.__nao.walkNav(0, 0, random.random() * 2 - 1, 0.1)




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
