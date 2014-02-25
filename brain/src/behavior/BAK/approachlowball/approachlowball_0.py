import basebehavior.behaviorimplementation
import time
import almath

nao = True
corr = 0

class Approachlowball_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior moves the Nao slowly towards the ball while looking down'''
   
    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.nao.say("Ick kike nahr Behnaidehn")
        self.last_ball_recogtime = 0
        self.ball_last_seen = time.time()
        self.temptime = time.time()
        if nao: self.nao.set_cam_vars()
        self.nao.set_eyes([255,0,0],[255,0,0])
        self.x_low = 54
        self.x_high = 68
        self.y_low = 71
        self.y_high = 80
       
    def implementation_update(self):

        if (self.m.n_occurs("combined_red") > 0):
            (recogtime, obs) = self.m.get_last_observation("combined_red")
            if not obs == None and recogtime > self.last_ball_recogtime:
                detectionlist = obs['sorted_contours']
                max_blob = detectionlist[0]
                self.last_ball_recogtime = recogtime
               
                if 1000 > max_blob['surface'] > 50:
                    self.ball_last_seen = time.time()
                    #if (not nao or not self.nao.isMoving()): print "AL: Ik zie de bal, surface = %f ,x=%d, y=%d ,width=%d" % (max_blob['surface'],max_blob['x'], max_blob['y'],max_blob['width'])
                                       
                    if (not nao or not self.nao.isMoving()) and (time.time() - self.temptime) > .5:
                        #Make sure that the ball is in the center of the camera:
                       
                        if (max_blob['y'] + corr)< self.y_low:
                            #ball is too far away
                            if max_blob['x'] <= (self.x_low - 20):
                                #ball is in left part of screen, turn
                                if nao: self.nao.walk(0, 0, 0.2)
                                time.sleep(.1)
                                self.temptime = time.time()
                                print "AL: turning left"
                            if (self.x_low - 20) < max_blob['x'] <= (self.x_high + 20):
                                #ball is in the middle of the screen, walk

                                self.temptime = time.time()
                                if nao: headstance = self.nao.get_yaw_pitch()
                                self.location = self.nao.ball_location(max_blob['x'],(max_blob['y'] + corr),headstance[1],headstance[0])
                                if nao: self.nao.walk((self.location[0]/100)*0.6 - 0.05, (self.location[1]/100)*0.6 -.05,0)
                                time.sleep(.1)
                                print "AL: zacht x =", (self.location[0]/100)*0.6 - 0.05, "y =", (self.location[1]/100)*0.6
                            if max_blob['x'] > (self.x_high + 20):
                                #ball is in right part of screen, turn
                                self.temptime = time.time()
                                if nao: self.nao.walk(0, 0, -0.2)
                                time.sleep(.1)
                                print "AL: turning right"
                        elif self.y_low <= (max_blob['y'] + corr) <= self.y_high:
                            #ball is near   
                            if max_blob['x'] <= (self.x_low):
                                #ball is in left part of screen, turn
                                if nao: self.nao.walk(0, .03, 0)
                                time.sleep(.1)
                                self.temptime = time.time()
                                print "AL: strafing a little left"
                            if (self.x_low) < max_blob['x'] <= (self.x_high):
                                #ball is in green zone, complete behavior
                                self.temptime = time.time()

                                self.m.add_item('approachlowball',time.time(),{})



                            if max_blob['x'] > (self.x_high):
                                #ball is in right part of screen, turn
                                self.temptime = time.time()
                                if nao: self.nao.walk(0, -.04, 0)
                                time.sleep(.1)
                                print "AL: strafing a little right"
                        else:
                            #ball is too close, walk backwards
                            if nao: self.nao.walk(-.02, 0, 0)
                            time.sleep(.1)
                            print "AL: moving backwards"
                            self.temptime = time.time()
                            
                                
                                
        if (time.time() - self.ball_last_seen) > 6:
            self.nao.say("Wahr is duh bahl hain?")
            self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})


