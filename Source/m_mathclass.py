from pico2d import*
import json
import random
etc_file = open('json\\Gamesystem.txt','r')                                                                 #제이슨 파일 불러오기
etc_data = json.load(etc_file)
etc_file.close()
logo_time = 0.03
gamesizex=int(etc_data["gamesize"])                                                                               #제이슨 파일에서 게임 크기 지정
gamesizey=(int)(etc_data["gamesize"]/4*3)                                                                         #4:3비율


class vector:
    def __init__(self):
        self.x,self.y= 1.0,1.0
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

class vector2d:
    def __init__(self):
        self.x,self.y = 0,0

    def dot(self,v2):
        return self.x*v2.x+self.y*v2.y
    def __sub__(self, other):
        return self.x-other.x,self.y-other.y

    def normalize(self):
        leng = math.fabs(math.sqrt(self.x*self.x + self.y*self.y))
        self.x = self.x/leng
        self.y = self.y/leng


class oobb:
    def __init__(self):
        self.xpos,self.ypos = 600,600
        self.a = [vector2d(),vector2d(),vector2d(),vector2d()]
        self.extent_x,self.extent_y =100 ,50
        self.m_rotation = 0
        self.tempRU , self.tempRD = vector2d(),vector2d()
        self.a[0].x,self.a[0].y = self.xpos + self.extent_x,self.ypos +self.extent_y
        self.a[1].x, self.a[1].y = self.xpos + self.extent_x, self.ypos - self.extent_y
        self.a[2].x, self.a[2].y = self.xpos - self.extent_x, self.ypos - self.extent_y
        self.a[3].x, self.a[3].y = self.xpos - self.extent_x, self.ypos + self.extent_y

    def update(self,x1,y1,x2,y2,rotation):
        self.xpos,self.ypos=x1, gamesizey-y1
        self.extent_x,self.extent_y = x2,y2
        self.a = self.roationFunction(math.degrees(-rotation))

    def roationFunction(self,rotationsize):
        temp = [vector2d(),vector2d(),vector2d(),vector2d()]
        temp[0].x,temp[0].y = self.xpos+self.extent_x*math.cos(math.radians(rotationsize))+self.extent_y*(-math.sin(math.radians(rotationsize))),\
                        self.ypos+self.extent_x * math.sin(math.radians(rotationsize)) + self.extent_y * (math.cos(math.radians(rotationsize)))
        temp[1].x, temp[1].y= self.xpos+self.extent_x*math.cos(math.radians(rotationsize))+(-self.extent_y)*(-math.sin(math.radians(rotationsize))),\
                        self.ypos+self.extent_x * math.sin(math.radians(rotationsize)) + (-self.extent_y) * (math.cos(math.radians(rotationsize)))
        temp[3].x, temp[3].y= self.xpos + -self.extent_x * math.cos(math.radians(rotationsize)) + self.extent_y * (
        -math.sin(math.radians(rotationsize))), \
                  self.ypos + -self.extent_x * math.sin(math.radians(rotationsize)) + self.extent_y * (
                  math.cos(math.radians(rotationsize)))
        temp[2].x, temp[2].y = self.xpos + -self.extent_x * math.cos(math.radians(rotationsize)) + (-self.extent_y) * (
        -math.sin(math.radians(rotationsize))), \
                  self.ypos + -self.extent_x * math.sin(math.radians(rotationsize)) + (-self.extent_y) * (
                  math.cos(math.radians(rotationsize)))

        return temp

    def rotate(self,rotationsize):
        self.a=self.roationFunction(rotationsize)

    def collision(self,obb):
        temp = [vector2d(),vector2d(),vector2d(),vector2d()]
        R = vector2d()
        R.x,R.y = self.xpos-obb.xpos,self.ypos-obb.ypos
        temp[0].x,temp.y = self.a[0]-self.a[1]
        temp[0].dot(R)
        temp[0].normalize()
        print(temp[0].x,temp[0].y)

    def print(self):
        for num in range(4):
            draw_line(int(self.a[num].x), int(self.a[num].y),int(self.a[(num+1)%4].x), int(self.a[(num+1)%4].y))
            #draw_point(int(self.a[num].x),int(self.a[num].y))

class playersort:
    def __init__(self,size,num):
        self.size=size
        self.num=num
    def sizeR(self):
        return self.size




mydll = windll["KinectDll"]
initfuc = mydll["InitKinect"]
Depthfunc = mydll["DepthImageUpdate"]
Contoursfunc = mydll["ContoursCenterLen"]
Contoursfunc.restype = c_long
getContursfunc = mydll["getContoursCenter"]
getContursfunc.argtypes = [POINTER(POINT),c_long,c_long]
createimage = mydll["CreateImage"]
createimage.restype = c_long
createrectfunc = mydll["CreateRect"]

BGCreatefunc = mydll["BGCreate"]
getContoursLen = mydll["getContoursLen"]
getContoursLen.restype = c_long
getContours = mydll["getContours"]
getContours.argtype = [POINTER(POINT),c_long,c_long]
closeCVwindow = mydll["closeCVwindow"]

getContourRect = mydll["getContoursRect"]
getContourRect.argtype = [POINTER(POINT),POINTER(POINT)]

getContourRectCountfunc = mydll["getContourRectCount"]
getContourRectCountfunc.restype = c_long