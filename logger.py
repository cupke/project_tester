# Standard
import logging as log

# Project
import config as cf


class Logger:
    def __init__(self):
        self._logging_path = cf.LOGGING_PATH / 'log.log'
        log.basicConfig(  # formatting output string
            format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
            datefmt='%Y-%m-%d:%H:%M:%S',
            filename=self._logging_path,
            level=log.INFO
        )

    @staticmethod
    def __show_in_console(msg: str):
        print(msg)

    def clear_log_file(self):
        if self._logging_path:
            with open(self._logging_path, "w") as f:
                f.write("")
        return ""

    @staticmethod
    def info(msg: str):
        Logger.__show_in_console(msg)
        log.info(msg=msg)

    @staticmethod
    def warning(msg: str):
        Logger.__show_in_console(msg)
        log.warning(msg=msg)

    @staticmethod
    def error(msg: str):
        Logger.__show_in_console(msg)
        log.error(msg=msg)


logger = Logger()