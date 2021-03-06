import itertools
import numpy
import logging
import util.nullhandler
import datetime
import pickle
import os
import shutil
logging.getLogger('Borg.Brain.Vision.hog.Matrix').addHandler(util.nullhandler.NullHandler())

class Matrix(object):
    '''
    In this class the clustered data , its labels and the action file is processed.
    The output is a transition probability matrix
    '''
    def __init__(self, path, rootPath = "" ,visualize = False, date=""):
        self.logger = logging.getLogger("Borg.Brain.Vision.hog.HoG")
        self.visualize = visualize
        self.path = os.path.join(path, "")
        if date == "":
            self.data = str(datetime.date.today())
        else:
            self.date = date
        if rootPath == "":
            self.rootPath = path
        else:
            self.rootPath = rootPath

        #Shall I take into account selfstate connection? If yes make it TRUE
        self.selfstate = True
        
    def calculate_tp_matrix(self, transitions, statenumber):
        
        tp_matrix = numpy.zeros((statenumber,statenumber,7),dtype=float)
        print "Number of actions, ", len(transitions)
        for i in range(len(transitions)- 1):
            startStateIndex = transitions[i][1] - 1
            endStateIndex = transitions[i+1][1] -1 
            
            if not self.selfstate:
                if startStateIndex == endStateIndex:
                    continue
            if transitions[i][0] == "move":
                tp_matrix[startStateIndex,endStateIndex,0] += 1
            elif transitions[i][0] == "left":
                tp_matrix[startStateIndex,endStateIndex,1] += 1
            elif transitions[i][0] == "right":
                tp_matrix[startStateIndex,endStateIndex,2] += 1
            elif transitions[i][0] == "obstacle":
                tp_matrix[startStateIndex,endStateIndex,3] += 1
            elif transitions[i][0] == "mmove":
                print "manual order move"
                tp_matrix[startStateIndex,endStateIndex,4] += 1
            elif transitions[i][0] == "mleft":
                print "manual order left"
                tp_matrix[startStateIndex,endStateIndex,5] += 1
            elif transitions[i][0] == "mright":
                print "manual order right"
                tp_matrix[startStateIndex,endStateIndex,6] += 1
                
            #tp_matrix[startStateIndex,endStateIndex,4] += 1

        
        sum0 = numpy.sum(tp_matrix[:,:,0], axis=1)
        tim = 0
        for x in range(215):
            tim += tp_matrix[1, x, 0]
        
        print "temp is: ", tim;
        print "sum0[1], ", sum0[1]
            
        sum1 = numpy.sum(tp_matrix[:,:,1], axis=1)
        sum2 = numpy.sum(tp_matrix[:,:,2], axis=1)
        sum3 = numpy.sum(tp_matrix[:,:,3], axis=1)
        
        sum4 = numpy.sum(tp_matrix[:,:,4], axis=1)
        sum5 = numpy.sum(tp_matrix[:,:,5], axis=1)
        sum6 = numpy.sum(tp_matrix[:,:,6], axis=1)

        
        temp = numpy.zeros_like(tp_matrix)
        for x in range(sum0.shape[0]):
            
            '''print "state is:", x, "action is : move \n"
            print tp_matrix[x,:,0],sum0[x]
            
            print "state is:", x, "action is : left \n"
            print tp_matrix[x,:,1],sum1[x]
            
            print "state is:", x, "action is : right \n"
            print tp_matrix[x,:,2],sum2[x]
            
            print "state is:", x, "action is : obstacle \n"
            print tp_matrix[x,:,3],sum3[x]'''
            
            temp[x,:,0] = numpy.divide(tp_matrix[x,:,0],sum0[x])
            temp[x,:,1] = numpy.divide(tp_matrix[x,:,1],sum1[x])
            temp[x,:,2] = numpy.divide(tp_matrix[x,:,2],sum2[x])
            temp[x,:,3] = numpy.divide(tp_matrix[x,:,3],sum3[x])
            temp[x,:,4] = numpy.divide(tp_matrix[x,:,4],sum4[x])
            temp[x,:,5] = numpy.divide(tp_matrix[x,:,5],sum5[x])
            temp[x,:,6] = numpy.divide(tp_matrix[x,:,6],sum6[x])
            
            
         

        
        whereAreNaNs = numpy.isnan(temp);
        print "number of nans, ", whereAreNaNs.shape
        temp[whereAreNaNs] = 0;
        #numpy.savetxt(self.path + 'tp_matrix.txt', tp_matrix, fmt='%.18e', delimiter=' ', newline='\n', header='', footer='', comments='# ')
        numpy.save(self.path + 'tp_matrix', temp)
        
        print "Final temp nonzero elements"
        return temp
        
    def observation_to_state(self, actions, matlab ):
        result = []
        statenumber = 0 
        matlab = sorted(matlab, key=lambda data: data[0])

        #Matches actions with statenumbers instead of filenames. 
        start = 0 
        for action in actions:
            for data in itertools.islice(matlab , start, len(matlab)):
                if action[1] == data[0]:
                    result.append((action[0], data[1]))
                    if data[1] > statenumber:
                        statenumber = data[1]
                    start += 1
                    break
                start += 1
                
        return result, statenumber
    
    def obsToStateTriple(self, actions, matlab ):
        '''
        Transforms action, obs1, obs2 tuple to action, state1,state2
        '''
        temp = []
        result = []
        
        statenumber = 0 
        matlab = sorted(matlab, key=lambda data: data[0])

        #Matches actions with statenumbers instead of filenames. 
        start = 0 
        for action in actions:
            for data in itertools.islice(matlab , start, len(matlab)):
                if action[1] == data[0]:
                    temp.append(action[0], data[1], action[2])
                    if data[1] > statenumber:
                        statenumber = data[1]
                    start += 1
                    break
                start += 1
                
        for action in temp:
            for data in itertools.islice(matlab , start, len(matlab)):
                if action[2] == data[0]:
                    result.append(action[0], action[1], data[1])
                    start += 1
                    break
                start += 1
                
        return actions, statenumber
    
    def loadActions(self, path = ""):
        if not path:
            path =  os.path.join(self.path , self.date + '.sa')
        
            
        result = []
        with open(path, 'r') as f:
            try:
                while True:
                    temp = pickle.load(f)
                    if isinstance(temp, tuple):
                        action, observation = pickle.load(f)
                        result.append((action, observation))
                    else:
                        for action, observation in temp:
                            result.append((action, observation))
            except:
                pass
        
        return result
    
    def loadTripleActions(self, path = ""):
        if not path:
            path =  os.path.join(self.path , self.date + '.sa')
        
            
        result = []
        with open(path, 'r') as f:
            try:
                while True:
                    temp = pickle.load(f)
                    if isinstance(temp, tuple):
                        action, observation1, observation2 = pickle.load(f)
                        result.append((action, observation1, observation2))
                    else:
                        for action, observation1, observation2 in temp:
                            result.append((action, observation1, observation2))
            except:
                pass
        
        return result
               
    def load_data_matlab(self, loadFromMatlab=True, mode = "pic"):
        path = os.path.join(self.path , 'matlab.txt')   
        filenames, labels = numpy.loadtxt(path, dtype = 'float', delimiter=',', unpack = True)
        
        X = filenames.shape
        result = []
        for i in range(X[0]):
            filename = "%10.2f" % filenames[i]   
            result.append((str(filename) + '.png' ,labels[i]))
        
        if mode == "pic":

            y = range(int(result[-1][1]))   
            i = 0
            try:
                shutil.rmtree(os.path.join(self.path,'../clusters'))
            except:
                pass
            try:
                os.mkdir(os.path.join(self.path , '../clusters'))
            except:
                pass
            for x in range(X[0]):
                
                newpath = os.path.join(self.path, '../clusters/' + str(int(result[x][1])))
                try:
                    os.mkdir(newpath)
                except:
                    pass
                
                command = "cp -l " + self.path + result[x][0] + " "+ newpath 
                os.system(command)
                try:
                    if result[x+1][1] != result[x][1]:
                        i += 1
                except:
                    pass
        elif mode == "hist":                
            try:
                shutil.rmtree(os.path.join(self.path,'../clusters'))
            except:
                pass
            try:
                os.mkdir(os.path.join(self.path , '../clusters'))
            except:
                pass
            for x in range(X[0]):
                
                newpath = os.path.join(self.path, '../clusters/' + str(int(result[x][1])))
                try:
                    os.mkdir(newpath)
                except:
                    pass
                
                command = "cp -l " + os.path.join(self.rootPath, result[x][0]) + " "+ newpath 
                os.system(command)
                try:
                    if result[x+1][1] != result[x][1]:
                        i += 1
                except:
                    pass
        return result
        
    
if __name__ == "__main__":
#path = ('/data/scratch/Shantia/MainCluster/2011-11-16sen/')
    path = ('/data/scratch/experiments/dataw')
    rootPath = ('/data/scratch/experiments/dataw')
    #path = os.path.abspath(os.environ['BORG'] + '/Brain/data/hog_test/data/2011-11-16') + '/'
    #path = "/home/borg/Robocup/data/20-01-2012/"
    #path = "/home/borg/Robocup/data/2012-02-01/"
    matrix = Matrix(path, rootPath, date="actions")
    #result = main.extractor(5, 5)    
    print "Loading Matlab data and copying files to respected cluster folders"
    data = matrix.load_data_matlab(mode="none")
    print "Loading Actions"

    actions = matrix.loadActions(os.path.join(matrix.path, 'actions.sa'))
    print "Extracting "
    transitions, statenumber = matrix.observation_to_state(actions, data)
    result = matrix.calculate_tp_matrix(transitions, statenumber)
    print "Finished"
