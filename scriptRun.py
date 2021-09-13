from Lib.GameManager import GameManager
from Lib.BaseClass import GamesDict, Script

if __name__ == "__main__":
    gdt = GamesDict()
    gdt.AddScript("TestGame", Script("TestGame_1", {"hunter": [500, 500]}))

    gdt.AddScript("FGO", Script("FGO_Test", {"Times": 2}))
    gdt.AddScript("FGO", Script("FGO_Test2", {"Times": 10}))

    gm = GameManager(gdt.gameDict)
    gm.scriptsStart()


