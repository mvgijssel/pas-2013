class Position:

    # maximum values for the joints
    LEFT = 116 # 119 is maximum
    RIGHT = -116 # 119 is maximum

    # TOP = -38
    # BOTTOM = 29
    CENTER_TOP = -21 # -38 is the maximum
    LEFT_TOP = -21#
    RIGHT_TOP = -21 #

    # bottom positions are different for the different angles
    # for example looking left, the nao can't turn his head all the way down
    CENTER_BOTTOM = 24 # maximum min 29
    LEFT_BOTTOM = 16
    RIGHT_BOTTOM = 16

    CENTER = 0

    def __init__(self, x, y):

        self.x = x
        self.y = y


class DetectableObject:

    def __init__(self, name, target_color, time_interval, min_surface):

        self.name = name
        self.target_color = target_color

        # time interval determines the factor time the current amount seconds per frame
        self.time_interval = time_interval
        self.min_surface = min_surface
        self.is_found = None
        self.previous_is_found = False

        # properties of the last observation
        self.x = None
        self.y = None
        self.size = None
        self.width = None
        self.height = None

        pass

class NaoSettings():

    blob_dimension_width = 160
    blob_dimension_height = 120

    # the ball object for the blob detector
    BALL_OBJECT = DetectableObject('ball', 'experiment_rood', 4, 20)

    _seconds_per_frame = None

    @classmethod
    def set_time_per_frame(cls, seconds_per_frame):

        # store the seconds per frame
        cls._seconds_per_frame = seconds_per_frame

    @classmethod
    def get_time_per_frame(cls):

        # get the time per frame
        return cls._seconds_per_frame