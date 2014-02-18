
import basebehavior.behaviorimplementation

import time

class Exampleblobdetector_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):
        print "Example BlobDetector Behavior Started!"
        self.nao = self.body.nao(0)
        self.start_time = time.time()
        self.nao.set_cam_vars()
        self.last_recogtime = time.time()
        self.looktime = time.time()
        self.seen_left = False
        self.state = "Init"
        self.balltime = time.time()
        self.nao.start_behavior("standup")
        

    def implementation_update(self):
        
        if (self.m.n_occurs("combined_red") > 0) and (time.time() - self.start_time) > 3:
            (recogtime, obs) = self.m.get_last_observation("combined_red")
            if not obs == None and recogtime > self.last_recogtime:
                detectionlist = obs['sorted_contours']
                blob_max = detectionlist[0]
                #print "red: x=%d, y=%d, size=%f" % (blob_max['x'], blob_max['y'], blob_max['surface'])
                self.last_recogtime = recogtime
                if 1500 > blob_max['surface'] > 1 and (time.time() - self.balltime) > 4:
                    self.balltime = time.time()
                    headstance =  self.nao.get_yaw_pitch()
                    bal = self.nao.ball_location(blob_max['x'],blob_max['y'],headstance[1],headstance[0])      
                    
                    print "X=",blob_max['x'],"Y=",blob_max['y'],"Pitch=",headstance[1],"Yaw=",headstance[0]
                    if bal[1]<0: print "de bal is", int(bal[0]), "cm ver", "\trechts", int(abs(bal[1]))
                    if bal[1]>0: print "de bal is", int(bal[0]), "cm ver", "\tlinks", int(abs(bal[1]))
                    print "Distance", int(bal[2]), "\tAngle", bal[3]
