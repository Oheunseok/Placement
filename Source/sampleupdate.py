from pico2d import*
import json
import random
import stage1
from ctypes import *

class xy:                                   ## 픽셀의 x,y좌표 구조체
    def __init__(self,x,y):
        self.x,self.y=x,y


class sampleinput:

    def __init__(self):
        self.mouse_x = -50    ##선택할 수 없는 위치
        self.mouse_y = -50
        self.pixel=[]
        for x in range(100, 200):
            for y in range(100, 200):
                self.pixel.append(xy(x,y))



    def inputreturn(self):                      ##x와 y값의 반환
        return self.mouse_x,self.mouse_y



    def handle_events(self, event):
        if(event.type,event.button)==(SDL_MOUSEBUTTONDOWN,SDL_BUTTON_LEFT):         ##마우스 피킹값반환
            self.mouse_x,self.mouse_y=event.x,(int)(stage1.gamesizey - event.y)
        elif(event.type,event.button)==(SDL_MOUSEBUTTONUP,SDL_BUTTON_LEFT):         ##마우스 업시킬시 마우스 좌표를 보이지 않는 좌표로 옮김
            self.mouse_x, self.mouse_y = -100,-100



