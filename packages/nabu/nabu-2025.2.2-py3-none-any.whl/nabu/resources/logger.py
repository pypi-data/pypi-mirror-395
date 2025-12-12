import logging
import logging.config


class Logger:
    def __init__(self, loggername, level="DEBUG", logfile="logger.log", console=True, prefix=""):
        """
        Configure a Logger object.

        Parameters
        -----------
        loggername: str
            Logger name.
        level: str, optional
            Logging level. Can be "debug", "info", "warning", "error", "critical".
            Default is "debug".
        logfile: str, optional
            File where the logs are written.
            If set to None, the logs are not written in a file.
            Default is "logger.log".
        console: bool, optional
            If set to True, the logs are (also) written in stdout/stderr.
            Default is True.
        """
        self.loggername = loggername
        self.level = level
        self.logfile = logfile
        self.console = console
        self.prefix = prefix
        self._configure_logger()

    def set_prefix(self, prefix):
        self.prefix = prefix

    def _configure_logger(self):
        conf = self._get_default_config_dict()
        for handler in conf["handlers"]:
            conf["handlers"][handler]["level"] = self.level.upper()
        conf["loggers"][self.loggername]["level"] = self.level.upper()
        if not (self.console):
            conf["loggers"][self.loggername]["handlers"].remove("console")

        self.config = conf
        logging.config.dictConfig(conf)
        self.logger = logging.getLogger(self.loggername)

    def _get_default_config_dict(self):
        conf = {
            "version": 1,
            "formatters": {
                "default": {"format": "%(asctime)s - %(levelname)s - %(message)s", "datefmt": "%d-%m-%Y %H:%M:%S"},
                "console": {"format": "%(message)s"},
            },
            "handlers": {
                "console": {
                    "level": "DEBUG",
                    "class": "logging.StreamHandler",
                    "formatter": "console",
                    "stream": "ext://sys.stdout",
                },
                "file": {
                    "level": "DEBUG",
                    "class": "logging.FileHandler",
                    "formatter": "default",
                    "filename": self.logfile,
                },
            },
            "loggers": {
                self.loggername: {
                    "level": "DEBUG",
                    "handlers": ["console", "file"],
                    # This logger inherits from root logger - dont propagate !
                    "propagate": False,
                }
            },
            "disable_existing_loggers": False,
        }
        return conf

    def info(self, msg):
        return self.logger.info(self.prefix + msg)

    def debug(self, msg):
        return self.logger.debug(self.prefix + msg)

    def warning(self, msg):
        return self.logger.warning(self.prefix + msg)

    warn = warning

    def error(self, msg):
        return self.logger.error(self.prefix + msg)

    def fatal(self, msg):
        return self.logger.fatal(self.prefix + msg)

    def critical(self, msg):
        return self.logger.critical(self.prefix + msg)


def LoggerOrPrint(logger):
    """
    Logger that is either a "true" logger object, or a fall-back to "print".
    """
    if logger is None:
        return PrinterLogger()
    return logger


class PrinterLogger:
    def __init__(self, prefix=""):
        self.prefix = prefix
        self._configure_logger()

    def _configure_logger(self):
        methods = [
            "debug",
            "warn",
            "warning",
            "info",
            "error",
            "fatal",
            "critical",
        ]

        def _print(msg):
            print(self.prefix + msg)

        for method in methods:
            self.__setattr__(method, _print)

    def set_prefix(self, prefix):
        self.prefix = prefix
        self._configure_logger()


LogLevel = {
    "notset": logging.NOTSET,
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warn": logging.WARNING,
    "warning": logging.WARNING,
    "error": logging.ERROR,
    "critical": logging.CRITICAL,
    "fatal": logging.FATAL,
}
