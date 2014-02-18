import time
import random

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation


class Searchball_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.nao.set_cam_vars()
        self.nao.say("Find the ball, we must!")
        self.start_time = time.time()
        self.idling = 0
        self.iter = 0
        #Make sure the robot is standing and looks horizontal:

        self.nao.look_horizontal()
        self.rng = random.random()
        self.last_recogtime = time.time()

    def implementation_update(self):

        if (time.time() - self.start_time) > 5:
            if (self.m.n_occurs("combined_red") > 0):
                self.temptime = time.time()
                (recogtime, obs) = self.m.get_last_observation("combined_red")
                if not obs == None and recogtime > self.last_recogtime:
                    detectionlist = obs['sorted_contours']
                    blob_max = detectionlist[0]
                    print "Red: x=%d, y=%d, surface=%f" % (blob_max['x'], blob_max['y'], blob_max['surface'])
                    self.last_recogtime = recogtime
                    #Ball is found if the detected ball is big enough (thus filtering noise):

                    if blob_max['surface'] > 50:
                        print "Ik zie de bal"
                        self.ball_last_seen = time.time()
                        #Is the ball in the correct location?:
                        if blob_max['y'] > 75 and blob_max['x'] > 60 and blob_max['x'] < 100 and not self.is_looking_horizontal:
                            # If the ball is seen close enough, use self.m.add_item('ball_approached',time.time(),{}) to finish this behavior.
                            headstance = self.nao.get_yaw_pitch()
                            pitch = headstance[1]
                            self.location = self.nao.ball_location(blob_max['x'],blob_max['y'],)                            
                            self.m.add_item('approachball', time.time(),{}) 
                            
                            print "Ik ben dicht genoeg bij de bal."
                            return
                        elif blob_max['surface'] > 60:
                            print "Ik zie iets dat rood is en waarschijnlijk groot genoeg is om de bal te kunnen zijn!"
                            self.nao.look_horizontal()
                            # Once the ball is properly found, use: self.m.add_item('searchball',time.time(),{}) to finish this behavior.
                            self.m.add_item('searchball',time.time(),{})
                            if not self.nao.isWalking():
                                #Walk a bit if the ball is not really close:
                                if blob_max['y'] < 80:
                                    self.nao.walkNav(0.05, 0, 0)
                                    pass
                                elif self.is_looking_horizontal:
                                    self.nao.look_down()
                                    self.is_looking_horizontal = False

            if(time.time() - self.start_time) > 4:
                
                if (self.idling == 0 and not self.nao.isMoving()):
                    self.temptime = time.time()
                    self.nao.start_behavior("rag_look_right")
                    self.idling = 1   
                
                if self.idling == 1 and (time.time() - self.temptime > 3):
                    self.temptime = time.time()
                    self.nao.start_behavior("rag_look_left")
                    self.idling = 2

                if self.idling == 2 and (time.time() - self.temptime > 4) and not self.nao.isMoving():
                    self.nao.look_horizontal()
                    self.temptime = time.time()
                    if (self.rng < 0.50 ):
                        self.nao.walkNav(0.10, 0, 1.57, 0.10)
                        self.iter +=1
                        self.idling = 3                    
                    else:
                        self.nao.walkNav(0.10, 0, -1.57, 0.10)
                        self.idling = 3
                        
                if self.idling == 3 and (time.time() - self.temptime > 4) and not self.nao.isMoving() and self.iter == 2:
                    self.nao.walkNav(0.30,0,0,0.10)
                    self.idling = 0
                
 #           if self.idling == 2 and not self.nao.isMoving() and (time.time() - self.temptime > 5) :
  #              self.idling = 3
                
           # if self.idling == 3 and (time.time() - self.temptime > 5):                        
           #     self.nao.start_behavior("rag_turnhead")
           #     if self.idling == 3 and not self.nao.isMoving():
           #         self.idling = 0

        #you can do things here that are low-level, not consisting of other behaviors

        #in this function you can check what behaviors have failed or finished
        #and do possibly other things when something has failed
        



