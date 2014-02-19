import cv2
import util.naovideo as naovid
import numpy as np
import sys
import socket

class HSVRangeFinder():

    def __init__(self):
        # Get Nao IP
        self.nao_ip = ""
        if len(sys.argv) <= 1:
            while True:
                try:
                    self.nao_ip = raw_input("You didn't specify the IP of the NAO, please specify it here:")
                    socket.inet_aton(str(self.nao_ip))
                    break
                except socket.error:
                    print("Not a valid IP address")
        else:
            self.nao_ip = sys.argv[1]
    
        # Get Nao video source
        self.vidsource = naovid.VideoModule(IP=self.nao_ip, resolution="160x120", output="160x120", camera=0, port=9559)
        
        # Create windows
        cv2.namedWindow('Nao video', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Thresholded image', cv2.WINDOW_NORMAL)
        cv2.namedWindow('Parameters', cv2.WINDOW_NORMAL)
        
        # Set mouse callback
        cv2.setMouseCallback('Nao video', self.mouseCallback)

        # create trackbars for color change
        cv2.createTrackbar('H - Lower bound', 'Parameters', 0, 255, self.parameterChangeHLower)
        cv2.createTrackbar('H - Upper bound', 'Parameters', 0, 255, self.parameterChangeHUpper)
        cv2.createTrackbar('S - Lower bound', 'Parameters', 0, 255, self.parameterChangeSLower)
        cv2.createTrackbar('S - Upper bound', 'Parameters', 0, 255, self.parameterChangeSUpper)
        cv2.createTrackbar('V - Lower bound', 'Parameters', 0, 255, self.parameterChangeVLower)
        cv2.createTrackbar('V - Upper bound', 'Parameters', 0, 255, self.parameterChangeVUpper)
        
        # Move windows to appropriate position
        cv2.moveWindow('Nao video', 0, 50)
        cv2.moveWindow('Thresholded image', 322, 50)
        cv2.moveWindow('Parameters', 644, 50)
        
        # Set initial parameters
        self.cnt = 0
        self.current_image = np.array([])
        self.lower_bound = np.array([0, 0, 0])
        self.upper_bound = np.array([255, 255, 255])
        self.prev_lower_bound = []
        self.prev_upper_bound = []
        self.range = 10
        self.cut_side = 0
        
        # Set initial trackbar pos
        self.updateSliders()
        
    # Changing parameters
    def parameterChangeHLower(self, value):
        self.lower_bound[0] = value
    
    def parameterChangeHUpper(self, value):
        self.upper_bound[0] = value
        
    def parameterChangeSLower(self, value):
        self.lower_bound[1] = value
        
    def parameterChangeSUpper(self, value):
        self.upper_bound[1] = value
        
    def parameterChangeVLower(self, value):
        self.lower_bound[2] = value
        
    def parameterChangeVUpper(self, value):
        self.upper_bound[2] = value     
        
    # Threshold image
    def thresholdImage(self, img):
        # Convert to HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        
        # Create mask and apply it
        mask = cv2.inRange(hsv, self.lower_bound, self.upper_bound)
        res = cv2.bitwise_and(img, img, mask=mask)
        
        return res
        
    # Check key
    def checkKeyPress(self, k):
        if k == 113:
            # Pressed: Q - H lower bound down
            self.lower_bound[0] = max(self.lower_bound[0] - 1, 0)
            cv2.setTrackbarPos('H - Lower bound', 'Parameters', self.lower_bound[0])
        elif k == 119:
            # Pressed: W - H lower bound up
            self.lower_bound[0] = min(self.lower_bound[0] + 1, 255)
            cv2.setTrackbarPos('H - Lower bound', 'Parameters', self.lower_bound[0])
        elif k == 101:
            # Pressed: E - H upper bound down
            self.upper_bound[0] = max(self.upper_bound[0] - 1, 0)
            cv2.setTrackbarPos('H - Upper bound', 'Parameters', self.upper_bound[0])
        elif k == 114:
            # Pressed: R - H upper bound up
            self.upper_bound[0] = min(self.upper_bound[0] + 1, 255)
            cv2.setTrackbarPos('H - Upper bound', 'Parameters', self.upper_bound[0])
        elif k == 97:
            # Pressed: A - S lower bound down
            self.lower_bound[1] = max(self.lower_bound[1] - 1, 0)
            cv2.setTrackbarPos('S - Lower bound', 'Parameters', self.lower_bound[1])
        elif k == 115:
            # Pressed: S - S lower bound up
            self.lower_bound[1] = min(self.lower_bound[1] + 1, 255)
            cv2.setTrackbarPos('S - Lower bound', 'Parameters', self.lower_bound[1])
        elif k == 100:
            # Pressed: D - S upper bound down
            self.upper_bound[1] = max(self.upper_bound[1] - 1, 0)
            cv2.setTrackbarPos('S - Upper bound', 'Parameters', self.upper_bound[1])
        elif k == 102:
            # Pressed: F - S upper bound up
            self.upper_bound[1] = min(self.upper_bound[1] + 1, 255)
            cv2.setTrackbarPos('S - Upper bound', 'Parameters', self.upper_bound[1])
        elif k == 122:
            # Pressed: Z - V lower bound down
            self.lower_bound[2] = max(self.lower_bound[2] - 1, 0)
            cv2.setTrackbarPos('V - Lower bound', 'Parameters', self.lower_bound[2])
        elif k == 120:
            # Pressed: X - V lower bound up
            self.lower_bound[2] = min(self.lower_bound[2] + 1, 255)
            cv2.setTrackbarPos('V - Lower bound', 'Parameters', self.lower_bound[2])
        elif k == 99:
            # Pressed: C - V upper bound down
            self.upper_bound[2] = max(self.upper_bound[2] - 1, 0)
            cv2.setTrackbarPos('V - Upper bound', 'Parameters', self.upper_bound[2])
        elif k == 118:
            # Pressed: V - V upper bound up
            self.upper_bound[2] = min(self.upper_bound[2] + 1, 255)
            cv2.setTrackbarPos('V - Upper bound', 'Parameters', self.upper_bound[2])
        elif k == 65288 and len(self.prev_lower_bound) > 0:
            # Pressed: Backspace
            self.lower_bound = np.copy(self.prev_lower_bound)
            self.upper_bound = np.copy(self.prev_upper_bound)
            self.updateSliders()
    
    def mouseCallback(self, event, x, y, flags, params):
        # Get pixel value
        rgb = np.array([[self.current_image[y, x]]])
        
        # Convert to HSV
        hsv = cv2.cvtColor(rgb, cv2.COLOR_BGR2HSV)
        
        # Add range
        if flags & cv2.EVENT_FLAG_LBUTTON:
            self.addRange(hsv[0, 0])
        # Delete range
        elif flags & cv2.EVENT_FLAG_RBUTTON:
            self.delRange(hsv[0, 0])
        
    def addRange(self, hsv):
        # Add
        print "Add: " + str(hsv)
        self.prev_lower_bound = np.copy(self.lower_bound)
        self.prev_upper_bound = np.copy(self.upper_bound)
        self.lower_bound[0] = max(min(hsv[0] - self.range, self.lower_bound[0]), 0)
        self.upper_bound[0] = min(max(hsv[0] + self.range, self.upper_bound[0]), 255)
        self.lower_bound[1] = max(min(hsv[1] - self.range, self.lower_bound[1]), 0)
        self.upper_bound[1] = min(max(hsv[1] + self.range, self.upper_bound[1]), 255)
        self.lower_bound[2] = max(min(hsv[2] - self.range, self.lower_bound[2]), 0)
        self.upper_bound[2] = min(max(hsv[2] + self.range, self.upper_bound[2]), 255)
        self.updateSliders()
        
    def delRange(self, hsv):
        # Del (doesn't always work as expected (sorry)
        print "Delete: " + str(hsv)
        self.prev_lower_bound = np.copy(self.lower_bound)
        self.prev_upper_bound = np.copy(self.upper_bound)
        if not ((hsv[0] - self.range) > self.upper_bound[0] or (hsv[0] + self.range) < self.lower_bound[0]):
            temp_upper = self.upper_bound[0]
            if (hsv[0] - self.range) > self.lower_bound[0] and (hsv[0] + self.range) < temp_upper:
                if self.cut_side == 0:  # I know, fugly has hell
                    self.lower_bound[0] = hsv[0] + self.range
                else:
                    self.upper_bound[0] = hsv[0] - self.range
            else:
                if (hsv[0] - self.range) > self.lower_bound[0]:
                    self.upper_bound[0] = hsv[0] - self.range
                if (hsv[0] + self.range) < temp_upper:
                    self.lower_bound[0] = hsv[0] + self.range
        if not ((hsv[1] - self.range) > self.upper_bound[1] or (hsv[1] + self.range) < self.lower_bound[1]):
            temp_upper = self.upper_bound[1]
            if (hsv[1] - self.range) > self.lower_bound[1] and (hsv[1] + self.range) < temp_upper:
                if self.cut_side == 0:
                    self.lower_bound[1] = hsv[1] + self.range
                else:
                    self.upper_bound[1] = hsv[1] - self.range
            else:
                if (hsv[1] - self.range) > self.lower_bound[1]:
                    self.upper_bound[1] = hsv[1] - self.range
                if (hsv[1] + self.range) < temp_upper:
                    self.lower_bound[1] = hsv[1] + self.range
        if not ((hsv[2] - self.range) > self.upper_bound[2] or (hsv[2] + self.range) < self.lower_bound[2]):
            temp_upper = self.upper_bound[2]
            if (hsv[2] - self.range) > self.lower_bound[2] and (hsv[2] + self.range) < temp_upper:
                if self.cut_side == 0:
                    self.lower_bound[2] = hsv[2] + self.range
                else:
                    self.upper_bound[2] = hsv[2] - self.range
            else:
                if (hsv[2] - self.range) > self.lower_bound[2]:
                    self.upper_bound[2] = hsv[2] - self.range
                if (hsv[2] + self.range) < temp_upper:
                    self.lower_bound[2] = hsv[2] + self.range
        if self.cut_side == 0:
            self.cut_side = 1
        else:
            self.cut_side = 0
        self.updateSliders()
        
    def updateSliders(self):
        cv2.setTrackbarPos('H - Lower bound', 'Parameters', self.lower_bound[0])
        cv2.setTrackbarPos('H - Upper bound', 'Parameters', self.upper_bound[0])
        cv2.setTrackbarPos('S - Lower bound', 'Parameters', self.lower_bound[1])
        cv2.setTrackbarPos('S - Upper bound', 'Parameters', self.upper_bound[1])
        cv2.setTrackbarPos('V - Lower bound', 'Parameters', self.lower_bound[2])
        cv2.setTrackbarPos('V - Upper bound', 'Parameters', self.upper_bound[2])
    
    def update(self):
        # Get latest image from Nao
        iplimage = self.vidsource.get_image()
        
        # Convert IPLImage to NParray
        self.current_image = np.asarray(iplimage[:,:])
        
        # Show windows
        cv2.imshow('Nao video', self.current_image)
        cv2.imshow('Thresholded image', self.thresholdImage(self.current_image))
        
        # Wait until key is pressed or update
        k = cv2.waitKey(300)
        if k == 0x1b:
            print "Escape was pressed. Quitting ..."
            return False
        else:
            self.checkKeyPress(k)
        print "Got image " + str(self.cnt)
        self.cnt = self.cnt + 1
        return True
    

if __name__ == "__main__":
    finder = HSVRangeFinder()
    while True:
        if not finder.update():
            break
        
