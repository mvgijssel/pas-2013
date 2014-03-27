import basebehavior.behaviorimplementation
import time

from util.custom_nao_classes import NaoSettings

class SillyWalkers_0(basebehavior.behaviorimplementation.BehaviorImplementation):

    # TODO: implement a behaviour which stands up when the nao falls down

    def implementation_init(self):

        # get the nao reference
        self.nao = self.body.nao(0)

        # get the ball object
        self.ball = NaoSettings.BALL_OBJECT

        # when the nao is done, don't do anything. Don't sit down
        self.nao.set_do_nothing_on_stop(True)

        # set the camera parameters
        self.nao.setup_camera_parameters()

        # set the head stiffness
        self.nao.get_proxy("motion").setStiffnesses("Head", 1.0)

        # TODO: is a hack, should be an external behaviour which stands up when nao isn't standing
        self.nao.complete_behavior("standup")

        # instantiate the behaviours, acts as a reset
        #define list of sub-behavior here
        self.naocalibration = self.ab.naocalibration({'debug': False})
        self.objectdetector = self.ab.objectdetector({'debug': False})
        self.findball = self.ab.findball({'debug': False, 'info': True})
        self.headfollowball = self.ab.headfollowball({'debug': True})
        self.approachball = self.ab.approachball({'debug': True})

        self.selected_behaviors = [
            ("naocalibration", "True"),
            ("objectdetector", "True"),
            ("findball", "True"),
            ("headfollowball", "True"),
            ("approachball", "True")
        ]

        self.restart_time = time.time()


    def implementation_update(self):

        # when first image is received, set the selected behaviours

        pass

    def instantiate_behaviours(self):

        # set the debug flag
        self.debug = True

        # NEED BEHAVIOUR FOR STANDING BACK UP

        # DO WE NEED TO MANUALLY STOP THE RUNNING BEHAVIOURS STILL RUNNING?

