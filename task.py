import cv2
import time
import numpy as np
import HandTrackingModule as htm
import ScreenShowModule as ssm
import random

class sight:
    # 定义测试阶段
    MAX_STAGE = 10
    MAX_SIZE = 20
    MAX_SESSION_TIME = 8
    MAX_CONFIRM_TIME = 2

    def __init__(self):
        self.stage = 0
        self.inverse = False
        self.cont = True
        self.screenShow = ssm.screenShow()

    def session_update(self):
        isCorrect = (self.dirc_sign == self.dirc_hand)
        self.cnt_ac += isCorrect
        self.cnt_wa += not isCorrect

        self.screenShow.create()
        self.screenShow.draw_session_outcome(dirc_hand=self.dirc_sign, isCorrect=isCorrect)
        ratio_session_remain = (self.time_session_end-time.time())/self.MAX_SESSION_TIME
        self.screenShow.draw_session_countdown(ratio=ratio_session_remain)
        self.screenShow.draw_sign()
        cv2.imshow('screen', self.screenShow.show())
        cv2.waitKey(1000)
        
        self.stage_update()
        self.session_refresh()
    
    def stage_update(self):
        # 若在一阶段，正确一个进入nextstage，错误两个进入二阶段
        if not self.inverse:
            if self.cnt_ac == 1:
                self.stage += 1
                self.cnt_ac = self.cnt_wa = 0
            elif self.cnt_wa == 2:
                self.inverse = True
        
        # 若在二阶段，正确两个结束测试，错误两个进入laststage
        if self.inverse:
            if self.cnt_ac == 2:
                self.cont = False
            elif self.cnt_wa == 2:
                self.stage += 1
                self.cnt_ac = self.cnt_wa = 0
    
    def session_refresh(self):
        self.dirc_sign = random.randint(1, 4)                       # 'E'朝向
        self.dirc_hand = None                                       # 手指方向
        self.time_session_end = time.time() + self.MAX_SESSION_TIME   # stage完成时间戳
        self.screenShow.update_sign(stage=self.stage, dirc_sign=self.dirc_sign)

    def print_result(self):
        pass

    def begin_task(self):

        cap = cv2.VideoCapture(0)
        handDetector = htm.handDetector()

        self.session_refresh()
        self.cnt_ac = 0
        self.cnt_wa = 0

        while self.cont:
            # print(self.cont)
            # 读取图像
            time_now = time.time()
            ret, img = cap.read()
            self.screenShow.create(background=img)
            
            # 识别手势
            # 传入 img-相机获取的一帧图像, 返回 dir-手的指向
            dirc_hand = handDetector.findDirection(img)

            # 如果有方向
            if dirc_hand:

                # 如果与记录不符（或者记录为零）
                if dirc_hand != self.dirc_hand:
                    # 重置记录
                    self.dirc_hand = dirc_hand
                    # 重置方向确认倒计时
                    time_confirm_end = time_now + self.MAX_CONFIRM_TIME
                # 如果方向确认倒计时归零
                elif time_now > time_confirm_end:
                    # 此轮结束，更新session
                    self.session_update()
                else:
                    # 显示方向确认倒计时
                    ratio_confirm_remain = (time_confirm_end-time_now)/self.MAX_CONFIRM_TIME
                    self.screenShow.draw_confirm_countdown(ratio=ratio_confirm_remain, dirc_hand=dirc_hand)
                
            else:
                # 重置记录
                self.dirc_hand = None
            
            # 如果session时间归零
            if time_now > self.time_session_end:
                # 此轮结束，更新session
                self.session_update()
            
            # 在屏幕上绘制倒计时
            ratio_session_remain = (self.time_session_end-time_now)/self.MAX_SESSION_TIME
            self.screenShow.draw_session_countdown(ratio=ratio_session_remain)

            # 在屏幕上绘制'E'字
            self.screenShow.draw_sign()

            cv2.imshow('screen', self.screenShow.show())

            k = cv2.waitKey(1)
            if k == 27:
                break
        
        cv2.destroyAllWindows()

        self.print_result()
