from almath import TO_RAD
import basebehavior.behaviorimplementation


from util.custom_nao_classes import NaoSettings

class ApproachBall_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):

        # store the reference of the nao
        self.nao = self.body.nao(0)

        # store the ball object
        self.ball = NaoSettings.BALL_OBJECT

        # store the motion proxy
        self.motion = self.nao.get_proxy('motion')

        # cone in degrees if the ball lies in it the nao will move towards it, otherwise only turns torso
        # 60 means: -30 to 30 degrees of the head yaw
        self.forward_movement_cone = 60

        # HeadPitch 	Head joint (Y) degrees: -38.5 to 29.5   rad: -0.6720 to 0.5149
        # fast movement cone means that when the head of the nao looks up enough it walks the fastest
        # the lowest part of the angle means walking fast
        self.fast_movement_cone = 40

        # the maximum amount of looking left in degrees the nao still walks
        self.left_cone_edge = (self.forward_movement_cone / 2)

        # the maximum amount of looking right in degrees the nao still walks
        self.right_cone_edge = -1 * (self.forward_movement_cone / 2)

        # -38.5 is the minimum the nao head pitch can handle
        # when the nao is at the top edge it should walk fast
        self.slow_cone_top_edge = -38.5 + self.fast_movement_cone

        # 29.5 is the maximum the nao head pitch can handle
        # when its at the bottom edge is should stop
        self.slow_cone_bottom_edge = 29.5

        # the degrees in which the nao gradually walks slower
        self.slow_cone_total = self.slow_cone_bottom_edge - self.slow_cone_top_edge

        # set the maximum movement speed
        self.max_movement_speed = 0.8

        # set the minimum movement speed at which time the nao stops movement
        self.min_movement_speed = 0.05

        # Maximum angles of the head
        # HeadYaw    Head joint (X) degrees:	-119.5 to 119.5 rad: -2.0857 to 2.0857
        # HeadPitch 	Head joint (Y) degrees: -38.5 to 29.5   rad: -0.6720 to 0.5149

    def implementation_update(self):

        if self.sees_the_ball():

            # get the nao degree angles
            # looking to the left gives positive angles, looking to the right negative angles
            (head_x, head_y) = self.get_head_angles(False)

            # set theta, the angle the nao has to walk in
            theta = head_x * TO_RAD

            # determine the movement speed
            movement_speed = self.max_movement_speed

            # if the head isn't looking up anymore
            # the ball is getting closer
            # -38.5 is the highest the nao can look
            if head_y > self.slow_cone_top_edge:

                # calculate the slow speed factor
                slow_speed_factor = 1 - (head_y - self.slow_cone_top_edge) / self.slow_cone_total

                # let the nao move gradually slower?
                movement_speed = self.max_movement_speed * slow_speed_factor

            # if the angle of the yaw, the x, is outside the movement cone, don't have any movement speed
            # OR if the movement speed is lower than the min, stop moving
            if head_x > self.left_cone_edge or \
               head_x < self.right_cone_edge or \
               movement_speed < self.min_movement_speed:

                movement_speed = 0

            if self.debug:
                print "Movement speed: " + str(movement_speed) + " - theta: " + str(theta)


            #  void ALMotionProxy::moveToward(const float& x, const float& y, const float& theta, const AL::ALValue moveConfig)
            # move in the direction of the head angle
            self.motion.moveToward(movement_speed, 0, theta)

        else:

            # stop moving
            # self.motion.moveToward(0, 0, 0)
            pass

    # get the current angles of the nao
    def get_head_angles(self, use_radians):

        # get the angles
         return self.nao.get_angles_sensors(['HeadYaw', 'HeadPitch'], radians=use_radians)

    def sees_the_ball(self):

         # get the ball observation
        (recogtime, observation) = self.m.get_last_observation(self.ball.name)

        # check if can see the ball, otherwise, restart behaviours
        return observation['is_found']