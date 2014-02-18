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
        #Make sure the robot is standing and looks horizontal:
        self.nao.start_behavior("standup")
        self.nao.look_horizontal()
        self.rng = random.random()
        self.last_recogtime = time.time()

    def implementation_update(self):
 #       
  #      if (time.time() - self.start_time) > 5:
   #         if self.state == "TURN":
    #            if not self.nao.isWalking():
     #               self.state = "WALK"
      #              self.nao.start_behavior("")walkNav(random.random() * 10, 10, 0)
       #     elif self.state == "WALK":
#
 #               if not self.nao.isWalking():
  #                  self.state = "TURN"
   #                 self.nao.walkNav(0, 0, random.random() * 2 - 1, 0.1)

        #Try to see if there is a ball in sight:
        if (self.m.n_occurs("combined_red") > 0):
            print "Ik zie iets dat rood is" 
            (recogtime, obs) = self.m.get_last_observation("combined_red")
            if not obs == None and recogtime > self.last_recogtime:
                detectionlist = obs['sorted_contours']
                blob_max = detectionlist[0]
                print "Red: x=%d, y=%d, surface=%f" % (blob_max['x'], blob_max['y'], blob_max['surface'])
                self.last_recogtime = recogtime
                #Ball is found if the detected ball is big enough (thus filtering noise):
                if blob_max['surface'] > 30:
                    print "Ik zie iets dat rood is en waarschijnlijk groot genoeg is om de bal te kunnen zijn!"
                    # Once the ball is properly found, use: self.m.add_item('ball_found',time.time(),{}) to finish this behavior.
                    self.m.add_item('searchball',time.time(),{})
        

        if(time.time() - self.start_time) > 5 :
            
            if self.idling == 0:
                self.temptime = time.time()
                self.nao.start_behavior("rag_turnhead")
                self.idling = 1   

            if self.idling == 1 and not self.nao.isMoving() and (time.time() - self.temptime > 5):
                if (self.rng < 0.50):
                    print "We gaan links"
                    self.nao.start_behavior("rag_search_left")
                    self.idling = 2                    
                else:
                    print "We gaan rechts"
                    self.nao.start_behavior("rag_search_right")
                    self.idling = 2
                
            if self.idling == 2 and not self.nao.isMoving() and (time.time() - self.temptime > 5):
                self.idling = 3
                
            if self.idling == 3 and (time.time() - self.temptime > 5):                        
                self.nao.start_behavior("rag_turnhead")
                if self.idling == 3 and not self.nao.isMoving():
                    self.idling = 0

        #you can do things here that are low-level, not consisting of other behaviors

        #in this function you can check what behaviors have failed or finished
        #and do possibly other things when something has failed
        



