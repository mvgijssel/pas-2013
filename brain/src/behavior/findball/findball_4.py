import basebehavior.behaviorimplementation
import time
import almath
import math

from util.nao_settings import NaoSettings

class Position:

    # maximum values for the joints
    LEFT = 116 # 119 is maximum
    RIGHT = -116 # 119 is maximum

    # TOP = -38
    # BOTTOM = 29
    TOP = -38 # -38 is the maximum

    # bottom positions are different for the different angles
    # for example looking left, the nao can't turn his head all the way down
    CENTER_BOTTOM = 24 # maximum min 29
    LEFT_BOTTOM = 16
    RIGHT_BOTTOM = 16

    CENTER = 0

    def __init__(self, x, y):

        self.x = x
        self.y = y


class FindBall_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    # instantiate all the user variables
    def implementation_init(self):

        self.ball = NaoSettings.BALL_OBJECT

        # store the nao reference
        self.nao = self.body.nao(0)

        # store the used proxy
        self.proxy = self.nao.get_proxy("motion")

        # set the nao stiffness
        self.proxy.setStiffnesses("Head", 1.0)

        # store the start time
        self.start_time = time.time()

        # time stamp for when nao head movement stops
        self.stopped_moving = self.start_time

        # store the current time
        self.current_time = self.start_time

        # list with states to move the head to
        self.states = []

        # the x speed used
        self.x_speed = 0.05

        # the speed used by the nao for moving it's head
        self.y_speed = 0.05

        # time out
        self.time_out = 30

        # the delay between states
        self.state_delay = 3

        # set the deviation from the target position
        self.position_deviation = 2

        # the sweep states
        # upper sweep
        self.states.append(Position(Position.LEFT, Position.TOP))
        self.states.append(Position(Position.CENTER, Position.TOP))
        self.states.append(Position(Position.RIGHT, Position.TOP))

        # lower sweep
        self.states.append(Position(Position.RIGHT, Position.RIGHT_BOTTOM))
        self.states.append(Position(Position.CENTER, Position.CENTER))
        self.states.append(Position(Position.LEFT, Position.LEFT_BOTTOM))

        # look straight ahead
        self.states.append(Position(Position.CENTER, Position.CENTER))

        # look at your feet
        self.states.append(Position(Position.CENTER, Position.CENTER_BOTTOM))

        # define the current state
        self.current_state = None

        # start the initial state
        self.switch_state()

    # the update loop
    def implementation_update(self):

        # update the current time
        self.current_time = time.time()

        # try to get the ball
        (recogtime, observation) = self.m.get_last_observation(self.ball.name)

        # if ball is found
        if observation['is_found']:

            # get the angles
            (x, y) = self.get_angles()

            # create a new position object on the current position
            pos = Position(x, y)

            # move the head to the position
            self.move_head_to(pos)

        # if no observation is, move the head
        else:

            # if the head is not moving, move the head
            if not self.is_head_moving():

                #

                if (self.current_time - self.stopped_moving) > self.state_delay:
                    self.switch_state()


    # switch the state
    def switch_state(self):

        # case for when starting the behaviour
        if self.current_state is None:

            # set to the first index
            self.current_state = 0

        else:

            # increment the current state
            self.current_state += 1

        # if the current state is larger / equal length of the sweep states, reset
        if self.current_state >= len(self.states):

            # reset the state of the current state
            self.current_state = 0

        # move the head to the new state
        self.move_head_to(self.states[self.current_state])

    # move the position of the head to the provided position instance
    def move_head_to(self, position):

        # adjusting the 'x' coordinate
        self.nao.set_angles('HeadYaw', position.x * almath.TO_RAD, self.x_speed, radians=True)

        # adjusting the 'y' coordinate
        self.nao.set_angles('HeadPitch', position.y * almath.TO_RAD, self.y_speed, radians=True)

    # determine if the angle is close to the target angle
    def is_close(self, val1, val2):

        upper = val1 + self.position_deviation

        lower = val1 - self.position_deviation

        return val2 <= upper and val2 >= lower

    # get the current angles of the nao
    def get_angles(self):

        # get the angles
         return self.nao.get_angles_sensors(['HeadYaw', 'HeadPitch'], radians=False)

    # returns a boolean value to determine if the head of the nao is moving
    def is_head_moving(self):

        # get the angles
        (head_yaw, head_pitch) = self.get_angles()

        # get the target position
        target = self.states[self.current_state]

        # return
        if (self.current_time - self.start_time) > self.time_out:

            # reset the timeout timer
            self.start_time = self.current_time

            # debug messages
            self.print_head_motion("TIMEOUT", target, head_yaw, head_pitch)

            # the head of the Nao is assumed stopped moving
            return False


        # # check if the position is reached
        if self.is_close(target.x, head_yaw) and self.is_close(target.y, head_pitch):

            # reset the timeout timer
            self.start_time = self.current_time

            self.pause_time

            # head is not moving when position is reached
            return False

        else:

            # head is moving when position not reached
            return True

    # print debug messages
    def print_head_motion(self, message, target, head_yaw, head_pitch):

        print ""
        print message
        print "X target: " + str(target.x) + " --- " + str(head_yaw)
        print "Y target: " + str(target.y) + " --- " + str(head_pitch)
