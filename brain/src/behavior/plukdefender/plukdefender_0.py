

'''
this is an automatically generated template, if you don't rename it, it will be overwritten!
'''

import basebehavior.behaviorimplementation


class Plukdefender_x(basebehavior.behaviorimplementation.BehaviorImplementation):

    '''this is a behavior implementation template'''

    #this implementation should not define an __init__ !!!


    def implementation_init(self):

        self.nao = self.body.nao(0)
        self.nao.complete_behavior("standup")
        self.nao.zeg_dit("end_song.wav")
        self.nao.look_horizontal()

        self.nao.set_do_nothing_on_stop(True) # The Nao will still be enslaved

        self.selected_behaviors = []

        self.found = False

    def implementation_update(self):

        self.nao.complete_behavior("stretch")
        # test


