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
    global image,sample,m_time,bgm,frame_time,m_right,minion,colisionlist, bitarray,earth,star,starttrigger
    global  m_down,m_up,m_right ,m_left,sun,saturn,playerlist,spaceship, inputlist,inputlen,startimage
    global mouse_x, mouse_y,current_time
    startimage = imageclass.startimage()
    current_time=0
    inputtype = m_mathclass.POINT * 255
    inputlen=0
    inputlist = inputtype()
    starttrigger = False

    mouse_x,mouse_y = -50,-50
    frame_time=0
    image = load_image('png\\SpaceBackground.png')         ## 배경화면
                                 ##플레이어

    minion = []
    playerlist =[]

    print(title.picturenumber)

    for picturenum in range(1):
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

    colisionlist = [minion[num] for num in range(stage1_data["minionnumber"])]
    sample = Sample()                               ##샘플 잇풋 클래스
    bgm = music.Space_music()
    m_time = timeclass.Time()





def exit():
    global image,player,sample,bgm,m_time,playerlist,star,sun,earth,saturn,spaceship
    del(star)
    del(sun,earth,saturn,spaceship)
    del(m_time)
    del(bgm)
    del(image)
    del(player)
    del(playerlist)
    del(sample)
    close_canvas()


def update():
    global mouse_x,mouse_y,colisionlist,inputlen,inputlist,starttrigger,current_time

    m_mathclass.Depthfunc(etc_data["Depthfunc"])
    inputlen = m_mathclass.Contoursfunc()
    m_mathclass.getContursfunc(inputlist, inputlen, 1)

    (mouse_x,mouse_y)=sample.inputreturn()

    frame_time=m_time.get_frame_time()
    current_time+=frame_time
    if not starttrigger:
        for num in range(inputlen):
                if startimage.collision(gamesizex-int(list(inputlist)[num].x*(gamesizex/512)), gamesizey-int(list(inputlist)[num].y*(gamesizey/424))):
                    starttrigger = True
        if current_time>5:
            starttrigger = True


    sinyposnum =0
    if not starttrigger:
        for player in playerlist:
            player.ypos += math.sin(math.radians(current_time)*100)
            sinyposnum+=1

    if starttrigger:
        for player in playerlist:
            player.update(frame_time)
            player.playeroutcollide()
            if player.movespeed > 500 and player.movebool:
                player.rotatesize += frame_time * 10

            elif player.springbool == False:
                for meltnum in range(pow(player.meltsize, 2)):  # 녹아내리는 트리거가 없어지면 실행
                    player.meltV[meltnum] = 0
                    player.meltS[meltnum] = 0
            if player.movebool == False:  ## 플레이어가 멈추면 같이 멈추는 트리거들
                player.scalebool = False


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






        for player in playerlist:
            for num in range(inputlen):
                if (player.collision(gamesizex-int(list(inputlist)[num].x*(gamesizex/512)), gamesizey-int(list(inputlist)[num].y*(gamesizey/424)))
                        and not player.movebool and not player.duplicatemovebool):
                    randonnumber = random.randint(0, 100)
                    if (randonnumber < 50):
                        player.movebool = True
                        player.scalebool = True
                        player.image.set_color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

                        if (len(playerlist) < stage1_data["playernumber"]):
                            playerlist.append(Player(player.num))  ##플레이어 추가 및, 분할
                            playerlist[-1].xpos, playerlist[-1].ypos = player.xpos, player.ypos
                            mouse_x, mouse_y = -50, -50
                            playerlist[-1].w, playerlist[-1].h, playerlist[-1].bb_w, playerlist[-1].bb_h =\
                                player.w, player.h, player.bb_w, player.bb_h
                            playerlist[-1].movebool = True
                            playerlist[-1].scalebool = True
                            playerlist[-1].image.set_color(random.randint(0, 255), random.randint(0, 255),random.randint(0, 255))
                            playerlist[-1].movevector.x, playerlist[-1].movevector.y = -player.movevector.x, -player.movevector.y

                    elif randonnumber < 75:
                        player.teleport()

                    else:
                        player.duplicatemovebool = True

    if current_time>etc_data["gametime"]:
        #title.stagenumber+=1
        game_framework.change_state(title)


    #if(minion.colide_player(player)):
    #    minion.explosion_bool =True                                       ##미니언 충돌체크
    #minion.update(frame_time)                                   ##미니언 에니메이션




def draw():
    global image,player,sample,minion,colisionlist,inputlist,inputlen,starttrigger
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

    if not starttrigger:
        startimage.draw()

    for num in range(stage1_data["minionnumber"]):
        colisionlist[num].draw()
    num =0

    if inputlen>0:
        for num in range(inputlen):
            draw_rectangle(gamesizex-int(list(inputlist)[num].x*(gamesizex/512)) - 10,gamesizey-int(list(inputlist)[num].y*(gamesizey/424)) - 10,
                           gamesizex-int(list(inputlist)[num].x*(gamesizex/512))+ 10, gamesizey-int(list(inputlist)[num].y*(gamesizey/424)) + 10)
            #print(list(inputlist)[num].x,list(inputlist)[num].y)

    #minion.draw()
    ##bitarray.draw(400,300)
    draw_rectangle(mouse_x-10,mouse_y-10,mouse_x+10,mouse_y+10)
    draw_point(mouse_x,mouse_y)
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

            for player in playerlist:
                if (player.collision(mouse_x, mouse_y) and not player.movebool and not player.duplicatemovebool and  starttrigger):
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
                            playerlist[-1].movevector.x,playerlist[-1].movevector.y =-player.movevector.x,-player.movevector.y

                    elif randonnumber<75:
                        player.teleport()

                    else :
                        player.duplicatemovebool =True
                if not starttrigger:
                    if startimage.collision(mouse_x, mouse_y):
                        starttrigger = True





def pause(): pass


def resume(): pass





