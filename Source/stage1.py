import game_framework
import random
from pico2d import *
from sampleupdate import sampleinput as Sample
from imageclass import player as Player
from m_mathclass import vector as vector
import m_mathclass
from ctypes import *
import imageclass
import music
import timeclass
import title


name = "StartState"
image = None
global mouse_x,mouse_y
global sample,gamesizex,gamesizexy
global current_time,frame_time,etc_file,m_time
etc_file = open('json\\Gamesystem.txt','r')                                                                 #제이슨 파일 불러오기
etc_data = json.load(etc_file)
etc_file.close()
logo_time = 0.03
gamesizex=int(etc_data["gamesize"])                                                                               #제이슨 파일에서 게임 크기 지정
gamesizey=(int)(etc_data["gamesize"]/4*3)                                                                         #4:3비율

stage1_file = open('json\stage1.txt','r')
stage1_data = json.load(stage1_file)
stage1_file.close()

bitarray = None




def enter():
    global image,sample,m_time,bgm,frame_time,m_right,minion,colisionlist, bitarray,earth,star
    global  m_down,m_up,m_right ,m_left,sun,saturn,playerlist,spaceship, inputlist,inputlen
    global mouse_x, mouse_y
    inputtype = m_mathclass.POINT * 255
    inputlen=0
    inputlist = inputtype()

    mouse_x,mouse_y = -50,-50
    frame_time=0
    image = load_image('png\\SpaceBackground.png')         ## 배경화면
                                 ##플레이어

    minion = []
    playerlist =[]

    #if title.picturenumber==0:                  #0이면 이전 사진을 사용
    #    title.picturenumber=1

    for picturenum in range(title.picturenumber):
        sampleplayer = Player(picturenum)
        sampleplayer.xpos, sampleplayer.ypos = (picturenum+1)*int(gamesizex / (title.picturenumber+1)), int(gamesizey / 2)
        playerlist.append(sampleplayer)                          #플레이어 리스트
    for num in range(stage1_data["minionnumber"]):
        minion.append(imageclass.minion(num%2))                    ##미니언
        minion[num].explosion_time=num

    star = imageclass.star()
    earth = imageclass.earth()                              #지구
    sun = imageclass.sun()
    saturn = imageclass.saturn()
    spaceship = imageclass.spaceship()

    colisionlist = [minion[num] for num in range(stage1_data["minionnumber"])]
    sample = Sample()                               ##샘플 잇풋 클래스
    bgm = music.Space_music()
    m_time = timeclass.Time()
    m_up, m_down, m_right, m_left = vector(),vector(),vector(),vector()
    m_up.x,m_up.y = 0,-1
    m_down.x,m_down.y=0,1
    m_right.x,m_right.y=-1,0
    m_left.x,m_left.y=1,0

   # mydll = WinDLL('KintctDLL')
   # initfuc = mydll["InitKinect"]

   # initfuc()

    b = (b'\xff\x00\xff\x00') * 100 * 100                       ## a , b,g,r 순서


    #print(b)
    bitarray = create_image_surface(b, 100, 100)

    #m_mathclass.initfuc()



def exit():
    global image,player,sample,bgm,m_time,playerlist
    del(m_time)
    del(bgm)
    del(image)
    del(player)
    del(playerlist)
    del(sample)
    close_canvas()


def update():
    global mouse_x,mouse_y,colisionlist,inputlen,inputlist

    (mouse_x,mouse_y)=sample.inputreturn()

    frame_time=m_time.get_frame_time()

    for player in playerlist:
        player.update(frame_time)
        player.playeroutcollide()
        if player.movespeed > 500 and player.movebool:
            player.rotatesize += frame_time * 10

    for num in range(stage1_data["minionnumber"]):
        for player in playerlist:                               ##모든 플레이어와 미니언 같의 충돌체크
            if(colisionlist[num].colide_player(player)):
                colisionlist[num].explosion_bool= True
                colisionlist[num].explosion_bgm.play_music()

            if player.movebool==False:                          ## 플레이어가 멈추면 같이 멈추는 트리거들
                player.scalebool = False


        colisionlist[num].update(frame_time)

    earth.update(frame_time)
    star.update(frame_time)
    sun.update(frame_time)
    saturn.update(frame_time)
    spaceship.update(frame_time)




    m_mathclass.Depthfunc(75)
    inputlen= m_mathclass.Contoursfunc()
    m_mathclass.getContursfunc(inputlist,inputlen,0)



    #if(minion.colide_player(player)):
    #    minion.explosion_bool =True                                       ##미니언 충돌체크
    #minion.update(frame_time)                                   ##미니언 에니메이션




def draw():
    global image,player,sample,minion,colisionlist,inputlist,inputlen
    global x, y
    global font, smallfont, bigfont

    clear_canvas()

    image.clip_draw(0,0,gamesizex,gamesizey,(int)(gamesizex/2),(int)(gamesizey/2))           #배경
    star.draw()
    earth.draw()
    sun.draw()
    saturn.draw()
    spaceship.draw()
    for player in playerlist:
        player.draw()

    for num in range(stage1_data["minionnumber"]):
        colisionlist[num].draw()
    num =0
    draw_rectangle( -20,-20,20,20)
    if inputlen>0:
        for num in range(inputlen):
            draw_rectangle(int(list(inputlist)[num].x*2.5) - 10,gamesizey-int(list(inputlist)[num].y*2.2) - 10, int(list(inputlist)[num].x*2.5)+ 10, gamesizey-int(list(inputlist)[num].y*2.2) + 10)
            print(list(inputlist)[num].x,list(inputlist)[num].y)

    #minion.draw()
    ##bitarray.draw(400,300)
    draw_rectangle(mouse_x-10,mouse_y-10,mouse_x+10,mouse_y+10)
    draw_point(mouse_x,mouse_y)
    update_canvas()


def handle_events():
    global player,mouse_x,mouse_y
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            sample.handle_events(event)                     ##샘플값의 인풋값
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):  ## red 플레이어 색깔변경
                for player in playerlist:
                    player.scalebool = not player.scalebool
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):  ## red 플레이어 색깔변경
                for player in playerlist:
                    player.image.set_color(0, 0, 0)
        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):  ##마우스 피킹값반환
            (mouse_x, mouse_y) = sample.inputreturn()
            randonnumber = 0
            for player in playerlist:
                if (player.collision(mouse_x, mouse_y) and not player.movebool and not player.duplicatemovebool):
                    randonnumber =random.randint(0,100)
                    if (randonnumber<50):
                        player.movebool = True
                        player.scalebool = True
                        #player.image.set_color(random.randint(0,255),random.randint(0,255),random.randint(0,255))

                        if (len(playerlist)<stage1_data["playernumber"]):
                            playerlist.append(Player(player.num))         ##플레이어 추가 및, 분할
                            playerlist[-1].xpos, playerlist[-1].ypos = player.xpos, player.ypos
                            mouse_x,mouse_y = -50,-50
                            playerlist[-1].w,playerlist[-1].h,playerlist[-1].bb_w,playerlist[-1].bb_h=player.w,player.h, player.bb_w,player.bb_h
                            playerlist[-1].movebool = True
                            playerlist[-1].scalebool = True
                            #playerlist[-1].image.set_color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                            playerlist[-1].movevector.x,playerlist[-1].movevector.y =-player.movevector.x,-player.movevector.y

                    elif randonnumber<75:
                        player.teleport()

                    else :
                        player.duplicatemovebool =True






def pause(): pass


def resume(): pass





