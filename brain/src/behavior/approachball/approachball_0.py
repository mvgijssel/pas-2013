import basebehavior.behaviorimplementation


from util.custom_nao_classes import NaoSettings

class ApproachBall_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):

        # store the reference of the nao
        self.nao = self.body.nao(0)

        # store the ball object
        self.ball = NaoSettings.BALL_OBJECT

        self.counter = 0


    def implementation_update(self):

        if self.sees_the_ball():

            distance = 0.3

            print "trying to walk times: " + str(self.counter) + " - "

            # walk in the direction of the head x
            # is a blocking call
            #self.nao.walkNav(1, distance, self.get_head_x())
            self.nao.walk(distance, 0, self.get_head_x())

            self.counter += 1
        pass

    # get the current angles of the nao
    def get_head_x(self):

        # get the angles
         return self.nao.get_angles_sensors(['HeadYaw'], radians=True)[0]

    def sees_the_ball(self):

         # get the ball observation
        (recogtime, observation) = self.m.get_last_observation(self.ball.name)

        # check if can see the ball, otherwise, restart behaviours
        return observation['is_found']