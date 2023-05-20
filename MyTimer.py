from threading import Timer
from time import time

class MyTimer():

    def __init__ (self, interval, function = lambda:None):

        self.interval = interval
        self.function = function
        self.timer = Timer(0,lambda:None)
        self.countdown = 0

    def is_alive(self):
        
        return self.timer.is_alive()

    def start(self):
        
        if not self.timer.is_alive():
            self.countdown_before_cancel = 0
            self.timer = Timer(self.interval, self.function)
            self.timer.start()
            self.time_start = time()

    def get_countdown(self):

        if self.timer.is_alive():
            return self.time_start + self.interval - time()
        else:
            return self.countdown
        
    def cancel(self):

        self.countdown = self.get_countdown()
        if self.timer.is_alive():
            self.timer.cancel()
