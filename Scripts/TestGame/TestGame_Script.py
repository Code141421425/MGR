
import os, sys

from Lib.Script import *
from  Lib.ScriptLauncher import  ScriptLauncher
from ConcreteGame import TestGame


tg = TestGame("TestGame")
#
# tg.Notify()
# tg.AddScript()
# tg.Notify()

sl = ScriptLauncher("TestGame", "TestGame_1")
#print(sl.SCRIPT_ROOT)

ats = QuickScript("TestGame", "TestGame_1")
#ats.run()

atsw = QuickScript_withArgs("TestGame", "TestGame_2", [(176, 1778)])
#atsw.run()


SL = ScriptLauncher()
SL.Run()