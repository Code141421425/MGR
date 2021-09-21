from Lib.ScriptLauncher import *


class ScriptsLauncherFactory:

    STARTUP_CLASS_NAME = "GameStartUp"
    TEARDOWN_CLASS_NAME = "GameTearDown"

    def createSingleScriptLauncher(self, scriptType, gameName, **kw):
        return globals()[scriptType](gameName, **kw)

    def createScriptLauncherSuit(self, gameDict, ifStartApp=True):
        result = []
        gameName = gameDict.pop("GameName")

        if ifStartApp:
            # 凭gameName，增加游戏开始脚本
            result.append(self.createSingleScriptLauncher(self.STARTUP_CLASS_NAME,
                                                          gameName))

        # 增加dict中的脚本
        for scriptKey in gameDict:
            print("已加载： "+scriptKey)
            result.append(self.createSingleScriptLauncher(gameDict[scriptKey]["scriptType"],
                                                          gameName,
                                                          scriptName=scriptKey,
                                                          scriptArgs=gameDict[scriptKey]["scriptArgs"]))

        if ifStartApp:
        # 凭gameName，增加游戏结束脚本
            result.append(self.createSingleScriptLauncher(self.TEARDOWN_CLASS_NAME,
                                                          gameName))

        return result


if __name__ == "__main__":
    pass
