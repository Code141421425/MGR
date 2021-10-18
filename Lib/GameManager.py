import os

from ScriptsLauncherFactory import ScriptsLauncherFactory
from BaseClass import *
from Logger import MGRLogger
from Notice import *


@singleton
class GameManager:
    scriptFactory = None
    scriptLauncherList = []
    ifStartApp = False
    app = None

    def __init__(self, dict=None, ifStartApp=True,app=None):
        self.scriptFactory = ScriptsLauncherFactory()
        self.ifStartApp = ifStartApp

        if dict:
            self.setScriptLauncherList(dict)

        if app:
            self.app = app
            self.logger = MGRLogger(app=app).logger
        else:
            self.logger = MGRLogger().logger

    def setScriptLauncherList(self, dict, is_startWith=None):
        result = []

        if is_startWith != None:
            self.ifStartApp = is_startWith

        # 将传入字典，按照每个游戏一个List的方式，实例化，之后存入scriptLauncherList
        for d in dict:
             result.append(ScriptsLauncherFactory().
                           createScriptLauncherSuit(dict[d], self.ifStartApp))

        self.scriptLauncherList = result

    def scriptsStart(self):
        for gsl in self.scriptLauncherList:
            self.logger.info("="*10+gsl[0].scriptName.split("_")[0]+"'s Script Start"+"="*10)# XXXScript Start Log
            # 每个游戏脚本实例列表
            for sl in gsl:
                # 每个实例的执行方法
                self.logger.info("=====>Script Start: "+sl.scriptName)
                try:
                    sl.runScript()
                except SystemExit:
                    self.logger.info("Script force exit")
                    break
                except:
                    # 暂停游戏，并通知
                    self.logger.error("Error occur")
                    #DingDingNotice().SendTextNotice("脚本发生错误，需要人工接管", True)
                    os.system("pause")

                MGRLogger().logger.info(f"{sl.scriptName} is finished")
                self.app.one_script_done(sl.scriptName)
        if self.app:
            self.app.countOver = True

    def singleScriptStart(self, scriptTypeCode, gameName, **kwargs):
        if scriptTypeCode == 0:
            scriptType = ScriptsLauncherFactory.STARTUP_CLASS_NAME
        elif scriptTypeCode == 1:
            scriptType = Script.DEFAULT_SCRIPT_TYPE
        elif scriptTypeCode == 2:
            scriptType = ScriptsLauncherFactory.TEARDOWN_CLASS_NAME
        else:
            return

        self.scriptFactory.createSingleScriptLauncher(
            scriptType,  gameName, **kwargs).runScript()

    def sync_ScriptProcess_GM_to_UI(self, scriptName, process):
        self.app.sync_ScriptProcess(scriptName, process)


if __name__ == "__main__":
    gm = GameManager()
    gm.scriptsStart()
