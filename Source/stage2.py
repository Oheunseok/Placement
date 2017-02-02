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




def enter():
    global image,sample,player,bgm,m_time,m_currenttime,colisionlist
    global inputlist,inputlen,startimage,starttrigger,minion,playerlist,starttrigger

    starttrigger=False
    m_time = timeclass.Time()
    m_currenttime = 0
    inputtype = m_mathclass.POINT * 255
    inputlen = 0
    inputlist = inputtype()
    starttrigger = False
    image = load_image('png\\SpaceBackground.png')  ## 배경화면
    ##플레이어

    minion = []
    playerlist = []

    for picturenum in range(1):
        sampleplayer = Player(picturenum)
        sampleplayer.xpos, sampleplayer.ypos = int((picturenum + 1) * (gamesizex / (title.picturenumber + 2))), int(
            gamesizey * 3 / 5)
        # sampleplayer.xpos, sampleplayer.ypos = (picturenum + 1) * int(gamesizex / 2), int(gamesizey / 2)
        playerlist.append(sampleplayer)  # 플레이어 리스트
    for num in range(stage1_data["minionnumber"]):
        minion.append(imageclass.minion(num % 2))  ##미니언
        minion[num].explosion_time = num

    colisionlist = [minion[num] for num in range(stage1_data["minionnumber"])]


def exit():
    global m_time
    del (m_time)
    del (bgm)
    del (image)
    del (player)
    close_canvas()

def update():
    global m_time,m_currenttime,starttrigger
    frame_time = m_time.get_frame_time()
    m_currenttime+=frame_time

    m_mathclass.Depthfunc(etc_data["Depthfunc"])
    inputlen = m_mathclass.Contoursfunc()
    m_mathclass.getContursfunc(inputlist, inputlen, 1)          #키넥트 뎁스 갱신

    if not starttrigger:
        for num in range(inputlen):
                if startimage.collision(gamesizex-int(list(inputlist)[num].x*(gamesizex/512)), gamesizey-int(list(inputlist)[num].y*(gamesizey/424))):
                    starttrigger = True
        if current_time>5:
            starttrigger = True                                                             #5초가 지나면 시작 or 스타트버튼 누르면 시작

    sinyposnum = 0
    if not starttrigger:
        for player in playerlist:
            player.ypos += math.sin(math.radians(current_time) * 100)
            sinyposnum += 1                                                                     #플레이어가 위아래로 움직이게하기

    if starttrigger:
        for player in playerlist:
            player.update(frame_time)
            player.playeroutcollide()


def draw():
    clear_canvas()

    image.clip_draw(0, 0, gamesizex, gamesizey, (int)(gamesizex / 2), (int)(gamesizey / 2))  # 배경
    image.draw(0,0,800,600)
    for player in playerlist:
        player.draw()


    update_canvas()



def handle_events():
    global player, mouse_x, mouse_y, starttrigger
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            sample.handle_events(event)  ##샘플값의 인풋값
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()

def pause(): pass


def resume(): pass