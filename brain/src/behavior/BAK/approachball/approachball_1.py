import basebehavior.behaviorimplementation

import time
import almath

class ApproachBall_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):
        self.idling = False

        self.__nao = self.body.nao(0)
        self.__nao.say("Lets approach the ball!")

        self.__last_ball_recogtime = 0
        self.__ball_last_seen = time.time()

        self.__is_looking_horizontal = True


    def implementation_update(self):
        if self.idling:
            return

        # If the ball is seen but not close enough, just walk towards it:
        if (self.m.n_occurs("combined_red") > 0):
            (recogtime, observation) = self.m.get_last_observation("combined_red")
            obs = observation['sorted_contours'][0]     # 0 Corresponds to the largest blob in the list
            if not obs == None and recogtime > self.__last_ball_recogtime:
                print "red: x=%d, y=%d, size=%f" % (obs['x'], obs['y'], obs['surface'])
                self.__last_ball_recogtime = recogtime
                #Ball is found if the detected ball is big enough (thus filtering noise):
                if obs['surface'] > 40:
                    self.__ball_last_seen = time.time()
                    #Is the ball in the correct location?:
                    if obs['y'] > 75 and obs['x'] > 60 and obs['x'] < 100 and not self.__is_looking_horizontal:
                        # If the ball is seen close enough, use self.m.add_item('ball_approached',time.time(),{}) to finish this behavior.
                        self.m.add_item('ball_approached', time.time(),{}) 
                        return
                    if not self.__nao.isWalking():
                        #Make sure that the ball is in the center of the camera:
                        if obs['x'] < 60:
                            self.__nao.walkNav(0, 0, 0.1)
                            pass
                        elif obs['x'] > 100:
                            self.__nao.walkNav(0, 0, -0.1)
                            pass
                    if not self.__nao.isWalking():
                        #Walk a bit if the ball is not really close:
                        if obs['y'] < 80:
                            self.__nao.walkNav(0.05, 0, 0)
                            pass
                        elif self.__is_looking_horizontal:
                            self.__nao.look_down()
                            self.__is_looking_horizontal = False
        
        # Timeout after 10 seconds if the ball is not seen anymore:
        if (time.time() - self.__ball_last_seen) > 10:
            self.__nao.say("I can not see the ball anymore!")
            self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})
            self.idling = True
