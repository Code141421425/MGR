# -*- coding: utf-8 -*-
import argparse
import sys

from AirtestCaseRunner import AirtestCase, run_script
from GameSettings.PackageNameMapping import PackageNameMapping as mapping
from airtest.core.api import *


class ScriptLauncher(AirtestCase):
    # DO：
    # 1、继承AirtestCase的类，可以实现传入参数的脚本启动
    # 2、为其他的Airtest脚本启动器，作为父类

    gameName = ""
    scriptName = ""
    deviceId = ""

    SCRIPT_ROOT = os.path.abspath(__file__ + "\\..\\..") + "\\Scripts\\"
    _DEFAULT_DEVICE_ID = "Android:///0123456789ABCDEF"

    def __init__(self, gameName, scriptName, deviceId=None):
        # TODO：
        # 当前的设备ID还是默认的，以后可以实现根据UI上的参数，进行初始化
        super().__init__()
        self.gameName = gameName
        self.scriptName = scriptName

        if not deviceId:
            self.deviceId = self._DEFAULT_DEVICE_ID

    def runScript(self):
        pass

    def _HandleArgs(self, script):
        # 按照规定的格式，返回启动器所必须的参数
        # 其他参数暂时写死

        # TODO：
        # log=None的地方，可以支持是否保存脚本log的功能
        return argparse.Namespace(
            compress=10, device=self.deviceId, no_image=None,
            log=None, recording=None, script=script)


class QuickScriptLauncher(ScriptLauncher):
    # DO：
    # 1、作为最常用的启动器，意在使用最少的参数，普通启动几乎所有的脚本
    # 2、在继承的AirtestCase中，采取了类似单测的框架，游戏脚本在执行前，会先执行setUp，脚本执行完毕后会执行tearDown
    # 3、在setup时，可以将从UI来的启动参数，对脚本进行注入

    launcherArgs = ""
    scriptArgs = ""

    def __init__(self, gameName=None, scriptName=None, scriptArgs=None, devicdId=None,):
        super(QuickScriptLauncher, self).__init__(gameName, scriptName, devicdId)
        # 在这里将启动参数，传入启动器的NameSpace中
        # 当前，之传入了一个script的路径
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
              "deviceId:%s,  launcherArgs:%s" %
              (self.gameName, self.scriptName, self.scriptArgs,
               self.deviceId, self.launcherArgs))


class GameStartUp(QuickScriptLauncher):
    # DO：
    # 1、作为
    # 2、能够通过自身的gameName，在PackageNameMapping中，寻找对应的包名，进行App的启动

    def __init__(self, gameName, deviceId=None):
        self.scriptName = gameName + "_StartUp"
        self.scriptArgs = {"packageName": mapping[str(gameName)]}
        super(GameStartUp, self).__init__(gameName, self.scriptName, self.scriptArgs)

    def runScript(self):
        print("游戏启动： " + self.scriptArgs["packageName"])
        super(GameStartUp, self).runScript()


class GameTearDown(ScriptLauncher):
    # DO：
    # 1、用于游戏脚本的卸载：在脚本执行结束之后，利用adb命令，杀掉该游戏的进程
    # 2、启动器的脚本名称，固定为：游戏名_TearDown
    # 3、但是之后感觉并不实用（直接启动其他游戏，能把现在执行的游戏退到后台，这就挺好的了）
    # 4、不过也可以启动除了Airtest脚本之外的adb命令，也是亮点之一

    ADB_PATH = ""

    def __init__(self, gameName):
        self.gameName = gameName
        self.scriptName = gameName + "_TearDown"
        self.ADB_PATH = os.path.abspath(__file__ + "\\..") + "\\ADB\\"

    def runScript(self):
        pass
        # 不实用，暂时注释掉

        # time.sleep(2.7)
        # cmd = "%sadb.exe shell am force-stop %s" % (self.ADB_PATH, mapping[self.gameName])
        # print(cmd)
        # os.system(cmd)


if __name__ == '__main__':
    pass
