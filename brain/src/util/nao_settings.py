class DetectableObject:

    def __init__(self, name, target_color, time_interval, min_surface):

        self.name = name
        self.target_color = target_color
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

    # the ball object for the blob detector
    BALL_OBJECT = DetectableObject('ball', 'experiment_rood', 2, 20)

    _seconds_per_frame = None

    @classmethod
    def set_time_per_frame(cls, seconds_per_frame):

        # store the seconds per frame
        cls._seconds_per_frame = seconds_per_frame

    @classmethod
    def get_time_per_frame(cls):

        # get the time per frame
        return cls._seconds_per_frame