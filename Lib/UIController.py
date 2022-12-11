import os, sys, threading, time
PROJECT_PATH = os.path.abspath(__file__+"..\\..\\..\\")
sys.path.append(PROJECT_PATH)
print(sys.path)
from functools import partial
from kivy.config import Config
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ListProperty, StringProperty, \
        NumericProperty, BooleanProperty, AliasProperty
from kivy.clock import Clock
from FileWirter import FileWriter
from Logger import MGRLogger
from GameManager import GameManager
from BaseClass import GamesDict, Script,stop_thread,singleton






class Controller(GridLayout):
    # DO：最底层的容器，装着所有的在1级界面上显示的东西

    def addToExecute(self, unit):
        self.ids.executeList.data.append({"is_finish": False,
                                          "script_title": unit.script_title,
                                          "script_args": unit.script_args,
                                          "now_progress": 0})
        unit.is_selected = True

    def reduceToExecute(self, unit):
        self.ids.executeList.reduce_from_execute(unit.script_title)
        self.ids.scriptManager.item_able(unit.script_title)

    def refreshExecuteList(self, config=None):
        self.ids.executeList.refresh_ExecuteList_Data(config)
        self.ids.scriptManager.refresh_ScriptList()


class RecycleViewItem(BoxLayout):
    # DO：作为在ScriptManager中循环列表的Item，展示其中的data

    is_selected = BooleanProperty(True)
    available = BooleanProperty(True)
    script_title = StringProperty()
    script_args = StringProperty()

    @staticmethod
    def call_ScriptArgsEditPopup(item):
        p = ScriptArgsEditPopup(item.script_title)
        p.title = item.script_title + "'s arg edit"
        p.open()


class ScriptArgsEditPopup(Popup):
    # DO：
    # 1、可以通过“+”，“-”号，来增加，或者删除在Boxlayout——scriptEdit_itemList中，该条脚本参数的键值对
    # 2、scriptEdit_itemList中，ArgsName和ArgsCount所对应输入框的值，每对都会组成一个字典，在运行时加入到对应脚本中，如果脚本用到了，该变量就会生效
    # 3、脚本参数，会通过FileWriter，存在ScriptSettings.ini中
    # 4、

    data = ListProperty()
    script_title = None

    def __init__(self, script_title=None, **kwargs):
        if script_title:
            # 加载参数，读取ScriptSetting.ini中，该脚本的参数对：
            scriptArgDict = FileWriter().LoadScriptData(script_title)
            self.script_title = script_title

        super(ScriptArgsEditPopup, self).__init__(**kwargs)

        if not scriptArgDict:
            # 没有就return，不添加
            return
        else:
            # 如果有，就凭借ScriptEditItem实例，增加到items；
            for argsName in scriptArgDict:
                self.ids.scriptEdit_itemList.add_widget(
                    ScriptEditItem(argsName, scriptArgDict[argsName], self))

    # 存储脚本设置更改
    def handle_saveArgs(self):
        FileWriter().SaveScriptData(self.script_title, self.__get_now_ArgsData())
        MGRApp().refresh_ManagerList()
        MGRApp().refresh_ExecuteList()
        self.dismiss()

    def __get_now_ArgsData(self):
        # DO：获取当前输入框中，Name非空的脚本参数的键值对，组成字典并返回
        data = {}
        for item in self.ids.scriptEdit_itemList.children:
            if item.ids.argsName_input.text != "":
                data[item.ids.argsName_input.text] = item.ids.argsCount_input.text

        return data

    def handle_addItems(self):
        self.ids.scriptEdit_itemList.add_widget(ScriptEditItem(fatherPopUp=self))

    def Reload_ScriptEditItem(self, configDict):
        # DO：删除scriptEdit_itemList列表中的所有输入键值对，并凭借configDict中的数据，重新加载
        self.ids.scriptEdit_itemList.clear_widgets()

        for k in configDict:
            self.ids.scriptEdit_itemList.add_widget(
                ScriptEditItem(argsName=k, argsCount=configDict[k], fatherPopUp=self))

    def get_data_for_loadConfigList(self):
        # DO：
        # 1、在FileWriter中，通过“LoadScriptEditData”方法，
        #    调取ScriptEditArgsSaved.ini中，自己脚本相关的所有参数方案
        # 2、其中的fatherPopUp，是为了参数方案在读取的时候，能够直接加载对应方案

        result = getattr(FileWriter(), "LoadScriptEditData")(loadArgs=self.script_title)
        for r in result:
            r["fatherPopUp"] = self

        return result

    data_for_loadConfigList = AliasProperty(get_data_for_loadConfigList, bind=["data"])

    def handle_scriptEdit_save(self):
        # DO：打开弹窗，输入名称，以保存参数计划
        p = SaveEditArgsPlanNamePopUp()
        p.title = "EditArgs Plan Save"
        p.setSaveData(self.__get_now_ArgsData(), self.script_title)
        p.father = self
        p.open()

    def refresh_scriptEdit(self):
        self.data = self.get_data_for_loadConfigList()


class ScriptEditItem(BoxLayout):
    argsName = StringProperty()
    argsCount = StringProperty()
    fatherPopUp = None

    def __init__(self, argsName="", argsCount="", fatherPopUp=None, **kwargs):
        super(ScriptEditItem, self).__init__(**kwargs)
        self.argsName = str(argsName)
        self.argsCount = str(argsCount)
        self.fatherPopUp = fatherPopUp

    def handle_reduceItem(self, item):
        self.fatherPopUp.ids.scriptEdit_itemList.remove_widget(item)


class ScriptManager(BoxLayout):
    # DO:
    # 1、用于管理，从Scripts文件夹下，所有的脚本和其启动参数
    # 2、在下拉列表中选择游戏后，下方循环列表显示该文件夹下对应的所有脚本
    # 3、每个脚本，显示其脚本名称，和一小行参数文本（超出变成...）
    # 4、可以挑选脚本，点击">"后按钮置灰（与“<”按钮相互呼应），该脚本进入执行列表，
    # 5、可以点击“edit”，进入编辑脚本参数弹窗
    # 6、点击“SingleExecute”，弹窗，单独执行此脚本

    gameList = os.listdir(PROJECT_PATH + "\\Scripts")
    selectedGame = gameList[0]  # 初始化，选择第一个，可以在init中传入以保存页签吧
    data = ListProperty()

    def __init__(self, **kwargs):
        super(ScriptManager, self).__init__(**kwargs)

    def generate_DropDownList(self):
        for game in self.gameList:
            btn = Button(text=game, size_hint_y=None, height=48)
            btn.bind(on_release=lambda btn: self.ids.dropdown.select(btn.text))
            self.ids.dropdown.bind(on_select=lambda instance, x: setattr(self.ids.dropdown_mainBtn, 'text', x))  # 有点儿看不太懂了
            self.ids.dropdown.add_widget(btn)

    def refresh_DropDownList(self):
        self.ids.dropdown.clear_widgets()
        self.generate_DropDownList()

    def refresh_ScriptList(self):
        self.data = self.generate_data_for_scriptList()

    def handle_DropDownSelect(self):
        print(self.ids.dropdown_mainBtn.text)
        self.selectedGame = self.ids.dropdown_mainBtn.text
        # 刷新数据
        self.refresh_ScriptList()

    def get_data_for_scriptList(self):
        return self.data

    def generate_data_for_scriptList(self):
        data = []
        scriptsList_FullName = os.listdir(PROJECT_PATH + "\\Scripts\\" + self.selectedGame)
        scriptsList = []
        # 获取路径下，所有的.air文件，去掉后4位，作为脚本名称
        for scriptName in scriptsList_FullName:
            if scriptName[-4:] == ".air":
                scriptsList.append(scriptName[:-4])

        scriptsArgsDict = FileWriter().LoadAllScriptDate_OptionString()  # 获取所有脚本参数
        selectList = MGRApp().get_if_in_executeList(scriptsList)  # 确认是否在执行列表
        usedCountDict = FileWriter().LoadScriptsUsedCount()

        for i in range(len(scriptsList)):
            scriptsArgs = ""
            if scriptsArgsDict.get(scriptsList[i]):
                scriptsArgs = scriptsArgsDict[scriptsList[i]]

            usedTimes = 0
            if usedCountDict.get(scriptsList[i]):
                usedTimes = usedCountDict[scriptsList[i]]

            data.append({"script_title": scriptsList[i],
                         "is_selected": selectList[i],
                         "script_args": scriptsArgs,
                         "used_times": usedTimes,
                         })

        # 之后，对于数据进行排序
        data.sort(key=lambda x: x["used_times"], reverse=True)
        return data

    data_for_scriptList = AliasProperty(get_data_for_scriptList,
                                        bind=["data"])

    def item_able(self, script_title, state=True):
        for scriptDict in self.data:
            if script_title == scriptDict["script_title"]:
                scriptDict['is_selected'] = state
                self.refresh_ScriptList()
                break


class SingleExecutePopUp(Popup):
    script_title = ""
    now_progress = 0

    def __init__(self, script_title=None, **kwargs):
        super(SingleExecutePopUp, self).__init__(**kwargs)
        if script_title:
            self.script_title = script_title

    def prepare_to_open(self, script_title):
        self.script_title = script_title
        self.title = script_title + "——Single Execute"
        self.ids.pb.value = 0


class TimeCounter:
    startTime = None

    def __init__(self, startTime=None):
        if startTime:
            self.startTime = startTime
        self.stop = False
        self.now_time = None

    def return_pass_time(self):
        if not self.stop:
            self.now_time = time.time()
        else:
            pass

        if not self.startTime:
            return "0:0"
        else:
            return "{}:{}".format(int((self.now_time - self.startTime) / 60),
                                  int(self.now_time - self.startTime) % 60)


class ExecuteList(BoxLayout):
    data = ListProperty()
    scriptsList = os.listdir(PROJECT_PATH + "\\GameSettings\\")
    accomplishedScriptNumber = NumericProperty()
    startTime = -1
    now_progress = 0

    def __init__(self, **kwargs):
        super(ExecuteList, self).__init__(**kwargs)
        self.data = self.__generate_data_for_executeList()

    def __generate_data_for_executeList(self, loadSetting=None):
        # DO：
        # 如果没有载入配置，就从新从文件中读取；
        # 如果有载入配置，就先拿去已存在与执行列表的标题组，之后按照标题，再从文件中读取
        if loadSetting:
            data = []
            scriptTitleList = FileWriter().LoadExecuteList(loadSetting)
        else:
            data = self.data
            if data:
                scriptTitleList = [scriptDict['script_title'] for scriptDict in data]
                # 因为数据是append的，所以在拿完标题列表之后，需要清空data重新拉取
                data = []
            else:
                scriptTitleList = []

        scriptsArgsDict = FileWriter().LoadAllScriptDate_OptionString()

        for scriptTitle in list(scriptTitleList):
            scriptsArgs = ""
            if scriptsArgsDict.get(scriptTitle):
                scriptsArgs = scriptsArgsDict[scriptTitle]

            data.append({"is_finish": False,
                         "script_title": scriptTitle,
                         "script_args": scriptsArgs,
                         "now_progress": 0,
                         })
        return data

    def get_data_for_executeList(self):
        return self.data

    def refresh_ExecuteList_Data(self, loadSetting=None):
        self.data = self.__generate_data_for_executeList(loadSetting)

    def refreshScriptCount(self):
        self.ids.scriptCount.parent.text = "Scripts: {}/{}".format(self.get_accomplishedScriptNumber(), len(self.data))
        # BoxLayout()
        # from kivy.uix.label import Label
        # Label().parent.

    def get_accomplishedScriptNumber(self):
        return self.accomplishedScriptNumber

    def call_saveListPopUp(self):
       slp = SaveListPopUp()
       slp.title = "SaveExecuteList"
       slp.open()

    @staticmethod
    def call_loadListPopUp():
        llp = LoadListPopUp(None, "LoadListPopUpItem", "LoadExecuteConfigList")
        llp.open()

    data_for_ExecuteList = AliasProperty(get_data_for_executeList,bind=["data"])

    def return_if_select_data(self, targetList):
        # 返回目标,在执行列表中是否出现的列表
        result = []
        executeList_scriptTitle = []
        for script in self.data:
            executeList_scriptTitle.append(script["script_title"])

        for tar in targetList:
            if executeList_scriptTitle.count(tar) != 0:
                result.append(True)
            else:
                result.append(False)

        return result

    def reduce_from_execute(self, script_title):
        for scriptDict in self.data:
            if script_title == scriptDict["script_title"]:
                self.data.remove(scriptDict)
                break


class ExecuteListRecycleViewItem(BoxLayout):
    partner = None
    is_finish = BooleanProperty(True)
    script_title = StringProperty()
    script_args = StringProperty()
    now_progress = NumericProperty()


class SaveListPopUp(Popup):
    pass


class SaveEditArgsPlanNamePopUp(Popup):
    # DO：
    # 1、用以在编辑脚本参数（ScriptArgsEditPopup）弹窗中，
    #    将当前输入框内的参数对，作为一个Plan进行保存
    # 2、需要在输入框中输入保存的Plan的名称，之后点击save按钮后，
    #    通过app中的handle_saveScriptEditData()方法进行保存

    savedData = None
    script_title = None
    father = None

    def setSaveData(self, data, script_title):
        self.savedData = data  # 需要保存的数据
        self.script_title = script_title


class LoadListPopUp(Popup):
    data = ListProperty()
    loadTarget = None
    loadArgs = None
    listItemClass = None
    fatherPopUp = None

    def __init__(self, fatherPopup, listItemClass=None, loadTarget=None, loadArgs=None, **kwargs):
        if loadTarget:
            self.loadTarget = loadTarget
        else:
            self.loadTarget = "LoadExecuteConfigList"

        if loadArgs:
            self.loadArgs = loadArgs

        if fatherPopup:
            self.fatherPopup = fatherPopup
        self.listItemClass = listItemClass

        super(LoadListPopUp, self).__init__(**kwargs)

        self.title = self.loadTarget

    def get_data_for_loadConfigList(self):
        return getattr(FileWriter(), self.loadTarget)(loadArgs=self.loadArgs)

    data_for_loadConfigList = AliasProperty(get_data_for_loadConfigList, bind=["data"])


class LoadListPopUpItem(BoxLayout):
    config_title = StringProperty()


class LoadListPopUpItem_ScriptEdit(BoxLayout):
    # DO：
    # 1、是在编辑参数弹窗，参数方案的循环列表，作为ViewClass，进行方案的展示，
    # 2、并可以提供在父弹窗中的输入框键值对中，载入对应的方案
    savedEditArgs_savedName = StringProperty()
    savedEditArgs_Dict = {}
    fatherPopUp = None

    def handle_scriptEdit_load(self):
        self.fatherPopUp.Reload_ScriptEditItem(self.savedEditArgs_Dict)


class ScriptSettings(BoxLayout):
    deviceID = None

    ##
    # TODO: 实现设备ID，保存脚本日志功能
    ##

    pass


class Log(BoxLayout):
    logData = StringProperty()

    def add_log(self, log):
        self.logData +=log+"\n"


class ScriptExecute(BoxLayout):
    pass


@singleton
class MGRApp(App):
    # DO：
    # 1、是单例的
    # 2、因为嫩通过app.进行调用，所以负责UI类的相互联系
    # 3、和脚本，logger的联系
    # 4、计时器，计数器

    gm = None  # 单例的GameManager
    singleExecutePopUp = None  # 单独执行弹窗的实例
    executeMode = None  # 分为“Single”或者“List”，同步进度条进度用
    countOver = False  # 用于停止计时
    nowThreading = None  # 保存现在执行脚本的线程，用于停止时，直接杀掉该进程
    timeCounter = None  # 是计时器的实例
    passTime = StringProperty()  # 是一个字符串，用于在界面上显示时间
    stepCount = StringProperty()  # 是一个字符串，用于在界面上显示做操作的步数（现在还有问题）
    stepCount_int = 0  # 逻辑上的操作步数的计数
    logger = None  # 单例的logger，用于记录log

    def build(self):
        self.root = Controller()
        self.gm = GameManager(app=self)
        self.singleExecutePopUp = SingleExecutePopUp()
        self.timeCounter = TimeCounter()
        self.stepCount = str(self.stepCount_int)
        Clock.schedule_interval(self._update_clock, 1)  # 是kivy的计时器，用它更新时间，每秒更新1次
        self.logger = MGRLogger(self).logger

        self.refresh_ManagerList()
        self.refresh_ExecuteList("lastConfig")  # 在执行列表中，加载“lastConfig”，这个配置的带执行脚本

        return self.root  # UI将显示返回的这个东西

    def handle_script_selected(self, unit):
        self.root.addToExecute(unit)

    def handle_script_selected_cancel(self, unit):
        self.root.reduceToExecute(unit)

    def refresh_ManagerList(self):
        self.root.ids.scriptManager.refresh_ScriptList()

    def refresh_ExecuteList(self, config=None):
        self.root.refreshExecuteList(config)

    def handle_saveExecuteList(self, item=None):
        saveName = None
        if item:
            saveName = item.ids.savelistName.text
            item.dismiss()

        saveData = []

        for item in self.root.ids.executeList.data:
            saveData.append(item['script_title'])

        if len(saveData) == 0:
            return

        FileWriter().SaveExecuteList(saveData, saveName)

    def handle_loadExecuteList(self, item):
        self.root.refreshExecuteList(item.config_title)

    @staticmethod
    def __str_scriptArgs_toInt(scriptArgsStr):
        scripts_args = {}
        # 如果是可以转化为数字，就转后存入;没有参数就空过
        if scriptArgsStr:
            for arg in scriptArgsStr.split(";"):
                arg_k = arg.split(":")[0]
                arg_v = arg.split(":")[1]
                try:
                    scripts_args[arg_k] = int(arg_v)
                except:
                    scripts_args[arg_k] = arg_v
        return scripts_args

    def handle_singleExecute(self, item):
        # 启动单独执行弹窗
        self.countOver = False
        self.executeMode = "Single"
        self.singleExecutePopUp.prepare_to_open(item.script_title)
        self.timeCounter = TimeCounter(time.time())
        self.singleExecutePopUp.open()
        gdt = GamesDict()

        gdt.AddScript(item.script_title.split("_")[0],
                      Script(item.script_title, self.__str_scriptArgs_toInt(item.script_args)))

        self.gm.setScriptLauncherList(gdt.gameDict, False)
        self.nowThreading = threading.Thread(target=self.gm.scriptsStart)
        self.nowThreading.start()
        self.logger.info("Single Script Done")

    def handle_ExecuteListRun(self):
        gdt = GamesDict()
        self.executeMode = "List"
        self.countOver = False
        self.root.ids.executeList.accomplishedScriptNumber = 0
        self.stepCount = str(0)
        self.timeCounter = TimeCounter(time.time())
        is_startWith = self.root.ids.scriptSettings.ids.switch_startWithStarUp.active

        for item in self.root.ids.executeList.data:
            print(item["script_args"])
            # 通过脚本名中，"_"来截取游戏名
            # 可以在此添加“脚本类型”这个参数
            gdt.AddScript(item["script_title"].split("_")[0],
                          Script(item["script_title"],
                          self.__str_scriptArgs_toInt(item["script_args"])))

        self.gm.setScriptLauncherList(gdt.gameDict, is_startWith)
        print(gdt.gameDict)
        self.nowThreading = threading.Thread(target=self.gm.scriptsStart)
        self.nowThreading.start()

    def sync_ScriptProcess(self, scriptTitle, scriptProcess):
        # DO：
        # 用于将脚本的执行进度，同步给单独执行弹窗，或者是执行列表

        if self.executeMode == "Single":
            self.singleExecutePopUp.ids.pb.value = scriptProcess
        elif self.executeMode == "List":
            for item in self.root.ids.executeList.data:
                if item["script_title"] == scriptTitle:
                    item["now_progress"] = scriptProcess
                    break

            self.root.ids.executeList.ids.executeList_RecycleView.refresh_from_data()
        else:
            self.logger.error("sync_ScriptProcess Error")

    def sync_StepProcess_add(self, process):
        # DO：同步逻辑上和现实上的操作步数
        self.stepCount_int += process
        self.stepCount = str(self.stepCount_int)

    def one_script_done(self, scriptName):
        self.sync_ScriptProcess(scriptName, 100)
        if self.executeMode == "List":
            self.root.ids.executeList.accomplishedScriptNumber += 1
            self.root.ids.executeList.refreshScriptCount()

    def handle_stopNowProcess(self):
        try:
            stop_thread(self.nowThreading)
        except ValueError:
            self.logger.warning("The process has been killed")

    def handle_clearExecuteList(self):
        self.root.ids.executeList.data = []
        self.root.ids.executeList.accomplishedScriptNumber = 0
        self.refresh_ExecuteList()

    def handle_saveScriptEditData(self, item):
        # DO：将需要作为Plan保存的数据和PlanName，在FileWriter进行保存
        FileWriter().SaveScriptEditData(item.savedData, item.ids.savePlanName.text, item.script_title)
        item.dismiss()
        item.father.refresh_scriptEdit()

    def add_AddLog(self, log):
        self.root.ids.logPanel.add_log(log)

    def get_if_in_executeList(self, targetList):
        return self.root.ids.executeList.return_if_select_data(targetList)

    def _update_clock(self, dt):
        if not self.countOver:
            self.passTime = self.timeCounter.return_pass_time()

    def test(self):
        print(233)


if __name__ == "__main__":
    Config.set('graphics', 'width', '1550')
    Config.set('graphics', 'height', '650')

    p = threading.Thread(target=MGRApp().run)
    p.start()

    #MGRApp().run()


