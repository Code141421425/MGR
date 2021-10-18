import json
import requests
from Logger import MGRLogger


class Notice:
    FINISH_REPORT = "Mission Complete"
    ERROR_REPORT = "Error occurred, Need manual handle"

    def SendNotice(self, noticeType):
        pass


class DingDingNotice(Notice):
    __WEBHOOK = "https://oapi.dingtalk.com/robot/send?access_token=0cb25d1a4cbc4ac1117b7c95b9242717dd77a5bc26a891545c6fbeabe1cb6141"
    KEY_WORD = "[MGR]"

    def SendTextNotice(self, content, isAtAdmin=False):
        HEADERS = {
            "Content-Type": "application/json",
            "charset": "utf-8"
        }
        DATA = {
            "msgtype": "text",
            "text": {
               "content": "%s:%s" % (self.KEY_WORD, str(content))
            },
        }

        if isAtAdmin:
            DATA["at"] = {"atMobiles": ["13261542384"]}

        DATA = json.dumps(DATA)
        res = requests.post(self.__WEBHOOK, data=DATA, headers=HEADERS)
        MGRLogger().logger.info(res.text)

if __name__ == "__main__":
    MGRLogger().logger.info("123443335")
    #DingDingNotice().SendTextNotice("123")
    #MGRLogger().logger.info("12")
