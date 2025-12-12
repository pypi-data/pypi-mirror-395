from pyxavi import Config, Dictionary, TerminalColor
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from logging import Logger as OriginalLogger
import logging
import multiprocessing_logging
import sys
import os
import re


class Logger:
    """Class to help on instantiating Logging

    It uses the built-in logging infra, but takes the
    configuration from the given config object.

    It is meant to be used the first time in the initial
    executor, then passed through the code.

    The built-in logging system can also be used to pick up
    an already instantiated logger with this class,
    making it very versatile.

    :Authors:
        Xavier Arnaus <xavi@arnaus.net>

    """

    TIME_FORMAT = "%H:%M:%S"
    DEFAULTS = {
        "name": "custom_logger",
        "loglevel": 20,
        "format": "[%(asctime)s] %(levelname)-8s %(name)-12s %(message)s",
        "file": {
            "active": False,
            "multiprocess": False,
            "filename": "debug.log",
            "encoding": "UTF-8",
            "rotate": {
                "active": False,
                "when": "midnight",
                "backup_count": 10,
                "utc": False,
                "at_time": "1:0:0"
            },
        },
        "stdout": {
            "active": False,
            "colorize": {
                "active": True,
                "profile": "by_level",
                "only_the_field": False,
                "by_level": {
                    "DEBUG": "WHITE",
                    "INFO": "BLUE",
                    "WARNING": "ORANGE",
                    "ERROR": "RED",
                    "CRITICAL": "RED_BRIGHT",
                },
                "by_process": {
                    "MainProcess": "GREEN_BRIGHT",
                },
                "by_thread": {
                    "MainThread": "GREEN_BRIGHT",
                },
                "support": {
                    "END": "END",
                    "UNKNOWN": "BOLD",
                },
                "colors": {
                    "BLACK": TerminalColor.BLACK,
                    "RED": TerminalColor.RED,
                    "GREEN": TerminalColor.GREEN,
                    "YELLOW": TerminalColor.YELLOW,
                    "BLUE": TerminalColor.BLUE,
                    "MAGENTA": TerminalColor.MAGENTA,
                    "CYAN": TerminalColor.CYAN,
                    "WHITE": TerminalColor.WHITE,
                    "ORANGE": TerminalColor.ORANGE,
                    "BLACK_BRIGHT": TerminalColor.BLACK_BRIGHT,
                    "RED_BRIGHT": TerminalColor.RED_BRIGHT,
                    "GREEN_BRIGHT": TerminalColor.GREEN_BRIGHT,
                    "YELLOW_BRIGHT": TerminalColor.YELLOW_BRIGHT,
                    "BLUE_BRIGHT": TerminalColor.BLUE_BRIGHT,
                    "MAGENTA_BRIGHT": TerminalColor.MAGENTA_BRIGHT,
                    "CYAN_BRIGHT": TerminalColor.CYAN_BRIGHT,
                    "WHITE_BRIGHT": TerminalColor.WHITE_BRIGHT,
                    "ORANGE_BRIGHT": TerminalColor.ORANGE_BRIGHT,
                    "BOLD": TerminalColor.BOLD,
                    "UNDERLINE": TerminalColor.UNDERLINE,
                    "END": TerminalColor.END,
                }
            },
            "multiprocess": False,
        }
    }

    _logger: OriginalLogger = None
    _base_path: str = None
    _logger_config: Dictionary = None
    _handlers = []
    __using_old_config = False

    def __init__(self, config: Config, base_path: str = None) -> None:

        self._base_path = base_path
        self._load_config(config=config)

        # Setting up the handlers straight away
        self._clean_handlers()
        self._set_handlers()

        # Define basic configuration
        logging.basicConfig(
            # Define logging level
            level=self._logger_config.get("loglevel"),
            # Define the format of log messages
            format=self._logger_config.get("format"),
            # Declare handlers
            handlers=self._handlers
        )

        # Define your own logger name
        self._logger = logging.getLogger(self._logger_config.get("name"))

        # Make it available for multiprocessing
        if self._logger_config.get("stdout.multiprocess"):
            multiprocessing_logging.install_mp_handler(logger=self._logger)

        # In case we are using the old config, show a warning
        if self.__using_old_config:
            self._logger.warning(
                f"{TerminalColor.YELLOW_BRIGHT}[pyxavi] " +
                "An old version of the configuration file structure for " +
                "the Logger module has been loaded. This is deprecated.\n" +
                "Please migrate your configuration file to the new structure.\n" +
                "Read https://github.com/XaviArnaus/pyxavi/blob/main/docs/logger.md" +
                f"{TerminalColor.END}"
            )

    def _load_config(self, config: Config) -> None:
        # We may receive the old config, so here the strategy:
        #   1. Try to read the old config. No defaults, empty spaces as None.
        #   2. Try to read the new config. No defaults, empty spaces as None.
        #   3. Merge the objects, intersecting with preference to whoever is not None.
        #   4. Load the defaults
        #   5. Merge the intersected config over the defaults.
        #   6. Do the normal amends (base path on filename, calculation of at_time)
        #   7. Set the config data as usual.
        #
        old_config_values = self._load_old_config_without_defaults(config=config)
        new_config_values = self._load_new_config_without_defaults(config=config)
        intersected = Dictionary(
            {
                "logger": {
                    "name": new_config_values.get(
                        "logger.name", old_config_values.get("logger.name")
                    ),
                    "loglevel": new_config_values.get(
                        "logger.loglevel", old_config_values.get("logger.loglevel")
                    ),
                    "format": new_config_values.get(
                        "logger.format", old_config_values.get("logger.format")
                    ),
                    "file": {
                        "active": new_config_values.get(
                            "logger.file.active", old_config_values.get("logger.file.active")
                        ),
                        "multiprocess": new_config_values.get("logger.file.multiprocess"),
                        "filename": new_config_values.get(
                            "logger.file.filename",
                            old_config_values.get("logger.file.filename")
                        ),
                        "encoding": new_config_values.get("logger.file.encoding"),
                        "rotate": {
                            "active": new_config_values.get("logger.file.rotate.active"),
                            "when": new_config_values.get("logger.file.rotate.when"),
                            "backup_count": new_config_values.
                            get("logger.file.rotate.backup_count"),
                            "utc": new_config_values.get("logger.file.rotate.utc"),
                            "at_time": new_config_values.get("logger.file.rotate.at_time")
                        },
                    },  # Standard output logging
                    "stdout": {
                        "active": new_config_values.get(
                            "logger.stdout.active",
                            old_config_values.get("logger.stdout.active")
                        ),
                        "multiprocess": new_config_values.get("logger.stdout.multiprocess"),
                        "colorize": {
                            "active": new_config_values.get("logger.stdout.colorize.active"),
                            "only_the_field": new_config_values.
                            get("logger.stdout.colorize.only_the_field"),
                            "profile": new_config_values.get("logger.stdout.colorize.profile"),
                            "by_level": new_config_values.
                            get("logger.stdout.colorize.by_level"),
                            "by_process": new_config_values.
                            get("logger.stdout.colorize.by_process"),
                            "by_thread": new_config_values.
                            get("logger.stdout.colorize.by_thread"),
                            "support": new_config_values.get("logger.stdout.colorize.support"),
                            "colors": new_config_values.get("logger.stdout.colorize.colors")
                        },
                    },
                }
            }
        )

        intersected.remove_none()
        if intersected.get_keys_in("logger.file.rotate") == []:
            intersected.delete("logger.file.rotate")
        defaults = Dictionary({"logger": self.DEFAULTS})
        defaults.merge(intersected)

        # And now the proper work:
        filename = defaults.get("logger.file.filename")
        if self._base_path is not None:
            defaults.set("logger.file.filename", os.path.join(self._base_path, filename))
        defaults.set(
            "logger.file.rotate.at_time",
            datetime.strptime(defaults.get("logger.file.rotate.at_time"),
                              self.TIME_FORMAT).time()
        )
        self._logger_config = Dictionary(defaults.get("logger"))

        #
        # Uncoment the following code once the deprecation is
        #   expired and the old support code above is gone
        #
        # Previous work
        # filename = config.get(
        #   "logger.file.filename", self.DEFAULT_FILE_LOGGING["file"]["filename"]
        # )
        # if self._base_path is not None:
        #     filename = os.path.join(self._base_path, filename)

        # # What we do here is to build a main dict where we ensure we always have a value.
        # self._logger_config = Dictionary(
        #     {
        #         "name": config.get("logger.name", self.DEFAULTS["name"]),
        #         "loglevel": config.get("logger.loglevel", self.DEFAULTS["loglevel"]),
        #         "format": config.get("logger.format", self.DEFAULTS["format"]),
        #         "file": {
        #             "active": config.get(
        #               "logger.file.active", self.DEFAULTS["file"]["active"]
        #              ),
        #             "filename": filename,
        #             "encoding": config.get(
        #                 "logger.file.encoding", self.DEFAULTS["file"]["encoding"]
        #             ),
        #             "rotate": {
        #                 "active": config.get(
        #                     "logger.file.rotate.active",
        #                     self.DEFAULTS["file"]["rotate"]["active"]
        #                 ),
        #                 "when": config.get(
        #                     "logger.file.rotate.when", self.DEFAULTS["file"]["rotate"]["when"]
        #                 ),
        #                 "backup_count": config.get(
        #                     "logger.file.rotate.backup_count",
        #                     self.DEFAULTS["file"]["rotate"]["backup_count"]
        #                 ),
        #                 "utc": config.get(
        #                     "logger.file.rotate.utc", self.DEFAULTS["file"]["rotate"]["utc"]
        #                 ),
        #                 "at_time": time(
        #                     *config.get(
        #                         "logger.file.rotate.at_time",
        #                         self.DEFAULTS["file"]["rotate"]["at_time"]
        #                     )
        #                 )
        #             },
        #         },
        #         "stdout": {
        #             "active": config.get(
        #                 "logger.stdout.active", self.DEFAULTS["stdout"]["active"]
        #             )
        #         }
        #     }
        # )

    def _load_old_config_without_defaults(self, config: Config) -> Dictionary:
        # Previous work
        filename = config.get("logger.filename")
        if self._base_path is not None and filename is not None:
            filename = os.path.join(self._base_path, filename)

        # What we do here is to build a main dict where we ensure we always have a value.
        logger_config = Dictionary(
            {
                "logger": {
                    # Common parameters
                    "name": config.get("logger.name"),
                    "loglevel": config.get("logger.loglevel"),
                    "format": config.get("logger.format"),  # File logging
                    "file": {
                        "active": config.get("logger.to_file"), "filename": filename
                    },  # Standard output logging
                    "stdout": {
                        "active": config.get("logger.to_stdout")
                    }
                }
            }
        )

        # In case we're using the condif loaded here, the old one,
        #   we want to warn that this is deprecated.
        if config.key_exists("logger.to_file") or config.key_exists("logger.to_stdout"):
            self.__using_old_config = True

        return logger_config

    def _load_new_config_without_defaults(self, config: Config) -> Dictionary:
        # Previous work
        filename = config.get("logger.file.filename")
        if self._base_path is not None and filename is not None:
            filename = os.path.join(self._base_path, filename)

        # What we do here is to build a main dict where we ensure we always have a value.
        return Dictionary(
            {
                "logger": {
                    # Common parameters
                    "name": config.get("logger.name"),
                    "loglevel": config.get("logger.loglevel"),
                    "format": config.get("logger.format"),  # File logging
                    "file": {
                        "active": config.get("logger.file.active"),
                        "multiprocess": config.get("logger.file.multiprocess"),
                        "filename": filename,
                        "encoding": config.get("logger.file.encoding"),
                        "rotate": {
                            "active": config.get("logger.file.rotate.active"),
                            "when": config.get("logger.file.rotate.when"),
                            "backup_count": config.get("logger.file.rotate.backup_count"),
                            "utc": config.get("logger.file.rotate.utc"),
                            "at_time": config.get("logger.file.rotate.at_time")
                        },
                    },  # Standard output logging
                    "stdout": {
                        "active": config.get("logger.stdout.active"),
                        "multiprocess": config.get("logger.stdout.multiprocess"),
                        "colorize": {
                            "active": config.get("logger.stdout.colorize.active"),
                            "only_the_field": config.
                            get("logger.stdout.colorize.only_the_field"),
                            "profile": config.get("logger.stdout.colorize.profile"),
                            "by_level": config.get("logger.stdout.colorize.by_level"),
                            "by_process": config.get("logger.stdout.colorize.by_process"),
                            "by_thread": config.get("logger.stdout.colorize.by_thread"),
                            "support": {
                                "END": config.get("logger.stdout.colorize.support.END"),
                                "UNKNOWN": config.get("logger.stdout.colorize.support.UNKNOWN"),
                            },
                            "colors": {
                                "BLACK": config.get("logger.stdout.colorize.colors.BLACK"),
                                "RED": config.get("logger.stdout.colorize.colors.RED"),
                                "GREEN": config.get("logger.stdout.colorize.colors.GREEN"),
                                "YELLOW": config.get("logger.stdout.colorize.colors.YELLOW"),
                                "BLUE": config.get("logger.stdout.colorize.colors.BLUE"),
                                "MAGENTA": config.get("logger.stdout.colorize.colors.MAGENTA"),
                                "CYAN": config.get("logger.stdout.colorize.colors.CYAN"),
                                "WHITE": config.get("logger.stdout.colorize.colors.WHITE"),
                                "ORANGE": config.get("logger.stdout.colorize.colors.ORANGE"),
                                "BLACK_BRIGHT": config.
                                get("logger.stdout.colorize.colors.BLACK_BRIGHT"),
                                "RED_BRIGHT": config.
                                get("logger.stdout.colorize.colors.RED_BRIGHT"),
                                "GREEN_BRIGHT": config.
                                get("logger.stdout.colorize.colors.GREEN_BRIGHT"),
                                "YELLOW_BRIGHT": config.
                                get("logger.stdout.colorize.colors.YELLOW_BRIGHT"),
                                "BLUE_BRIGHT": config.
                                get("logger.stdout.colorize.colors.BLUE_BRIGHT"),
                                "MAGENTA_BRIGHT": config.
                                get("logger.stdout.colorize.colors.MAGENTA_BRIGHT"),
                                "CYAN_BRIGHT": config.
                                get("logger.stdout.colorize.colors.CYAN_BRIGHT"),
                                "WHITE_BRIGHT": config.
                                get("logger.stdout.colorize.colors.WHITE_BRIGHT"),
                                "ORANGE_BRIGHT": config.
                                get("logger.stdout.colorize.colors.ORANGE_BRIGHT"),
                                "BOLD": config.get("logger.stdout.colorize.colors.BOLD"),
                                "UNDERLINE": config.
                                get("logger.stdout.colorize.colors.UNDERLINE"),
                                "END": config.get("logger.stdout.colorize.colors.END"),
                            }
                        },
                    }
                }
            }
        )

    def _set_handlers(self) -> None:
        if self._logger_config.get("file.active"):
            if self._logger_config.get("file.rotate.active"):
                class_handler = PIDTimedRotateFileHandler \
                    if self._logger_config.get("file.multiprocess") \
                    else TimedRotatingFileHandler
                self._handlers.append(
                    class_handler(
                        filename=self._logger_config.get("file.filename"),
                        when=self._logger_config.get("file.rotate.when"),
                        backupCount=self._logger_config.get("file.rotate.backup_count"),
                        encoding=self._logger_config.get("file.encoding"),
                        utc=self._logger_config.get("file.rotate.utc"),
                        atTime=self._logger_config.get("file.rotate.at_time"),
                    )
                )
            else:
                class_handler = PIDFileHandler \
                    if self._logger_config.get("file.multiprocess") \
                    else logging.FileHandler
                self._handlers.append(
                    class_handler(
                        filename=self._logger_config.get("file.filename"),
                        mode='a',
                        encoding=self._logger_config.get("file.encoding")
                    )
                )

        if self._logger_config.get("stdout.active"):
            handler = logging.StreamHandler(sys.stdout)
            if self._logger_config.get("stdout.colorize.active"):
                handler.setFormatter(ColorFormatter(self._logger_config))
            self._handlers.append(handler)

    def _clean_handlers(self) -> None:
        if self._logger is not None and self._logger.hasHandlers():
            self._logger.handlers.clear()
        if len(self._handlers) > 0:
            self._handlers = []

    def get_logger(self) -> OriginalLogger:
        return self._logger


class ColorFormatter(logging.Formatter):

    colors = Logger.DEFAULTS["stdout"]["colorize"]["colors"]
    fmt = Logger.DEFAULTS["format"]
    profile = Logger.DEFAULTS["stdout"]["colorize"]["profile"]
    only_the_field = Logger.DEFAULTS["stdout"]["colorize"]["only_the_field"]

    pattern_whole_line = re.compile(r"^(.*)$", re.MULTILINE)
    patterns_by_profile = {
        "by_level": re.compile(r"(\%\(levelname\)(-[0-9]+)?s)"),
        "by_process": re.compile(r"(\%\(processName\)(-[0-9]+)?s)"),
        "by_thread": re.compile(r"(\%\(threadName\)(-[0-9]+)?s)"),
    }
    keywords_by_profile = {
        "by_level": "levelname",
        "by_process": "processName",
        "by_thread": "threadName",
    }

    FORMATS = {}

    def __init__(self, config: Config = None):
        super(ColorFormatter, self).__init__()

        if config is not None:
            self.colors = self.load_colors_from_config(config)
            self.fmt = config.get("format", self.fmt)
            self.profile = config.get("stdout.colorize.profile", self.profile)
            self.only_the_field = config.get("stdout.colorize.only_the_field", True)
            self.alter_format_by_profile(config)

    def load_colors_from_config(self, config: Config):
        colors: dict = config.get("stdout.colorize.colors", self.colors)
        for name, color in colors.items():
            colors[name] = color.encode('utf-8').decode('unicode-escape')
        return colors

    def alter_format_by_profile(self, config: Config):

        profile = config.get("stdout.colorize.profile", "by_level")
        self.replace_format_string_with_placeholders(profile)

        if profile == "by_level":
            self.FORMATS = {
                logging.DEBUG: self.fmt.format(
                    self.colors[config.get("stdout.colorize.by_level.DEBUG", "WHITE")],
                    self.colors["END"]
                ),
                logging.INFO: self.fmt.format(
                    self.colors[config.get("stdout.colorize.by_level.INFO", "BLUE")],
                    self.colors["END"]
                ),
                logging.WARNING: self.fmt.format(
                    self.colors[config.get("stdout.colorize.by_level.WARNING", "ORANGE")],
                    self.colors["END"]
                ),
                logging.ERROR: self.fmt.format(
                    self.colors[config.get("stdout.colorize.by_level.ERROR", "RED")],
                    self.colors["END"]
                ),
                logging.CRITICAL: self.fmt.format(
                    self.colors[config.get("stdout.colorize.by_level.CRITICAL", "RED_BRIGHT")],
                    self.colors["END"]
                ),
            }
        elif profile == "by_process":
            for process_name, color in config.get("stdout.colorize.by_process", {}).items():
                self.FORMATS[process_name] = self.fmt.format(
                    self.colors[color], self.colors["END"]
                )
        elif profile == "by_thread":
            for thread_name, color in config.get("stdout.colorize.by_thread", {}).items():
                self.FORMATS[thread_name] = self.fmt.format(
                    self.colors[color], self.colors["END"]
                )

    def replace_format_string_with_placeholders(self, profile: str):
        if self.only_the_field:
            pattern = self.patterns_by_profile.get(profile)
        else:
            pattern = self.pattern_whole_line
        self.fmt = pattern.sub(r"{}\1{}", self.fmt)

    def clean_process_or_thread_name(self, name: str) -> str:
        return re.sub(r'[^a-zA-Z0-9](.)*', '', name)

    def format(self, record: logging.LogRecord):
        if self.profile == "by_process":
            log_fmt = self.FORMATS.get(self.clean_process_or_thread_name(record.processName))
        elif self.profile == "by_thread":
            log_fmt = self.FORMATS.get(self.clean_process_or_thread_name(record.threadName))
        else:
            log_fmt = self.FORMATS.get(record.levelno)

        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class PIDTimedRotateFileHandler(TimedRotatingFileHandler):

    def __init__(
        self,
        filename,
        when='h',
        interval=1,
        backupCount=0,
        encoding=None,
        delay=False,
        utc=False,
        atTime=None,
        errors=None
    ):
        filename = self._append_pid_to_filename(filename)
        super(PIDTimedRotateFileHandler, self).__init__(
            filename=filename,
            when=when,
            backupCount=backupCount,
            encoding=encoding,
            utc=utc,
            atTime=atTime
        )

    def _append_pid_to_filename(self, filename):
        pid = os.getpid()
        path, extension = os.path.splitext(filename)
        return '{0}-{1}{2}'.format(path, pid, extension)


class PIDFileHandler(logging.FileHandler):

    def __init__(self, filename, mode='a', encoding=None, delay=0):
        filename = self._append_pid_to_filename(filename)
        super(PIDFileHandler, self).__init__(filename, mode, encoding, delay)

    def _append_pid_to_filename(self, filename):
        pid = os.getpid()
        path, extension = os.path.splitext(filename)
        return '{0}-{1}{2}'.format(path, pid, extension)
