

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

        # properties of the last observation
        self.x = None
        self.y = None
        self.size = None
        self.width = None
        self.height = None

        pass


class ObjectDetector_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):

        # create the detectable objects
        # surface of 20 is the lower bound!
        ball1 = DetectableObject('ball', 'balrood', 0.5, 40)

        # instantiate the array with target objects
        self._target_objects = [ball1]

        # store the nao reference
        self._nao = self.body.nao(0)

        # update the nao with the detectable objects
        self._nao.set_detectable_objects(self._target_objects)

    def implementation_update(self):

        # get the time for this iteration
        self._current_time = time.time()

        # iterate all the target objects
        for target_object in self._target_objects:

            # for each object call the detect object method
            self.detect_object(target_object)

    # try to detect an object
    # if detected add the object to memory
    def detect_object(self, obj):

        # set the found default, False
        obj.is_found = False

        # scope for the largest observation
        largest_observation = None

        # check if the ball color is in memory
        # maybe a redundant check?
        if self.m.n_occurs(obj.target_color) > 0:

            # get the last observations in a specific interval
            # returns an (empty) array
            observations = self.m.get_recent_observations(obj.target_color, self._current_time - obj.time_interval)

            # sort the observations
            # if there are any observations
            if len(observations):

                # get the largest observation
                largest_observation = self.get_largest_observation(observations)

                # get the first observation, get the second key of the tuple
                if largest_observation['size'] > obj.min_surface:

                    # found the ball!
                    obj.is_found = True

        # print messages about the object and the largest observation
        self.print_messages(obj, largest_observation)

        # update memory using the object setting and the largest observation
        self.update_memory(obj, largest_observation)

        # update the object using the object setting and the largest observation
        # self.update_object(obj, largest_observation)


    def print_messages(self, obj, largest_observation):

        # maybe update properties directly on the nao object? instead of adding to memory?
        # debugging
        print "Found the '" + str(obj.name) + "': " + str(obj.is_found)

        # ball properties
        props = {'is_found': obj.is_found}

        print largest_observation
        print ""

    # get the largest observation
    def get_largest_observation(self, observations):

        # print of the data:
        # [(1393928541.30118, {'source': ('', '/tmp//tmp/Vision_50033'), 'identifier': ('localhost', 'colorblob'), 'blobs': [{'y': 44, 'x': 88, 'size': 378, 'width': 18, 'height': 21}]})]

        # sort the observations on the size of the largest blob
        observations.sort(key=lambda obs: self.get_largest_blob(obs)['size'], reverse=True)

        # return the first largest observation
        return self.get_largest_blob(observations[0])

    # get the largests blob from an observation
    def get_largest_blob(self, observation):

        # check if there exist any blobs
        if len(observation[1]['blobs']):

            # sort the blobs in the observation
            observation[1]['blobs'].sort(key=lambda obs: obs['size'], reverse=True)

            # return the largest of the blobs
            return observation[1]['blobs'][0]

        else:

            # return 0 as no surface is detected
            return {'size': 0}

    # function for updating memory, target object has the target object settings
    def update_memory(self, target_object, largest_observation):

        # instantiate properties object
        props = {'is_found': target_object.is_found}

        # if the target object is found
        if target_object.is_found:

            # ball properties
            props = {'is_found': target_object.is_found, 'x': largest_observation['x'], 'y': largest_observation['y'],
                     'width': largest_observation['width'], 'height': largest_observation['height'],
                     'size': largest_observation['size']}

        # add to the actual memory
        self.m.add_item(target_object.name, self._current_time, props)

    # update the values on the detectable object
    def update_object(self, detectable_object, largest_observation):

        if detectable_object.is_found:

            detectable_object.x = largest_observation['x']
            detectable_object.y = largest_observation['y']
            detectable_object.width = largest_observation['width']
            detectable_object.height = largest_observation['height']
            detectable_object.size = largest_observation['size']

        else:

            detectable_object.x = None
            detectable_object.y = None
            detectable_object.width = None
            detectable_object.height = None
            detectable_object.size = None

