import cv2
import numpy
import math
import MonitorFitModule
import StandardVisualAcuitySheet as Sheet
from SessionModule import Session

class ScreenShow:

    FPS = 20

    def __init__(self, session: Session, sign_source = 'sign.png'):

        self.session = session
        self.flag_test_end = False

        self.sign_img_ori = cv2.imread(sign_source)
        self.sign_w, self.sign_h, self.sign_c = self.sign_img_ori.shape
        self.scn_w = 1080 # TODO
        self.scn_h = 720  # TODO
        self.center = (int(self.scn_w/2),int(self.scn_h/2))
        self.radius_outcut = int(math.hypot(self.scn_w/2, self.scn_h/2))
        self.radius_white = 200
        self.thinkness_session_countdown = 20

        self.color_while = (255,255,255)
        self.color_grey = (64,64,64)
        self.color_dark_grey = (32,32,32)
        self.color_red = (0,0,255)
        self.color_green = (0,255,0)

        # get monitor info and set scale
        self.monitor = MonitorFitModule.monitor()
        self.sheet = Sheet.standardSheet()
        self.sheet.set_ppm(self.monitor.get_ppm())
        self.sheet.set_distance(1)

    def start(self):

        while not self.flag_test_end:

            self.create()

            if self.session.timer_pause.is_alive():
                self.draw_session_result()
            elif self.session.timer_confirm.is_alive():
                self.draw_confirm_countdown()
            
            self.draw_session_countdown()
            self.draw_sign()

            cv2.imshow('screen', self.screen)
            k = cv2.waitKey(int(1000/self.FPS))
            if k == 27:
                break
        
        self.create()
        self.draw_test_result()
        cv2.imshow('screen', self.screen)
        while cv2.waitKey(1) != 27:
            pass

        cv2.destroyAllWindows()
    
    def notify_test_end(self):

        self.flag_test_end = True

    def notify_sign_update(self):
        
        stage = self.session.stage
        sign_dirc = self.session.sign_direction
        scale = self.sheet.get_stage_scale(stage)
        size = (int(self.sign_w * scale), int(self.sign_h * scale))
        
        # 旋转
        self.img_sign = self.sign_img_ori
        for i in range(sign_dirc - 1):
            self.img_sign = cv2.rotate(self.img_sign, 0)
        # 缩放
        self.img_sign = cv2.resize(self.img_sign, size)

    def create(self):

        self.screen = numpy.zeros((self.scn_h, self.scn_w, 3), numpy.uint8)

    def draw_confirm_countdown(self):
        hand_dirc = self.session.hand_direction
        if not hand_dirc:
            return
        ratio = self.session.timer_confirm.countdown() / self.session.INTERVAL_CONFIRM
        radius = int(self.radius_white + (self.radius_outcut - self.radius_white) * ratio)
        self.screen = cv2.ellipse(img=self.screen, center=self.center, 
                                  axes=(self.radius_outcut, self.radius_outcut), 
                                  angle=hand_dirc*90-135, startAngle=0, endAngle=90, 
                                  color=self.color_dark_grey, thickness=-1)
        self.screen = cv2.ellipse(img=self.screen, center=self.center, 
                                  axes=(radius, radius), 
                                  angle=hand_dirc*90-135, startAngle=0, endAngle=90, 
                                  color=self.color_grey, thickness=-1)

    def draw_session_countdown(self):
        
        ratio = self.session.timer_session.countdown() / self.session.INTERVAL_SESSION
        radius = self.radius_white + self.thinkness_session_countdown
        self.screen = cv2.ellipse(img=self.screen, center=self.center, 
                                  axes=(radius,radius), 
                                  angle=-90, startAngle=0, endAngle=max(0,360*ratio), 
                                  color=self.color_red, thickness=-1)

    def draw_session_result(self):
        sign_dirc = self.session.sign_direction
        result = self.session.result
        self.screen = cv2.ellipse(img=self.screen, center=self.center, 
                                  axes=(self.radius_outcut, self.radius_outcut), 
                                  angle=sign_dirc*90-135, startAngle=0, endAngle=90, 
                                  color=self.color_green if result else self.color_red, thickness=-1)

    def draw_sign(self):
        # 保留中心空白
        self.screen = cv2.circle(img=self.screen, center=self.center, 
                                 radius=self.radius_white, color=self.color_while, thickness=-1)
        # 覆盖到屏幕
        sign_w, sign_h, sign_c = self.img_sign.shape
        self.screen[int(self.center[1] - sign_h / 2) : int(self.center[1] + sign_h / 2),
                      int(self.center[0] - sign_w / 2) : int(self.center[0] + sign_w / 2)] = self.img_sign

    def draw_test_result(self):
        pass
