import logging
import os
from logging.handlers import TimedRotatingFileHandler
from BaseClass import singleton


@singleton
class MGRLogger:
    notice = None
    logger = None
    LOG_PATH = os.path.abspath(__file__)+'/../../Log/'

    def __init__(self, noticeType=None,app=None):
        self.notice = noticeType

        self.logger = logging.getLogger("MGR_Logger")
        self.logger.setLevel(logging.DEBUG)

        self.streamHandler = logging.StreamHandler()
        self.streamHandler.setLevel(logging.INFO)
        self.fileHandler = TimedRotatingFileHandler(self.LOG_PATH+"MGR Report",
                                                    when="D")
        self.fileHandler.suffix = "%Y-%m-%d_%H-%M-%S.log"
        self.fileHandler.setLevel(logging.INFO)

        self.formatter = logging.Formatter("[%(levelname)-8s]%(asctime)s "
                                           "|%(filename)s: %(funcName)s (%(lineno)s) "
                                           "| %(message)s",
                                           datefmt="%Y-%m-%d %H:%M:%S")
        self.shortFormatter = logging.Formatter("[%(levelname)-8s]%(asctime)s | %(message)s",
                                           datefmt="%H:%M:%S")

        self.logger.addHandler(self.streamHandler)
        self.logger.addHandler(self.fileHandler)
        self.streamHandler.setFormatter(self.formatter)
        self.fileHandler.setFormatter(self.formatter)

        if app:
            self.appHandler = MGRHandler(app)
            self.appHandler.setLevel(logging.DEBUG)
            self.logger.addHandler(self.appHandler)
            self.appHandler.setFormatter(self.shortFormatter)


class MGRHandler(logging.Handler):
    def __init__(self, app, **kwargs):
        super(MGRHandler, self).__init__(**kwargs)
        self.app = app

    def emit(self, record):
        msg = self.format(record)
        print(msg)
        self.app.add_AddLog(msg)

if __name__ == "__main__":
    lg = MGRLogger().logger

    lg.debug("000")
    lg.info("111")
    lg.warning("222")
    lg.error("333")


