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

    # set distance from screen, Std 5m
    def set_distance(self, dist):
        self.dist_to_screen = dist
        self.dist_ratio = self.dist_to_screen / 5

    def set_ppm(self, ppm):
        self.screen_ppm = ppm

    def get_stage_scale(self, stage):
        # print('scale = ',self.real_size[stage] * self.screen_ppm / self.img_sign.shape[0])
        return self.real_size[stage] * self.screen_ppm / self.img_sign.shape[0] * self.dist_ratio

# test = standardSheet()
# test.set_ppm(100)
# print(test.get_stage_scale(0))