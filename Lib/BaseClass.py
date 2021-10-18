import ctypes
import inspect

class Script:
    scriptName = ""
    scriptArgs = {}
    scriptType = ""

    DEFAULT_SCRIPT_TYPE = "QuickScriptLauncher"

    def __init__(self, scriptName, scriptArgs=None, scriptType=DEFAULT_SCRIPT_TYPE):
        self.scriptName = scriptName
        self.scriptType = scriptType
        self.scriptArgs = scriptArgs


class GamesDict:
    gameDict = {}

    def __init__(self):
        self.gameDict = {}

    def AddScript(self, gameName, script):
        # 如果是 新的游戏，则多创建一个GameName的键值对
        if not self.gameDict.get(gameName):
            self.gameDict[gameName] = {}
            self.gameDict[gameName]["GameName"] = gameName

        # 在字典的新的游戏中，创建一个脚本的字典
        self.gameDict[gameName][script.scriptName] = {}
        self.gameDict[gameName][script.scriptName]["scriptType"] = script.scriptType
        self.gameDict[gameName][script.scriptName]["scriptArgs"] = script.scriptArgs

    def ShowAll(self):
        for k in self.gameDict:
            print("{}:{}".format(k, self.gameDict[k]))


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


def _async_raise(tid, exctype):
    tid = ctypes.c_long(tid)
    print(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread error")
    elif res != 1:
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")


def stop_thread(thread):
    if thread == None:
        print("thread is None,return...")
        return
    _async_raise(thread.ident, SystemExit)


if __name__ == "__main__":
    pass


