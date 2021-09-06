
class Game:
    gameName = ""
    scriptList = []
    gameEnterScript = None
    gameOutScript = None

    def __init__(self, name):
        self.gameName = name

    def Notify(self):
        pass


class TestGame(Game):

    def AddScript(self, script):
        self.scriptList.append(script)

    def RemoveScript(self, script):
        self.scriptList.remove(script)

    def Notify(self):
        for sp in self.scriptList:
            sp.run()








