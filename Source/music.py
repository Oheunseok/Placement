from pico2d import*
import json
import random



class Space_music():

    def __init__(self):

            self.bgm=load_music('ogg\\SPACE.ogg')
            self.bgm.set_volume(98)
            self.bgm.repeat_play()
class Cartoon_music():

    def __init__(self):

            self.bgm=load_music('ogg\\pixelland.ogg')
            self.bgm.set_volume(98)
            self.bgm.repeat_play()

class stage3_music():

    def __init__(self):

            self.bgm = load_music('ogg\\Professor Umlaut.ogg')
            self.bgm.set_volume(98)
            self.bgm.repeat_play()

class Camera_music():
    bgm = None
    def __init__(self):
        if self.bgm == None:
            self.bgm = load_music('ogg\\MOVE_STOP.ogg')
            self.bgm.set_volume(98)
            self.bgm.play()

class Explosion_music():
    bgm = None
    dead = None
    def __init__(self):
        if Explosion_music.bgm == None and self.dead == None:
            Explosion_music.bgm = load_wav('ogg\\explosion.ogg')
            Explosion_music.dead = load_wav('ogg\\artoo.ogg')
            Explosion_music.bgm.set_volume(24)
            Explosion_music.dead.set_volume(24)
    def play_music(self):
        Explosion_music.bgm.play()
        Explosion_music.dead.play()

class Rocket_music():
    bgm = None
    def __init__(self):
        if Rocket_music.bgm == None:
            Rocket_music.bgm = load_wav('ogg\\rocket.ogg')
            Explosion_music.bgm.set_volume(1)
        #self.bgm.repeat_play()

class Teleport_music():
    bgm = None
    def __init__(self):
        if Teleport_music.bgm == None:
            Teleport_music.bgm = load_wav('ogg\\shadow.ogg')
            Teleport_music.bgm.set_volume(128)
    def play_music(self):
        Teleport_music.bgm.play()

class Spring_music():
    bgm = None

    def __init__(self):
        if Spring_music.bgm == None:
            Spring_music.bgm = load_wav('ogg\\shadow.ogg')
            Spring_music.bgm.set_volume(128)

    def play_music(self):
        Spring_music.bgm.play()

class Bear_music():
    bgm = None
    def __init__(self):
        if Bear_music.bgm == None:
            Bear_music.bgm = load_wav('ogg\\bear.ogg')
            Bear_music.bgm.set_volume(180)
        #self.bgm.repeat_play()
    def play_music(self):
        Bear_music.bgm.play()

class Rabbit_music():
    bgm = None
    def __init__(self):
        if Rabbit_music.bgm == None:
            Rabbit_music.bgm = load_wav('ogg\\rabbit.ogg')
            Rabbit_music.bgm.set_volume(180)
        #self.bgm.repeat_play()
    def play_music(self):
        Rabbit_music.bgm.play()