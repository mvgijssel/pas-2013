from docutils.parsers.rst.directives.body import MathBlock
from random import uniform
import basebehavior.behaviorimplementation
import time
import almath

from util.custom_nao_classes import NaoSettings
from util.custom_nao_classes import Position

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
        self.stopped_moving_time = self.start_time

        # instantiate the stopped moving
        self.stopped_moving = False

        # store the current time
        self.current_time = self.start_time

        # list with states to move the head to
        self.states = []

        # the x speed used
        self.x_speed = 0.4

        # the speed used by the nao for moving it's head
        self.y_speed = 0.4

        # time out, when can't detect is done moving head
        self.time_out = 4

        # the delay between states: 1.5 times the seconds per frame
        self.state_delay = 3

        # set the deviation from the target position
        self.position_deviation = 5

        # define the sweep counter
        self.sweep_counter = 0

        # define the rotate counter
        self.rotate_counter = 0

        # the sweep states
        # upper sweep
        self.states.append(Position(1.0 * Position.CENTER, Position.CENTER))
        self.states.append(Position(1.0 * Position.LEFT, Position.LEFT_TOP))
        self.states.append(Position(0.5 * Position.LEFT, Position.LEFT_TOP))
        self.states.append(Position(Position.CENTER, Position.CENTER_TOP))
        self.states.append(Position(0.5 * Position.RIGHT, Position.RIGHT_TOP))
        self.states.append(Position(1.0 * Position.RIGHT, Position.RIGHT_TOP))

        # lower sweep
        self.states.append(Position(1.0 * Position.RIGHT, Position.RIGHT_BOTTOM))
        self.states.append(Position(0.5 * Position.RIGHT, Position.RIGHT_BOTTOM))
        self.states.append(Position(Position.CENTER, Position.CENTER_BOTTOM))
        self.states.append(Position(0.5 * Position.LEFT, Position.LEFT_BOTTOM))
        self.states.append(Position(1.0 * Position.LEFT, Position.LEFT_BOTTOM))

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

        # change the delay beteen states to twice the framerate
        if NaoSettings.get_time_per_frame():
            self.state_delay = 2.5 * NaoSettings.get_time_per_frame()

        # update the current time
        self.current_time = time.time()

        # if the sweep counter exceeded the maximum rotate the nao
        if self.sweep_counter > 0:

            # reset the sweep counter
            self.sweep_counter = 0

            if self.info:
                print "Rotating the nao for the next sweep"

            # rotate the nao 120? degrees, teta 1 is 180?
            # this is a blocking call
            self.nao.walk(0, 0, 120 * self.nao.TO_RAD)

            # update the rotate counter
            self.rotate_counter += 1

        # when made an entire circle
        if self.rotate_counter > 2:

            # reset the rotate counter
            self.rotate_counter = 0

            # get a random angle
            random_angle = uniform(0, 360) * self.nao.TO_RAD

            if self.info:
                print "Rotating to a random angle: " + str(random_angle)

            # rotate to a random angle
            self.nao.walk(0, 0, random_angle)

            if self.info:
                print "Walking 0.5 meter ahead"

            # walk 0.5 meters straight ahead
            self.nao.walkNav(0, 0.5, 0)

        # try to get the ball
        (recogtime, observation) = self.m.get_last_observation(self.ball.name)

        # if no observation is, move the head
        if not observation['is_found']:

            # if the head is not moving, move the head
            if not self.is_head_moving():

                if not self.stopped_moving:
                    self.stopped_moving = True
                    self.stopped_moving_time = self.current_time

                if (self.current_time - self.stopped_moving_time) > self.state_delay:
                    self.stopped_moving = False
                    self.switch_state()
                else:
                    if self.info:
                        print "Waiting"

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

            # update sweep counter
            self.sweep_counter += 1

            # reset the state of the current state
            self.current_state = 0

        # move the head to the new state
        self.move_head_to(self.states[self.current_state])

    # determine if the angle is close to the target angle
    def is_close(self, val1, val2):

        upper = val1 + self.position_deviation

        lower = val1 - self.position_deviation

        return val2 <= upper and val2 >= lower

    # get the current angles of the nao
    def get_angles(self):

        # get the angles
         return self.nao.get_angles_sensors(['HeadYaw', 'HeadPitch'], radians=False)

    # move the position of the head to the provided position instance
    def move_head_to(self, position):

        # adjusting the 'x' coordinate
        self.nao.set_angles('HeadYaw', position.x * almath.TO_RAD, self.x_speed, radians=True)

        # adjusting the 'y' coordinate
        self.nao.set_angles('HeadPitch', position.y * almath.TO_RAD, self.y_speed, radians=True)

    # returns a boolean value to determine if the head of the nao is moving
    def is_head_moving(self):

        # get the angles
        (head_yaw, head_pitch) = self.get_angles()

        # get the target position
        target = self.states[self.current_state]

        # debug messages
        if self.debug:
            self.print_head_motion("CHECKING", target, head_yaw, head_pitch)

        # return
        if (self.current_time - self.start_time) > self.time_out:

            # reset the timeout timer
            self.start_time = self.current_time

            # debug messages
            if self.info:
                self.print_head_motion("TIMEOUT", target, head_yaw, head_pitch)

            # the head of the Nao is assumed stopped moving
            return False


        # # check if the position is reached
        if self.is_close(target.x, head_yaw) and self.is_close(target.y, head_pitch):

            # reset the timeout timer
            self.start_time = self.current_time

            # head is not moving when position is reached
            return False

        else:

            # head is moving when position not reached
            return True

    # print debug messages
    def print_head_motion(self, message, target, head_yaw, head_pitch):

        print message
        print "X target: " + str(target.x) + " --- " + str(head_yaw)
        print "Y target: " + str(target.y) + " --- " + str(head_pitch)
