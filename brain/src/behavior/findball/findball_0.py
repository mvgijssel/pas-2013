import basebehavior.behaviorimplementation
import time
import almath

class Position:

    # maximum values for the joints
    LEFT = 119
    RIGHT = -119

    TOP = -38
    BOTTOM = 29

    CENTER = 0

    def __init__(self, x, y):

        self.x = x
        self.y = y


class FindBall_x(basebehavior.behaviorimplementation.BehaviorImplementation):


    def implementation_init(self):

        # store the nao reference
        self.nao = self.body.nao(0)

        # store the used proxy
        self.proxy = self.nao.get_proxy("motion")

        # set the nao stiffness
        self.proxy.setStiffnesses("Head", 1.0)

        # store the start time
        self.start_time = time.time()

        # list with states to move the head to
        self.states = []

        # use the sensors when determining the angles of the nao?
        self.use_sensors = True

        # the sensor names
        self.sensor_names = ['HeadYaw', 'HeadPitch']

        # the x speed used
        self.x_speed = 0.4

        # the speed used by the nao for moving it's head
        self.y_speed = 0.3

        # the sweep states
        self.states.append(Position(Position.LEFT, Position.TOP))
        self.states.append(Position(Position.CENTER, Position.TOP))
        self.states.append(Position(Position.RIGHT, Position.TOP))

        self.states.append(Position(Position.LEFT, Position.CENTER))
        self.states.append(Position(Position.CENTER, Position.CENTER))
        self.states.append(Position(Position.RIGHT, Position.CENTER))

        self.states.append(Position(Position.LEFT, Position.BOTTOM))
        self.states.append(Position(Position.CENTER, Position.BOTTOM))
        self.states.append(Position(Position.RIGHT, Position.BOTTOM))

        # set the state
        # go to the state
        # on each iteration get the angles from the nao
        # when state is done, the angles from the nao are the set angles, go to next state
        # timeout within 10 seconds

        # define the current state
        self.current_state = None

        # switch the current state
        self.switch_state()

    def implementation_update(self):

        if not self.is_head_moving():

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

    # returns a boolean value to determine if the head of the nao is moving
    def is_head_moving(self):

        # get the angles
        (head_yaw, head_pitch) = self.proxy.getAngles(self.sensor_names, self.use_sensors)

        # get the target position
        target = self.states[self.current_state]

        print "X target: " + target.x + " --- " + head_yaw
        print "Y target: " + target.y + " --- " + head_pitch


