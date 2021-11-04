import configparser
import os,sys
from Logger import MGRLogger


class FileWriter:
    SETTING_PATH = os.path.abspath(__file__+"..\\..\\..\\GameSettings\\")
    SCRIPT_SETTING_NAME = "\\ScriptSettings.ini"
    BASE_SETTING_NAME = "\\BaseSettings.ini"
    SCRIPT_EDIT_SETTING_NAME = "\\ScriptEditArgsSaved.ini"
    EXECUTE_LIST_CONFIG = "ExecuteListConfig"
    nowFile = None
    translator = None

    def __init__(self):
        self.conf =configparser.RawConfigParser()
        self.conf.optionxform = lambda option: option
        self.translator = Translator()

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

    def LoadExecuteConfigList(self,**kwargs):
        self.__switchNowFile(self.BASE_SETTING_NAME)

        return [{
            "config_title": configName,
        } for configName in self.conf.options(self.EXECUTE_LIST_CONFIG)]

    def SaveScriptEditData(self, data, saveName=None):
        self.__switchNowFile(self.SCRIPT_EDIT_SETTING_NAME)

        if not saveName:
            saveName = 'lastConfig'

        pass

    def LoadScriptEditData(self, loadArgs, codeMode=""):
        # DO:
        # 输入：loadArgs - 载入目标的sectionName
        # 输出: 该section下，所有的方案组成的字典
        # [{”savedEditArgs_savedName“：方案1，”savedEditArgs_Dict“:方案1参数组成的dict},{..}...]

        self.__switchNowFile(self.SCRIPT_EDIT_SETTING_NAME)
        result = []
        self.translator = globals()[codeMode+'Translator']()

        if not self.conf.has_section(loadArgs):
            return []
        configOp = self.conf.options(loadArgs)

        for i in range(len(configOp)):
            configName = configOp[i]
            resultDict = self.translator.decode(self.conf.get(loadArgs, configName))
            result.append({
                "savedEditArgs_savedName": configName,
                "savedEditArgs_Dict": resultDict,
            })
        return result

    def SaveScriptEditData(self, UIData, PlanName, script_title, codeMode=""):
        self.__switchNowFile(self.SCRIPT_EDIT_SETTING_NAME)
        self.translator = globals()[codeMode+'Translator']()

        if not self.conf.has_section(script_title):
            self.conf.add_section(script_title)

        data = self.translator.encode(UIData)
        self.conf.set(script_title, PlanName, data)
        MGRLogger().logger.info("New ScriptArgs Plan:{} saved:{}".format(PlanName, data))
        self.conf.write(open(self.nowFile, "w"))


class Translator:
    # 基础格式：
    # [脚本名]
    # 方案名 = 参数名1：参数值1；参数名2：参数值2；

    def encode(self, dataDict):
        result = ""
        for k in dataDict:
            result = result + k+":"+dataDict[k]+";"

        return result[:-1]

    def decode(self, rawData):
        # DO:
        # 输入：方案的值
        # 输出： {“参数名”：参数值}

        result = {}
        rawData = [data for data in rawData.split(";")]

        for data in rawData:
            result[data.split(":")[0]] = data.split(":")[1]
        print(result)

        return result


class FGOTranslator(Translator):
    def decode(self, rawData):
        # DO:
        # 输入：方案的值
        # 输出： {“参数名”：['参数值1','参数值2']}
        result = {}
        rawData = [data for data in rawData.split(";")]

        for data in rawData:
            result[data.split(":")[0]] = data.split(":")[1].split(",")
        print(result)
        return result



if __name__ == "__main__":

    FileWriter().SaveScriptEditData({"test4":223},"233","TestGame_2")
    #FileWriter().LoadScriptData("TestGame_2")

    print(FileWriter().LoadScriptEditData("TestGame_1"))


