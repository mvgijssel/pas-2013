import basebehavior.behaviorimplementation
import time
import random
import math

nao = True

class searchball_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will move the Nao around until the ball is seen in the middle of the FoV.'''

    def implementation_init(self):
        self.nao = self.body.nao(0)
        self.nao.say("Ick zook duh bahl")
        self.start_time = time.time()
        if nao: self.nao.set_cam_vars()
        if nao: self.nao.look_horizontal()
        self.last_recogtime = time.time()
        self.looktime = time.time()
        self.seen_left = False
        self.state = "Init"
        # when balltime is smaller than time.time(), the behavior completes. We assume the ball will be found within 16 minutes
        self.balltime = time.time() + 1000
        self.nao.set_eyes([0,255,0],[0,255,0])
        


    def implementation_update(self):
        # Make use of your sight, first look up and down, before looking left and right.
        # If the ball is not yet seen, turn around.
        # We therefore assume that the ball can be found by looking and turing around.
        
        # TODO misschien een random loopje erin?
        
        if self.state == "Init" and (time.time() - self.looktime) > 4:
            print "S: Looking down"
            self.looktime = time.time()
            if nao: self.nao.look_down()
            time.sleep(0.3)
            self.state = "down"
        
        if self.state == "down" and (time.time() - self.looktime) > 2 and not self.seen_left:   
            print "S: Looking Left"
            self.looktime = time.time()
            if nao: self.nao.start_behavior("rag_look_left2")
            time.sleep(0.1)
            self.seen_left = True
            self.state = "Left"
        
        if (self.state == "Left" or (self.state == "down" and self.seen_left)) and (time.time() - self.looktime) > 3:   
            print "S: Looking Right"
            self.looktime = time.time()
            if nao: self.nao.start_behavior("rag_look_right")
            time.sleep(0.1)
            self.state = "Right"
            
            
        if self.state == "Right" and (time.time() - self.looktime) > 2:
            print "S: Looking up"
            self.looktime = time.time()
            if nao: self.nao.look_up()
            time.sleep(0.5)
            self.nao.look_horizontal()
            self.state = "up"      
               
        if self.state == "up" and (not nao or not self.nao.isMoving()) and (time.time() - self.looktime) > 3:      
            print "S: Moving clockwise"
            self.looktime = time.time()
            if nao: self.nao.walk(0,0,-1.2)
            time.sleep(0.1)
            self.state = "walk"
            
        if self.state == "walk" and (not nao or not self.nao.isMoving()) and (time.time() - self.looktime) > 4:
            self.getal = random.random()
            if self.getal > .5:
                print "S: Walking"
                if nao: self.nao.walk(.20,0,0)
                self.looktime = time.time()
                time.sleep(.1)
            self.state = "Init"

        #Try to see if there is a ball in sight:
        if (self.m.n_occurs("combined_red") > 0) and (time.time() - self.start_time) > 3:
            (recogtime, obs) = self.m.get_last_observation("combined_red")
            if not obs == None and recogtime > self.last_recogtime:
                detectionlist = obs['sorted_contours']
                blob_max = detectionlist[0]
                #print "red: x=%d, y=%d, size=%f" % (blob_max['x'], blob_max['y'], blob_max['surface'])
                self.last_recogtime = recogtime
                
                #When the ball is seen, print its location, where negative y is to the right
                if 1500 > blob_max['surface'] > 50:
                    self.balltime = time.time()
                    headstance =  self.nao.get_yaw_pitch()
                    bal = self.nao.ball_location(blob_max['x'],blob_max['y'],headstance[1],headstance[0])      
                    print "S: Ik zie de bal", "x=", bal[0], "y=", bal[1]
                    
                    # if the ball was seen while looking left or right, turn towards the ball
                    if (self.state == "Right" or self.state == "Left") and (not nao or not self.nao.isMoving()):
                        print "S: bijdraaien ahv ball_location"  
                        self.nao.say("Daahr is duh bahl")
                        # balltime is increased in order to allow the Nao to complete its turn
                        self.balltime += 2
                        if nao: self.nao.walk(0,0,max(min(math.atan(bal[1]*4/bal[0]),1),-1))
                        time.sleep(.5)
                        self.m.add_item('subsume_stopped',time.time(),{'reason':'ball seen while right/left'})
                                        
                    # if the ball is seen while looking down, keep the head down and continue in approachlowball                   
                    elif self.state == "down" and (not nao or not self.nao.isMoving()):
                        if nao: self.nao.look_down()
                        self.m.add_item('approachball',time.time(),{})
                    
                    # if the ball is seen while looking up, turn and head towards the ball
                    elif self.state == "up" and (not nao or not self.nao.isMoving()):
                        print "s: We gaan naar voren"
                        self.nao.say("Ick gah nahr foohren")
                        # balltime is increased in order to allow the Nao to complete its walk
                        self.balltime += 4
                        if nao: self.nao.walk(0,0,math.atan(bal[1]/bal[0]))
                        time.sleep(0.1)
                        if nao: self.nao.walk(0.3,0,0)
                        time.sleep(0.5)
                    
                    # if the bal is seen N seconds ago, continue to approachball
                    if (time.time() - self.balltime) >= 0:
                        self.m.add_item('searchball',time.time(),{})
