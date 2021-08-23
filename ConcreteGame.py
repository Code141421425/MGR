
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

    def Notify(self):
        pass

