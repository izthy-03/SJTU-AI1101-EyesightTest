import cv2
import numpy
import math

class screenShow:

    def __init__(self):
        
        self.scn_w = 1080
        self.scn_h = 720
        self.center = (int(self.scn_w/2),int(self.scn_h/2))
        self.radius_outcut = int(math.hypot(self.scn_w/2, self.scn_h/2))
        self.radius_white = 200
        self.thinkness_session_countdown = 10

        self.color_while = (255,255,255)
        self.color_grey = (64,64,64)
        self.color_dark_grey = (32,32,32)
        self.color_red = (0,0,255)
        self.color_green = (0,255,0)

    def create(self, background = None):

        self.background = background

        # 创建空白屏
        self.screen = numpy.zeros((self.scn_h, self.scn_w, 3), numpy.uint8)
        self.screen = cv2.circle(img=self.screen, center=self.center, radius=self.radius_white, 
                                 color=self.color_while, thickness=-1)
        
    def show(self):
        return self.screen

    def draw_confirm_countdown(self, ratio, dirc_hand):
        # countdown = self.time_confirm_end - time.time()
        radius_dynamic = int(self.radius_white + (self.radius_outcut - self.radius_white) * ratio)
        self.screen = cv2.ellipse(img=self.screen, center=self.center, 
                                  axes=(self.radius_outcut, self.radius_outcut), 
                                  angle=dirc_hand*90-135, startAngle=0, endAngle=90, 
                                  color=self.color_dark_grey, thickness=-1)
        self.screen = cv2.ellipse(img=self.screen, center=self.center, 
                                  axes=(radius_dynamic, radius_dynamic), 
                                  angle=dirc_hand*90-135, startAngle=0, endAngle=90, 
                                  color=self.color_grey, thickness=-1)

    def draw_session_countdown(self, ratio):
        # countdown = self.time_stage_end - time.time() 360*countdown/self.MAX_STAGE_TIME
        radius = self.radius_white + self.thinkness_session_countdown
        self.screen = cv2.ellipse(img=self.screen, center=self.center, 
                                  axes=(radius,radius), 
                                  angle=-90, startAngle=0, endAngle=360*ratio, 
                                  color=self.color_red, thickness=-1)

    def draw_session_outcome(self, dirc_hand, isCorrect):
        self.screen = cv2.ellipse(img=self.screen, center=self.center, 
                                  axes=(self.radius_outcut, self.radius_outcut), 
                                  angle=dirc_hand*90-135, startAngle=0, endAngle=90, 
                                  color=self.color_green if isCorrect else self.color_red, thickness=-1)

    def update_sign(self, stage, dirc_sign):
        # 计算缩放比例
        scale = 1 / (1 + 0.1 * stage)
        # 读取
        self.img_sign = cv2.imread('sign.png')
        sign_w, sign_h, sign_c = self.img_sign.shape
        # 旋转
        for i in range(dirc_sign - 1):
            self.img_sign = cv2.rotate(self.img_sign, 0)
        # 缩放
        self.img_sign = cv2.resize(self.img_sign, (int(sign_w * scale), int(sign_h * scale)))

    def draw_sign(self):
        # 保留中心空白
        self.screen = cv2.circle(img=self.screen, center=self.center, 
                                 radius=self.radius_white, color=self.color_while, thickness=-1)
        # 覆盖到屏幕
        sign_w, sign_h, sign_c = self.img_sign.shape
        self.screen[int(self.center[1] - sign_h / 2) : int(self.center[1] + sign_h / 2),
                    int(self.center[0] - sign_w / 2) : int(self.center[0] + sign_w / 2)] = self.img_sign
