import time
import datetime
import basebehavior.behaviorimplementation

nao = True

class Ragnarok_x(basebehavior.behaviorimplementation.BehaviorImplementation):


    def implementation_init(self):

	    #define list of sub-behavior here
        self.nao = self.body.nao(0)     
        self.timer = time.time()
        self.searchball = self.ab.searchball({})
        self.approachball = self.ab.approachball({})
        self.approachlowball = self.ab.approachlowball({})
        self.aligngoal = self.ab.aligngoal({})
        self.alignball = self.ab.alignball({})
        self.schiet = self.ab.schiet({})
        self.string = ''
        
        # List of Timers
        self.searchballtime = float(0)
        self.approachballtime = float(0)
        self.approachlowballtime = float(0)
        self.aligngoaltime = float(0)
        self.alignballtime = float(0)
        self.schiettime = float(0)
        self.zandloper = time.time()

        self.nao.start_behavior("standup")
        self.nao.say("lahten wuh camp ee oon wor den")
        if nao: self.nao.set_cam_vars()
        
        self.selected_behaviors = [
            ("searchball","True"), \
            ("approachball","self.searchball.is_finished()"), \
            ("approachlowball","self.approachball.is_finished()"), \
            ("aligngoal","self.approachlowball.is_finished()"), \
            ("alignball","self.aligngoal.is_finished()"), \
            ("schiet","self.alignball.is_finished()")  \
        ]
        
        self.restart_time = time.time()

    def implementation_update(self):
        if self.schiet.is_finished():
            return

        if ((time.time()-self.restart_time)>5 and self.m.is_now('subsume_stopped', ['True'])):
            print "Lower level restarting @", datetime.datetime.fromtimestamp(self.timer)
            
            self.START = int(time.time())
            try:
                self.searchballtime = float(self.m.get_last_observation('searchball')[0])
                self.approachballtime = float(self.m.get_last_observation('approachball')[0])
                self.approachlowballtime = float(self.m.get_last_observation('approachlowball')[0])
                self.aligngoaltime = float(self.m.get_last_observation('aligngoal')[0])
                self.alignballtime = float(self.m.get_last_observation('alignball')[0])
                self.schiettime = float(self.m.get_last_observation('schiet')[0])
            except IndexError:
                pass
            except TypeError:
                pass

            self.string += 'START : \t' + str(datetime.datetime.fromtimestamp(self.zandloper).strftime('%Y-%m-%d  %H:%M:%S')) + "\n"
            if self.searchballtime != 0: self.string += 'Searchball:\t\t\t\t' + str(datetime.datetime.fromtimestamp(self.searchballtime).strftime('%H:%M:%S')) +  "\n"
            if self.approachballtime != 0: self.string += 'Approachball:\t\t\t' + str(datetime.datetime.fromtimestamp(self.approachballtime).strftime('%H:%M:%S')) + "\n"
            if self.approachlowballtime != 0: self.string += 'Approachlowball:\t\t' + str(datetime.datetime.fromtimestamp(self.approachlowballtime).strftime('%H:%M:%S')) + "\n"
            if self.aligngoaltime != 0: self.string += 'Aligngoal:\t\t\t\t' + str(datetime.datetime.fromtimestamp(self.aligngoaltime).strftime('%H:%M:%S')) + "\n"
            if self.alignballtime != 0: self.string += 'Alignball:\t\t\t\t' + str(datetime.datetime.fromtimestamp(self.alignballtime).strftime('%H:%M:%S')) +"\n"
            if self.schiettime != 0: self.string += 'Schiet:\t\t\t\t' + str(datetime.datetime.fromtimestamp(self.schiettime).strftime('%H:%M:%S')) + "\n" 
            if self.approachlowballtime != 0 : 
                self.string += "Tijd: " + str((self.aligngoaltime - self.approachlowballtime)) + "\n\n"
            else:
                self.string += "Tijd: N/a\n\n"  
            try:
                logfile = open("Timers.txt","a")
                try:
                    logfile.write(self.string)
                finally:
                    logfile.close()
            except IOError:
                pass

            self.restart_time = time.time()                
            self.searchball = self.ab.searchball({})
            self.approachball = self.ab.approachball({})
            self.approachlowball = self.ab.approachlowball({})
            self.aligngoal = self.ab.aligngoal({})
            self.alignball = self.ab.alignball({})
            self.schiet = self.ab.schiet({})
            return


