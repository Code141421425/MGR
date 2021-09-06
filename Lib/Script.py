import os


class Script:
    scriptName = ""
    gameName = ""
    deviceId = ""
    _defaultDeviceId = "0123456789ABCDEF"
    rootPath = os.path.abspath("..\\..\\")

    def __init__(self, gameName, scriptName, deviceId = None):
        self.scriptName = scriptName
        self.gameName = gameName

        if deviceId:
            self.deviceId = deviceId
        else:
            self.deviceId = self._defaultDeviceId

    def run(self):
        pass


class QuickScript(Script):
    def run(self):
        cmd_start = "python %s\\Lib\\ScriptLauncher.py %s\\Scripts\\%s\\%s.air --device Android:///%s" % (
            self.rootPath, self.rootPath, self.gameName, self.scriptName, self.deviceId)
        print("启动脚本：" + self.scriptName + " |:|->" + cmd_start)
        os.system(cmd_start)


class QuickScript_withArgs(Script):
    args = []

    def __init__(self, scriptName, gameName, args, deviceId = None):
        super().__init__(scriptName, gameName, deviceId)
        self.args = args

    def run(self):
        path = self.rootPath + "\\Scripts\\" + self.gameName
        cmd_start = "python %s\\Lib\\ScriptLauncher.py %s\\%s.air --device Android:///%s" % (
        self.rootPath, path, self.scriptName, self.deviceId)
        print("启动脚本：" + self.scriptName + " |:|->" + cmd_start)
        print(self.scriptName, self.args)
