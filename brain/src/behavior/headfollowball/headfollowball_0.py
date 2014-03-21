import almath
import basebehavior.behaviorimplementation
from util.custom_nao_classes import NaoSettings

class Headfollowball_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.ball = NaoSettings.BALL_OBJECT

        self.head_pitch_increment = 5
        self.head_yaw_increment = 3
        self.head_center_speed = 0.4

        # the deviation from the center of the screen thats
        self.head_center_deviation = 10

    def implementation_update(self):

         # get the ball observation
        (recogtime, observation) = self.m.get_last_observation(self.ball.name)

        # check if can see the ball, otherwise, restart behaviours
        if observation['is_found']:

            # get the relative positions from the observation
            # (0, 0) is the center
            (rel_x, rel_y) = self.calculate_relative_position(observation['x'], observation['y'])

            print "rel_x: " + str(rel_x) + " - rel_y: " + str(rel_y)

            # get the head angles
            (head_x, head_y) = self.get_angles()

            if rel_x > self.head_center_deviation:

                # move the head to the right
                self.set_head_x(head_x - self.head_yaw_increment)

            elif rel_x < -self.head_center_deviation:

                # move the head to the left
                self.set_head_x(head_x + self.head_yaw_increment)

            if rel_y > self.head_center_deviation:

                print "current y: " + str(head_y) + " - target y: " + str(head_y + self.head_pitch_increment)

                # move the head up
                self.set_head_y(head_y + self.head_pitch_increment)

            elif rel_y < -self.head_center_deviation:

                print "current y: " + str(head_y) + " - target y: " + str(head_y - self.head_pitch_increment)

                # move the head down
                self.set_head_y(head_y - self.head_pitch_increment)

            #print "rel x: " + str(rel_x) + " - rel y:" + str(rel_y)
            #print "head x: " + str(head_x) + " - head y: " + str(head_y)
            # print ""

    def set_head_x(self, x):

        # head yaw is the 'x' of the head
        self.nao.set_angles('HeadYaw', x * almath.TO_RAD, self.head_center_speed, radians=True)

    def set_head_y(self, y):

         # adjusting the 'y' coordinate
        self.nao.set_angles('HeadPitch', y * almath.TO_RAD, self.head_center_speed, radians=True)

    def calculate_relative_position(self, x, y):

        x -= NaoSettings.blob_dimension_width / 2
        y -= NaoSettings.blob_dimension_height / 2

        return x, y

    # get the current angles of the nao
    def get_angles(self):

        # get the angles
         return self.nao.get_angles_sensors(['HeadYaw', 'HeadPitch'], radians=False)