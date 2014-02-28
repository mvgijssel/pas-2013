

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

# used for the class inheritance
import basebehavior.behaviorimplementation

# imports used in the code
import time

# import used for sorting list of dictionaries
# import operator


class BallDetector_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    def implementation_init(self):

        #define list of sub-behavior here

        # define the ball color color from the hsv color file
        self._ball_color_name = "global_red_1"

        # time interval for detection
        self._time_interval = 0.5

        # minimal surface
        self._minimal_surface = 40

        # the ball finding state, None for initial so always adds the ball to the memory
        self._is_found = None

        # tweaking on multiple parameters:
        # - surface of the blob
        # - color settings of the blob

        pass

    def implementation_update(self):

        # get the time for this iteration
        self._current_time = time.time()

        # copy the current is found state
        previous_is_found = self._is_found

        # set the found default, False
        self._is_found = False

        # scope for the largest observation
        largest_observation = None

        # check if the ball color is in memory
        # maybe a redundant check?
        if self.m.n_occurs(self._ball_color_name) > 0:

            # get the last observations in a specific interval
            # returns an (empty) array
            observations = self.m.get_recent_observations(self._ball_color_name, self._current_time - self._time_interval)

            # sort the observations
            # if there are any observations
            if len(observations):

                # sort the observations on the surface key, with the largest first
                # use the [1] index because the observations is a list of tuples: (recognition time, observations)
                observations.sort(key=lambda obs: obs[1]['surface'], reverse=True)

                # get the observation with the largest surface
                largest_observation = observations[0][1]

                # get the first observation, get the second key of the tuple
                if largest_observation['surface'] > self._minimal_surface:

                    # found the ball!
                    self._is_found = True

        # if the previous state is different from the current state, add to memory
        if self._is_found != previous_is_found:

            # debugging
            print "Found the ball: " + str(self._is_found)

            # ball properties
            props = {'is_found': self._is_found}

            # if the blob is found
            if self._is_found:

                # copy the properties to the memory object
                props['x'] = largest_observation['x']
                props['y'] = largest_observation['y']
                props['surface'] = largest_observation['surface']

            # add the item to memory
            self.m.add_item('ball', self._current_time, props)