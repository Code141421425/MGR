from Lib.GameManager import GameManager
from Lib.BaseClass import GamesDict, Script

if __name__ == "__main__":
    # DO：
    # 已经基本上不怎么用的，通过代码启动程序的地方

    gdt = GamesDict()
    #gdt.AddScript("TestGame", Script("TestGame_1", {"hunter": [500, 500]}))

    # gdt.AddScript("HA", Script("HA_getRedSpot"))
    # gdt.AddScript("HA", Script("HA_getEnergy"))
    # gdt.AddScript("HA", Script("HA_getDailyBonus"))
    # gdt.AddScript("HA", Script("HA_giveFriendsEnergy"))
    # gdt.AddScript("HA", Script("HA_training"))
    # gdt.AddScript("HA", Script("HA_getUnionBonus"))
    # gdt.AddScript("HA", Script("HA_FS_Crusade", {"battleTimes": 5}))
    # gdt.AddScript("HA", Script("HA_FS_Arena", {"battleTimes": 9}))
    # gdt.AddScript("HA", Script("HA_FS_expedition", {"battleTimes": 1}))
    # gdt.AddScript("HA", Script("HA_GetQuestBonus"))



    #gdt.AddScript("ArkNights",Script("ArkNights_Battle", {"battleTimes": 3}))
    #gdt.AddScript("TestGame", Script("TestGame_1", {"battleTimes": 3}))

    gdt.AddScript("PCR", Script("PCR_GetEnergy"))
    gdt.AddScript("PCR", Script("PCR_Explore"))
    # gdt.AddScript("PCR", Script("PCR_Investigate"))
    # gdt.AddScript("PCR", Script("PCR_Common"))
    # gdt.AddScript("PCR", Script("PCR_SweepVH"))


    gm = GameManager(gdt.gameDict)#, False)
    gm.scriptsStart()

    # =============================

    # gm2 = GameManager()
    # #gm.singleScriptStart(0, "HA")
    # #gm.singleScriptStart(1, "HA", scriptName="HA_FS_Arena",scriptArgs={"battleTimes": 7})
    #
    # gm2.singleScriptStart(1, "HA", scriptName="HA_MiscScript")
    # gm2.scriptsStart()





