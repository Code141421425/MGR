import logging
import os
from logging.handlers import TimedRotatingFileHandler


def singleton(cls):
    instances = {}

    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return _singleton


@singleton
class MGRLogger:
    notice = None
    logger = None
    LOG_PATH = os.path.abspath(__file__)+'/../../Log/'

    def __init__(self, noticeType=None):
        self.notice = noticeType

        self.logger = logging.getLogger("MGR_Logger")
        self.logger.setLevel(logging.INFO)

        self.streamHandler = logging.StreamHandler()
        self.fileHandler = TimedRotatingFileHandler(self.LOG_PATH+"MGR Report",
                                                    when="D")
        self.fileHandler.suffix = "%Y-%m-%d_%H-%M-%S.log"

        self.formatter = logging.Formatter("[%(levelname)-8s]%(asctime)s "
                                           "|%(filename)s: %(funcName)s (%(lineno)s) "
                                           "| %(message)s",
                                           datefmt="%Y-%m-%d %H:%M:%S")

        self.logger.addHandler(self.streamHandler)
        self.logger.addHandler(self.fileHandler)
        self.streamHandler.setFormatter(self.formatter)
        self.fileHandler.setFormatter(self.formatter)


if __name__ == "__main__":
    lg = MGRLogger().logger

    lg.debug("000")
    lg.info("111")
    lg.warning("222")
    lg.error("333")


