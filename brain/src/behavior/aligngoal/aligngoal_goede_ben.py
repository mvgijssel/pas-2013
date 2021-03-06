import basebehavior.behaviorimplementation
import time

nao = True

class AlignGoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will circle around the ball until it and the target goal are in one line.'''



    def implementation_init(self):

        self.goal = "yellow" #DEFAULT GOAL IS YELLOW
        
        if self.goal == "yellow":
            self.target_goal = "yellow"
            self.own_goal = "blue" 
        else:
            self.target_goal = "blue"
            self.own_goal = "yellow"
                    
        self.nao = self.body.nao(0)
        self.nao.say("ick drye nahr hat dool")
        
        self.start_time = time.time()
        self.last_recogtime_y = time.time()
        self.last_recogtime_b = time.time()
        self.temptime = time.time()
        
        if nao: self.nao.set_cam_vars()
        if nao: self.nao.set_angles(['HeadPitch'], [-0.3], 0.2, radians=True)   
        self.blob_y = {'surface':0, 'x':0, 'y':0}
        self.blob_b = {'surface':0, 'x':0, 'y':0}
        self.aligned = False
        self.state = "None"
        self.previous_state = ""
        
    def implementation_update(self):
        # start detecting after 2 seconds
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


            #### Zet oppervlak van blob op 1 indien een seconde of langer niet gezien. ####
            
            if abs(self.last_recogtime_y - time.time()) > 1: 
                self.blob_y['surface'] = 1
                
            if abs(self.last_recogtime_b - time.time()) > 1: 
                self.blob_b['surface'] = 1                

                    
            #### states aanpassen ahv waarnemingen ####
            
            if self.blob_y['surface'] < 150 and self.blob_b['surface'] < 150 and self.state != "None":
                if (self.previous_state != self.state):
                    self.previous_state = self.state
                self.state = "None"
            
            # I see the yellow goal
            if self.blob_y['surface'] > 150 and self.blob_b['surface'] < 150:
                # print "Yellow surface: " + str(self.blob_y['surface']) + " Blue surface: " + str(self.blob_b['surface'])
                # Do I see the yellow goal, or do I see the lower part of the BlueYellow marker?
                if (self.blob_y['y'] + self.blob_y['height']) < 30:
                    """Als je maar een klein gedeelte (qua hoogte) van de blob ziet: kijk omhoog! """
                    if nao: self.nao.set_angles(['HeadPitch'], [-0.4], 0.2, radians=True)   
                elif self.state != "Yellow_Goal":
                    if (self.previous_state != self.state):
                        self.previous_state = self.state
                    self.state = "Yellow_Goal"
                
            # I see the blue goal
            if self.blob_y['surface'] < 150 and self.blob_b['surface'] > 150:
                # print "Yellow surface: " + str(self.blob_y['surface']) + " Blue surface: " + str(self.blob_b['surface'])
                # Do I see the blue goal, or do I see the lower part of the YellowBlue marker?
                if (self.blob_b['y'] + self.blob_b['height']) < 30:
                    """Als je maar een klein gedeelte (qua hoogte) van de blob ziet: kijk omhoog! """
                    if nao: self.nao.set_angles(['HeadPitch'], [-0.4], 0.2, radians=True)   
                elif self.state != "Blue_Goal":
                    if (self.previous_state != self.state):
                        self.previous_state = self.state
                    self.state = "Blue_Goal"
            
            # I see one of the markers
            if self.blob_y['surface'] > 150 and self.blob_b['surface'] > 150 \
            and self.blob_y['width'] > self.blob_y['height'] \
            and self.blob_b['width'] > self.blob_b['height']:

                #print "Yellow surface: " + str(self.blob_y['surface']) + " Blue surface: " + str(self.blob_b['surface'])
                if nao: self.nao.set_angles(['HeadPitch'], [-0.3], 0.2, radians=True)   
                if self.blob_y['y'] < self.blob_b['y'] and self.state !="Yellow_Blue":
                    if (self.previous_state != self.state):
                        self.previous_state = self.state
                    self.state = "Yellow_Blue"
                if self.blob_y['y'] > self.blob_b['y'] and self.state !="Blue_Yellow":
                    if (self.previous_state != self.state):
                        self.previous_state = self.state
                    self.state = "Blue_Yellow"
            
            '''if (time.time() - self.temptime) > 3: 
                print "Current state: " + self.state
                print "Previous state: " + self.previous_state'''
            
            #### draaien aan de hand van de states ####
            
            if (not nao or not self.nao.isMoving()) and (time.time() - self.temptime) > 6:
                self.temptime = time.time()
                
                # set states depending on target_goal
                self.doel = (self.state == "Yellow_Goal" and self.target_goal == "yellow") or (self.state == "Blue_Goal" and self.target_goal == "blue")
                self.prev_doel = (self.state == "None" and ((self.previous_state == "Yellow_Goal" and self.target_goal == "yellow") or (self.previous_state == "Blue_Goal" and self.target_goal == "blue")))
               
                self.anderdoel = (self.state == "Yellow_Goal" and self.target_goal == "blue") or (self.state == "Blue_Goal" and self.target_goal == "yellow")
                self.prev_anderdoel = (self.state == "None" and ((self.previous_state == "Yellow_Goal" and self.target_goal == "blue") or (self.previous_state == "Blue_Goal" and self.target_goal == "yellow")))
                
                self.links = (self.state == "Blue_Yellow" and self.target_goal == "yellow") or (self.state == "Yellow_Blue" and self.target_goal == "blue")
                self.prev_links = (self.state == "None" and ((self.previous_state == "Blue_Yellow" and self.target_goal == "yellow") or (self.previous_state == "Yellow_Blue" and self.target_goal == "blue")))
                
                self.rechts = (self.state == "Yellow_Blue" and self.target_goal == "yellow") or (self.state == "Blue_Yellow" and self.target_goal == "blue")
                self.prev_rechts = (self.state == "None" and ((self.previous_state == "Yellow_Blue" and self.target_goal == "yellow") or (self.previous_state == "Blue_Yellow" and self.target_goal == "blue")))               
                
                # huidige of laatste observatie het andere doel, clockwise
                if self.anderdoel or self.prev_anderdoel:
                    print "AG: Ik zie het andere doel"
                    self.nao.walk(.04,.12,-.85)
                    time.sleep(.1)
                
                elif self.doel:
                    
                    print "AG: Ik zie de target goal"
                    if (self.target_goal == 'yellow' and (self.blob_y['x'] + .5 * self.blob_y['width']) < 50 ) \
                    or (self.target_goal == 'blue' and (self.blob_b['x'] + .5 * self.blob_b['width']) < 50):
                        
                        #YYY       Y       #
                        #YYY       Y       #
                        #YYY       Y       # 
                        #YYY       Y       # 
                        #YYY       Y       #
                        
                        print "nog een beetje ccw"
                        self.nao.walk(.015,-.06,.44)
                        time.sleep(.1)
                    elif (self.target_goal == 'yellow' and (self.blob_y['x'] + .5 * self.blob_y['width']) > 110) \
                    or (self.target_goal == 'blue' and (self.blob_b['x'] + .5 * self.blob_b['width']) > 110):
                        print "nog een beetje cw"
                        #guesstimate!!!
                        self.nao.walk(.015,.06,-.44)
                        time.sleep(.1) 
                    else:                       
                        self.m.add_item('aligngoal',time.time(),{})
          
               
                # left mark, turn clockwise
                elif self.links or self.prev_links:
                    print "AG: ik zie/zag de linkermarkering."
                    self.nao.walk(.04,.12,-.85)
                    time.sleep(.1)
                
                # right mark, turn counterclockwise
                elif self.rechts or self.prev_rechts:
                    print "AG: Ik zie/zag de rechtermarkering."
                    self.nao.walk(.04,-.11,.65)
                    time.sleep(.1)
                
                #geen van bovenstaande    
                else:
                    print "AG: Ik zie niks"
                    self.nao.walk(.04,-.11,.65)
                    time.sleep(.1)                 
               
