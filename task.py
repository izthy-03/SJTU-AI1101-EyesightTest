import cv2
import time
import numpy as np
import HandTrackingModule as htm
import random

class sight:
    # 定义测试阶段
    stage = 0
    MAX_STAGE = 10
    MAX_SIZE = 20
    MAX_STAGE_TIME = 10
    MAX_CONFIRM_TIME = 2

    def __init__(self):
        # 开启摄像头
        self.cap = cv2.VideoCapture(0)
        '''initialize detector'''
        self.detector = htm.handDetector()
        self.stage = 0
        self.inverse = False
        self.cont = True 

    def session_update(self):
        # 指向正确
        if self.dirc_sign == self.dirc_hand:
            self.cnt_ac += 1
        # 指向错误
        else:
            self.cnt_wa += 1
        
        # 若在一阶段，正确一个进入nextstage，错误两个进入二阶段
        if not self.inverse:
            if self.cnt_ac == 1:
                self.stage_update(1)
            elif self.cnt_wa == 2:
                self.inverse = True
        
        # 若在二阶段，正确两个结束测试，错误两个进入laststage
        if self.inverse:
            if self.cnt_ac == 2:
                self.cont = False
                print("test ends")
            elif self.cnt_wa == 2:
                self.stage_update(-1)
        
        self.session_refresh()
    
    def session_refresh(self):
        self.dirc_sign = random.randint(1, 4)       # 'E'朝向
        self.dirc_hand = None           # 手指方向
        self.time_confirm_end = None    # 方向确认完成时间戳
        self.time_stage_end = time.time() + self.MAX_STAGE_TIME  # stage完成时间戳
        self.sign_update()

    def stage_update(self, stage_change = 0):
        self.stage += stage_change
        self.cnt_wa = 0                 # 错误次数
        self.cnt_ac = 0                 # 正确次数

    def print_result(self):
        pass

    def sign_update(self):
        # 计算缩放比例
        scale = 1 / (1 + 0.1 * self.stage)
        # 读取，旋转，缩放
        self.img_sign = cv2.imread('sign.png')
        sign_w, sign_h, sign_c = self.img_sign.shape
        for i in range(self.dirc_sign - 1):
            self.img_sign = cv2.rotate(self.img_sign, 0)
        self.img_sign = cv2.resize(self.img_sign, (int(sign_w * scale), int(sign_h * scale)))

    def draw_sign(self):
        # 覆盖到屏幕
        screen_w, screen_h, screen_c = self.screen.shape
        sign_w, sign_h, sign_c = self.img_sign.shape
        self.screen[int((screen_w - sign_w) / 2) : int((screen_w + sign_w) / 2),
                    int((screen_h - sign_h) / 2) : int((screen_h + sign_h) / 2)] = self.img_sign

    def draw_stage_countdown(self):
        roundoff = int(self.time_stage_end - time.time())
        cv2.putText(self.screen, text=str(roundoff),
                    org = (int(self.screen.shape[0] / 2), int(self.screen.shape[1] / 2 - 20)),
                    fontFace = cv2.FONT_HERSHEY_PLAIN,
                    fontScale = 3, color=(0, 0, 0), thickness = 2)
        cv2.putText(self.screen, text=f'st = {self.stage}, ac = {self.cnt_ac}, wa = {self.cnt_wa}', 
                    org = (int(self.screen.shape[0] / 2), int(self.screen.shape[1] / 2 + 60)),
                    fontFace = cv2.FONT_HERSHEY_PLAIN,
                    fontScale = 3, color=(0, 0, 0), thickness = 2)

    def draw_confirm_countdown(self):
        cv2.putText(self.screen, text=str(self.time_confirm_end - time.time()), 
                    org = (int(self.screen.shape[0] / 2), int(self.screen.shape[1] / 2 + 20)),
                    fontFace = cv2.FONT_HERSHEY_PLAIN,
                    fontScale = 3, color=(0, 0, 0), thickness = 2)

    def begin_task(self):

        self.session_refresh()
        self.stage_update(0)

        while self.cont:
            # print(self.cont)
            # 读取图像
            ret, img = self.cap.read()

            # 识别手势
            # 传入 img-相机获取的一帧图像, 返回 dir-手的指向
            dirc_hand = self.detector.findDirection(img)

            # 创建空白屏幕
            # self.screen = np.zeros((720, 1080, 3), np.uint8) + 255
            self.screen = img

            # 在屏幕上绘制'E'字
            self.draw_sign()
            # 在屏幕上绘制倒计时
            self.draw_stage_countdown()

            # 如果有方向
            if dirc_hand:

                # 如果与记录不符（或者记录为零）
                if dirc_hand != self.dirc_hand:
                    # 重置记录
                    self.dirc_hand = dirc_hand
                    # 重置方向确认倒计时
                    self.time_confirm_end = time.time() + self.MAX_CONFIRM_TIME
                # 如果方向确认倒计时归零
                elif time.time() > self.time_confirm_end:
                    # 此轮结束，更新stage
                    self.session_update()
                else:
                    # 显示方向确认倒计时
                    self.draw_confirm_countdown()
                
            else:
                # 重置记录
                self.dirc_hand = None
            
            # 如果stage时间归零
            if time.time() > self.time_stage_end:
                # 此轮结束，更新stage
                self.session_update()
            
            cv2.imshow('screen', self.screen)

            k = cv2.waitKey(1)
            if k == 27:
                break
        
        cv2.destroyAllWindows()

        self.print_result()

