
import random
import math

class player:
    def __init__(self,x,y):
        self.xpos = x
        self.ypos = y
class playersort:
    def __init__(self,size,num):
        self.size=size
        self.num=num
    def sizeR(self):
        return self.size



playerlist = [player(random.randint(-100,100),random.randint(-100,100)) for x in range(10)]


list = []

k = player(30,30)
num =0
for play in playerlist:
    list.append(playersort(math.fabs(k.xpos - play.xpos) + math.fabs(k.ypos-play.ypos),num))
    num +=1
list.sort(key=playersort.sizeR)
print(len(list))
for x in range(10):
    print(list[x].size )