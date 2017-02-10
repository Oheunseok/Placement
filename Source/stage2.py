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

stage2_file = open('json\\stage2.txt','r')
stage2_data = json.load(stage2_file)
stage2_file.close()


def enter():
    global image,sample,bgm,m_time,m_currenttime,fingerlist,contourRectCenter,contourR, minion,applelist,basket
    global inputlist,inputlen,minion,playerlist,starttrigger,inputAABB,current_time,inputobject


    starttrigger=False
    inputlen = 0
    current_time=0
    contourRectType = m_mathclass.POINT * 500
    contourRectCenter = contourRectType()
    contourR = contourRectType()
    sample = Sample()  ##샘플 잇풋 클래스
    m_time = timeclass.Time()
    m_currenttime = 0
    inputtype = m_mathclass.POINT * 255
    inputlen = 0
    inputlist = inputtype()
    image = load_image('png\\stage2back.png')  ## 배경화면
    ##플레이어

    bgm = music.Cartoon_music()
    minion = []
    playerlist = []
    inputAABB = []
    applelist = []

    basket = imageclass.basket()

    if title.picturenumber==0:
        title.picturenumber = 1

    for picturenum in range(title.picturenumber):
        sampleplayer = Player(picturenum)
        sampleplayer.xpos, sampleplayer.ypos = int((picturenum + 1) * (gamesizex / (title.picturenumber + 2))), int(
            gamesizey * 3 / 5)
        # sampleplayer.xpos, sampleplayer.ypos = (picturenum + 1) * int(gamesizex / 2), int(gamesizey / 2)
        playerlist.append(sampleplayer)  # 플레이어 리스트

    for num in range(stage2_data["minionnumber"]):                          #2분의 1 확률로 토끼 or 곰
        if num%2== 0:
            minion.append(imageclass.rabbit())  ##
        elif num%2 ==1:
            minion.append(imageclass.bear(basket))  ##미니언                   #곰은 바스켓과 이어줘서 바스켓 이미지를 바꿔준다

    for num in range(stage2_data["applenumber"]):
        applelist.append(imageclass.apple())
        applelist[num].xpos = random.randint(int(gamesizex/stage2_data["applenumber"]*num),int(gamesizex/stage2_data["applenumber"]*(num+1)))


    fingerlist = [imageclass.finger() for num in range(title.picturenumber)]
    for num in range(1):
        fingerlist[num].xpos, fingerlist[num].ypos = int((num + 1) * (gamesizex / (title.picturenumber + 2))), int(
            gamesizey * 3 / 5)





def exit():
    global image, sample, bgm, m_time, m_currenttime, fingerlist, contourRectCenter, contourR,  applelist, basket
    global inputlist, inputlen,   playerlist, starttrigger, inputAABB, current_time
    del(image, sample,  bgm, m_time, m_currenttime, fingerlist, contourRectCenter, contourR,  applelist, basket)
    del (inputlist, inputlen,   playerlist, starttrigger, inputAABB, current_time )


def update():
    global m_time,m_currenttime,starttrigger,inputAABB,current_time,inputobject, mouse_x, mouse_y,minion,basket
    global  colisionlist,applelist
    frame_time = m_time.get_frame_time()
    current_time+=frame_time

    del (inputAABB)                         #인풋 리스트를 초기화
    inputAABB = []
    m_mathclass.Depthfunc()
    m_mathclass.getContourRect(contourRectCenter, contourR)
    inputlen = m_mathclass.getContourRectCountfunc()
    (mouse_x, mouse_y) = sample.inputreturn()
    for aabb in range(inputlen):                            #충돌체크 리스트트
       inputAABB.append(imageclass.AABB(gamesizex - int(list(contourRectCenter)[aabb].x * (gamesizex / 512)),
                                         gamesizey - int(list(contourRectCenter)[aabb].y * (gamesizey / 424)),
                                         int(list(contourR)[aabb].y * (gamesizey / 424) * 2),
                                         int(list(contourR)[aabb].x * (gamesizex / 512)) * 2))

    sinyposnum = 0
    if not starttrigger:                                                                    #시작전
        for player in playerlist:
            player.ypos += math.sin(math.radians(current_time) * 100)
            sinyposnum += 1                                                                     #플레이어가 위아래로 움직이게하기
        if current_time>5:
            starttrigger = True
        for finger in fingerlist:                                                           #손바닥 움직이기
            finger.update(frame_time)

    if starttrigger:                                                                        #게임시작
        for player in playerlist:                                                           #플레이어 업데이트
            player.update(frame_time)
            player.playeroutcollide()


        for object in minion:
            object.update(frame_time)
            for player in playerlist:                   ##모든 플레이어와 미니언 같의 충돌체크
                if (object.colide_player(player)) and player.AItrigger and object.explosion_bool == False:
                    object.explosion_bool = True
                    object.bgm.play_music()
                    #object[num].explosion_bgm.play_music()
            for apple in applelist:
                if apple.explosion_bool:
                    if apple.collide(object):
                        apple.anim_bool = True


        for num in range(stage2_data["applenumber"]):
            applelist[num].update(frame_time)
            for player in playerlist:                   ##모든 플레이어와 미니언 같의 충돌체크
                if (applelist[num].colide_player(player)):
                    applelist[num].explosion_bool = True




    if current_time>etc_data["gametime"]:
        title.stagenumber+=1
        game_framework.change_state(title)
    mouse_x, mouse_y = -50, -50


def draw():
    global image
    clear_canvas()

    image.clip_draw(0, 0, image.w, image.h, (int)(gamesizex / 2), (int)(gamesizey / 2), gamesizex, gamesizey)  # 배경
    basket.draw()
    for player in playerlist:
        player.draw()

    if not starttrigger:
        for finger in fingerlist:
            finger.draw()

    if starttrigger:

        for obejct in minion:
            obejct.draw()
        for num in range(stage2_data["applenumber"]):
            applelist[num].draw()


    update_canvas()



def handle_events():
    global player, mouse_x, mouse_y, starttrigger,inputobject,cannonlist
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            sample.handle_events(event)  ##샘플값의 인풋값
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):  ##마우스 피킹값반환
                (mouse_x, mouse_y) = sample.inputreturn()

                for player in playerlist:
                    if (player.collision(mouse_x, mouse_y)):
                        player.AItrigger = True
                        randonnumber = random.randint(0, 100)
                        if (randonnumber < 50):
                            if (len(playerlist) < stage1_data["playernumber"]):
                                playerlist.append(Player(player.num))  ##플레이어 추가 및, 분할
                                playerlist[-1].xpos, playerlist[-1].ypos = player.xpos, player.ypos
                                mouse_x, mouse_y = -50, -50
                                playerlist[-1].w, playerlist[-1].h, playerlist[-1].bb_w, playerlist[
                                    -1].bb_h = player.w, player.h, player.bb_w, player.bb_h
                                playerlist[-1].movevector.x, playerlist[
                                    -1].movevector.y = -player.movevector.x, -player.movevector.y
                                playerlist[-1].AItrigger = True
            mouse_x, mouse_y = -50, -50

def pause(): pass


def resume(): pass