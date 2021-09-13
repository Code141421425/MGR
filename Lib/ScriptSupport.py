import random
from airtest.core.api import *


class RandomPosTime:
    DEFAULT_POS = [500, 500]
    DEFAULT_SLEEP_TIME = 1
    TRY_EXISTS_TIMES = 3

    def randomPos(self, tarPos=None, scale=0):
        # 为空位置，附加默认值
        if not tarPos:
            tarPos = self.DEFAULT_POS

        # 如果是图片，返回坐标值
        if type(tarPos) == Template:
            for i in range(self.TRY_EXISTS_TIMES):
                if exists(tarPos):
                    tarPos = exists(tarPos)
                    break
                else:
                    sleep(self.DEFAULT_SLEEP_TIME)

        if (type(tarPos) != list) & (type(tarPos) != tuple):
            print("Do Not find the picture when touch")
            return

        print(tarPos)

        variable = 0
        if scale == 0:
            variable = 5  # 做一个默认的，极小范围的随机
        elif scale == 1:
            variable = 20  # 小图标用，技能图标的大小边长大概为100
        elif scale == 2:
            variable = 70  # 长方形图标用，上下200，左右
        elif scale == 3:
            variable = 350

        finPos = [0, 0]
        finPos[0] = tarPos[0] + random.randint(-variable, variable)
        finPos[1] = tarPos[1] + random.randint(-variable, variable)

        return finPos

    def randomTime(self, tarTime=1, scale=0, customTime=0):
        # 如果没有目标时间，就使用默认时间
        if not tarTime:
            tarTime = self.DEFAULT_SLEEP_TIME

        variableTime = 0
        if scale == 0:
            variableTime = 0.2
        elif scale == 1:
            variableTime = 0.5  # 适用于战斗间隙（技能）
        elif scale == 2:
            variableTime = 6  # 适用于长时间间隔（每面结束）
        elif scale == 3:
            variableTime = 5  # 战斗结束
        elif scale == -1:
            variableTime = customTime

        tarTime = tarTime + random.uniform(-variableTime, variableTime)

        return tarTime

