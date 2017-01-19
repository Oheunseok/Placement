from pico2d import*
import json
import random



class Time():
    def __init__(self):
        self.current_time = get_time()
        self.frame_time = 0

    def get_frame_time(self):
        self.frame_time = get_time() - self.current_time
        self.current_time += self.frame_time
        return self.frame_time
