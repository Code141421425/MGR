import os,sys
from airtest.core.api import *
from ScriptSupport import RandomPosTime


class Operation:
    @staticmethod
    def _ListHandle(target, operated, filler=None):
        if not operated:
            operated = []
            operated.append(filler)

        if len(target) < len(operated):
            print("Error: operated should shorter than target")
            return

        while len(operated) != len(target):
            operated.append(filler)

        return operated

    def Execute(self):
        pass


class WaitAndTouch(Operation):
    def Execute(self, pos, sleep_time=1, template=None):
        if template:
            try:
                wait(template)
            except TargetNotFoundError:
                print("Do not find the picture")
                return

        touch(RandomPosTime().randomPos(pos))
        sleep(RandomPosTime().randomTime(sleep_time))


class Touch(Operation):
    def Execute(self, pos, sleep_time=1):
        touch(RandomPosTime.randomPos(pos))
        sleep(RandomPosTime.randomTime(sleep_time))


class Swipe(Operation):
    def Execute(self):
        pass


class ExistsAndTouch(WaitAndTouch):
    _DEFAULT_TRY_TIMES = 2
    _DEFAULT_SLEEP_TIME = 1

    def Execute(self, targetTemplate, pos,
                sleep_time=_DEFAULT_SLEEP_TIME, tryTimes=_DEFAULT_TRY_TIMES):

        isFounded = False

        if targetTemplate:
            # 如果存在就开始找
            for i in range(tryTimes):
                if exists(targetTemplate):
                    isFounded = True
                    break
        else:
            # 不存在，就直接点
            isFounded = True

        if not isFounded:
            return
        else:
            super(ExistsAndTouch, self).Execute(pos, sleep_time)


class ExistsAndTouchSuit(ExistsAndTouch):
    def Execute(self, targetTemplateList, touchPosList, sleep_timeList=None, tryTimesList=None):
        tryTimesList = self._ListHandle(targetTemplateList, tryTimesList, self._DEFAULT_TRY_TIMES)
        sleep_timeList = self._ListHandle(targetTemplateList, sleep_timeList, self._DEFAULT_SLEEP_TIME)

        for i in range(len(targetTemplateList)):
            super(ExistsAndTouchSuit, self).Execute(
                targetTemplateList[i], touchPosList[i],
                sleep_timeList[i], tryTimesList[i])


class WaitAndTouchSuit(WaitAndTouch):

    def Execute(self, posList,  sleep_timeList=None, templateList=None):
        # 将所有的数组，处理成统一posList的长度
        templateList = self._ListHandle(posList, templateList)
        sleep_timeList = self._ListHandle(posList, sleep_timeList)

        for i in range(0, len(posList)):
            super(WaitAndTouchSuit, self).Execute(
                posList[i], sleep_timeList[i], templateList[i], )



#######
# ScriptTemplate
#######


class ScriptTemplate:
    def runScriptTemplate(self):
        pass


class GameStart(ScriptTemplate):
    packageName = []
    START_SLEEP = 6
    mainCityTemplate = []
    passCloseNotice = False
    passGameUpdate = True

    def __init__(self, packageName, template):
        self.packageName = packageName
        self.mainCityTemplate = template

    def StartAPP(self):
        start_app(self.packageName)

    def GameUpdate(self):
        pass

    def Login(self):
        pass

    def CloseNotice(self):
        pass

    def InMainCity(self):
        try:
            wait(self.mainCityTemplate)
        except "TargetNotFoundError":
            return False

    def runScriptTemplate(self):
        self.StartAPP()
        sleep(self.START_SLEEP)

        if not self.passGameUpdate:
            self.GameUpdate()

        self.Login()

        if not self.passCloseNotice:
            self.CloseNotice()

        self.InMainCity()


class Battle(ScriptTemplate):
    battleTimes = []

    def __init__(self, battleTimes=1):
        self.battleTimes = battleTimes

    def ToBattleField(self):
        pass

    def BattleOnce(self):
        pass

    def BackToMainCity(self):
        pass

    def runScriptTemplate(self):
        self.ToBattleField()

        for i in range(self.battleTimes):
            self.BattleOnce()

        self.BackToMainCity()


class SimpleQuest(ScriptTemplate):
    mainCity = None

    def __init__(self, mainCity):
        self.mainCity = mainCity

    def ExecuteSimpleQuest(self):
        pass

    def BackToMainCity(self):
        pass

    def InMainCity(self):
        wait(self.mainCity)

    def runScriptTemplate(self):
        self.ExecuteSimpleQuest()
        self.BackToMainCity()
        self.InMainCity()




if __name__ == "__main__":
    pass
