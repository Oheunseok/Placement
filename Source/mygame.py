import platform
import os

if platform.architecture()[0]=='32bit':
   os.environ["PYSLD2_DLL_PATH"]="./SDL2/x86"
else :
    os.environ["PYSDL2_DLL_PATH"]="./SDL2/x64"

import game_framework

import stage1
import title
import start
import shadowtimer





game_framework.run(start)


