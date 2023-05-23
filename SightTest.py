import time

from SessionModule import Session
from ScreenShowModule import ScreenShow
from threading import Thread
import numpy as np
import cv2

class SightTest:

    MAX_STAGE = 14

    def __init__(self):

        self.stage = 0
        self.inverse = False
        self.test_end = False
        self.reset_stage_record()

    def start(self):

        self.draw_prompt()
        session = Session()
        screenShow = ScreenShow(session=session)
        t_screenShow = Thread(target=screenShow.start)
        t_screenShow.start()

        while not self.test_end:
            session.update(self.stage)
            screenShow.notify_sign_update()
            session.start()
            result = session.result
            self.result_handler(result)
        
        session.handDetector.capture.release()
        screenShow.notify_test_end(self.stage)
        t_screenShow.join()

    def reset_stage_record(self):

        self.cnt_ac = 0
        self.cnt_wa = 0

    def result_handler(self, result: bool):

        self.cnt_ac += result
        self.cnt_wa += not result

        # 若在一阶段，正确一个进入nextstage，错误两个进入二阶段
        if not self.inverse:
            if self.cnt_ac == 1:
                self.stage += 1
                self.reset_stage_record()
            elif self.cnt_wa == 2:
                self.inverse = True
        
        # 若在二阶段，正确两个结束测试，错误两个进入laststage
        if self.inverse:
            if self.cnt_ac == 2:
                self.test_end = True
            elif self.cnt_wa == 2:
                self.stage -= 1
                self.reset_stage_record()
        
        if self.stage == -1 or self.stage == self.MAX_STAGE:
            self.test_end = True

    # 测试前提示
    def draw_prompt(self):
        from ScreenShowModule import putCenterText
        img = np.zeros((720, 1080, 3), np.uint8)
        # text = u"测试即将开始,请与屏幕保持一米距离"
        text = "Press any key to start"
        img = putCenterText(img, text, org=(1080 / 2, 720 / 2 - 50), color=(200, 200, 200),
                      fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=2, thickness=5)
        text = "Please keep 1 meter away from screen"
        img = putCenterText(img, text, org=(1080 / 2, 720 / 2 + 50), color=(200, 200, 200),
                            fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=1, thickness=2)

        cv2.imshow('prompt', img)
        cv2.waitKey(0)
        cv2.destroyWindow('prompt')