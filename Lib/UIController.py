import os, threading,time
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
from BaseClass import GamesDict, Script,stop_thread


PROJECT_PATH = os.path.abspath(__file__+"..\\..\\..\\")


class Controller(GridLayout):

    def addToExecute(self, unit):
        self.ids.executeList.data.append({"partner": unit,
                                             "is_finish": False,
                                             "script_title": unit.script_title,
                                             "script_args": unit.script_args,
                                             "now_progress": 0})
        unit.is_selected = True

    def reduceToExecute(self, unit):
        self.ids.executeList.reduce_from_execute(unit.script_title)
        self.ids.scriptManager.item_able(unit.script_title)

    def refreshExecuteList(self, config=None):
        self.ids.executeList.refreshExecuteList(config)
        self.ids.scriptManager.refresh_ScriptList()


class RecycleViewItem(BoxLayout):
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

    def __init__(self, script_title=None, **kwargs):
        super(ScriptArgsEditPopup, self).__init__(**kwargs)

        if script_title:
            # 读取ScriptSetting.ini中，改脚本的配置：
            # 如果有就增加items；没有就return
            scriptArgDict = FileWriter().LoadScriptData(script_title)
            self.script_title = script_title
            if not scriptArgDict:
                return
            else:
                for argsName in scriptArgDict:
                    self.ids.scriptEdit_itemList.add_widget(
                        ScriptEditItem(argsName, scriptArgDict[argsName], self))

    # 存储脚本设置更改
    def handle_saveArgs(self):
        saveData = {}
        for item in self.ids.scriptEdit_itemList.children:
            if item.ids.argsName_input.text != "":
                saveData[item.ids.argsName_input.text] = item.ids.argsCount_input.text
        FileWriter().SaveScriptData(self.script_title, saveData)
        MGRApp().refresh_ManagerList()
        MGRApp().refresh_ExecuteList()
        self.dismiss()

    def handle_addItems(self):
        self.ids.scriptEdit_itemList.add_widget(ScriptEditItem(fatherPopUp=self))


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
    gameList = os.listdir(PROJECT_PATH + "\\Scripts")
    selectedGame = gameList[0]
    data = ListProperty()

    def __init__(self, **kwargs):
        super(ScriptManager, self).__init__(**kwargs)

    def generate_DropDownList(self):
        for game in self.gameList:
            btn = Button(text=game, size_hint_y=None, height=48)
            btn.bind(on_release=lambda btn: self.ids.dropdown.select(btn.text))
            self.ids.dropdown.bind(on_select=lambda instance, x: setattr(self.ids.dropdown_mainBtn, 'text', x))
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
        for scriptName in scriptsList_FullName:
            if scriptName[-4:] == ".air":
                scriptsList.append(scriptName[:-4])

        scriptsArgsDict = FileWriter().LoadAllScriptDate_OptionString()
        selectList = MGRApp().get_if_in_executeList(scriptsList)

        for i in range(len(scriptsList)):
            scriptsArgs = ""
            if scriptsArgsDict.get(scriptsList[i]):
                scriptsArgs = scriptsArgsDict[scriptsList[i]]

            data.append({"script_title": scriptsList[i],
                         "is_selected": selectList[i],
                         "script_args": scriptsArgs,
                         })

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

    @staticmethod
    def __generate_data_for_executeList(loadSetting=None):
        data = []
        scriptTitleList = FileWriter().LoadExecuteList(loadSetting)
        scriptsArgsDict = FileWriter().LoadAllScriptDate_OptionString()

        for scriptTitle in list(scriptTitleList):
            scriptsArgs = ""
            if scriptsArgsDict.get(scriptTitle):
                scriptsArgs = scriptsArgsDict[scriptTitle]

            data.append({"partner": None,
                        "is_finish": False,
                        "script_title": scriptTitle,
                        "script_args": scriptsArgs,
                        "now_progress": 0,
                        })

        return data

    def get_data_for_executeList(self):
        return self.data

    def refreshExecuteList(self, loadSetting=None):
        self.data = self.__generate_data_for_executeList(loadSetting)

    def refreshScriptCount(self):
        print(233)
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
        llp = LoadListPopUp()
        llp.title = "LoadExecuteList"
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


class LoadListPopUp(Popup):
    data = ListProperty()

    def __init__(self, **kwargs):
        super(LoadListPopUp, self).__init__(**kwargs)

    def get_data_for_loadConfigList(self):
        return [{
            "config_title": configName,
        } for configName in FileWriter().LoadExecuteConfigList()]

    data_for_loadConfigList = AliasProperty(get_data_for_loadConfigList, bind=["data"])


class LoadListPopUpItem(BoxLayout):
    config_title = StringProperty()


class ScriptSettings(BoxLayout):
    pass


class Log(BoxLayout):
    logData = StringProperty()

    def add_log(self, log):
        self.logData +=log+"\n"


class ScriptExecute(BoxLayout):
    pass


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton
class MGRApp(App):
    gm = None
    singleExecutePopUp = None
    executeMode = None
    countOver = False
    nowThreading = None
    timeCounter = None
    passTime = StringProperty()

    def build(self):
        self.root = Controller()
        self.gm = GameManager(app=self)
        self.singleExecutePopUp = SingleExecutePopUp()
        self.timeCounter = TimeCounter()
        Clock.schedule_interval(self._update_clock, 1)

        self.refresh_ManagerList()

        return self.root

    def handle_script_selected(self, unit):
        self.root.addToExecute(unit)

    def handle_script_selected_cancel(self, unit):
        self.root.reduceToExecute(unit)

    def refresh_ManagerList(self):
        self.root.ids.scriptManager.refresh_ScriptList()

    def refresh_ExecuteList(self):
        self.root.refreshExecuteList()

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
        print("Single Done")

    def handle_ExecuteListRun(self):
        gdt = GamesDict()
        self.executeMode = "List"
        self.countOver = False
        self.root.ids.executeList.accomplishedScriptNumber = 0
        self.timeCounter = TimeCounter(time.time())
        is_startWith = self.root.ids.scriptSettings.ids.switch_startWithStarUp.active

        for item in self.root.ids.executeList.data:
            print(item["script_args"])
            gdt.AddScript(item["script_title"].split("_")[0],
                          Script(item["script_title"],
                                 self.__str_scriptArgs_toInt(item["script_args"])))

        self.gm.setScriptLauncherList(gdt.gameDict, is_startWith)
        self.nowThreading = threading.Thread(target=self.gm.scriptsStart)
        self.nowThreading.start()

    def sync_ScriptProcess(self, scriptTitle, scriptProcess):
        if self.executeMode == "Single":
            self.singleExecutePopUp.ids.pb.value = scriptProcess
        elif self.executeMode == "List":
            for item in self.root.ids.executeList.data:
                if item["script_title"] == scriptTitle:
                    item["now_progress"] = scriptProcess
                    break

            self.root.ids.executeList.ids.executeList_RecycleView.refresh_from_data()
        else:
            print("sync_ScriptProcess Error")

    def one_script_done(self, scriptName):
        self.sync_ScriptProcess(scriptName, 100)
        if self.executeMode == "List":
            self.root.ids.executeList.accomplishedScriptNumber += 1
            self.root.ids.executeList.refreshScriptCount()

    def handle_stopNowProcess(self):
        stop_thread(self.nowThreading)

    def handle_clearExecuteList(self):
        self.root.ids.executeList.data = []

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


