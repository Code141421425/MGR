from airtest.core.api import *
from ScriptSupport import RandomPosTime


class Operation:
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


class WaitAndTouchSuit(WaitAndTouch):
    def Execute(self, posList,  sleep_timeList=None, templateList=None):
        # 将所有的数组，处理成统一posList的长度
        templateList = self.__ListHandle(posList, templateList)
        sleep_timeList = self.__ListHandle(posList, sleep_timeList)

        for i in range(0, len(posList)):
            super(WaitAndTouchSuit, self).Execute(
                posList[i], sleep_timeList[i], templateList[i], )

    def __ListHandle(self, target, operated):
        if not operated:
            operated = []
            operated.append(None)

        while len(operated) != len(target):
            operated.append(None)

        return operated


if __name__ == "__main__":
    pass
