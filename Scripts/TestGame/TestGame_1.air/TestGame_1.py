from airtest.core.api import *

import os,sys

sys.path.append("../../../Lib")

from ScriptTemplate import *

auto_setup(__file__)



tl = [Template(r"tpl1631273915075.png", record_pos=(-0.337, 0.912), resolution=(1080, 2340)),Template(r"tpl1631273920372.png", record_pos=(-0.118, 0.894), resolution=(1080, 2340)),Template(r"tpl1631273933324.png", record_pos=(0.12, -0.837), resolution=(1080, 2340))]

WaitAndTouchSuit().Execute(tl,[1,2,3])

# touch(hunter)

# #hunter = ""

# #start_app("com.bilibili.fatego")

# print("="*20)
# print(hunter)
# #print(add(100))

