import basebehavior.behaviorimplementation
import time
import random

nao = True

class searchball_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''This behavior will move the Nao around until the ball is seen in the middle of the FoV.'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):
        self.nao = self.body.nao(0)
        self.nao.say("Ick zook duh bahl")
        self.start_time = time.time()
        if nao: self.nao.set_cam_vars()
        # if nao: self.nao.start_behavior("standup")
        self.last_recogtime = time.time()
        self.looktime = time.time()
        if nao: self.nao.look_horizontal()
        # om zonder detectie de postconditie te bereiken wordt de balltime op groot gezet.
        self.balltime = time.time() + 1000
        self.state = "Init"


    def implementation_update(self):
        # Turn around in a certain direction unless you see the ball.
        # In that case, turn towards it until you have it fairly central in the Field of Vision.
        
        if self.state == "Init" and (time.time() - self.looktime) > 5:
            print "Looking down"
            self.looktime = time.time()
            self.nao.look_down()
            time.sleep(0.5)
            self.state = "down"
        
        if self.state == "down" and (time.time() - self.looktime) > 3:
            print "Looking up"
            self.looktime = time.time()
            self.nao.set_angles(['HeadPitch'], [-0.3], 0.2, radians=True)
            time.sleep(0.5)
            self.state = "up"
        
        if self.state == "up" and (time.time() - self.looktime) > 3:   
            print "Looking Left"
            self.looktime = time.time()
            self.nao.start_behavior("rag_look_left")
            time.sleep(0.5)
            self.state = "Left"
              
        if (self.state == "Left" or self.state == "Standing") and (time.time() - self.looktime) > 3:   
            print "Looking Right"
            self.looktime = time.time()
            self.nao.start_behavior("rag_look_right")
            time.sleep(0.5)
            self.state = "Right"
               
        if self.state == "Right" and (not nao or not self.nao.isMoving()) and (time.time() - self.looktime) > 5:      
            print "Moving clockwise"
            self.looktime = time.time()
            if nao: self.nao.walkNav(0,0,-1.2,0.10)
            time.sleep(0.5)
            self.state = "Standing"

        #Try to see if there is a ball in sight:
        if (self.m.n_occurs("combined_red") > 0):
            (recogtime, obs) = self.m.get_last_observation("combined_red")
            if not obs == None and recogtime > self.last_recogtime:
                detectionlist = obs['sorted_contours']
                blob_max = detectionlist[0]
                #print "red: x=%d, y=%d, size=%f" % (blob_max['x'], blob_max['y'], blob_max['surface'])
                self.last_recogtime = recogtime
                
                #Ball is found if the detected ball is big enough (thus filtering noise):
                if 1500 > blob_max['surface'] > 50:
                    self.balltime = time.time()
                    
                    #Ball was found while looking Right, Turning Right
                    if self.state == "Right" and (not nao or not self.nao.isMoving()):
                        print "We gaan naar Rechts draaien en dan fancy doen!"
                        self.nao.say("Ick gah nahr reghts")
                        self.balltime += 2
                        if nao: self.nao.walkNav(0,.1,-.46,0.10)
                    
                    #Ball was found while looking Left, Turning Left
                    elif self.state == "Left" and (not nao or not self.nao.isMoving()):
                        print "We gaan naar Links draaien en dan fancy doen!"
                        self.nao.say("Ick gah nahr links")
                        self.balltime += 2
                        if nao: self.nao.walkNav(0,-.1,.46,0.10)
                    
                    
                    
                    elif self.state == "down" and (not nao or not self.nao.isMoving()):
                        print "We gaan naar Achter lopen"
                        self.nao.say("Ick gah nahr ackter")
                        self.balltime += 3
                        if nao: self.nao.walkNav(-.20,0,0,0.10)
                        self.m.add_item('searchball',time.time(),{})
                    
                    elif self.state == "up" and (not nao or not self.nao.isMoving()):
                        print "We gaan naar Voren lopen"
                        self.nao.say("Ick gah nahr foohren")
                        self.balltime += 4
                        if nao: self.nao.walkNav(.40,0,0,0.10)
                    print "S: Ik zie de bal"
                    # Once the ball is properly found, use: self.m.add_item('ball_found',time.time(),{}) to finish this behavior.
                    
                    if (time.time() - self.balltime) >= 0:
                        self.m.add_item('searchball',time.time(),{})
