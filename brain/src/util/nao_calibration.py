import time

class NaoCalibration():

    # instantiate number of measurements
    _number_of_measurements = 0

    # instantiate the previous time
    _start_time = time.time()

    # instantiate time per frame
    _time_per_frame = None

    # call method received image when an actual image is received
    @classmethod
    def received_image(cls, is_received):

        # store the current time
        current_time = time.time()

        # update number of measurements when image is received

        if is_received:
            cls._number_of_measurements += 1

        # first calculate the delta between start time and current time
        # Then calculate time per frame by dividing by number of measurements
        cls._time_per_frame = (current_time - cls._start_time) / cls._number_of_measurements


    @classmethod
    def time_per_frame(cls):

        # return amount of time for a single frame in seconds
        return cls._time_per_frame