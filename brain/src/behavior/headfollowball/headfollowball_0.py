import basebehavior.behaviorimplementation
from util.nao_settings import NaoSettings


class HeadFollowBall_x(basebehavior.behaviorimplementation.BehaviorImplementation):


    def implementation_init(self):

        #define list of sub-behavior here

        # store the ball reference
        self.ball = NaoSettings.BALL_OBJECT

        # store the nao reference
        self.nao = self.body.nao(0)

        # get the motion proxy
        # motion = self.nao.get_proxy('motion')

        # also blocking operation
        # adjust the x, the headyaw
        #
        #motion.angleInterpolation("HeadYaw", 0, 1.0, True)

        # adjust the y, the headpitch
        # motion.angleInterpolation("HeadPitch", 0, 1.0, True)


    def implementation_update(self):

        # calibrate the settings using the current framerate
        self.calibrate_settings()

        # try to get the ball
        (recogtime, observation) = self.m.get_last_observation(self.ball.name)

        # if ball is found
        if observation['is_found']:



            if self.debug:
                print "Centering the ball"


        else:

            if self.debug:
                print "Lost the ball!"

    def calibrate_settings(self):

        pass