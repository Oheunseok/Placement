from pico2d import*
import json
import random
import stage1
import m_mathclass
import music
from ctypes import *

debugmode = False
etc_file = open('json\\Gamesystem.txt','r')
etc_data = json.load(etc_file)
etc_file.close()
gamesizex=etc_data["gamesize"]
gamesizey=(int)(etc_data["gamesize"]/4*3)

global player_data

player_file = open('json\\player_data.txt','r')
player_data = json.load(player_file)
player_file.close()

stage1_file = open('json\\stage1.txt','r')
stage1_data = json.load(stage1_file)
stage1_file.close()

stage2_file = open('json\\stage2.txt','r')
stage2_data = json.load(stage2_file)
stage2_file.close()

class AABB:
    def __init__(self,xpos,ypos,bb_h,bb_w):
        self.xpos =xpos
        self.ypos = ypos
        self.bb_h = bb_h
        self.bb_w = bb_w

    def get_bb(self):
        return self.xpos - int(self.bb_w / 2), self.ypos - int(self.bb_h / 2), self.xpos + int(
            self.bb_w / 2), self.ypos + int(self.bb_h / 2)


class image:                                                                           #이미지 기반
    image = None
    def __init__(self):
        self.image = load_image('png\\playersample.png')
        self.rotatesize=0
        self.rotatebool=False
        self.scalebool = False
        self.reversescale = False
        self.w,self.h = self.image.w,self.image.h
        self.bb_w,self.bb_h = self.image.w,self.image.h
        self.First_bb_w, self.First_bb_h = self.image.w,self.image.h
        self.xpos,self.ypos = 400,300
        self.colorbool = False


    def update(self,frame_time):
        pass

    def set_color(self,r,g,b):
        self.image.set_color(r,g,b)

    def draw(self):
        pass

    def handle_events(self, event):
        pass

    def collision(self,x,y):                                                            ##충돌체크
        if(x>self.xpos-self.bb_w/2 and x<self.xpos+self.bb_w/2 and y>self.ypos-self.bb_h/2 and y<self.ypos+self.bb_h/2):            ##지신의 왼쪽아래에서 오른쪽 위까지 충돌체크
            return True
        else:
            return False

    def get_bb(self):                                                                                      ##bb_구역 반환
        return self.xpos-int(self.bb_w/2),self.ypos-int(self.bb_h/2),self.xpos+int(self.bb_w/2),self.ypos+int(self.bb_h/2)

    def collide(self, b):                                                                                                                               #get_bb를 반환할 수 있는 객체와의 충돌체크
        left_a,bottom_a,right_a,top_a = self.get_bb()
        left_b,bottom_b,right_b,top_b = b.get_bb()

        if left_a> right_b : return  False
        if right_a < left_b : return False
        if top_a < bottom_b : return False
        if bottom_a > top_b : return False
        return True

    def collide_object(self, b):
        left_a,bottom_a,right_a,top_a = self.get_bb()
        left_b,bottom_b,right_b,top_b = b.get_bb()


        right_temp_b = right_b
        left_temp_b = right_b-2
        bottom_temp_b = bottom_b
        top_temp_b = top_b                              #사각형 오른쪽 판별
        if not (left_a> right_temp_b) and not(right_a < left_temp_b) and not(top_a < bottom_temp_b) and not(bottom_a > top_temp_b) :
                     self.movevector.x = 1
                     return True
        right_temp_b = left_b+2
        left_temp_b = left_b

        if not (left_a > right_temp_b) and not (right_a < left_temp_b) and not (top_a < bottom_temp_b) and not (
            bottom_a > top_temp_b):
            self.movevector.x = -1
            return True
        right_temp_b = right_b
        bottom_temp_b = top_b-2                     #사각형 위쪽
        if not (left_a > right_temp_b) and not (right_a < left_temp_b) and not (top_a < bottom_temp_b) and not (
                    bottom_a > top_temp_b):
            self.movevector.y = 1
            return True
        bottom_temp_b = bottom_b
        top_temp_b = bottom_b+2

        if not (left_a > right_temp_b) and not (right_a < left_temp_b) and not (top_a < bottom_temp_b) and not (
                        bottom_a > top_temp_b):
                self.movevector.y = -1
                return True
        return False


class player(image):
    global player_data
    playersize = player_data["playersize"]
    collapeV = player_data["collapeV"]
    collapeA = player_data["collapeA"]
    rotateV = player_data["rotateV"]
    rotateA = player_data["rotateA"]
    collapsex, collapey = player_data["collapsex"],player_data["collapey"]
    meltsize = player_data["meltsize"]
    movespeed = player_data["movespeed"]
    moveA = player_data["moveA"]
    melt_first_V = player_data["melt_first_V"]
    meltA = player_data["meltA"]
    duplicateA = player_data["dilicateA"]
    fixedV = player_data["fixedV"]
    fixedA = player_data["fixedA"]

    def __init__(self,num):                                                     #플레이어 클래스
        self.num = num
        name = "picture%d"%num
        print(name)
        self.image = load_image(name+'.png')
        self.shadowimage = load_image('s'+name+'.png')
        self.shadowimage.set_color(0,0,0)
        #self.image = load_image('alpha.png')
        self.circlemovebool = False
        self.rotatesize=0
        self.rotatebool=False
        self.scalebool = False
        self.colorbool = False
        self.meltbool = False
        self. collapsebool = False
        self.movebool = False
        self.movevector = m_mathclass.vector()
        self.movetime=0
        self.reversescale = False
        self.duplicatebool = True
        self.duplicatemovebool =False
        self.springreverse = True
        self.springbool = False
        self.AItrigger = False
        self.AItype = False
        self.melttime =0
        self.AItime =0
        self.springnumber=0
        self.duplicatemovetime = 0
        self.w,self.h = self.image.w*self.playersize,self.image.h*self.playersize                                       ##사진 크기
        self.F_w,self.F_h = self.image.w*self.playersize,self.image.h*self.playersize
        self.bb_w, self.bb_h = self.image.w*self.playersize, self.image.h*self.playersize                          ##충돌체크 크기
        self.First_bb_w,self.First_bb_h = self.image.w*self.playersize, self.image.h*self.playersize
        self.xpos,self.ypos = -1000,-1000                     ##이미지 위치
        self.meltV = []
        self.meltS = []
        self.duplicatexpos,self.duplicateypos,self.duplicaterotate = [self.xpos for num in range(player_data["duplicatesize"])],\
                                                                     [self.ypos for num in range(player_data["duplicatesize"])],\
                                                                     [self.rotatesize for num in range(player_data["duplicatesize"])]           ##이전 환영 위치값
        for x in range(pow(self.meltsize,2)):                                    ##제곱
            self.meltV.append(self.melt_first_V)
            self.meltS.append(0)
        self.duplicate_time = 0
        self.teleportmusic = music.Teleport_music()

        self.oobb = m_mathclass.oobb()

    ###기본적인 애니메이션들은 각각의 bool값을 on하면 frame_time의 시간에 따라 구현된다

    def update(self, frame_time):

        self.oobb.update(self.xpos,self.ypos,self.bb_w/2,self.bb_h/2,self.rotatesize)

        self.AI(frame_time)                                                         #인풋 값에 따른 스테이트 머신 구현

        if self.duplicatebool:                                                  # 잔상효과
            self.duplicateupdate(frame_time)

        if (self.w < self.F_w*3/5 and self.h < self.F_h*3/5):
            self.reversescale = True
        elif (self.w > self.F_w*1.4 and self.h > self.F_h*1.4):
            self.reversescale = False

        if (self.scalebool):                                                                 ## 사이즈를 줄이는 트리거
            self.reverseupdate(not self.reversescale,frame_time)
        if (self.rotatebool):                                                                ##회전 트리거
            self.rotatesize += frame_time*self.rotateV
        if (self.colorbool):                                                                ##랜덤 칼러
            self.image.set_color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        if(self.collapsebool):                                                              #조각나는 트리거
            self.collapsex,self.collapey = self.collapsex+(frame_time*self.collapeV),self.collapey+(frame_time*self.collapeV)       #벌어지는 거리가 속력에 의해 정해짐
        if(self.collapeV>0):
            self.collapeV-=self.collapeA*frame_time
        if(self.rotateV>1):                                                                 ##속도는 가속도에 따라 줄어든다
            self.rotateV-=self.rotateA*frame_time
        if(self.meltbool):                                          #녹아내리기
            self.melteupdate(frame_time)
        if(self.movebool):                                                                                  #이동
            self.move(frame_time)
        elif self.circlemovebool:
            self.circlemove(frame_time)
        else:
            self.fixedplayerposition(frame_time)
        if self.springbool:
            self.springupdate(frame_time)

    def AI(self,frametime):
        if self.AItrigger:
            self.AItime+=frametime
            if self.AItype == False:                    #AI시작시 트리거 on, ai타입 역시 on 2가지 트리거를 기반으로 스테이트 머신 구현
                self.AItype = True
                num = random.randint(0,100)                                             # 이동, 녹기, 원형이동, 좌우 복제 이동은 각각 따로 작동해야 되기 때문에 각각의 확률로 구현
                if num < 60 :                                            #이동,녹기,분할
                    self.movebool = True
                elif num<75:
                    self.meltbool = True
                elif num<85:
                    self.circlemovebool = True
                else :
                    self.duplicatemovebool = True

                num = random.randint(0, 100)                    # 4분의1 확률로 각각 회전과 축소확대가 되는지 안되는지 설정
                if num<25 and self.meltbool == False:           #총 4*4로 16가지 에니메이션 구현
                    self.rotatebool =True
                elif num<50 and self.meltbool == False:
                    self.scalebool = True
                elif num<75:
                    self.rotatebool,self.scalebool = True,True
                else:
                    self.rotatebool, self.scalebool = False,False



            if self.AItime>5:                           #AI가 최대 5초간 지속, 이후에는 모든 애니메이션을 off시켜 인풋 값을 받게 한다.
                self.AItime=0
                self.AItype = False
                self.movebool = False
                self.AItrigger = False
                self.rotatebool = False
                self.scalebool = False




    def move(self,frametime):                                   #이동
        #self.rotatebool = True
        self.movetime+=frametime
        self.xpos += self.movevector.x * frametime * self.movespeed
        self.ypos += self.movevector.y * frametime * self.movespeed
        self.movespeed =  self.moveA * math.fabs(math.sin(math.radians(self.movetime * 45)))
        if (self.movetime>4):                              # 플레이어가 멈추면 회전, 크기변환 제거
            self.movebool = False
            self.rotateV = player_data["rotateV"]
            self.movetime=0
            self.movespeed = player_data["movespeed"]
            self.randommovevector()

    def circlemove(self, frametime):  # 이동
        # self.rotatebool = True
        self.movetime += frametime
        if self.xpos <= gamesizex/2:
            self.xpos -=frametime*self.movespeed + frametime*50 * math.cos(self.movetime+360)
        else:
            self.xpos += frametime * self.movespeed + frametime*50 * math.cos(self.movetime+360)
        self.ypos += frametime * self.movespeed +frametime*50 * math.sin(self.movetime+360)

        if (self.movetime>4):                              # 플레이어가 멈추면 회전, 크기변환 제거
            self.circlemovebool = False
            self.movebool = False

    def randommovevector(self):
        self.movevector.x = random.randint(-10,10)/10
        self.movevector.y = random.randint(-10, 10) / 10



    def fixedplayerposition(self,frametime):              #플레이어를 내리거나 올리거나 중앙으로 약간 옮기게하기
        if self.ypos>gamesizey*(2/5):               ## 플레이어가 너무 위에 있으면 아래로 내려오게한다
            self.ypos-=frametime*self.fixedV
            self.fixedV+=self.fixedA
        if self.ypos<gamesizey*(1/6):
            self.ypos+=frametime*self.fixedV
            self.fixedV += self.fixedA
        if self.xpos <gamesizex*(1/8):
            self.xpos+=frametime*self.fixedV
            self.fixedV += self.fixedA
        if self.xpos > gamesizex*(7/8):
            self.xpos -= frametime * self.fixedV
            self.fixedV += self.fixedA

        if not self.ypos>gamesizey*(2/5) and not self.ypos<gamesizey*(1/6)\
                and not self.xpos <gamesizex*(1/8) and not self.xpos > gamesizex*(7/8):
            self.fixedV = player_data["fixedV"]


    def duplicateupdate(self,frametime):
        self.duplicate_time += frametime
        if self.duplicatemovebool:  # 잔상이동
            self.duplicatemovetime += frametime
            if self.duplicatemovetime < 2 :
                self.xpos += frametime * self.duplicateA *math.sin(math.radians(self.duplicatemovetime*180))
            elif self.duplicatemovetime < 4 :
                self.xpos -= frametime * self.duplicateA * math.sin(math.radians(self.duplicatemovetime * 180))
            elif self.duplicatemovetime>4:
                self.duplicatemovebool = False
                self.duplicatemovetime = 0

        if self.duplicate_time > 0.1:
            for num in range(player_data["duplicatesize"]):
                if not num == player_data["duplicatesize"] - 1:  # 마지막것이 아닐때까지 뒤에 것을 앞으로 복사
                    self.duplicatexpos[num] = self.duplicatexpos[num + 1]
                    self.duplicateypos[num] = self.duplicateypos[num + 1]
                    self.duplicaterotate[num] = self.duplicaterotate[num + 1]
                else:
                    self.duplicatexpos[num] = self.xpos
                    self.duplicateypos[num] = self.ypos
                    self.duplicaterotate[num] = self.rotatesize
            self.duplicate_time=0



    def reverseupdate(self,bool,frametime):                                                             ##축소 업데이트

        if(bool):
            self.w = self.w - frametime * self.F_w* player_data["scalesize"]
            self.h = self.h - frametime * self.F_h*player_data["scalesize"]
            self.bb_w = self.bb_w- frametime * self.First_bb_w *player_data["scalesize"]
            self.bb_h =  self.bb_h - frametime * self.First_bb_h *player_data["scalesize"]
        else:
            self.w = self.w + frametime * self.F_w *player_data["scalesize"]
            self.h = self.h + frametime * self.F_h *player_data["scalesize"]
            self.bb_w = self.bb_w + frametime * self.First_bb_w *player_data["scalesize"]
            self.bb_h = self.bb_h + frametime * self.First_bb_h *player_data["scalesize"]


    def melteupdate(self,frame_time):
        self.melttime += frame_time
        for x in range(self.meltsize):
            for y in range(self.meltsize):
                if (self.ypos - (int)(self.h / 2) + (int)(self.h / (self.meltsize * 2)) +
                            (int)(self.h / self.meltsize) * y - self.meltS[self.meltsize * y + x]> self.ypos - (int)(self.h / 2)):
                    self.meltS[self.meltsize * y + x] += self.meltV[self.meltsize * y + x] * frame_time  # S=S+Vt
                    self.meltV[self.meltsize * y + x] += self.meltA * frame_time  # V = V+

                elif self.melttime>3:
                        self.melttime = 0
                        self.meltbool = False
                        self.teleport()
                        self.AItrigger = False
                        self.AItype  = False
                        self.AItime = 0
                        for k in range(self.meltsize):
                            for t in range(self.meltsize):
                                    self.meltV[self.meltsize * k + t]= self.melt_first_V
                                    self.meltS[self.meltsize * k + t] = 0



    def springupdate(self,frame_time):                                           #스프링
        for x in range(self.meltsize):
            for y in range(self.meltsize):
                if self.springreverse:
                    if (self.ypos - (int)(self.h / 2) + (int)(self.h / (self.meltsize * 2)) +
                                (int)(self.h / self.meltsize) * y - self.meltS[self.meltsize * x + y]
                            > self.ypos - (int)(self.h / 2)):
                        self.meltS[self.meltsize * x + y] += self.meltV[self.meltsize * x + y] * frame_time  # S=S+Vt
                        self.meltV[self.meltsize * x + y] += self.meltA * frame_time  # V = V+

                    if self.meltS[-1] >= self.h - (int)(self.h / (self.meltsize * 2)):
                            self.springreverse = False
                else :
                       if self.meltS[self.meltsize*x+y]>=0:
                             self.meltS[self.meltsize * x + y] -= (20+30*y) * frame_time  # S=S+Vt
                             self.meltV[self.meltsize * x + y] = 0  # V = V+
                             if self.meltS[-1] < 0:
                                 self.springnumber+=1
                                 self.springreverse = True
                             if self.springnumber>2:
                                 self.springbool=False


    def teleport(self):                                                                                     #텔레포트
        self.teleportmusic.play_music()
        if gamesizex*(2/5)<self.bb_w or gamesizey*(2/5)<self.bb_h:
            self.xpos = random.randint(0 + 100, gamesizex - 100)
            self.ypos = random.randint(0 + 100, gamesizey - 100)
        else:
            self.xpos = random.randint(0 + int(self.bb_w), gamesizex - int(self.bb_w))
            self.ypos = random.randint(0 + int(self.bb_h), gamesizey - int(self.bb_h))



    def draw(self):

        if self.meltbool or self.springbool:
            self.playermelt()                                                                           #녹아내리는 현상
        elif (self.collapsebool):
            self.playercliprotate()  # 분리 회전
        else :
            if (self.duplicatebool):
                for num in range(player_data["duplicatesize"]):
                    self.shadowimage.set_alpha(int(255 / player_data["duplicatesize"] * num))
                    self.shadowimage.rotate_draw(self.duplicaterotate[num], self.duplicatexpos[num],
                                                 self.duplicateypos[num], self.w, self.h)  # 기본 축소하면서 회전
                    self.shadowimage.set_alpha(255)
            self.image.rotate_draw(self.rotatesize,self.xpos,self.ypos,self.w,self.h)                                 #기본 축소하면서 회전



    def playercliprotate(self):                                                                                     #분리회전
        self.image.clip_rotate_draw(
            self.rotatesize,                                                                                    #회전각
            0, 0,                                                                                               #이미지 시작위치
            (int)(self.F_w / 2), (int)(self.F_h / 2),                                                               #이미지 크기
            self.xpos - (int)(self.F_w/ 4) + pow(self.F_h/4,2) - self.collapsex,                                                     #화면 위치x
            self.ypos - (int)(self.F_h/ 4) - self.collapey,                     ##왼쪽아래                       화면위치y
            (int)(self.w / 2), (int)(self.h / 2))                                                                   #화면크기
        self.image.clip_rotate_draw(self.rotatesize,
                                      (int)(self.F_w/ 2), 0,
                                      (int)(self.F_w / 2), (int)(self.F_h / 2),
                                      self.xpos + (int)(self.F_w/4) + self.collapsex,
                                      self.ypos - (int)(self.F_h/ 4) - self.collapey,
                                      (int)(self.w / 2), (int)(self.h / 2))                                 ##오른쪽아래
        self.image.clip_rotate_draw(self.rotatesize,
                                      0, (int)(self.F_h / 2),
                                      (int)(self.w / 2), (int)(self.h / 2),
                                      self.xpos - (int)(self.F_w/4) - self.collapsex,
                                      self.ypos + (int)(self.F_h/ 4) + self.collapey,
                                      (int)(self.w / 2), (int)(self.h / 2))                                  ##왼쪽위에
        self.image.clip_rotate_draw(self.rotatesize,
                                      (int)(self.F_w / 2), (int)(self.F_h/ 2),
                                      (int)(self.F_w/ 2), (int)(self.F_h/ 2),
                                      self.xpos + (int)(self.F_w/4) + self.collapsex,
                                      self.ypos + (int)(self.F_h/ 4) + self.collapey,
                                      (int)(self.w / 2), (int)(self.h / 2))                                     ##오른쪽 위에

    def  playermelt(self):
        for x in range(self.meltsize):
            for y in range(self.meltsize):
                self.shadowimage.clip_draw((int)(self.image.w/self.meltsize)*x,(int)(self.image.h/self.meltsize)*y,         #이미지에서의 위치
                                       (int)(self.image.w/self.meltsize),(int)(self.image.h/self.meltsize),                 #조각난 크기
                                       self.xpos-(int)(self.w/2)+(int)(self.w/(self.meltsize*2))+(int)(self.w/self.meltsize)*x,      #화면에서의 x위치
                                       self.ypos-(int)(self.h/2)+(int)(self.h/(self.meltsize*2))+(int)(self.h/self.meltsize)*y-self.meltS[self.meltsize * y + x],   #화면에서의 y위치
                                           (int)(self.w / self.meltsize), (int)(self.h / self.meltsize))



    def playeroutcollide(self):                                                                     #맵바깥 충돌
        if (self.ypos + int(self.bb_h)/2 > gamesizey):
            self.movevector.y = -1
            self.movespeed -=player_data["Friction"]
        elif (self.ypos - int(self.bb_h)/2 < 0):
            self.movevector.y = 1
            self.movespeed -= player_data["Friction"]
        elif (self.xpos + int(self.bb_w)/2 > gamesizex):
            self.movevector.x = -1
            self.movespeed -= player_data["Friction"]
        elif (self.xpos - int(self.bb_w)/2 < 0):
            self.movevector.x = 1
            self.movespeed -= player_data["Friction"]

    def handle_events(self, event):
        if (event.type, event.key) == (SDL_KEYDOWN,SDLK_1):                                                         ## red 플레이어 색깔변경
            self.image.set_color(0,0,0)
        elif (event.type, event.key) ==(SDL_KEYDOWN,SDLK_2):                                                         ## green 플레이어 색깔변경
            self.image.set_color(0, 255, 0)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3):                                                         ## blue 플레이어 색깔변경
            self.image.set_color(0, 0, 255)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_5):                                         # 갈라지는 효과
            self.collapsebool = not self.collapsebool
            self.collapeV=player_data["collapeV"]
            self.collapsex, self.collapey=0,0
        elif (event.type , event.key)==(SDL_KEYDOWN, SDLK_6):                                   #흘러내리는 효과 온오프 및 초기화
            self.meltbool = not self.meltbool
            for x in range(pow(self.meltsize,2)):
                self.meltV[x]=0
                self.meltS[x]=0
        elif (event.type , event.key)==(SDL_KEYDOWN, SDLK_7):
            self.movebool = not self.movebool

        if (event.type, event.key) == (SDL_KEYDOWN, SDLK_4):  # 랜덤 색깔
            self.colorbool = not self.colorbool
        elif (event.type)==SDL_KEYDOWN:
            self.colorbool=False




class minion(image):                                                  #스테이지1 미니언
    explosion_image = None
    explosion_Chracter_image = None
    explosion_bgm = None
    explosion_dead_bgm = None
    speed = stage1_data["minionspeed"]

    def __init__(self,num):
        if(num==0):                                                   #클래스에 이미지 저장, num에따라 색깔이 바뀜
            self.image = load_image('png\\Alien.png')
            self.explosion_Chracter_image=load_image("png\\UnderAttackAlien.png")
        elif(num==1):
            self.image = load_image('png\\YellowAilen.png')
            self.explosion_Chracter_image = load_image("png\\UnderAttackYellowAlien.png")
        if (minion.explosion_image == None):
            minion.explosion_image = load_image("png\\Explosion.png")
        if (minion.explosion_bgm ==None):
            minion.explosion_bgm = music.Explosion_music()

        self.explosion_xpos = [x*400 for x in range(8)]
        self.anim_xpos =  [x*400 for x in range(8)]
        self.anim_time=0
        self.w = gamesizey*100/600
        self.h = gamesizey*100/600
        self.xpos = random.randint(0 + self.w, gamesizex - self.w)
        self.ypos = random.randint(0 + self.h, gamesizey - self.h)
        self.bb_w, self.bb_h = self.w/2,self.h/2
        self.explosion_bool = False
        self.explosion_time = 0
        self.angle = math.radians(45)

    def update(self,frametime):
        self.angle+=frametime*self.speed

        self.anim_time+=frametime*10
        if(self.anim_time>100):
            self.anim_time=0

        if(self.explosion_bool):                                                  #충돌트리거
            self.explosion_time += frametime*10

            if(self.explosion_time>8):
                self.xpos = random.randint(0 + self.w, gamesizex - self.w)
                self.ypos = random.randint(0 + self.h, gamesizey - self.h)
                self.explosion_bool = False
                self.explosion_time = 0
                self.explosion_num = 0
        else:                                                  #회전이동
            self.xpos +=frametime*50 * math.cos(self.angle+90)
            self.ypos +=frametime*50* math.sin(self.angle+90);




    def draw(self):

        if debugmode:                                                  #디버그 True시 충돌박스보여줌
            draw_rectangle(self.xpos - self.bb_w / 2, self.ypos - self.bb_h / 2,
                           self.xpos + self.bb_w / 2, self.ypos + self.bb_h / 2)
        if(self.explosion_bool):
            self.explosion_Chracter_image.clip_rotate_draw(self.angle,0 + self.explosion_xpos[int(self.explosion_time) % 8], 0, 400, 400,
                                                    self.xpos, self.ypos, self.w, self.h)
            self.explosion_image.clip_draw(0+self.explosion_xpos[int(self.explosion_time)%8],0,400, 400,self.xpos,self.ypos-self.image.h/30,self.w,self.h)

        else :
            self.image.clip_rotate_draw(self.angle, 0 + self.anim_xpos[int(self.anim_time) % 6], 0, 400, 400, self.xpos,
                                        self.ypos, self.w, self.h)

    def colide_player(self, player):                                                    #플레이어와 충돌체크시 플레이어 팅기게 하기
        if(self.collide(player) and not self.explosion_bool):
            player.collide_object(self)
            return True

class earth(image):

    def __init__(self):

        self.image = load_image('png\\Earth.png')
        self.anim_xpos = [x * 400 for x in range(2)]
        self.anim_time = 0
        self.temp_time =0
        self.time = 50
        self.pivot = gamesizex * 240 / 800

    def update(self, frametime):
        if(self.anim_time<4):
            self.anim_time += frametime * 5
        elif(self.temp_time<2):
            self.temp_time+=frametime
        else:
            self.temp_time=0
            self.anim_time=0
        self.time += frametime*4

    def draw(self):
        self.image.clip_draw(0+self.anim_xpos[int(self.anim_time)%2],0,400,400,gamesizex*400/800+math.sin(math.radians(self.time))*self.pivot,gamesizey*300/600+math.cos(math.radians(self.time))*self.pivot
                             ,gamesizey*150/600,gamesizey*150/600)


class saturn(image):

    def __init__(self):

        self.image = load_image('png\\saturn.png')
        self.anim_xpos = [x * 400 for x in range(2)]
        self.anim_time = 0
        self.time = 230
        self.pivot = gamesizex * 300 / 800

    def update(self, frametime):
        if(self.anim_time<4):
            self.anim_time += frametime * 7
        else:
            self.anim_time=0
        self.time+=frametime*5

    def draw(self):
        self.image.clip_draw(0+self.anim_xpos[int(self.anim_time)%2],0,400,400,gamesizex*400/800+math.sin(math.radians(self.time))*self.pivot,gamesizey*300/600+math.cos(math.radians(self.time))*self.pivot
                             ,gamesizey*160/600,gamesizey*160/600)


class sun(image):

    def __init__(self):

        self.image = load_image('png\\Sun.png')
        self.anim_xpos = [x * 400 for x in range(2)]
        self.anim_time = 0
        self.time = 90
        self.pivot = gamesizex * 200 / 800

    def update(self, frametime):
        if(self.anim_time<4):
            self.anim_time += frametime * 6
        else:
            self.anim_time=0
        self.time += frametime*3


    def draw(self):
        self.image.clip_draw(0+self.anim_xpos[int(self.anim_time)%2],0,400,400,gamesizex*400/800,gamesizey*300/600
                             ,gamesizey*200/600,gamesizey*200/600)

class star():

    def __init__(self):
        self.image = load_image('png\\SpaceStar.png')
        self.rotate_time =0

    def update(self, frametime):
        self.rotate_time +=frametime/20

    def draw(self):
        self.image.clip_rotate_draw(self.rotate_time,0,0,800,800,gamesizex/2,gamesizey/2,gamesizex*900/800,gamesizey*900/600)


class spaceship():

    def __init__(self):

        self.image = load_image('png\\Spaceship.png')
        self.rocket_music = music.Rocket_music()
        self.rotate_time = 0
        self.anim_xpos = [x * 400 for x in range(6)]
        self.anim_time = 0
        self.xpos = 0
        self.ypos = 0

    def update(self, frametime):
        self.anim_time += frametime*10
        self.xpos,self.ypos = self.xpos+frametime*60,self.ypos+frametime*60
        if(self.ypos > gamesizey*500/600):
            self.ypos = 0
            self.xpos = 0

    def draw(self):
        self.image.clip_rotate_draw(math.radians(-40),0 + self.anim_xpos[int(self.anim_time) % 6], 0, 400, 400, gamesizex*400/800+self.xpos, gamesizey*-100/600+self.ypos, gamesizey*180/600, gamesizey*180/600)


class finger(image):

    def __init__(self):
        self.image = load_image('png\\Finger.png')              #손바닥
        self.anim_xpos = [x * 400 for x in range(2)]
        self.anim_time = 0
        self.temp_time =0
        self.xpos =0
        self.ypos = 0

    def update(self, frametime):
        if(self.anim_time<4):
            self.anim_time += frametime * 5
        else:
            self.temp_time=0
            self.anim_time=0

    def draw(self):
        self.image.clip_draw(0+self.anim_xpos[int(self.anim_time)%2],0,400,400,self.xpos,self.ypos,gamesizey*150/600,gamesizey*150/600)


class threetwoone(image):                                                          #하나,둘,셋 손가락

    def __init__(self):
        self.image = load_image('png\\hand.png')
        self.anim_xpos = [x * 400 for x in range(3)]
        self.anim_num = 0
        self.rotate_time =0

    def update(self, frametime):
        self.rotate_time+= frametime*10

    def draw(self):
        self.image.clip_rotate_draw(math.radians(30)*math.sin(self.rotate_time),0+self.anim_xpos[self.anim_num],0,400,400,gamesizex*200/800,gamesizey*300/600,gamesizey*150/600,gamesizey*150/600)


class meteor(image):

    def __init__(self,num):                                                          #메테오 클래스

        self.meteorimage = load_image('png\\meteor.png')
        self.fireimage = load_image('png\\meteor2.png')
        self.anim_xpos = [x * 400 for x in range(5)]
        self.anim_time = 0
        self.time = 0
        self.xpos = random.randint(50,gamesizex*3/2)
        self.ypos = random.randint(0,gamesizey*5/4)
        self.size = random.randint(30, 100)
        self.num = num

    def update(self, frametime):
        if(self.anim_time<5):
            self.anim_time += frametime * 5
        else:
            self.anim_time=0
        self.time +=frametime*3
        self.xpos-=frametime*self.size*4
        self.ypos-=frametime*self.size*4

        if self.ypos < -300:
            self.ypos = gamesizey+30
            self.xpos = random.randint(50, gamesizex *3/2)

    def draw(self):
        if self.num%3==0:
            self.fireimage.clip_draw(0 + self.anim_xpos[int(self.anim_time) % 5], 0, 400, 400, self.xpos + gamesizey*self.size/3600,
                                     self.ypos - gamesizey*self.size/3600,
                                     gamesizey * self.size / 1200, gamesizey * self.size / 1200)
            self.meteorimage.clip_rotate_draw(self.time, 0, 0, 400, 400, self.xpos + gamesizey*self.size/3600,
                                              self.ypos - gamesizey*self.size/3600, gamesizey * self.size / 1600,
                                              gamesizey * self.size / 1600)
        self.fireimage.clip_draw(0+self.anim_xpos[int(self.anim_time)%5],0,400,400,self.xpos,self.ypos,gamesizey*self.size/600,gamesizey*self.size/600)
        self.meteorimage.clip_rotate_draw(self.time,0,0,400,400,self.xpos,self.ypos,gamesizey*self.size/800,gamesizey*self.size/800)



################################################################################################################
################################################################################################################
################################################################################################################stage2


class cannon(image):

    def __init__(self):
        self.image = load_image('png\\cannon.png')
        self.anim_xpos = [x * 400 for x in range(2)]
        self.anim_num = 0
        self.anim_time =0
        self.animtrigger = False
        self.xpos = gamesizey*100/600
        self.ypos = gamesizey*100/600
        self.bb_w = gamesizey*150/600
        self.bb_h = gamesizey*150/600
        self.id = 0
        #self.rotate_time =0

    def update(self, frametime):
        if self.animtrigger:
            self.anim_num=1
            self.anim_time+=frametime
        if self.anim_time>2:
                self.anim_time=0
                self.anim_num = 0
                self.animtrigger=False

    def draw(self):
        self.image.clip_draw(0+self.anim_xpos[self.anim_num],0,400,400,self.xpos,self.ypos,gamesizey*150/600,gamesizey*150/600)

class rightcannon(cannon):
    def __init__(self):
        cannon.__init__(self)
        self.image = load_image('png\\rightcannon.png')
        self.xpos = gamesizex * 700 / 800
        self.id = 1

    def draw(self):
        self.image.clip_draw(0+self.anim_xpos[self.anim_num],0,400,400,self.xpos,self.ypos,gamesizey*150/600,gamesizey*150/600)



class cannonball(image):

    def __init__(self):
        self.image = load_image('png\\cannonball.png')
        self.anim_xpos = [x * 400 for x in range(2)]
        self.anim_num = 0
        self.anim_time =0
        self.animtrigger = False
        self.xpos = gamesizey*120/600
        self.ypos = gamesizey*110/600
        self.bb_w = gamesizey*150/600
        self.bb_h = gamesizey*150/600
        self.speed = stage2_data["cannonspeed"]
        #self.rotate_time =0

    def update(self, frametime):
        self.xpos+=frametime*400
        self.ypos+= self.speed
        self.speed-=frametime*stage2_data["cannongravity"]

    def draw(self):
        self.image.clip_draw(0+self.anim_xpos[self.anim_num],0,400,400,self.xpos,self.ypos,gamesizey*100/600,gamesizey*100/600)

class rightcannonball(cannonball):
    def __init__(self):
        cannonball.__init__(self)
        self.xpos = self.xpos = gamesizex * 650 / 800

    def update(self, frametime):
        self.xpos-=frametime*400
        self.ypos+= self.speed
        self.speed-=frametime*stage2_data["cannongravity"]

    def draw(self):
        self.image.clip_draw(0 + self.anim_xpos[self.anim_num], 0, 400, 400, self.xpos, self.ypos,
                             gamesizey * 100 / 600, gamesizey * 100 / 600)

class basket(cannon):
    def __init__(self):
        cannon.__init__(self)
        self.image = load_image('png\\basket.png')
        self.anim_num =0
        self.anim_xpos = [200*x for x in range(7)]


    def draw(self):
        if self.anim_num>=6:
            self.anim_num=6
        self.image.clip_draw(0 + self.anim_xpos[self.anim_num], 0,200,200,self.xpos,self.ypos,gamesizey*150/600,gamesizey*150/600)


class rabbit(minion):
    right = stage2_data["mov_vec_right"]
    left = stage2_data["mov_vec_left"]
    stop = stage2_data["mov_vec_stop"]
    def __init__(self):
        self.image  = load_image('png\\rabbit.png')
        self.left = load_image('png\\rabbitleft.png')
        self.right = load_image('png\\rabbitright.png')
        self.attack = load_image('png\\rabbitattack.png')
        self.w = gamesizey * 70 / 600
        self.h = gamesizey * 90 / 600
        self.xpos = random.randint(0 + self.w, gamesizex - self.w)
        self.ypos = random.randint(0 + self.h, gamesizey*3/4 - self.h)
        self.bb_w, self.bb_h = self.w , self.h
        if self.xpos > gamesizex/2:
            self.vector = self.right
        else :
            self.vector = self.left

        self.speed = random.randint(stage2_data["min_speed"],stage2_data["max_speed"])
        self.explosion_bool = False
        self.time = 0
        self.anim_xpos = [400*x for x in range(5)]
        self.anim_num = 0
        self.anim_time = 0
        self.yspeed = stage2_data["rabbityspeed"]
        self.xspeed = stage2_data["rabbitxspeed"]
        self.gravity = stage2_data["rabbitygravity"]
        self.bgm = music.Rabbit_music()

    def update(self,frametime):
        if not self.explosion_bool:
            if self.vector == self.right:
                self.xpos-=frametime*self.speed
            elif self.vector == self.left :
                self.xpos+=frametime*self.speed
        self.time+=frametime*3
        if self.explosion_bool:
            self.anim_time+=frametime
            self.anim_num = int(self.anim_time*20)%5
            if self.vector == self.right:
                self.xpos+=frametime*self.xspeed
            elif self.vector == self.left :
                self.xpos-=frametime*self.xspeed
            self.ypos += frametime*self.yspeed
            self.yspeed-=frametime*self.gravity

            if self.anim_time>5:
                self.explosion_bool=False
                self.anim_time = 0
                self.xpos = random.randint(0 + self.w, gamesizex - self.w)
                self.ypos = random.randint(0 + self.h, gamesizey * 3 / 4 - self.h)
                if self.xpos > gamesizex / 2:
                    self.vector = self.right
                else:
                    self.vector = self.left
                self.yspeed = stage2_data["rabbityspeed"]
                self.gravity = stage2_data["rabbitygravity"]

    def draw(self):
        x1,y1,x2,y2 = self.get_bb()
        draw_rectangle(x1,y1,x2,y2)
        if not self.explosion_bool:
            self.image.clip_draw(0 , 0, 800, 800, self.xpos, self.ypos,
                                 gamesizey * 200 / 600, gamesizey * 200 / 600)
            self.left.clip_rotate_draw(math.radians(10)*math.sin(self.time),0 , 0, 800, 800, self.xpos-gamesizey * 10 / 600, self.ypos-gamesizey * 10 / 600,
                                 gamesizey * 200 / 600, gamesizey * 200 / 600)
            self.right.clip_rotate_draw(math.radians(10) * math.sin(self.time-9), 0, 0, 800, 800,
                                       self.xpos + gamesizey * 10 / 600, self.ypos - gamesizey * 10 / 600,
                                       gamesizey * 200 / 600, gamesizey * 200 / 600)
        else :
            self.attack.clip_rotate_draw(math.radians(self.anim_time*360),0 + self.anim_xpos[self.anim_num] , 0, 400, 400, self.xpos, self.ypos,
                                 gamesizey * 100 / 600, gamesizey * 100 / 600)

class bear(rabbit):
    def __init__(self,bask):
        self.basket = bask
        rabbit.__init__(self)
        self.w = gamesizey * 100 / 600
        self.h = gamesizey * 90 / 600
        self.bb_w, self.bb_h = self.w, self.h
        self.image = load_image('png\\bear.png')
        self.left = load_image('png\\bearhand.png')
        self.attack = load_image('png\\bearattack.png')
        self.squirrel = squirrel()
        self.bgm = music.Bear_music()

    def update(self,frametime):
        if not self.explosion_bool:
            if self.vector == self.right:
                self.xpos -= frametime * self.speed
            elif self.vector == self.left:
                self.xpos += frametime * self.speed
        self.time += frametime * 3
        if self.explosion_bool:
            if self.squirrel.drawonoff == False:
                self.squirrel.xpos,self.squirrel.ypos = self.xpos+ gamesizey * 40 / 600,self.ypos- gamesizey * 10 / 600
                self.squirrel.drawonoff = True
            self.anim_time += frametime
            self.anim_num = int(self.anim_time * 20) % 5
            if self.vector == self.right:
                self.xpos += frametime * self.xspeed
            elif self.vector == self.left:
                self.xpos -= frametime * self.xspeed
            self.ypos += frametime * self.yspeed
            self.yspeed -= frametime * self.gravity

            if self.anim_time > 5:
                self.explosion_bool = False
                self.anim_time = 0
                self.xpos = random.randint(0 + self.w, gamesizex - self.w)
                self.ypos = random.randint(0 + self.h, gamesizey * 3 / 4 - self.h)
                self.squirrel.drawonoff = False
                if self.xpos > gamesizex / 2:
                    self.vector = self.right
                else:
                    self.vector = self.left
                self.yspeed = stage2_data["rabbityspeed"]
                self.gravity = stage2_data["rabbitygravity"]

    def draw(self):
        x1, y1, x2, y2 = self.get_bb()
        draw_rectangle(x1, y1, x2, y2)
        if self.explosion_bool == False:
            self.image.clip_draw(0 , 0, 800, 800, self.xpos- gamesizey * 40 / 600, self.ypos,
                                 gamesizey * 220 / 600, gamesizey * 220 / 600)
            self.left.clip_rotate_draw(math.radians(10) * math.sin(self.time), 0, 0, 800, 800,
                                       self.xpos - gamesizey * 40 / 600, self.ypos,
                                       gamesizey * 220 / 600, gamesizey * 220 / 600)
        else :
            self.attack.clip_rotate_draw(math.radians(self.anim_time*360),0 + self.anim_xpos[self.anim_num] , 0, 400, 400,
                                       self.xpos - gamesizey * 40 / 600, self.ypos,
                                       gamesizey * 110 / 600, gamesizey * 110 / 600)
            self.squirrel.draw()


class squirrel(rabbit):
    def __init__(self):
        rabbit.__init__(self)
        self.image = load_image('png\\squirrel.png')
        self.drawonoff = False
    def draw(self):
        self.image.clip_draw(0 , 0, 400, 400, self.xpos, self.ypos,
                             gamesizey * 60 / 600, gamesizey * 60 / 600)


class apple(minion):

    def __init__(self):
        self.image = load_image("png\\apple.png")
        self.anim_xpos = [x * 400 for x in range(8)]
        self.anim_time = 0
        self.w = gamesizey * 30 / 600
        self.h = gamesizey * 30 / 600
        self.bb_w, self.bb_h = self.w, self.h
        self.xpos = random.randint(0 + self.w, gamesizex - self.w)
        self.ypos = random.randint(gamesizey*3/4, gamesizey - self.h)
        self.speed = stage2_data["applespeed"]
        self.explosion_bool = False
        self.anim_bool = False
        self.time = 0

    def randomxpos(self):
        self.xpos = random.randint(0 + self.w, gamesizex - self.w)

    def update(self,frametime):
        if self.anim_bool:
            self.anim_time+=frametime
            self.anim_num = int(self.anim_time*10)%5
            if self.anim_time>2:
                self.ypos = random.randint(gamesizey * 3 / 4, gamesizey - self.h)
                self.speed = stage2_data["applespeed"]
                self.explosion_bool = False
                self.anim_bool = False
                self.anim_time = 0
        elif self.explosion_bool:
            self.ypos -= frametime*self.speed
            self.speed +=frametime*stage2_data["appleA"]
            self.time +=frametime*60
            if self.ypos < -100:
                self.ypos =  random.randint(gamesizey*3/4, gamesizey - self.h)
                self.speed = stage2_data["applespeed"]
                self.explosion_bool = False


    def draw(self):
        if self.anim_bool:
            self.image.clip_rotate_draw(math.radians(self.time),self.anim_num*400 , 0, 400, 400, self.xpos, self.ypos,
                             self.w, self.h)
        else:
            self.image.clip_rotate_draw(math.radians(self.time),0 , 0, 400, 400, self.xpos, self.ypos,
                             self.w, self.h)



###################################################################################stage3

class ghost(image):
    def __init__(self):
        self.image = load_image('png\\rabbit.png')
        self.w = gamesizey * 70 / 600
        self.h = gamesizey * 90 / 600
        self.xpos = random.randint(0 + self.w, gamesizex - self.w)
        self.ypos = random.randint(0 + self.h, gamesizey * 3 / 4 - self.h)
        self.bb_w, self.bb_h = self.w, self.h
        self.speed = random.randint(stage2_data["min_speed"], stage2_data["max_speed"])
        self.explosion_bool = False
        self.time = 0
        self.anim_xpos = [400 * x for x in range(5)]
        self.anim_num = 0
        self.anim_time = 0
        self.playerlist = []

    def update(self,frame_time,player):
        del(self.playerlist)
        self.playerlist = []
        num = 0
        for play in player:
            list.append(m_mathclass.playersort(math.fabs(self.xpos - play.xpos) + math.fabs(self.ypos - play.ypos), num))
            num += 1
        self.playerlist.sort(key=m_mathclass.playersort.sizeR)
