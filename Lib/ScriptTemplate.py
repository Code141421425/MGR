import os,sys
from airtest.core.api import *
from ScriptSupport import RandomPosTime
from Logger import MGRLogger
from GameManager import GameManager


def stepProcessAdd(*args,**kwargs):
    try:
        GameManager().sync_StepProcessAdd_GM_to_UI(1)
    except:
        print("No UI")


class Operation:
    def __init__(self, args=None):
        if args:
            self.Execute(args)

    @staticmethod
    def _ListHandle(target, operated, filler=None):
        # DO：
        # 1、用于处理一个列表，使其变得和target一样长
        # 2、 默认使用None进行填充，也可以进行配置

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
    # DO：
    # 1、点击一张图或者一个坐标，之后等待一定时间
    # 2、最后尝试向UI同步点击计数进度
    def Execute(self, pos, sleep_time=1, template=None):
        if template:
            try:
                wait(template)
            except TargetNotFoundError:
                print("Do not find the picture")
                return

        touch(RandomPosTime().randomPos(pos),)
        sleep(RandomPosTime().randomTime(sleep_time))
        try:
            GameManager().sync_StepProcessAdd_GM_to_UI(1)
        except:
            print("No UI")


class Touch(Operation):
    # DO：
    # 1、利用randomPT，进行一次点击
    # 2、基本不用
    def Execute(self, pos, sleep_time=1):
        touch(RandomPosTime.randomPos(pos))
        sleep(RandomPosTime.randomTime(sleep_time))


class Swipe(Operation):
    def Execute(self):
        pass


class SnapShort(Operation):
    # DO:
    # 1、进行截图
    # 2、默认存到一个文件夹，以日期和明明

    def __init__(self,gameName=""):
        self.gameName = gameName
        self.Execute()

    def Execute(self):
        nowTime = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(time.time()))
        currentPath = os.path.dirname(os.path.realpath(__file__))
        snapshot(filename=currentPath + '/../SnapShort/' + self.gameName + nowTime + '.jpg')



class TryChain(Operation):
    # DO：
    # 1、尝试点击一个操作或者操作序列，直到出现目标
    # 2、可以决定最后是否点击
    # 3、如果没有操作序列，将默认每隔1s，点击一个点，数次
    # Example：公主连结，在战斗结束后的分支判断

    def __init__(self, tar, tryList=None, ifTouch=False, tryTimes=None):
        self.Execute(tar, tryList, ifTouch, tryTimes)

    # 如果没有找到目标，就尝试列表中的下一个行为组
    def Execute(self, tar, tryList=None, ifTouch=None, tryTimes=None):
        success = False

        # 如果没有尝试列表，就设为5次[500,500]
        if not tryList:
            tryList=[[500,500],[500,500],[500,500],[500,500],[500,500],[500,500]]

        if tryTimes:
            for i in range(tryTimes):
                tryList.append(tryList[0])

        print(tryList)
        for t in tryList:
            print(t)
            if not exists(tar):
                # try:
                # 如果输入的是一张图：就查点这张图
                if type(t) != list:
                    ExistsAndTouch(t)
                elif type(t) == list:
                    # 如果输入的是一个列表：就查点这个列表
                    # if type(t[0]) != list:
                    WaitAndTouchSuit().Execute(t)
                    sleep()
                    # # 如果输入的是两个列表：就查第1个列表，点第2个列表的位置
                    # else:
                    #     ExistsAndTouchSuit().Execute(t[0], t[1])
                else:
                    try:
                        MGRLogger.logger.Error("Try Chain Error to match")
                    except:
                        print("No logger")
            # except Exception as e:
            #     print(e)
            else:
                success = True
                if ifTouch:
                    WaitAndTouch(tar)
                break

        if not success:
            try:
                MGRLogger().logger.error("Fail to get target in TryList")
            except:
                print("No logger")


class TouchListUntilTargetAppear(Operation):
    # DO：
    # 1、尝试点击一个操作或者操作序列，直到出现目标
    # 2、可以决定最后是否点击
    # 3、如果没有操作序列，将默认每隔1s，点击一个点，数次
    # Example：公主连结，在战斗结束后的分支判断

    def __init__(self, tar, tryList=None, ifTouch=False, tryTimes=None):
        self.Execute(tar, tryList, ifTouch, tryTimes)

    # 如果没有找到目标，就尝试列表中的下一个行为组
    def Execute(self, tar, tryList=None, ifTouch=None, tryTimes=None):
        success = False

        if not tryList:
            tryList = [[[500, 500]],[[500, 500]],[[500, 500]],[[500, 500]],[[500, 500]],[[500, 500]],[[500, 500]]]

        for t in tryList:
            print(t)
            if not exists(tar):
                # 尝试点击这个列表
                try:
                    WaitAndTouchSuit().Execute(t)
                    sleep()
                except:
                    print("can't find this time")

            # except Exception as e:
            #     print(e)
            else:
                success = True
                if ifTouch:
                    WaitAndTouch(tar)
                break

        if not success:
            try:
                MGRLogger().logger.error("Fail to get target in TryList")
            except:
                print("No logger")


class SwipeToSeeTarget(Operation):
    # DO：
    # 1、滑动一下界面，看到目标就过；没有就报错
    # 2、可以选择点不点
    # Example：公主连结，活动界面找VH本 / FGO，在一列目标中，找到目标本
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
    # DO:
    # 一直操作，直到目标消失
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
    # Example:游戏王：决斗链接（已废弃）

    def __init__(self, tar, templateList):
        self.Execute(tar, templateList)

    def Execute(self, tar, templateList):
        for template in templateList:
            if exists(template):
                # 找到目标，点击
                touch(template)
                if exists(tar):
                    # 存在目标，返回
                    return True
                else:
                    pass

        # 没有找到目标，报错
        return False


class ExistsAndTouch(WaitAndTouch):
    # DO：
    # 1、尝试在寻找一个目标，找到之后，进行一次WaitandTouch
    # 2、用处较少

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
    # DO：
    # 1、按照所给的列表，执行一系列的ExistsAndTouch操作

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
    # DO：
    # 1、执行一系列的 WaitAndTouch操作

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
    # DO：
    # 1、按照启动游戏->游戏更新->登陆->关闭通知，最后直到到指定的主界面画面为止
    # 2、在runScriptTemplate中，规定执行方法的顺序
    # 3、子类脚本覆写父类对应方法

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
    # DO：
    # 1、前往战场->战斗数次->回到主界面，的模板
    # 2、BattleOnce中编写一次战斗中所需要做的事情，然后会按照初始化所给定的BattleTimes进行循环
    # 3、在使用此模板时，每次战斗都会向UI同步进度
    # 4、在初始化实例时，可以给定battleField参数，子类脚本将按照所给定的参数对应的脚本，前往战场
    # 5、用的很多

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
    # DO：
    # 1、前往任务地点->执行->返回任务地点，的模板
    # 2、可以视作简化的，只执行一次的Battle模板
    # 3、最后可以验证是否在主界面
    # 4、基本上不怎么用

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
