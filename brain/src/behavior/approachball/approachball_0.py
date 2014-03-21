import basebehavior.behaviorimplementation


from util.custom_nao_classes import NaoSettings

class ApproachBall_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):

        # store the reference of the nao
        self.nao = self.body.nao(0)

        # store the ball object
        self.ball = NaoSettings.BALL_OBJECT


    def implementation_update(self):

        if self.sees_the_ball():

            print "approaching the ball"

        pass

    def sees_the_ball(self):

         # get the ball observation
        (recogtime, observation) = self.m.get_last_observation(self.ball.name)

        # check if can see the ball, otherwise, restart behaviours
        return observation['is_found']