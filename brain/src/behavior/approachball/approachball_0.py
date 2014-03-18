import basebehavior.behaviorimplementation

import time
import almath
from util.nao_settings import NaoSettings

class ApproachBall_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):

        # store the reference of the nao
        self.nao = self.body.nao(0)

        # store the ball object
        self.ball = NaoSettings.BALL_OBJECT

        if self.debug:
            print "Approaching the ball!"


    def implementation_update(self):

        if self.sees_the_ball():

            if self.debug:
                print "See the ball"

            # walk halfway?

        else:

            if self.debug:
                print "Dont see the ball anymore"

            self.set_failed("Can't see the ball anymore/.")


        # if obs['y'] > 75 and obs['x'] > 60 and obs['x'] < 100 and not self.__is_looking_horizontal:
        #     # If the ball is seen close enough, use self.m.add_item('ball_approached',time.time(),{}) to finish this behavior.
        #     self.m.add_item('ball_approached', time.time(),{})
        #     return
        # if not self.__nao.isWalking():
        #     #Make sure that the ball is in the center of the camera:
        #     if obs['x'] < 60:
        #         self.__nao.walkNav(0, 0, 0.1)
        #         pass
        #     elif obs['x'] > 100:
        #         self.__nao.walkNav(0, 0, -0.1)
        #         pass
        # if not self.__nao.isWalking():
        #     #Walk a bit if the ball is not really close:
        #     if obs['y'] < 80:
        #         self.__nao.walkNav(0.05, 0, 0)
        #         pass
        #     elif self.__is_looking_horizontal:
        #         self.__nao.look_down()
        #         self.__is_looking_horizontal = False
        

    def sees_the_ball(self):

         # get the ball observation
        (recogtime, observation) = self.m.get_last_observation(self.ball.name)

        # check if can see the ball, otherwise, restart behaviours
        return observation['is_found']