import platform
import os
from ctypes import *
import random
import time



class POINT(Structure):
    _fields_ = [("x",c_long),("y",c_long)]


mydll = windll["KintctDLL"]

initfuc = mydll["InitKinect"]
initfuc()
time.sleep(3)

Depthfunc = mydll["DepthImage"]
Contoursfunc = mydll["ContoursCenterLen"]
Contoursfunc.restype = c_long
getContursfunc = mydll["getContoursCenter"]
getContursfunc.argtypes = [POINTER(POINT),c_long]

Depthfunc(95)
len = Contoursfunc()
arrayType = POINT * 255
array = arrayType()

#time.sleep(4)
getContursfunc(array, len)

for num in range(len):
    print(list(array)[num].x,list(array)[num].y)
for i in range(5):
   time.sleep(0.03)
   Depthfunc(95)
   time.sleep(2)
   len = Contoursfunc()
   getContursfunc(array, len)
   for num in range(len):
       print(list(array)[num].x, list(array)[num].y)