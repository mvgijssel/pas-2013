import basebehavior.behaviorimplementation

import time

class AlignGoal_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will circle around the ball until it and the target goal in in a line.'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):
        self.idling = False
        self.target_goal = "yellow"
        self.eigen_goal = self.target_goal
        if self.eigen_goal == "yellow":
            self.andere_goal = "blue"
        else:
            self.andere_goal = "yellow"
        self.__start_time = time.time()
        self.__nao = self.body.nao(0)
        self.__nao.say("Lahten wuh duh bahl nar het goal richten!")
        #self.__nao.look_horizontal()
        self.last_recogtime = time.time()
        self.last_recogtime2 = time.time()
        self.temptime = time.time()
        #self.__nao.setCamVars()
        
        self.iter = 0
        
        self.Yellow= False
        self.Blue = False
        self.YellowLeft = False
        self.YellowRight = False        
        self.BlueLeft = False
        self.BlueRight = False
        
    def implementation_update(self):
        
        blob_max = {'surface':0,'y':0}
        blob_max2 = {'surface':0,'y':0}
        #YELLOW
        if (True and time.time() - self.__start_time > 3):
            if (self.m.n_occurs("combined_yellow") > 0):
                self.temptime = time.time()
                (recogtime, obs) = self.m.get_last_observation("combined_yellow")
                if not obs == None and recogtime > self.last_recogtime:
                    detectionlist = obs['sorted_contours']
                    blob_max = detectionlist[0]
#                    print "Yellow: x=%d, y=%d, surface=%f" % (blob_max['x'], blob_max['y'], blob_max['surface'])
                    self.last_recogtime = recogtime
                    
                    """if blob_max['surface'] > 100:
                        print "GEEL "
                        self.ball_last_seen = time.time()"""
                   
            if (self.m.n_occurs("combined_blue") > 0):
                self.temptime2 = time.time()
                (recogtime2, obs2) = self.m.get_last_observation("combined_blue")
                if not obs2 == None and recogtime2 > self.last_recogtime2:
                    detectionlist2 = obs2['sorted_contours']
                    blob_max2 = detectionlist[0]
#                    print "Blue: x=%d, y=%d, surface=%f" % (blob_max['x'], blob_max['y'], blob_max['surface'])
                    self.last_recogtime2 = recogtime2
                    """if blob_max2['surface'] > 100:
                        print "BLAUW "
                        self.ball_last_seen = time.time()"""
        
        #Als geel gedetecteerd: zet boolean op true
        if blob_max['surface'] > 100:
            if self.iter == 0:
                self.Yellow = True
            #Als gedetecteerd tijdens Rag_look_right, zet right op true
            elif self.iter == 1:
                self.YellowRight = True
            #Als gedetecteerd tijdens Rag_look_left, zet left op true
            elif self.iter == 2:
                self.YellowLeft = True
        
        #Als blauw gedetecteerd: zet boolean op true        
        if blob_max2['surface'] > 100:
            if self.iter == 0:
                self.Blue = True
            #Als gedetecteerd tijdens Rag_look_right, zet right op true
            elif self.iter == 1:
                self.BlueLeft = True
            #Als gedetecteerd tijdens Rag_look_left, zet left op true
            elif self.iter == 2:
                self.BlueRight = True
           
        if ((blob_max['surface'] < 100) and (blob_max2['surface'] < 100) and (self.temptime - time.time()) > 3 and self.iter == 0):
            self.temptime = time.time()
            self.__nao.start_behavior("rag_look_right")
            self.iter = 1
        
        if True and (blob_max['surface'] < 100) and (blob_max2['surface'] < 100) and self.temptime - time.time() > 3 and self.iter == 1:
            self.temptime = time.time()
            self.__nao.start_behavior("rag_look_left")
            self.iter = 2
            
        if True and (blob_max['surface'] < 100) and (blob_max2['surface'] < 100) and self.temptime - time.time() > 3 and self.iter == 2:
            self.temptime = time.time()
            self.__nao.look_horizontal()
            self.iter = 3
        
        
        ##Deze stap is noodzakelijk om ervoor te zorgen dat hij Left of Right niet op True zet terwijl hij nog naar links kijkt terwijl de iter al wel op 0 is gezet.
        if True and (blob_max['surface'] < 100) and (blob_max2['surface'] < 100) and self.temptime - time.time() > 3 and self.iter == 3:
            self.temptime = time.time()
            self.iter = 0
            
        ##Hier moet worden gekeken of de bal wordt gezien en dan en of er een blob van 1 kleur is, die ongeveer midden in het beeld ligt (het goal). De searchball zorgt dat je weet waar de bal blijft en wisselt met dit behaviour.    
        if (zie ik de goal) and (goal in het midden):
            self.m.add_item('goal_aligned',time.time(),{})
        elif (zie ik de goal niet):
            self.wachttijd = time.time()
            if self.nao.isMoving and self.wachttijd > 3:
                vlaggetje += 1
                if self.nao.isMoving and self.wachttijd > 3 and vlaggetje = 3:
                    self.nao.walkNav(0, 0.05, 1)
            vlaggetje = 0
        elif (goal niet in het midden)
            self.nao.WalkNav(???)
            
        if (time.time() - self.__start_time) > 5:
            self.m.add_item('subsume_stopped',time.time(),{'reason':'Ball no longer seen.'})
            self.idling = True

