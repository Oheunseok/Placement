from pico2d import*
import json
import random



class vector:
    def __init__(self):
        self.x,self.y= 1,1
        self.v =30
        self. vector2_input = 1
        self. collect = 5

    def reflection_vec_to_vec(self, vector2_input):                                                                 # a는 x,y 변수가 있는 vector2 클래스를 넣는다 법선벡터
        rad = 2*(-self.x * vector2_input.x + -self.y* vector2_input.y)
        self.x = int(rad * vector2_input.x) + self.x
        self.y = int(rad * vector2_input.y) + self.y

    def reflection_vec_to_xy(self, x,y):                                                                 # a는 x,y 변수가 있는 vector2 클래스를 넣는다 법선벡터
        rad = 2*(-self.x * x + -self.y* y)
        self.x = int(rad * x) + self.x
        self.y = int(rad * y) + self.y


class POINT(Structure):
    _fields_ = [("x",c_long),("y",c_long)]

mydll = windll["KintctDLL"]
initfuc = mydll["InitKinect"]
Depthfunc = mydll["DepthImage"]
Contoursfunc = mydll["ContoursCenterLen"]
Contoursfunc.restype = c_long
getContursfunc = mydll["getContoursCenter"]
getContursfunc.argtypes = [POINTER(POINT),c_long,c_long]
createimage = mydll["CreateImage"]
createimage.restype = c_long