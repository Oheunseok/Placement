import game_framework
from pico2d import *
from sampleupdate import sampleinput as Sample
import music
import timeclass
import stage1
import stage2
import stage3
import imageclass
import shadowtimer
import time
from ctypes import *
import m_mathclass
etc_file = open('json\\Gamesystem.txt','r')                                                                 #제이슨 파일 불러오기
etc_data = json.load(etc_file)
etc_file.close()
gamesizex=etc_data["gamesize"]                                                                               #제이슨 파일에서 게임 크기 지정


gamesizey=(int)(etc_data["gamesize"]/4*3)
cameraalpha = etc_data["alpha"]

stagelist = [stage1,stage2]
stagenumber=0
picturenumber = 1


def enter():
    global image,bgm,m_time,frame_time,m_currenttime,announcement_image,logo_image
    global black_image,white_image,m_cameratime,threetwoone




    #time.sleep(15)
    m_time = timeclass.Time()
    bgm = music.Camera_music()
    image = load_image('png\\Camera.png')
    threetwoone = imageclass.threetwoone()
    announcement_image = load_image('png\\Dance.png')
    logo_image = load_image('png\\Logo.png')
    black_image = load_image('png\\Black.png')
    white_image = load_image('png\\White.png')
    m_currenttime=0
    m_cameratime = 0


def exit():
    global image,  bgm, m_time, frame_time, m_currenttime, announcement_image, logo_image
    global black_image, white_image, m_cameratime, threetwoone
    del (image,  bgm, m_time, frame_time, m_currenttime, announcement_image, logo_image)
    del ( black_image, white_image, m_cameratime, threetwoone)

def update():
    global m_time,frame_time,m_currenttime,announcement_image,m_cameratime,picturenumber,threetwoone

    frame_time = m_time.get_frame_time(  )
    m_currenttime += frame_time
    threetwoone.update(frame_time)
    if(m_currenttime>4):
        announcement_image.changetexture('png\\Cameranumber.png')
    if (m_currenttime > 5):
        threetwoone.anim_num = 1
    if(m_currenttime>6):
        threetwoone.anim_num = 2
    if m_currenttime>7:
        m_cameratime += frame_time*10
    if (m_currenttime > 8 ):
        game_framework.change_state(stagelist[stagenumber%2])

def draw():

    global  picturenumber,threetwoone
    clear_canvas()

    image.clip_draw(20, 0, 2560, 1920, (int)(gamesizex / 2), (int)(gamesizey / 2),gamesizex,gamesizey)  # 배경
    announcement_image.clip_draw(0, 0, 800, 180, (int)(gamesizex / 2), (int)(gamesizey*4 /5) )  # 배경
    logo_image.clip_draw(0,0,600,300,etc_data["logoxpos"],etc_data["logoypos"],500,200)


    if m_currenttime>7:
        #if int(m_cameratime)%2 == 0:
             #white_image.clip_draw(0,0,gamesizex,gamesizey,(int)(gamesizex / 2), (int)(gamesizey / 2))
        #else :
        white_image.set_color(cameraalpha,cameraalpha,cameraalpha)
        white_image.clip_draw(0,0,gamesizex,gamesizey,(int)(gamesizex / 2), (int)(gamesizey / 2))

    if m_currenttime>7.5:
        picturenumber=m_mathclass.createimage()

    if m_currenttime>4 and m_currenttime<7:
        threetwoone.draw()

    update_canvas()

def handle_events():
    global rectbool
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()


def pause(): pass


def resume(): pass


