from pico2d import*
import json
import random
import stage1
import m_mathclass
import music
from ctypes import *

debugmode = True
etc_file = open('json\\Gamesystem.txt','r')
etc_data = json.load(etc_file)
etc_file.close()
gamesizex=etc_data["gamesize"]
gamesizey=(int)(etc_data["gamesize"]/4*3)

global player_data

player_file = open('json\\player_data.txt','r')
player_data = json.load(player_file)
player_file.close()



class image:
    image = None
    def __init__(self):
        self.image = load_image('png\\playersample.png')
        self.rotatesize=0
        self.rotatebool=False
        self.scalebool = False
        self.reversescale = False
        self.w,self.h = self.image.w,self.image.h
        self.bb_w,self.bb_h = self.image.w,self.image.h
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

    def get_bb(self):
        return self.xpos-int(self.bb_w/2),self.ypos-int(self.bb_h/2),self.xpos+int(self.bb_w/2),self.ypos+int(self.bb_h/2)

    def collide(self, b):
        left_a,bottom_a,right_a,top_a = self.get_bb()
        left_b,bottom_b,right_b,top_b = b.get_bb()

        if left_a> right_b : return  False
        if right_a < left_b : return False
        if top_a < bottom_b : return False
        if bottom_a > top_b : return False
        return True



class player(image):
    global player_data

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

    def __init__(self,num):
        self.num = num
        name = "picture%d"%num
        print(name)
        self.image = load_image(name+'.png')
        #self.image = load_image('alpha.png')
        self.image.set_color(0, 0, 0)
        self.rotatesize=0
        self.rotatebool=False
        self.scalebool = False
        self.colorbool = False
        self.meltbool = False
        self. collapsebool = False
        self.movebool = False
        self.movevector = m_mathclass.vector()
        self.reversescale = False
        self.duplicatebool = True
        self.duplicatemovebool =False
        self.duplicatemovetime = 0
        self.w,self.h = self.image.w/2,self.image.h/2                                       ##사진 크기
        self.F_w,self.F_h = self.image.w/2,self.image.h/2
        self.bb_w, self.bb_h = self.image.w/2, self.image.h/2                          ##충돌체크 크기
        self.First_bb_w,self.First_bb_h = self.image.w/2, self.image.h/2
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




    def update(self, frame_time):
        if self.duplicatebool:                                                  # 잔상효과
            self.duplicateupdate(frame_time)
        if (self.w < self.F_w and self.h < self.F_h):
            self.reversescale = True
        elif (self.w > self.F_w and self.h > self.F_h):
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
        if(self.meltbool):
            self.melteupdate(frame_time)
        if(self.movebool):
            self.xpos += self.movevector.x*frame_time*self.movespeed
            self.ypos += self.movevector.y*frame_time*self.movespeed
            self.movespeed-=self.moveA*frame_time
            if(self.movespeed<0):
                self.movebool=False
                self.movespeed = 1000

    def duplicateupdate(self,frametime):
        self.duplicate_time += frametime
        if self.duplicatemovebool:  # 잔상이동
            self.duplicatemovetime += frametime
            if self.duplicatemovetime < 0.5 :
                self.xpos += frametime * self.duplicateA *math.sin(self.duplicatemovetime*2)
            elif self.duplicatemovetime<1.5:
                self.xpos -= frametime * self.duplicateA*math.sin(self.duplicatemovetime*3)
            elif self.duplicatemovetime<2:
                self.xpos += frametime * self.duplicateA*math.sin(self.duplicatemovetime*2)
            elif self.duplicatemovetime>2:
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
        for x in range(self.meltsize):
            for y in range(self.meltsize):
                if (self.ypos - (int)(self.h / 2) + (int)(self.h / (self.meltsize * 2)) + (int)(
                            self.h / self.meltsize) * y - self.meltS[self.meltsize * x + y]
                        > self.ypos - (int)(self.h / 2)):
                    self.meltS[self.meltsize * x + y] += self.meltV[self.meltsize * x + y] * frame_time  # S=S+Vt
                    self.meltV[self.meltsize * x + y] += self.meltA * frame_time  # V = V+At

    def teleport(self):
        self.teleportmusic.play_music()
        self.xpos = random.randint(0 + int(self.bb_w), gamesizex - int(self.bb_w))
        self.ypos = random.randint(0 + int(self.bb_h), gamesizey - int(self.bb_h))



    def draw(self):
        if  (not self.collapsebool and not self.meltbool):
            self.image.rotate_draw(self.rotatesize,self.xpos,self.ypos,self.w,self.h)                                 #기본 축소하면서 회전
            if(self.duplicatebool):
                for num in range(player_data["duplicatesize"]):
                    self.image.set_alpha(int(255/player_data["duplicatesize"]*num))
                    self.image.rotate_draw(self.duplicaterotate[num], self.duplicatexpos[num], self.duplicateypos[num], self.w, self.h)  # 기본 축소하면서 회전
                    self.image.set_alpha(255)
        elif  (self.collapsebool and not self.meltbool):
            self.playercliprotate()                                                                         #분리 회전
        elif (self.meltbool):
            self.playermelt()


        if debugmode :
            draw_rectangle(int(self.xpos-self.bb_w/2) , int(self.ypos-self.bb_h/2) ,
                           int(self.xpos+self.bb_w/2),  int(self.ypos+self.bb_h/2))


    def playercliprotate(self):                                                                                     #분리회전
        self.image.clip_rotate_draw(
            self.rotatesize,                                                                                    #회전각
            0, 0,                                                                                               #이미지 시작위치
            (int)(self.F_w / 2), (int)(self.F_h / 2),                                                               #이미지 크기
            self.xpos - (int)(self.F_w/ 4) + pow(self.F_h/4,2) - self.collapsex,                                                     #화면 위치x
            self.ypos - (int)(self.F_h/ 4) - self.collapey,                     ##왼쪽아래                       화면위치y
            (int)(self.w / 2), (int)(self.h / 2))                                                                   #화면크기
        print(math.sqrt(pow(self.F_w/4,2) + pow(self.F_h/4,2)))
        print((math.cos(math.radians(45))* (math.sqrt(pow(self.F_w/4,2) + pow(self.F_h/4,2)))))
        print(math.acos(((self.F_w/4) /(math.sqrt(pow(self.F_w/4,2) + pow(self.F_h/4,2)))))*180/math.pi)

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
                self.image.clip_draw(0+(int)(self.w/self.meltsize)*x,0+(int)(self.h/self.meltsize)*y,         #이미지에서의 위치
                                       (int)(self.w/self.meltsize),(int)(self.h/self.meltsize),                 #조각난 크기
                                       self.xpos-(int)(self.w/2)+(int)(self.w/(self.meltsize*2))+(int)(self.w/self.meltsize)*x,      #화면에서의 x위치
                                       self.ypos-(int)(self.h/2)+(int)(self.h/(self.meltsize*2))+(int)(self.h/self.meltsize)*y-self.meltS[self.meltsize*x+y])      #화면에서의 y위치





    def playeroutcollide(self):                                                                     #맵바깥 충돌
        if (self.ypos + int(self.bb_h) > gamesizey):
            self.movevector.y = -1
            self.movespeed -=player_data["Friction"]
        elif (self.ypos - int(self.bb_h) < 0):
            self.movevector.y = 1
            self.movespeed -= player_data["Friction"]
        elif (self.xpos + int(self.bb_w) > gamesizex):
            self.movevector.x = -1
            self.movespeed -= player_data["Friction"]
        elif (self.xpos - int(self.bb_w) < 0):
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
        elif (event.type , event.key)==(SDL_KEYDOWN, SDLK_6):                                   #흘러내리는 효과 오오프 및 초기화
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

    def collide_object(self, b):
        left_a,bottom_a,right_a,top_a = self.get_bb()
        left_b,bottom_b,right_b,top_b = b.get_bb()

        right_temp_b = right_b
        left_temp_b = right_b-2
        bottom_temp_b = bottom_b
        top_temp_b = top_b                              #사각형 오른쪽 판별
        if not (left_a> right_temp_b) and not(right_a < left_temp_b) and not(top_a < bottom_temp_b) and not(bottom_a > top_temp_b) :
                     self.movevector.x = 1
        right_temp_b = left_b+2
        left_temp_b = left_b

        if not (left_a > right_temp_b) and not (right_a < left_temp_b) and not (top_a < bottom_temp_b) and not (
            bottom_a > top_temp_b):
            self.movevector.x = -1

        right_temp_b = right_b
        bottom_temp_b = top_b-2                     #사각형 위쪽
        if not (left_a > right_temp_b) and not (right_a < left_temp_b) and not (top_a < bottom_temp_b) and not (
                    bottom_a > top_temp_b):
            self.movevector.y = 1

        bottom_temp_b = bottom_b
        top_temp_b = bottom_b+2

        if not (left_a > right_temp_b) and not (right_a < left_temp_b) and not (top_a < bottom_temp_b) and not (
                        bottom_a > top_temp_b):
                self.movevector.y = -1


class minion(image):
    image = None
    explosion_image = None
    explosion_Chracter_image = None
    explosion_bgm = None
    explosion_dead_bgm = None

    def __init__(self,num):
        if(num==0):
            self.image = load_image('png\\Alien.png')
            self.explosion_Chracter_image=load_image("png\\UnderAttackAlien.png")
        elif(num==1):
            self.image = load_image('png\\YellowAilen.png')
            self.explosion_Chracter_image = load_image("png\\UnderAttackYellowAlien.png")
        if (minion.explosion_image == None):
            minion.explosion_image = load_image("png\\Explosion.png")
        if (minion.explosion_bgm ==None):
            minion.explosion_bgm = music.Explosion_music()
        if (minion.explosion_dead_bgm == None):
            minion.explosion_dead_bgm == music.Explosion_music()

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
        self.angle+=frametime/2

        self.anim_time+=frametime*10
        if(self.anim_time>100):
            self.anim_time=0

        if(self.explosion_bool):
            self.explosion_time += frametime*10

            if(self.explosion_time>8):
                self.xpos = random.randint(0 + self.w, gamesizex - self.w)
                self.ypos = random.randint(0 + self.h, gamesizey - self.h)
                self.explosion_bool = False
                self.explosion_time = 0
                self.explosion_num = 0
        else:
            self.xpos +=frametime*50 * math.cos(self.angle+90)
            self.ypos +=frametime*50* math.sin(self.angle+90);




    def draw(self):

        if debugmode:
            draw_rectangle(self.xpos - self.bb_w / 2, self.ypos - self.bb_h / 2,
                           self.xpos + self.bb_w / 2, self.ypos + self.bb_h / 2)
        if(self.explosion_bool):
            self.explosion_Chracter_image.clip_rotate_draw(math.radians(self.angle-90),0 + self.explosion_xpos[int(self.explosion_time) % 8], 0, 400, 400,
                                                    self.xpos, self.ypos, self.w, self.h)
            self.explosion_image.clip_draw(0+self.explosion_xpos[int(self.explosion_time)%8],0,400, 400,self.xpos,self.ypos-self.image.h/30,self.w,self.h)

        else :
            self.image.clip_rotate_draw(self.angle, 0 + self.anim_xpos[int(self.anim_time) % 6], 0, 400, 400, self.xpos,
                                        self.ypos, self.w, self.h)

    def colide_player(self, player):
        if(self.collide(player)):
            player.collide_object(self)
            return True

class earth(image):
    image = None

    def __init__(self):
        if (earth.image == None):
            earth.image = load_image('png\\Earth.png')
        self.anim_xpos = [x * 400 for x in range(2)]
        self.anim_time = 0
        self.temp_time =0

    def update(self, frametime):
        if(self.anim_time<4):
            self.anim_time += frametime * 5
        elif(self.temp_time<2):
            self.temp_time+=frametime
        else:
            self.temp_time=0
            self.anim_time=0

    def draw(self):
        self.image.clip_draw(0+self.anim_xpos[int(self.anim_time)%2],0,400,400,gamesizex*300/800,gamesizey*430/600,gamesizey*150/600,gamesizey*150/600)


class saturn(image):
    image = None

    def __init__(self):
        if (saturn.image == None):
            saturn.image = load_image('png\\saturn.png')
        self.anim_xpos = [x * 400 for x in range(2)]
        self.anim_time = 0
        self.temp_time =0

    def update(self, frametime):
        if(self.anim_time<4):
            self.anim_time += frametime * 7
        elif(self.temp_time<2):
            self.temp_time+=frametime
        else:
            self.temp_time=0
            self.anim_time=0

    def draw(self):
        self.image.clip_draw(0+self.anim_xpos[int(self.anim_time)%2],0,400,400,gamesizex*150/800,gamesizey*150/600,gamesizey*200/600,gamesizey*200/600)


class sun(image):
    image = None
    def __init__(self):
        if (sun.image == None):
            sun.image = load_image('png\\Sun.png')
        self.anim_xpos = [x * 400 for x in range(2)]
        self.anim_time = 0
        self.temp_time =0

    def update(self, frametime):
        if(self.anim_time<4):
            self.anim_time += frametime * 6
        elif(self.temp_time<2):
            self.temp_time+=frametime
        else:
            self.temp_time=0
            self.anim_time=0

    def draw(self):
        self.image.clip_draw(0+self.anim_xpos[int(self.anim_time)%2],0,400,400,gamesizex*690/800,gamesizey*490/600,gamesizey*250/600,gamesizey*250/600)

class star():
    image = None
    def __init__(self):
        if (star.image == None):
            star.image = load_image('png\\SpaceStar.png')
        self.rotate_time =0

    def update(self, frametime):
        self.rotate_time +=frametime/20

    def draw(self):
        self.image.clip_rotate_draw(self.rotate_time,0,0,800,800,gamesizex/2,gamesizey/2,gamesizex*900/800,gamesizey*900/600)


class spaceship():
    image = None

    def __init__(self):
        if (spaceship.image == None):
            spaceship.image = load_image('png\\Spaceship.png')
        self.rocket_music = music.Rocket_music()
        self.rotate_time = 0
        self.anim_xpos = [x * 400 for x in range(6)]
        self.anim_time = 0
        self.temp_time = 0
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

