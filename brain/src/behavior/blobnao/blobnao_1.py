import basebehavior.behaviorimplementation
import visioncontroller.visioncontroller
import time

class BlobNao_1(basebehavior.behaviorimplementation.BehaviorImplementation):

    def implementation_init(self):
    	self.__last_ball_time = 0
    	self.__last_goal_1_time = 0
    	self.__last_goal_2_time = 0
        pass
        
    def implementation_update(self):
        if (self.m.n_occurs('Ball') > 0):
        	(recogtime, observation) = self.m.get_last_observation('Ball')
        	if (recogtime > self.__last_ball_time):
        		self.__last_ball_time = recogtime
        		print "BALLS"
        		print observation['blobs']

        if (self.m.n_occurs('Goal_1') > 0):
        	(recogtime, observation) = self.m.get_last_observation('Goal_1')
        	if (recogtime > self.__last_goal_1_time):
        		self.__last_ball_time = recogtime
        		print "Goal_1"
        		print observation['blobs']


        if (self.m.n_occurs('Goal_2') > 0):
        	(recogtime, observation) = self.m.get_last_observation('Goal_2')
        	if (recogtime > self.__last_goal_2_time):
        		self.__last_ball_time = recogtime
        		print "Goal_2"
        		print observation['blobs']




