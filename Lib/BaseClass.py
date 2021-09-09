class Script:
    scriptName = ""
    scriptArgs = {}
    scriptType = ""

    DEFAULT_SCRIPT_TYPE = "QuickScriptLauncher"

    def __init__(self, scriptName, scriptArgs=None, scriptType=DEFAULT_SCRIPT_TYPE):
        self.scriptName = scriptName
        self.scriptType = scriptType
        self.scriptArgs = scriptArgs


class GamesDict:
    gameDict = {}

    def AddScript(self, gameName, script):
        # 如果是 新的游戏，则多创建一个GameName的键值对
        if not self.gameDict.get(gameName):
            self.gameDict[gameName] = {}
            self.gameDict[gameName]["GameName"] = gameName

        # 在字典的新的游戏中，创建一个脚本的字典
        self.gameDict[gameName][script.scriptName] = {}
        self.gameDict[gameName][script.scriptName]["scriptType"] = script.scriptType
        self.gameDict[gameName][script.scriptName]["scriptArgs"] = script.scriptArgs


if __name__ == "__main__":
    # gd = GamesDict()
    # gd.AddScript("FGO", Script("Attack", {"Times": 2}))

    gdt = GamesDict()
    gdt.AddScript("TestGame", Script("TestGame_1", {"hunter": [500, 500]}))

    gdt.AddScript("FGO", Script("FGO_Test", {"Times": 2}))
    gdt.AddScript("FGO", Script("FGO_Test2", {"Times": 10}))

    from Lib.GameManager import GameManager

    gm = GameManager(gdt.gameDict)
    gm.scriptsStart()

    print(gdt.gameDict)



