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
    global image,sample,m_time,bgm,frame_time,m_right,minion,colisionlist, bitarray,earth,star,starttrigger,contourRectCenter,contourR
    global  sun,saturn,playerlist,spaceship, inputlist,inputlen,meteolist,inputAABB,fingerlist
    global mouse_x, mouse_y,current_time
    #startimage = imageclass.startimage()
    current_time=0

    contourRectType = m_mathclass.POINT * 500           #컨투어 자료형


    inputlen=0
    contourRectCenter = contourRectType()           #컨투어 센터 리스트
    contourR = contourRectType()                    #컨투어 바운딩 박스 크기 리스트
    starttrigger = False

    mouse_x,mouse_y = -50,-50
    frame_time=0
    image = load_image('png\\SpaceBackground.png')         ## 배경화면
                                 ##플레이어

    minion = []
    playerlist =[]
    inputAABB = []

    #print(title.picturenumber)
    if title.picturenumber == 0:                                             #아무도 안찍혔을때 전의 사진을 띄움
        title.picturenumber = 1
    for picturenum in range(title.picturenumber):                       #타이틀에서 찍힌 사람 수 만큼 플레이어 리스트 생성
        sampleplayer = Player(picturenum)
        sampleplayer.xpos, sampleplayer.ypos = int((picturenum + 1) * (gamesizex / (title.picturenumber + 2))), int(gamesizey* 3/ 5)
        #sampleplayer.xpos, sampleplayer.ypos = (picturenum + 1) * int(gamesizex / 2), int(gamesizey / 2)
        playerlist.append(sampleplayer)                          #플레이어 리스트
    for num in range(stage1_data["minionnumber"]):
        minion.append(imageclass.minion(num%2))                    ##미니언
        minion[num].explosion_time=num

    star = imageclass.star()
    earth = imageclass.earth()                              #지구
    sun = imageclass.sun()
    saturn = imageclass.saturn()
    spaceship = imageclass.spaceship()

    fingerlist = [imageclass.finger() for num in range(1)]
    for num in range(title.picturenumber):              #플레이어 이미지 위에 손바닥 이미지 생성
        fingerlist[num].xpos,fingerlist[num].ypos = int((num + 1) * (gamesizex / (title.picturenumber + 2))), int(gamesizey* 3/ 5)


    colisionlist = [minion[num] for num in range(stage1_data["minionnumber"])]
    sample = Sample()                               ##샘플 잇풋 클래스
    bgm = music.Space_music()
    m_time = timeclass.Time()
    meteolist = [imageclass.meteor(x) for x in range(6)]





def exit():
    global image, sample, m_time, bgm, frame_time,  minion, colisionlist,  earth, star, starttrigger, contourRectCenter, contourR
    global  sun, saturn, playerlist, spaceship,  inputlen,  meteolist, inputAABB, fingerlist
    global mouse_x, mouse_y, current_time
    del(image, sample, m_time, bgm, frame_time, minion, colisionlist, earth, star, starttrigger, contourRectCenter, contourR)
    del(sun, saturn, playerlist, spaceship, inputlen,  meteolist, inputAABB, fingerlist)



def update():
    global mouse_x,mouse_y,colisionlist,inputlen,starttrigger,current_time,meteolist,contourRectCenter,contourR,inputAABB,fingerlist

    del(inputAABB)
    inputAABB = []
    m_mathclass.Depthfunc()
    #inputlen = m_mathclass.Contoursfunc()
    ############################################ contours
    if __name__ == '__main__':
        m_mathclass.getContourRect(contourRectCenter, contourR)         #컨투어 센터와 크기를 리스트 안에 넣어준다
    inputlen = m_mathclass.getContourRectCountfunc()                    #컨투어 센터들의 길이 반환
    (mouse_x,mouse_y)=sample.inputreturn()                              #마우스 피킹 값
    for aabb in range(inputlen):                            #바운딩 박스 생성, 컨투어 센터를 기반으로
        inputAABB.append(imageclass.AABB(gamesizex-int(list(contourRectCenter)[aabb].x*(gamesizex/512)),gamesizey-int(list(contourRectCenter)[aabb].y*(gamesizey/424)),
                                                       int(list(contourR)[aabb].y*(gamesizey/424)*2),int(list(contourR)[aabb].x*(gamesizex/512))*2))

    frame_time=m_time.get_frame_time()
    current_time+=frame_time
    if not starttrigger:
        if current_time>5:
            starttrigger = True


    sinyposnum =0
    if not starttrigger:
        for player in playerlist:                       #풍선처럼 둥둥 떠다니게핟기
            player.ypos += math.sin(math.radians(current_time)*100)
            sinyposnum+=1
        for finger in fingerlist:
            finger.update(frame_time)



    if starttrigger:                    #시작 트리거
        for player in playerlist:
            player.update(frame_time)
            player.playeroutcollide()       #플레이어의 외부벽과의 충돌


        for num in range(stage1_data["minionnumber"]):
            for player in playerlist:                               ##모든 플레이어와 미니언 같의 충돌체크
                if(colisionlist[num].colide_player(player)):
                    colisionlist[num].explosion_bool= True
                    colisionlist[num].explosion_bgm.play_music()
            colisionlist[num].update(frame_time)

        earth.update(frame_time)
        star.update(frame_time)
        sun.update(frame_time)
        saturn.update(frame_time)
        spaceship.update(frame_time)
        for meteo in meteolist:
            meteo.update(frame_time)


    if current_time>etc_data["gametime"]:
        title.stagenumber+=1
        game_framework.change_state(title)


    #if(minion.colide_player(player)):
    #    minion.explosion_bool =True                                       ##미니언 충돌체크
    #minion.update(frame_time)                                   ##미니언 에니메이션




def draw():
    global image,player,sample,minion,colisionlist,inputlist,inputlen,starttrigger,contourRectCenter,contourR
    global x, y
    global font, smallfont, bigfont,fingerlist

    clear_canvas()

    image.clip_draw(0,0,gamesizex,gamesizey,(int)(gamesizex/2),(int)(gamesizey/2))           #배경
    star.draw()
    earth.draw()
    sun.draw()
    saturn.draw()
    spaceship.draw()
    for meteo in meteolist:
        meteo.draw()

    for player in playerlist:
        player.draw()

    if not starttrigger:
        for finger in fingerlist:
            finger.draw()

    for num in range(stage1_data["minionnumber"]):
        colisionlist[num].draw()
    num =0
    if inputlen > 0:
       for num in range(inputlen):                                                   #인풋값을 확인
           draw_rectangle(gamesizex-int(list(contourRectCenter)[num].x*(gamesizex/512)) - int(list(contourR)[num].x*(gamesizex/512)),
                          gamesizey-int(list(contourRectCenter)[num].y*(gamesizey/424)) - int(list(contourR)[num].y*(gamesizey/424)),
                          gamesizex-int(list(contourRectCenter)[num].x*(gamesizex/512))+ int(list(contourR)[num].x*(gamesizex/512)), gamesizey-int(list(contourRectCenter)[num].y*(gamesizey/424)) + int(list(contourR)[num].y*(gamesizey/424)))

    update_canvas()


def handle_events():
    global player,mouse_x,mouse_y,starttrigger
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            sample.handle_events(event)                     ##샘플값의 인풋값
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):  ## red 플레이어 색깔변경
                if star:
                    print(star)
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):  ## red 플레이어 색깔변경
                for player in playerlist:
                    player.image.set_color(255, 0, 0)
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_6):  # 흘러내리는 효과 온오프 및 초기화
                for player in playerlist:
                    player.springbool = True
                    #player.meltbool = not player.meltbool

        if (event.type, event.button) == (SDL_MOUSEBUTTONDOWN, SDL_BUTTON_LEFT):  ##마우스 피킹값반환
            (mouse_x, mouse_y) = sample.inputreturn()
            randonnumber = 0

            for player in playerlist:                                                    #플레이어 마우스 피킹 충돌체크
                if (player.collision(mouse_x, mouse_y) ):
                    player.AItrigger = True
                    randonnumber =random.randint(0,100)
                    if (randonnumber<50):
                        if (len(playerlist)<stage1_data["playernumber"]):
                            playerlist.append(Player(player.num))         ##플레이어 추가 및, 분할
                            playerlist[-1].xpos, playerlist[-1].ypos = player.xpos, player.ypos
                            mouse_x,mouse_y = -50,-50
                            playerlist[-1].w,playerlist[-1].h,playerlist[-1].bb_w,playerlist[-1].bb_h=player.w,player.h, player.bb_w,player.bb_h
                            playerlist[-1].movevector.x,playerlist[-1].movevector.y =-player.movevector.x,-player.movevector.y
                            playerlist[-1].AItrigger = True






def pause(): pass


def resume(): pass





