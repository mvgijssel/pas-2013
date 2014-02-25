import basebehavior.behaviorimplementation
import time
import almath

nao = True 

class Approachlowball_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior moves the Nao slowly towards the ball while looking down'''
    
    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.nao.say("Ick kike nahr Behnaidehn")
        self.last_ball_recogtime = 0
        self.ball_last_seen = time.time()
        self.temptime = time.time()
        if nao: self.nao.set_cam_vars()

    def implementation_update(self):

        if (self.m.n_occurs("combined_red") > 0):
            (recogtime, obs) = self.m.get_last_observation("combined_red")
            if not obs == None and recogtime > self.last_ball_recogtime:
                detectionlist = obs['sorted_contours']
                max_blob = detectionlist[0]
                self.last_ball_recogtime = recogtime
                
                if 1000 > max_blob['surface'] > 50:
                    self.ball_last_seen = time.time()
                    if (not nao or not self.nao.isMoving()): print "AL: Ik zie de bal, surface = %f ,x=%d, y=%d" % (max_blob['surface'],max_blob['x'], max_blob['y']) 
                                        
                    if (not nao or not self.nao.isMoving()) and (time.time() - self.temptime) > 2:
                        #Make sure that the ball is in the center of the camera:
                        if max_blob['y'] < 70:   
                            #when the ball is further away, the accepted center is larger
                            if max_blob['x'] < 50:
                                if nao: self.nao.walkNav(0, 0, 0.2)
                                self.temptime = time.time()
                                print "AL: turning left"
                            if max_blob['x'] > 110:
                                self.temptime = time.time()
                                if nao: self.nao.walkNav(0, 0, -0.2)
                                print "AL: turning right"
                        else: 
                            #when the ball is near the feet, just move left and right    
                            if max_blob['x'] < 70:
                                if nao: self.nao.walkNav(0, .05, .1)
                                self.temptime = time.time()
                                print "AL: moving left"
                            if max_blob['x'] > 90:
                                self.temptime = time.time()
                                if nao: self.nao.walkNav(0, -.05, -.1)
                                print "AL: moving right"

                # if the ball is in the upper part of the screen and fairly centered, walk towards it.
                if (not nao or not self.nao.isMoving()) and max_blob['y'] < 65 and 50 < max_blob['x'] < 110 and (time.time() - self.temptime) > 3:
                    self.temptime = time.time()
                    if nao: headstance = self.nao.get_yaw_pitch()
                    self.location = self.nao.ball_location(max_blob['x'],max_blob['y'],headstance[1],headstance[0])
                    # voor de y is er een correctie omdat de camera niet recht vooruit kijkt. Verder wordt er een factor van de afstand gebruikt. 
                    if nao: self.nao.walkNav((self.location[0]/100)*0.6 -0.05, (self.location[1]/100),-0.05,0.10)
                    print "AL: Zacht x =", self.location[0], "y =", self.location[1]
                
                # if the ball is in the lower part of the screen and centered precisely, the behavior is complete        
                if (not nao or not self.nao.isMoving()) and max_blob['y'] > 64 and 70 < max_blob['x'] < 90 and (time.time() - self.temptime) > 3:    
                        self.temptime = time.time()
                        self.m.add_item('approachlowball',time.time(),{})

        #in this function you can check what behaviors have failed or finished
        #and do possibly other things when something has failed
        pass



