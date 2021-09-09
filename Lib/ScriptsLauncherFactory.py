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
    clf = ScriptsLauncherFactory()

    #cl1 = clf.createScriptLauncher("QuickScriptLauncher", "TestGame", "TestGame_1", scriptArgs = {"hunter":[176, 1778]})
    #cl1.runScript()

    dict = {"TestGame": {
        "GameName": "TestGame",
        "TestGame_1": {
            "scriptType": "QuickScriptLauncher",
            "scriptArgs": {
                "Times": 2
            }
        },
    },
        "FGO": {
            "GameName": "FGO",
            "Test": {
                "scriptType": "QuickScriptLauncher",
                "scriptArgs": {
                    "Times": 2
                }
            },
            "Test2": {
                "scriptType": "QuickScriptLauncher",
                "scriptArgs": {
                    "Times": 10
                }
            }
        }
    }

    reslut = []

    for d in dict:
        reslut.append(clf.createScriptLauncherSuit(dict[d]))


    print(reslut)


    for r in reslut:
        for sr in r:
            r.runScript()
