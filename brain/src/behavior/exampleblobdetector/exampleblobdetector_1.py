
import basebehavior.behaviorimplementation

import time

'''This blobdetector example reads single detections of color blobs from memory. It is also possible
to request all detections of one color at any moment in time. For an application of this method,
see the default soccer behaviors that were provided.'''

class ExampleBlobdetector_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):
        print "Example BlobDetector Behavior Started!"
        self.__last_recogtime = 0

        self.__blob_list = [
                ["green", False, time.time()],
                ["red", False, time.time()],
                ["blue", False, time.time()],
                ["yellow", False, time.time()],
            ]
        self.__nao = self.body.nao(0)

    def implementation_update(self):
        for blob in self.__blob_list:
            if (self.m.n_occurs(blob[0]) > 0):
                (recogtime, obs) = self.m.get_last_observation(blob[0])
                if recogtime > blob[2]:
                    blob[2] = time.time()
                    print "%s: x=%d, y=%d, width=%d, height=%d, surface=%d" \
                        % (blob[0], obs['x'], obs['y'], obs['width'], obs['height'], obs['surface'])
                    if obs['surface'] > 300 and not blob[1]:
                        self.__nao.say("Yeah, ok I found the %s blob." % blob[0])
                        blob[1] = True
            if (time.time() - blob[2]) > 10:
                 blob[1] = False
