

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation


class HeadFollowBall_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        #define list of sub-behavior here



        pass

    def implementation_update(self):

        #you can do things here that are low-level, not consisting of other behaviors

        #in this function you can check what behaviors have failed or finished
        #and do possibly other things when something has failed
        if (self.m.n_occurs("global_red_1") > 0):

            (recogtime, observation) = self.m.get_last_observation("global_red_1")

            print observation

            # # get the largest contour
            # blob = observation['sorted_contours'][0]
            #
            # if not blob == None:
            #
            #     print "red: x=%d, y=%d, size=%f" % (blob['x'], blob['y'], blob['surface'])
            #
            #     pass



            # print 'combined red'
            # pass

        # (recogtime, observation) = self.m.get_last_observation("combined_red")
        # obs = observation['sorted_contours'][0]     # 0 Corresponds to the largest blob in the list

        # pass



