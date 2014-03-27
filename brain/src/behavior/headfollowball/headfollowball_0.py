import almath
import basebehavior.behaviorimplementation
from util.custom_nao_classes import NaoSettings

class Headfollowball_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.ball = NaoSettings.BALL_OBJECT

        self.head_pitch_increment = 2 # previous 1
        self.head_yaw_increment = 2 # previous 1
        self.head_center_speed = 0.5 # previous 0.1

        # the deviation from the center of the screen that's
        self.head_center_deviation = 15

    def implementation_update(self):

         # get the ball observation
        (recogtime, observation) = self.m.get_last_observation(self.ball.name)

        # check if can see the ball, otherwise, restart behaviours
        if observation['is_found']:

            # get the relative positions from the observation
            # (0, 0) is the center
            (rel_x, rel_y) = self.calculate_relative_position(observation['x'], observation['y'])

            if rel_x > self.head_center_deviation:

                # move the head to the right
                self.change_head_x(-self.head_yaw_increment)

            elif rel_x < -self.head_center_deviation:

                # move the head to the left
                self.change_head_x(self.head_yaw_increment)

            if rel_y > self.head_center_deviation:

                # move the head up
                self.change_head_y(self.head_pitch_increment)

            elif rel_y < -self.head_center_deviation:

                # move the head down
                self.change_head_y(-self.head_pitch_increment)

    def change_head_x(self, x):

        # change_angles(self, names, angles, max_speed, disable_stiffness=False, radians=False):

        # head yaw is the 'x' of the head
        self.nao.change_angles('HeadYaw', x * almath.TO_RAD, self.head_center_speed, radians=True)

    def change_head_y(self, y):

         # adjusting the 'y' coordinate
        self.nao.change_angles('HeadPitch', y * almath.TO_RAD, self.head_center_speed, radians=True)

    def calculate_relative_position(self, x, y):

        x -= NaoSettings.blob_dimension_width / 2
        y -= NaoSettings.blob_dimension_height / 2

        return x, y
