import cv2
import time

class sight:
    # 定义测试阶段
    stage = 0
    MAXSTAGE = 10
    MAXSIZE = 20
    MAXTIME = 5

    def __init__(self):
        # 开启摄像头
        self.cap = cv2.VideoCapture(0)


    def update_stage(self, stg):
        self.err_cnt = 0               # 错误次数
        self.size = self.MAXSIZE            # 当前大小
        self.E_dir = rand()            # 当前'E'朝向
        self.countdown = self.MAXTIME       # 倒计时
        self.time_stamp = time.time()  # 开始时间戳
        pass

    def print_result(self):
        pass

    def rec_hands(self, img):
        pass

    def draw_E(self, img):
        pass

    def draw_second(self, img):
        pass

    def begin_task(self):
        self.update_stage()
        while True:
            # 读取图像
            ret, img = self.cap.read()

            # 识别手势
            # 传入 img-相机获取的一帧图像, 返回 dir-手的指向, img-重绘的图像
            hand_dir, img = self.rec_hands(img)

            # 在图像上绘制'E'字
            # 传入 img-图像, size-字号, 返回 img-重绘的图像
            img = self.draw_E(img, self.size)

            # 在图像上绘制倒计时
            # 传入 img-图像, countdown-当前测试阶段剩余时间 , 返回 img-重绘的图像
            img = self.draw_second(img, self.countdown)

            # 更新测试倒计时
            self.countdown = self.MAXTIME - (time.time() - self.time_stamp)  # 待修改
            # 指向正确，进入下一阶段
            if self.E_dir == hand_dir:
                self.stage = self.stage + 1
            # 时间到
            if self.countdown <= 0:
                self.err_cnt = self.err_cnt + 1
            # 更新测试状态
            self.update_stage()

            # 判断结束
            if self.stage > self.MAXSTAGE or self.err_cnt > 2:
                break

        self.print_result()
