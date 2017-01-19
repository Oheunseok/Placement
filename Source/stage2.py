import game_framework
from pico2d import *
from sampleupdate import sampleinput as Sample
from imageclass import player as Player
import music
import timeclass
from ctypes import *

etc_file = open('etc\\inputsample.txt','r')                                                                 #제이슨 파일 불러오기
etc_data = json.load(etc_file)
etc_file.close()
gamesizex=etc_data["gamesize"]                                                                               #제이슨 파일에서 게임 크기 지정


gamesizey=(int)(etc_data["gamesize"]/4*3)

image = None

def enter():
    global image,sample,player,bgm,m_time,m_currenttime
    open_canvas(etc_data["gamesize"], (int)(etc_data["gamesize"] / 4 * 3))
    m_time = timeclass.Time()
    m_currenttime = 0





def exit():
    global m_time
    del (m_time)
    del (bgm)
    del (image)
    del (player)


def update():
    global m_time,m_currenttime
    frame_time = m_time.get_frame_time()



def draw():
    clear_canvas()

    draw_rectangle(300 - 10, 300 - 10, 300+ 10, 300 + 10)
    image.draw(0,0,800,600)
    update_canvas()



def handle_events():
    pass

def pause(): pass


def resume(): pass