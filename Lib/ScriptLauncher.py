# -*- coding: utf-8 -*-
import argparse
import os
from Lib.AirtestCaseRunner import AirtestCase, run_script
from GameSettings.PackageNameMapping import PackageNameMapping as mapping
from airtest.core.api import *


class ScriptLauncher(AirtestCase):
    gameName = ""
    scriptName = ""
    deviceId = ""

    SCRIPT_ROOT = os.path.abspath(__file__ + "\\..\\..") + "\\Scripts\\"
    _DEFAULT_DEVICE_ID = "Android:///0123456789ABCDEF"

    def __init__(self, gameName, scriptName, devicdId=None):
        super().__init__()
        self.gameName = gameName
        self.scriptName = scriptName

        if not devicdId:
            self.deviceId = self._DEFAULT_DEVICE_ID

    def runScript(self):
        pass

    def _HandleArgs(self, script):
        return argparse.Namespace(
            compress=10, device=self.deviceId, no_image=None,
            log=None, recording=None, script=script)


class QuickScriptLauncher(ScriptLauncher):
    launcherArgs = ""
    scriptArgs = ""

    def __init__(self, gameName=None, scriptName=None, scriptArgs=None, devicdId=None,):
        super(QuickScriptLauncher, self).__init__(gameName, scriptName, devicdId)
        self.launcherArgs = self._HandleArgs(("%s\\%s\\%s.air")
                                              % (self.SCRIPT_ROOT, self.gameName, self.scriptName))
        self.scriptArgs = scriptArgs

    def setUp(self):
        print("custom setup")
        for scriptArg in self.scriptArgs:
            self.scope[scriptArg] = self.scriptArgs[scriptArg]
        super(QuickScriptLauncher, self).setUp()

    def tearDown(self):
        print("custom tearDown")
        super(QuickScriptLauncher, self).tearDown()

    def runScript(self):
        run_script(self.launcherArgs, self)

    def ShowAttr(self):
        print("gameName:%s, scriptName:%s, scriptArgs:%s, "
              "devicdId:%s,  launcherArgs:%s,scriptArgs:%s" %
              (self.gameName, self.scriptName, self.scriptArgs,
               self.deviceId, self.launcherArgs, self.scriptArgs))


class GameStartUp(QuickScriptLauncher):
    def __init__(self, gameName, devicdId=None):
        self.scriptName = gameName + "_StartUp"
        self.scriptArgs = {"packageName": mapping[str(gameName)]}
        super(GameStartUp, self).__init__(gameName, self.scriptName, self.scriptArgs)


class GameTearDown(ScriptLauncher):
    ADB_PATH = ""

    def __init__(self, gameName):
        self.gameName = gameName
        self.ADB_PATH = os.path.abspath(__file__ + "\\..") + "\\ADB\\"

    def runScript(self):
        cmd = "%sadb.exe shell am force-stop %s" % (self.ADB_PATH, mapping[self.gameName])
        print(cmd)
        os.system(cmd)


if __name__ == '__main__':
    print("="*10)

    qsl = QuickScriptLauncher("TestGame", "TestGame_1", {"hunter":[176, 1778]})
    print(qsl.ShowAttr())
    #qsl.runScript()

    qsl2 = QuickScriptLauncher("FGO", "FGO_StartUp")
    #qsl2.runScript()

    stt = GameStartUp("FGO")
   # stt.runScript()

    gtd = GameTearDown("FGO")
    gtd.runScript()
