

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

# used for the class inheritance
import basebehavior.behaviorimplementation

# imports used in the code
import time

# import used for sorting list of dictionaries
import operator


class BallDetector_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    def implementation_init(self):

        #define list of sub-behavior here

        # define the ball color color from the hsv color file
        self._ball_color_name = "global_red_1"

        # time interval for detection
        self._time_interval = 0.5

        pass

    def implementation_update(self):

        # get the time for this iteration
        self._current_time = time.time()

        # tweaking on multiple parameters:
        # - surface of the blob
        # - color settings of the blob

        # check if the ball is in memory
        # maybe a redundant check?
        if self.m.n_occurs(self._ball_color_name) > 0:

            # get the last observation of the ball
            #( recogtime, observation) = self.m.get_last_observation(self._ball_color_name)

            # get the last observations in a specific interval
            # returns an (empty) array
            observations = self.m.get_recent_observations(self._ball_color_name, self._current_time - self._time_interval)

            # sort the observations

            # if there are any observations
            if len(observations):

                # filter the observations

                # get the most recent observation with surface larger than??

                for idx, obs in enumerate(observations):
                    print obs

                print ""

            pass

        # add something to memory
        # self.m.add_item('ball_found',time.time(),{})

        #you can do things here that are low-level, not consisting of other behaviors

        #in this function you can check what behaviors have failed or finished
        #and do possibly other things when something has failed
        pass



