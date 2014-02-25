

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation

# for the time.time() method
import time

class DetectableObject:

    def __init__(self, name, target_color, time_interval, min_surface):

        self.name = name
        self.target_color = target_color
        self.time_interval = time_interval
        self.min_surface = min_surface
        self.is_found = None
        self.previous_is_found = False

        pass


class ObjectDetector_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        # create the detectable objects
        ball1 = DetectableObject('ball1', 'global_red_1', 0.5, 40)
        ball2 = DetectableObject('ball2', 'global_red_1', 0.5, 40)

        # instantiate an array of detectable objects
        self._target_objects = [ball1, ball2]

        pass

    def implementation_update(self):

        # get the time for this iteration
        self._current_time = time.time()

        # iterate all the target objects
        for target_object in self._target_objects:

            # for each object call the detect object method
            self.detect_object(target_object, self._current_time)

    # try to detect an object
    # if detected add the object to memory
    def detect_object(self, obj, current_time):

        # copy the current is found state
        obj.previous_is_found = obj.is_found

        # set the found default, False
        obj.is_found = False

        # scope for the largest observation
        largest_observation = None

        # check if the ball color is in memory
        # maybe a redundant check?
        if self.m.n_occurs(obj.target_color) > 0:

            # get the last observations in a specific interval
            # returns an (empty) array
            observations = self.m.get_recent_observations(obj.target_color, current_time - obj.time_interval)

            # sort the observations
            # if there are any observations
            if len(observations):

                # sort the observations on the surface key, with the largest first
                # use the [1] index because the observations is a list of tuples: (recognition time, observations)
                observations.sort(key=lambda obs: obs[1]['surface'], reverse=True)

                # get the observation with the largest surface
                largest_observation = observations[0][1]

                # get the first observation, get the second key of the tuple
                if largest_observation['surface'] > obj.min_surface:

                    # found the ball!
                    obj.is_found = True

        # if the previous state is different from the current state, add to memory
        if obj.is_found != obj.previous_is_found:

            # debugging
            print "Found the ball: " + str(obj.is_found)

            # ball properties
            props = {'is_found': obj.is_found}

            # if the blob is found
            if obj.is_found:

                # copy the properties to the memory object
                props['x'] = largest_observation['x']
                props['y'] = largest_observation['y']
                props['surface'] = largest_observation['surface']

            # add the item to memory with the object name
            self.m.add_item(obj.name, current_time, props)



