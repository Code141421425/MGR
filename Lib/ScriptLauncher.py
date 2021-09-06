import argparse
from airtest.cli.runner import AirtestCase, run_script
from airtest.cli.parser import runner_parser
import os


class ScriptLauncher(AirtestCase):
    gameName = ""
    scriptList = []
    deviceId = ""
    launcherArgs = ""

    PROJECT_ROOT = os.path.abspath(__file__ + "\\..\\..")
    SCRIPT_ROOT = PROJECT_ROOT + "\\Scripts\\"
    _defaultDeviceId = "Android:///0123456789ABCDEF"

    def __init__(self, gameName="TestGame", scriptList="TestGame_1", devicdId=_defaultDeviceId):
        super().__init__()
        self.gameName = gameName
        self.scriptList = scriptList
        self.deviceId = devicdId
        self.launcherArgs = self.__HandleArgs(("%s\\%s\\%s_1.air")
                                       % (self.SCRIPT_ROOT, self.gameName, self.gameName))

    # @classmethod
    # def setUpClass(cls):
    #     print("setUpClass")
    #     # print(cls,cls.__HandleArgs(("%s\\%s\\%s_StartUp.air")
    #     #                                % (cls.SCRIPT_ROOT, cls.gameName, cls.gameName)))
    #
    #     # run_script(cls.__HandleArgs(("%s\\%s\\%s_StartUp.air")
    #     #                                % (cls.SCRIPT_ROOT, cls.gameName, cls.gameName)))


    def setUp(self):
        print("custom setup")
        # add var/function/class/.. to globals
        self.scope["hunter"] = [176, 1778]
        self.scope["add"] = lambda x: x+1

        # exec setup script


        super(ScriptLauncher, self).setUp()

    def tearDown(self):
        print("custom tearDown")
        # exec teardown script
        super(ScriptLauncher, self).tearDown()

    @classmethod
    def tearDownClass(cls) -> None:
        print("tearDownClass(cls) -> None:")


    def __HandleArgs(self, script):
        return argparse.Namespace(
            compress=10, device=self.deviceId, no_image=None,
            log=None, recording=None, script=script)

    def Run(self):
        run_script(self.launcherArgs, ScriptLauncher)
        ##self.__setUp()
        ##self.__tearDown()


if __name__ == '__main__':
    print("="*10)
    #ap = runner_parser()
    #args = ap.parse_args()
   # print(args)
    #run_script(args, ScriptLauncher)

    run_script(ScriptLauncher().args,ScriptLauncher)

    #ScriptLauncher().Run()




    # print(sl.pt())
