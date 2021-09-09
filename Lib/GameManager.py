from Lib.ScriptsLauncherFactory import ScriptsLauncherFactory


class GameManager:
    scriptFactory = None
    scriptLauncherList = []

    def setScriptLauncherList(self, dict):
        result = []
        for d in dict:
             result.append(ScriptsLauncherFactory().createScriptLauncherSuit(dict[d]))

        self.scriptLauncherList = result

    def scriptsStart(self):
        for gsl in self.scriptLauncherList:
            for sl in gsl:
                sl.runScript()


if __name__ == "__main__":
    gm = GameManager()
    dict = {"TestGame": {
        "GameName": "TestGame",
        "TestGame_1": {
            "scriptType": "QuickScriptLauncher",
            "scriptArgs": {
                "hunter": [500, 500]
            }
        },
    },
        "FGO": {
            "GameName": "FGO",
            "FGO_Test": {
                "scriptType": "QuickScriptLauncher",
                "scriptArgs": {
                    "Times": 2
                }
            },
            "FGO_Test2": {
                "scriptType": "QuickScriptLauncher",
                "scriptArgs": {
                    "Times": 10
                }
            }
        }
    }

    gm.setScriptLauncherList(dict)
    gm.scriptsStart()