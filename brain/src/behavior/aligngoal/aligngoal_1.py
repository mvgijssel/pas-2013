import basebehavior.behaviorimplementation
import time

nao = True

class AlignGoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will circle around the ball until it and the target goal in in a line.'''



    def implementation_init(self):
    
        self.goal = "yellow" #DEFAULT GOAL IS YELLOW
        
        if self.goal == "yellow":
            self.target_goal = "yellow"
            self.own_goal = "blue" 
        else:
            self.target_goal = "blue"
            self.own_goal = "yellow"

        self.state = "None"
        self.start_time = time.time()
        self.nao = self.body.nao(0)
        self.nao.say("ick drye nahr hat dool")
        self.last_recogtime_y = time.time()
        self.last_recogtime_b = time.time()
        self.temptime = time.time()
        self.aligned = False
        if nao: self.nao.set_cam_vars()
        self.nao.start_behavior("standup")
        if nao: self.nao.set_angles(['HeadPitch'], [-0.3], 0.2, radians=True)   
        self.blob_y = {'surface':0, 'x':0, 'y':0}
        self.blob_b = {'surface':0, 'x':0, 'y':0}
        
    def implementation_update(self):
 
        if (time.time() - self.start_time) > 2:
            if (self.m.n_occurs("combined_yellow") > 0):
                (recogtime_y, obs_y) = self.m.get_last_observation("combined_yellow")
                if not obs_y == None and recogtime_y > self.last_recogtime_y:
                    detectionlist_y = obs_y['sorted_contours']
                    self.blob_y = detectionlist_y[0]
                    #print "Yellow: x=%d, y=%d, surface=%f" % (blob_max['x'], blob_max['y'], blob_max['surface'])
                    self.last_recogtime_y = recogtime_y
                    
                   
            if (self.m.n_occurs("combined_blue") > 0):
                (recogtime_b, obs_b) = self.m.get_last_observation("combined_blue")
                if not obs_b == None and recogtime_b > self.last_recogtime_b:
                    detectionlist_b = obs_b['sorted_contours']
                    self.blob_b = detectionlist_b[0]
                    #print "Blue: x=%d, y=%d, surface=%f" % (blob_max['x'], blob_max['y'], blob_max['surface'])
                    self.last_recogtime_b = recogtime_b
                    
            #### states aanpassen ahv waarnemingen ####
            
            # i see the yellow goal
            if self.blob_y['surface'] > 150 and self.blob_b['surface'] < 150 and self.blob_y['y'] < 50:
                self.state = "Yellow_Goal"
                
            # i see the blue goal
            if self.blob_y['surface'] < 150 and self.blob_b['surface'] > 150 and self.blob_b['y'] < 50:
                self.state = "Blue_Goal"
            
            # i see one of the markers
            # TODO breedte groter dan hoogte    
            if self.blob_y['surface'] > 150 and self.blob_b['surface'] > 150 and self.blob_y['width'] > self.blob_y['height'] and self.blob_b['width'] > self.blob_b['height']:
                if self.blob_y['y'] < self.blob_b['y']:
                    self.state = "Yellow_Blue"
                if self.blob_y['y'] > self.blob_b['y']:
                    self.state = "Blue_Yellow"
            
            #### draaien aan de hand van de states ####
            
            if (not nao or not self.nao.isMoving()) and (time.time() - self.temptime) > 3:
                print self.state
                if self.state == "None":
                    self.temptime = time.time()
                    # draai links om de bal, beeld verschuift naar rechts
                    if nao: self.nao.walkNav(.05,.15,-1,0.1)
                    print "N: linksom!"
                
                if (self.state == "Yellow_Goal" and self.target_goal == "yellow") or (self.state == "Blue_Goal" and self.target_goal == "blue"):
                    self.temptime = time.time()
                    # x zit tussen de 0 en 160
                    if self.blob_y['x'] > 40:
                        # een klein beetje naar links om de bal, zodat doel meer tegen linkerrand zicht zit.
                        if nao: self.nao.walkNav(.015,.06,-.44,0.1)
                        print "Y: linksom!"
                    
                    # TODO TODO TODO
                    # if self.blob_y['x'] < 40 and self.blob_y['width'] < 70
                    #     if nao: self.nao.walkNav( VERKLEINDE RECHTSOMDEBAL)
                    #
                    # TODO TODO TODO
                    
                    else:
                        self.m.add_item('aligngoal',time.time(),{})
                
                if (self.state == "Blue_Goal" and self.target_goal == "yellow") or (self.state == "Yellow_Goal" and self.target_goal == "blue"):
                    self.temptime = time.time()
                    # we maken een kwart cirkel.
                    self.nao.walkNav(.04,.12,-.85,0.1)
                    print "B: 1L"
                    time.sleep(.5)
                    self.nao.walkNav(.04,.12,-.85,0.1)
                    print "B: 2L"
                    time.sleep(.5)
                    print "B: 5 half turn done"
                            
                if (self.state == "Blue_Yellow" and self.target_goal == "yellow") or (self.state == "Yellow_Blue" and self.target_goal == "blue"):
                    self.temptime = time.time()
                    # een kwart clockwise / linksomdebal draaien
                    self.nao.walkNav(.04,.12,-.85,0.1)
                    print "BY: 1L"
                    time.sleep(.5)
                    self.nao.walkNav(.04,.12,-.85,0.1)
                    print "BY: 2L turning done"
                        
                if (self.state == "Yellow_Blue" and self.target_goal == "yellow") or (self.state == "Blue_Yellow" and self.target_goal == "blue"):
                    self.temptime = time.time()
                    # een kwart counterclockwise / rechtsomomdebal draaien
                    self.nao.walkNav(.04,-.11,.65,0.1)
                    print "YB: 1R"
                    time.sleep(.5)
                    self.nao.walkNav(.04,-.11,.65,0.1)
                    time.sleep(.5)
                    print "YB: 2 turning done"
            

        
            

       
        # TO DO: Remove the following with the steps mentioned below (e.d. align the robot so that it can kick the ball in the direction of the goal):
        # It now simply assumes that it is already aligned:
        # self.m.add_item('goal_aligned',time.time(),{})
            
        # If the ball and the goal are both in sight, check if they are in line with each other.
        # If they are aligned, use self.m.add_item('goal_aligned',time.time(),{}) to finish this behavior.
        # Else, turn to align them.
        # If the ball is in sight but the goal is not, strafe/circle in a single direction, keeping the ball in sight.

        # TO DO: Remove simple timeout with:
        # Check if you can see the ball. If you can't, go idle so the structure resets.
        
        #if (time.time() - self.start_time) > 5:
        #    self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})
        #    self.idling = True
        
