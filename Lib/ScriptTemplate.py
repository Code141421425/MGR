import os,sys
from airtest.core.api import *
from ScriptSupport import RandomPosTime
from Logger import MGRLogger
from GameManager import GameManager


class Operation:
    def __init__(self, args=None):
        if args:
            self.Execute(args)

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


class TryChain(Operation):
    def __init__(self, tar, tryList=None, ifTouch=False):
        self.Execute(tar, tryList, ifTouch)

    # 如果没有找到目标，就尝试列表中的下一个行为组
    def Execute(self, tar, tryList=None, ifTouch=None):
        success = False

        # 如果没有尝试列表，就设为5次[500,500]
        if not tryList:
            tryList=[[500,500],[500,500],[500,500],[500,500],[500,500],[500,500]]

        for t in tryList:
            if not exists(tar):
                # try:
                # 如果输入的是一张图：就查点这张图
                if type(t) != list:
                    ExistsAndTouch(t)
                elif type(t) == list:
                    # 如果输入的是一个列表：就查点这个列表
                    if type(t[0]) != list:
                        WaitAndTouch().Execute(t)
                    # 如果输入的是两个列表：就查第1个列表，点第2个列表的位置
                    else:
                        ExistsAndTouchSuit().Execute(t[0], t[1])
                else:
                    MGRLogger.logger.Error("Try Chain Error to match")
            # except Exception as e:
            #     print(e)
            else:
                success = True
                WaitAndTouch(tar)
                break

        if not success:
            MGRLogger().logger.error("Fail to get target in TryList")


class SwipeToSeeTarget(Operation):
    def __init__(self, tar, SwipeList=None, ifTouch=False):
        self.Execute(tar, SwipeList, ifTouch)

    def Execute(self, tar, SwipeList, ifTouch):
        # 如果存在，就直接return
        if exists(tar):
            if ifTouch:
                WaitAndTouch(tar)
        # 不存在就划一下
        else:
            swipe(SwipeList[0], SwipeList[1])
            if exists(tar):
                if ifTouch:
                    WaitAndTouch(tar)
                    return
            else:
                # 还没有就报错
                MGRLogger.logger.Error("Swipe but can't see target")
                raise TargetNotFoundError(str(__class__))


class TouchUntilTargetDisappear(Operation):
    # DO: 一直操作，直到目标消失
    def Execute(self, target, actionList=None):
        if not actionList:
            actionList = [target]
        while exists(target):
            WaitAndTouchSuit(actionList)
            sleep(4)

        print("Done")


class FindFromTemplateList(Operation):
    # DO:
    # 1、从一组图像中，看界面上是否存在列表中的图像
    # 2、如果有的话，点击，如果有出现目标就返回，没有就就继续找
    # 3、如果都找了一边，仍然没有找到，就报错
    # Example:游戏王：决斗链接

    def __init__(self, tar, templateList):
        self.Execute(tar, templateList)

    def Execute(self, tar, templateList):
        for template in templateList:
            if exists(template):
                # 找到目标，点击
                touch(template)
                if exists(tar):
                    # 存在目标，返回
                    return
                else:
                    pass

        # 没有找到目标，报错
        raise TargetNotFoundError("FindFromTemplateList can't find target")


class ExistsAndTouch(WaitAndTouch):
    _DEFAULT_TRY_TIMES = 2
    _DEFAULT_SLEEP_TIME = 1

    def Execute(self, targetTemplate, pos=None,
                sleep_time=_DEFAULT_SLEEP_TIME, tryTimes=_DEFAULT_TRY_TIMES):
        print(targetTemplate)
        print(pos)

        # 如果没有需要点击的目标，就点击需要寻找的目标
        if not pos:
            pos = targetTemplate

        isFounded = False

        if targetTemplate:
            # 如果存在需要匹配的目标，就开始找
            for i in range(tryTimes):
                if exists(targetTemplate):
                    isFounded = True
                    break
        else:
            # 不存在，就直默认找到了，直接点击
            isFounded = True

        if not isFounded:
            return
        else:
            super(ExistsAndTouch, self).Execute(pos, sleep_time)


class ExistsAndTouchSuit(ExistsAndTouch):
    def Execute(self, targetTemplateList, touchPosList=None, sleep_timeList=None, tryTimesList=None):
        if not touchPosList:
            touchPosList = targetTemplateList

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

        # 如果在主界面，就不用尝试关闭通知了
        if not exists(self.mainCityTemplate):
            if not self.passCloseNotice:
                self.CloseNotice()

        self.InMainCity()


class Battle(ScriptTemplate):
    battleTimes = []
    _nowTimes = 0
    battleFiled = None

    def __init__(self, battleTimes=1, battleFiled=None):
        self.battleTimes = battleTimes
        self._nowTimes = 0
        self.battleFiled = battleFiled

    def ToBattleField(self):
        if self.battleFiled:
            getattr(self, "ToBattleField_"+self.battleFiled)()

    def BattleOnce(self):
        pass

    def BackToMainCity(self):
        pass

    def runScriptTemplate(self):
        self.ToBattleField()

        for i in range(self.battleTimes):
            self.BattleOnce()
            self._nowTimes += 1
            MGRLogger().logger.info("Script has run:{} times".format(str(self._nowTimes)))
            self._sync_process()


        self.BackToMainCity()

    def _sync_process(self):
        try:
            GameManager().sync_ScriptProcess_GM_to_UI(self.__class__.__name__, self._nowTimes *100/self.battleTimes)
        except:
            pass


class SimpleQuest(ScriptTemplate):
    mainCity = None

    def __init__(self, mainCity=None):
        if mainCity:
            self.mainCity = mainCity

    def ToQuestField(self):
        pass

    def ExecuteSimpleQuest(self):
        pass

    def BackToMainCity(self):
        pass

    def InMainCity(self):
        if self.mainCity:
            wait(self.mainCity)

    def runScriptTemplate(self):
        self.ToQuestField()
        self.ExecuteSimpleQuest()
        self.BackToMainCity()
        self.InMainCity()


if __name__ == "__main__":
    pass
