import configparser
import os,sys
from Logger import MGRLogger


class FileWriter:
    SETTING_PATH = os.path.abspath(__file__+"..\\..\\..\\GameSettings\\")
    nowFile = None
    SCRIPT_SETTING_NAME = "\\ScriptSettings.ini"
    BASE_SETTING_NAME = "\\BaseSettings.ini"

    EXECUTE_LIST_CONFIG = "ExecuteListConfig"

    def __init__(self):
        self.conf =configparser.RawConfigParser()
        self.conf.optionxform = lambda option: option

    def __switchNowFile(self, target):
        self.nowFile = self.SETTING_PATH+target
        self.conf.read(self.nowFile)

    def SaveScriptData(self, scriptName, scriptArgsDict):
        self.__switchNowFile(self.SCRIPT_SETTING_NAME)

        # 如果没有模块，就先添加一个
        if not self.conf.has_section(scriptName):
            self.conf.add_section(scriptName)

        # 写入-移除被存数据中，没有的项
        for confk in self.conf.options(scriptName):
            if list(scriptArgsDict.keys()).count(confk) == 0:
                self.conf.remove_option(scriptName, confk)

        # 写入-更新
        for k in scriptArgsDict:
            self.conf.set(scriptName, k, str(scriptArgsDict[k]))
        MGRLogger().logger.info("Script:{} Args saved:{}".format(scriptName, scriptArgsDict))

        self.conf.write(open(self.nowFile, "w"))

    def LoadScriptData(self, scriptName):
        self.__switchNowFile(self.SCRIPT_SETTING_NAME)

        if not self.conf.has_section(scriptName):
            # 如果没有需要这个脚本，返回
            # MGRLogger().logger.error("Load Settings Failed, the section: {} is not exist".format(scriptName))
            return
        else:
            result = {}
            for option in self.conf.options(scriptName):
                result[option] = self.conf.get(scriptName, option)
            return result

    def LoadAllScriptDate_OptionString(self):
        self.__switchNowFile(self.SCRIPT_SETTING_NAME)

        result = {}
        for section in self.conf.sections():
            allOptionStr = ""
            for option in self.conf.options(section):
                allOptionStr = allOptionStr + "{}:{};".format(option, self.conf.get(section, option))
            allOptionStr=allOptionStr[0:-1]
            result[section] = allOptionStr

        return result

    def SaveExecuteList(self, scriptNameList, saveName=None):
        self.__switchNowFile(self.BASE_SETTING_NAME)

        if not saveName:
            saveName = 'lastConfig'

        # 将列表变成每个元素以逗号隔开的形式，进行存贮
        listStr = ""
        for sn in scriptNameList:
            listStr = listStr+sn+","
        listStr = listStr[:-1]

        self.conf.set(self.EXECUTE_LIST_CONFIG, saveName, listStr)
        MGRLogger().logger.info("New executeList:{} saved:{}".format(saveName, listStr))
        self.conf.write(open(self.nowFile, "w"))

    def LoadExecuteList(self, loadTarget=None):
        if not loadTarget:
            loadTarget = 'lastConfig'
        self.__switchNowFile(self.BASE_SETTING_NAME)

        listStr = self.conf.get(self.EXECUTE_LIST_CONFIG, loadTarget)
        result = []

        for scriptName in listStr.split(","):
            result.append(scriptName)

        return result

    def LoadExecuteConfigList(self):
        self.__switchNowFile(self.BASE_SETTING_NAME)
        return  self.conf.options(self.EXECUTE_LIST_CONFIG)



if __name__ == "__main__":

    #FileWriter().SaveScriptData("TestGame_2", {"test4":223})
    #FileWriter().LoadScriptData("TestGame_2")
    print(FileWriter().LoadExecuteConfigList())


