# -*- coding: utf-8 -*-
import argparse
import os
import time
from Lib.AirtestCaseRunner import AirtestCase, run_script
from GameSettings.PackageNameMapping import PackageNameMapping as mapping
from airtest.core.api import *


class ScriptLauncher(AirtestCase):
    gameName = ""
    scriptName = ""
    deviceId = ""

    SCRIPT_ROOT = os.path.abspath(__file__ + "\\..\\..") + "\\Scripts\\"
    _DEFAULT_DEVICE_ID = "Android:///0123456789ABCDEF"

    def __init__(self, gameName, scriptName, deviceId=None):
        super().__init__()
        self.gameName = gameName
        self.scriptName = scriptName

        if not deviceId:
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

        if self.scriptArgs:
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
              "deviceId:%s,  launcherArgs:%s,scriptArgs:%s" %
              (self.gameName, self.scriptName, self.scriptArgs,
               self.deviceId, self.launcherArgs, self.scriptArgs))


class GameStartUp(QuickScriptLauncher):
    def __init__(self, gameName, deviceId=None):
        self.scriptName = gameName + "_StartUp"
        self.scriptArgs = {"packageName": mapping[str(gameName)]}
        super(GameStartUp, self).__init__(gameName, self.scriptName, self.scriptArgs)

    def runScript(self):
        print("游戏启动： " + self.scriptArgs["packageName"])
        super(GameStartUp, self).runScript()


class GameTearDown(ScriptLauncher):
    ADB_PATH = ""

    def __init__(self, gameName):
        self.gameName = gameName
        self.scriptName = gameName + "_TearDown"
        self.ADB_PATH = os.path.abspath(__file__ + "\\..") + "\\ADB\\"

    def runScript(self):
        pass
        # time.sleep(2.7)
        # cmd = "%sadb.exe shell am force-stop %s" % (self.ADB_PATH, mapping[self.gameName])
        # print(cmd)
        # os.system(cmd)


if __name__ == '__main__':
    pass
