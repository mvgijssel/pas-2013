import basebehavior.behaviorimplementation


class Aligntorso_0(basebehavior.behaviorimplementation.BehaviorImplementation):


    def implementation_init(self):

        if self.debug:
            print "Aligning torso!"

        # store the nao reference
        self.nao = self.body.nao(0)

        # get the angles of the head
        (head_yaw, head_pitch) = self.get_angles()

        # head_yaw is x
        # turn the torso of the nao to the head_yaw angle
        self.nao.walk(0, 0, head_yaw)

        # turn only the x of the head

        # ALMotionProxy::setAngles(const AL::ALValue& names, const AL::ALValue& angles, const float& fractionMaxSpeed)
        #  ALMotionProxy::angleInterpolation(names, angleLists, const AL::ALValue& timeLists, const bool& isAbsolute)
        motion = self.nao.get_proxy('motion')

        # use absolute angles, needs to look ahead
        # also blocking operation
        motion.angleInterpolation("HeadYaw", 0, 1.0, True)

        # adjusting the 'x' coordinate
        #self.nao.set_angles('HeadYaw', position.x * almath.TO_RAD, self.x_speed, radians=True)
        #self.nao.set_angles('HeadYaw', position.x * almath.TO_RAD, self.x_speed, radians=True)

        # the behaviour is done
        self.set_finished()

    def implementation_update(self):

        pass

        # get the current angles of the nao
    def get_angles(self):

        # get the angles
         return self.nao.get_angles_sensors(['HeadYaw', 'HeadPitch'], radians=True)



