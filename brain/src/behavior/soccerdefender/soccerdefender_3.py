import basebehavior.behaviorimplementation
import time
import random



class SoccerDefender_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):
        #Select Nao and make it stand up.
        self.nao = self.body.nao(0)
        self.nao.say("We are invinsible!")
        self.nao.start_behavior("standup")
        self.nao.set_cam_vars()
        self.nao.look_horizontal()
        self.position = 0 #goal is 60 cm wide
        self.walktime = time.time()
        self.state = "stand"
        self.looktime = time.time()
        self.last_recogtime = time.time()
        self.starttime = time.time()
        self.leftpost = -.20
        self.rightpost = .20
        
    def implementation_update(self):
        #Make the Nao move to the right and left:
        '''
        if not self.__nao.isWalking():
            self.__nao.walkNav(0, self.__position, 0)
            self.__position *= -1
        '''
        
        # haal blobdetector binnen en zet de hoofdhoek goed
        if self.state == "stand" and not self.nao.isMoving() and ((time.time() - self.starttime) > 7) :
            self.nao.set_angles(['HeadPitch'], [0.3267], 0.2, radians=True)
            self.state = "looking down"
            self.nao.start_behavior("rag_keeper-stance5")
        
        
        if (self.m.n_occurs("combined_red") > 0) and ((time.time() - self.starttime) > 11):
            # print "Ik zie iets dat rood is"
            (recogtime, obs) = self.m.get_last_observation("combined_red")
            if not obs == None and recogtime > self.last_recogtime:
                detectionlist = obs['sorted_contours']
                blob_max = detectionlist[0]
                # print "Red: x=%d, y=%d, surface=%f" % (blob_max['x'], blob_max['y'], blob_max['surface'])
                self.last_recogtime = recogtime
                if blob_max['surface'] > 60 and ((time.time() - self.looktime) > 2):
                    #self.nao.say("here it comes")
                    headstance =  self.nao.get_yaw_pitch()
                    bal = self.nao.ball_location(blob_max['x'],blob_max['y'],headstance[0],headstance[1])                    
                    #print "X =", bal[0], "Y =",bal[1],"\n"  
                    self.looktime = time.time()
                    
                    
                    


                    #zet een stap naar rechts
                    if not self.nao.isMoving() and (time.time() - self.walktime > 2):
                        #Make sure that the ball is in the center of the camera:
                        print "X" + "_"*int((self.position+.3)*20) + 'N' + "_"*(12-int((self.position+.3)*20)) + "X"
                        if blob_max['x'] < 70:
                            self.links = bal[1]/100*.95
                            print self.links, "links"
                            self.movement = max(self.leftpost - self.position, self.links)
                            self.nao.walkNav(-.01, self.movement, 0, 0.1)
                            self.position += self.movement
                            self.walktime = time.time()
                            pass
                        elif blob_max['x'] > 90:
                            self.rechts = bal[1]/100*1.05
                            print self.rechts, "rechts"
                            self.movement = min(self.rechts, self.rightpost - self.position)
                            self.nao.walkNav(-.01, self.movement, 0, 0.1)
                            self.position += self.movement
                            self.walktime = time.time()
                            pass
        
                            
      

        if (self.state == "stand" or self.state == "left") and ((time.time() - self.looktime) > 4):
            self.looktime = time.time()
            print "looking left"
            self.nao.start_behavior("rag_look_right")
            self.state = "right"
          
        if self.state == "right" and ((time.time() - self.looktime) > 4):
            self.looktime = time.time()
            print "looking right"
            self.nao.start_behavior("rag_look_left")
            self.state = "left"

