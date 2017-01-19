import game_framework
from pico2d import *
from sampleupdate import sampleinput as Sample
import music
import timeclass
import stage1
from ctypes import *
import m_mathclass
etc_file = open('json\\Gamesystem.txt','r')                                                                 #제이슨 파일 불러오기
etc_data = json.load(etc_file)
etc_file.close()
gamesizex=etc_data["gamesize"]                                                                               #제이슨 파일에서 게임 크기 지정


gamesizey=(int)(etc_data["gamesize"]/4*3)





def enter():
    global image,sample,bgm,m_time,frame_time,m_currenttime,announcement_image,logo_image
    global black_image,white_image,m_cameratime

    open_canvas(gamesizex, gamesizey)
    m_mathclass.initfuc()
    m_time = timeclass.Time()
    bgm = music.Camera_music()
    image = load_image('png\\Camera.png')
    announcement_image = load_image('png\\Dance.png')
    logo_image = load_image('png\\Logo.png')
    black_image = load_image('png\\Black.png')
    white_image = load_image('png\\White.png')
    m_currenttime=0
    m_cameratime = 0

def exit():
    global m_time,bgm,image
    del (m_time)
    del (bgm)
    del (image)

def update():
    global m_time,frame_time,m_currenttime,announcement_image,m_cameratime,picturenumber
    frame_time = m_time.get_frame_time(  )
    m_currenttime += frame_time

    if(m_currenttime>4):
        announcement_image.changetexture('png\\Cameranumber.png')
    if m_currenttime>7:
        m_cameratime += frame_time*10
    if (m_currenttime > 8 ):
        game_framework.change_state(stage1)

def draw():

    global  picturenumber
    clear_canvas()

    image.clip_draw(20, 0, 2560, 1920, (int)(gamesizex / 2), (int)(gamesizey / 2),gamesizex,gamesizey)  # 배경
    announcement_image.clip_draw(0, 0, 800, 180, (int)(gamesizex / 2), (int)(gamesizey*4 /5) )  # 배경
    logo_image.clip_draw(0,0,600,300,etc_data["logoxpos"],etc_data["logoypos"],500,200)

    if m_currenttime>7:
        if int(m_cameratime)%2 == 0:
             white_image.clip_draw(0,0,1280,960,(int)(gamesizex / 2), (int)(gamesizey / 2))
        else :
            black_image.clip_draw(0,0,1280,960,(int)(gamesizex / 2), (int)(gamesizey / 2))
    if m_currenttime>7.5:
        picturenumber=m_mathclass.createimage()



    update_canvas()

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if (event.type, event.key) == (SDL_KEYDOWN,SDLK_1):                                                         ##
            pass

def pause(): pass


def resume(): pass

def kinectimage():
    myfun = mydll[""]
    myfun()
