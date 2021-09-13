from Lib.ScriptsLauncherFactory import ScriptsLauncherFactory
from Lib.BaseClass import Script


class GameManager:
    scriptFactory = None
    scriptLauncherList = []

    def __init__(self, dict=None):
        self.scriptFactory = ScriptsLauncherFactory()
        if dict:
            self.setScriptLauncherList(dict)

    def setScriptLauncherList(self, dict):
        result = []

        # 将传入字典，按照每个游戏一个List的方式，实例化，之后存入scriptLauncherList
        for d in dict:
             result.append(ScriptsLauncherFactory().createScriptLauncherSuit(dict[d]))

        self.scriptLauncherList = result

    def scriptsStart(self):
        for gsl in self.scriptLauncherList:
            # 每个游戏脚本实例列表
            for sl in gsl:
                # 每个实例的执行方法
                print("启动脚本： "+sl.scriptName)
                sl.runScript()
                print(">>"*20)

    def singleScriptStart(self, scriptTypeCode, gameName,  scriptName=None, **kwargs):
        if scriptTypeCode == 0:
            scriptType = ScriptsLauncherFactory.STARTUP_CLASS_NAME
        elif scriptTypeCode == 1:
            scriptType = Script.DEFAULT_SCRIPT_TYPE
        elif scriptTypeCode == 2:
            scriptType = ScriptsLauncherFactory.TEARDOWN_CLASS_NAME
        else:
            return

        self.scriptFactory.createSingleScriptLauncher(
            scriptType,  gameName).runScript()


if __name__ == "__main__":
    gm = GameManager(dict)
    gm.scriptsStart()
