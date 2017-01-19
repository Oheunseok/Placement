import platform
import os
from ctypes import *
import random
import time



class POINT(Structure):
    _fields_ = [("x",c_long),("y",c_long)]



#Depthfunc(95)
#len = Contoursfunc()
#print("hi")
#del arrayType
#print("hihi")
#del(array)
#print("hihihi")
#arrayType = POINT * len
#print(arrayType)

#array1 = arrayType()
#time.sleep(4)
#getContursfunc(array, len)
#del array



fakedll = windll["FakeKinectDLL"]
counfunc = fakedll["ContoursCenterLen"]
counfunc.restype = c_long
len = counfunc()

getCountoursCenterfun = fakedll["getContoursCenter"]
getCountoursCenterfun.argtypes = [POINTER(POINT),c_long]


##되는거
for j in range(25):
    len = random.randint(100, 254)
    arrType = POINT * len


    arr = arrType()
    getCountoursCenterfun(arr,len)

    for i in range(len):
        print(list(arr)[i].x,list(arr)[i].y)
    print(j)
    print("count")

    del arr