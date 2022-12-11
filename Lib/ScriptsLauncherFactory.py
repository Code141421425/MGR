from ScriptLauncher import *


class ScriptsLauncherFactory:
    # DO:
    # 1、是启动器的工厂，通过映射，生成一个个的启动器实例组成的List，用以批量启动脚本
    # 2、每个游戏需要启动的脚本可以构成一个suit，这个suit的头尾，可以有该游戏的启动脚本和关闭脚本
    # 3、创建一个启动器的实例，需要脚本类型，游戏名称，脚本名称，脚本参数组成的一个dict

    STARTUP_CLASS_NAME = "GameStartUp"
    TEARDOWN_CLASS_NAME = "GameTearDown"

    @staticmethod
    def createSingleScriptLauncher(scriptType, gameName, **kw):
        return globals()[scriptType](gameName, **kw)

    def createScriptLauncherSuit(self, gameDict, ifStartApp=True):
        # DO：
        # 1、通过传入的gameDict，返回一个启动器的列表,用以在gameManager进行循环执行
        # 2、如果需要额外生成开始脚本，就在列表的最前边增加该游戏的启动脚本

        result = []
        gameName = gameDict.pop("GameName")

        if ifStartApp:
            # 凭gameName，增加游戏开始脚本
            result.append(self.createSingleScriptLauncher(self.STARTUP_CLASS_NAME,
                                                          gameName))

        # 增加dict中的脚本
        for scriptKey in gameDict:
            result.append(self.createSingleScriptLauncher(gameDict[scriptKey]["scriptType"],
                                                          gameName,
                                                          scriptName=scriptKey,
                                                          scriptArgs=gameDict[scriptKey]["scriptArgs"]))
            print("已加载： " + scriptKey)

        if ifStartApp:
            # 凭gameName，增加游戏结束脚本
            result.append(self.createSingleScriptLauncher(self.TEARDOWN_CLASS_NAME,
                                                          gameName))
        gameDict["GameName"] = gameName

        return result


if __name__ == "__main__":
    pass
