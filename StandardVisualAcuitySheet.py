import numpy as np
import cv2

class standardSheet:
    def __init__(self):
        # 单位: mm
        self.base = 7.27
        self.ratio = [14, 12, 11, 10, 9, 8.5, 7.5, 6.6, 6, 5, 4, 3, 2, 1.5, 1]
        self.real_size = list(np.array(self.ratio) * self.base)
        self.img_sign = cv2.imread('sign.png')
        self.screen_ppm = 10
        self.score = [4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3]
        # default distance 1m
        self.dist_to_screen = 1
        self.dist_ratio = self.dist_to_screen / 5

    # set distance from screen, Std 5m
    def set_distance(self, dist):
        self.dist_to_screen = dist
        self.dist_ratio = self.dist_to_screen / 5

    def set_ppm(self, ppm):
        self.screen_ppm = ppm

    def get_stage_scale(self, stage):
        # print('scale = ',self.real_size[stage] * self.screen_ppm / self.img_sign.shape[0])
        return self.real_size[stage] * self.screen_ppm / self.img_sign.shape[0] * self.dist_ratio

    # get corresponding final score
    def get_stage_result(self, stage):
        return self.score[stage]

# test = standardSheet()
# test.set_ppm(100)
# print(test.get_stage_scale(0))