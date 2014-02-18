
import basebehavior.behaviorimplementation
import time
import almath

nao = True
corr = 0

class ApproachBall_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior moves the Nao towards the ball untill the ball is in the lower part of the screen.'''
    
    def implementation_init(self):
        self.nao = self.body.nao(0)
        self.nao.say("Ick ghaa nahr duh bahl")
        self.last_ball_recogtime = 0
        self.ball_last_seen = time.time()
        self.temptime = time.time()
        if nao: self.nao.set_cam_vars()
        if nao: self.nao.look_horizontal()
        self.is_looking_horizontal = True

    def implementation_update(self):
        
        if (self.m.n_occurs("combined_red") > 0):
            (recogtime, obs) = self.m.get_last_observation("combined_red")
            if not obs == None and recogtime > self.last_ball_recogtime:
                detectionlist = obs['sorted_contours']
                max_blob = detectionlist[0]
                # print "ROOD: x=%d, y=%d, size=%f" % (max_blob['x'], max_blob['y'], max_blob['surface'])
                self.last_ball_recogtime = recogtime
                
                if 1000 > max_blob['surface'] > 50:
                    self.ball_last_seen = time.time()
                    if (not nao or not self.nao.isMoving()): print "A: Ik zie de bal, surface = %f ,x=%d, y=%d" % (max_blob['surface'],max_blob['x'], max_blob['y']) 
                    
                    # If not moving, make sure that the ball is in the center of the camera:
                    if (not nao or not self.nao.isMoving()) and (time.time() - self.temptime) > 2:
                       if self.is_looking_horizontal:
                            if max_blob['x'] < 60:
                                self.temptime = time.time()
                                if nao: self.nao.walk(0, 0, 0.3)
                                print "A: turning left"
                            
                            if max_blob['x'] > 100:
                                self.temptime = time.time()
                                if nao: self.nao.walk(0, 0, -0.3)
                                print "A: turning right"
                                           
                    if (not nao or not self.nao.isMoving()) and (time.time() - self.temptime) > 3 and self.is_looking_horizontal:
                        self.temptime = time.time()
                       
                        #If the ball is seen and it's not close enough, approximate distance and walk towards it
                        if self.is_looking_horizontal and (max_blob['y']+corr) < 80:
                            if nao: headstance = self.nao.get_yaw_pitch()
                            self.temptime = time.time()
                            self.location = self.nao.ball_location(max_blob['x'],(max_blob['y']+corr),headstance[1],headstance[0])
                            print "A: lopen naar x =", self.location[0], "y =", self.location[1]
                            self.nao.walk((self.location[0]/100)*0.95, (self.location[1]/100)*.5,0)
                        
                        #If the ball is seen in the below screen while looking horizontal, look down and continue movement
                        if (max_blob['y']+corr) > 70 and self.is_looking_horizontal and (not nao or not self.nao.isMoving()) and 60 <= max_blob['x'] <= 100:
                            if nao: self.nao.look_down()
                            time.sleep(.1)
                            self.is_looking_horizontal = False
                            self.m.add_item('approachball',time.time(),{})
                            
        
        
      #   Timeout after 10 seconds if the ball is not seen anymore:
        if (time.time() - self.ball_last_seen) > 5:
            self.nao.say("Wahr is duh bahl hain?")
            self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})
#            self.idling = True
