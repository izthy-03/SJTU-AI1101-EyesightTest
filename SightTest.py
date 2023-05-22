from SessionModule import Session
from ScreenShowModule import ScreenShow
from threading import Thread

class SightTest:

    def __init__(self):

        self.stage = 0
        self.inverse = False
        self.test_end = False
        self.reset_stage_record()

    def start(self):

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
        
        screenShow.notify_test_end(self.stage)

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
                self.stage += 1
                self.reset_stage_record()
