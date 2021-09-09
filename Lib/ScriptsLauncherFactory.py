from Lib.ScriptLauncher import *


class ScriptsLauncherFactory:

    STARTUP_CLASS_NAME = "GameStartUp"
    TEARDOWN_CLASS_NAME = "GameTearDown"

    def createSingleScriptLauncher(self, scriptType, gameName, **kw):
        return globals()[scriptType](gameName, **kw)

    def createScriptLauncherSuit(self, gameDict):
        reslut = []
        gameName = gameDict.pop("GameName")

        # 凭gameName，增加游戏开始脚本
        reslut.append(self.createSingleScriptLauncher(self.STARTUP_CLASS_NAME,
                                                      gameName))

        # 增加dict中的脚本
        for scriptKey in gameDict:
            print("已加载： "+scriptKey)
            reslut.append(self.createSingleScriptLauncher(gameDict[scriptKey]["scriptType"],
                                                          gameName,
                                                          scriptName=scriptKey,
                                                          scriptArgs=gameDict[scriptKey]["scriptArgs"]))

        # 凭gameName，增加游戏结束脚本
        reslut.append(self.createSingleScriptLauncher(self.TEARDOWN_CLASS_NAME,
                                                      gameName))

        return reslut


if __name__ == "__main__":
    pass
