import json
import logging
from datetime import datetime, timedelta
from flask import (
    Request, Response,
    request, jsonify, send_file
)
from io import BytesIO
from enum import StrEnum
from pathlib import Path
from pypomes_core import (
    APP_PREFIX, TEMP_FOLDER, Mimetype, DatetimeFormat, IntEnumUseName,
    env_get_str, env_get_path, env_get_enum,
    datetime_parse, dict_jsonify, str_as_list,
    validate_enum, validate_format_error, validate_format_errors
)
from typing import Any, Final


class LogLevel(IntEnumUseName):
    """
    The Python log levels.
    """
    NOTSET = logging.NOTSET         # 0
    DEBUG = logging.DEBUG           # 10
    INFO = logging.INFO             # 20
    WARNING = logging.WARNING       # 30
    ERROR = logging.ERROR           # 40
    CRITICAL = logging.CRITICAL     # 50


class LogGetParam(StrEnum):
    """
    Parameters for configuring the logger.
    """
    LOG_FILENAME = "log-filename"            # a POSIX-style filename
    LOG_LEVEL = "log-level"                  # 'debug', 'info', 'warning', 'error', 'critical', defaults to 'debug'
    LOG_THREADS = "log-threads"              # threads identification
    LOG_FROM_DATETIME = "log-from-datetime"  # interval start (YYYYMMDDhhmmss)
    LOG_TO_DATETIME = "log-to-datetime"      # interval finish (YYYYMMDDhhmmss)
    LOG_LAST_DAYS = "log-last-days"          # back days to start from
    LOG_LAST_HOURS = "log-last-hours"        # back hours to start from


class LogPostParam(StrEnum):
    """
    Parameters for configuring the logger.
    """
    LOG_FILEMODE = "log-filemode"    # 'a' or 'w'
    LOG_FILEPATH = "log-filepath"    # a valid path
    LOG_FORMAT = "log-format"        # defaults to __LOG_DEFAULT_FORMAT (see below)
    LOG_LEVEL = "log-level"          # 'debug', 'info', 'warning', 'error', 'critical', 'notset' (default)
    LOG_STYLE = "log-style"          # '{', '%', '$'
    LOG_TIMESTAMP = "log-timestamp"  # defaults to '%Y-%m-%d %H:%M:%S'


PYPOMES_LOGGER: logging.Logger | None = None
_LOG_CONFIG: dict[LogPostParam, Any] = {}

__LOG_ID: Final[str] = APP_PREFIX or "_L"
__LOG_DEFAULT_FORMAT: Final[str] = ("{asctime} {levelname:1.1} {thread:5d} "
                                    "{module:20.20} {funcName:20.20} {lineno:3d} {message}")
__LOG_DEFAULT_FILEPATH: Final[Path] = Path(TEMP_FOLDER, f"{APP_PREFIX.lower()}.log")


def logging_startup(args: dict[str, Any] = None) -> None:
    """
    Configure/reconfigure and start/restart the log service.

    The parameters for configuring the log can be found either as environment variables, or as
    attributes in *args*. Default values are used, if necessary.

    :param args: optional log parameters and corresponding values
    """
    args = args or {}

    logging_level: LogLevel = args.get(LogPostParam.LOG_LEVEL,
                                       _LOG_CONFIG.get(LogPostParam.LOG_LEVEL) or
                                       env_get_enum(key=f"{APP_PREFIX}_LOGGING_LEVEL",
                                                    enum_class=LogLevel,
                                                    def_value=LogLevel.NOTSET))
    logging_format: str = args.get(LogPostParam.LOG_FORMAT,
                                   _LOG_CONFIG.get(LogPostParam.LOG_FORMAT) or
                                   env_get_str(key=f"{APP_PREFIX}_LOGGING_FORMAT",
                                               def_value=__LOG_DEFAULT_FORMAT))
    logging_style: str = args.get(LogPostParam.LOG_STYLE,
                                  _LOG_CONFIG.get(LogPostParam.LOG_STYLE) or
                                  env_get_str(key=f"{APP_PREFIX}_LOGGING_STYLE",
                                              def_value="{"))
    logging_datetime: str = args.get(LogPostParam.LOG_TIMESTAMP,
                                     _LOG_CONFIG.get(LogPostParam.LOG_TIMESTAMP) or
                                     env_get_str(key=f"{APP_PREFIX}_LOGGING_TIMESTAMP",
                                                 def_value=DatetimeFormat.INV))
    logging_filemode: str = args.get(LogPostParam.LOG_FILEMODE,
                                     _LOG_CONFIG.get(LogPostParam.LOG_FILEMODE) or
                                     env_get_str(key=f"{APP_PREFIX}_LOGGING_FILEMODE",
                                                 def_value="w"))
    logging_filepath: Path = Path(args.get(LogPostParam.LOG_FILEPATH,
                                           _LOG_CONFIG.get(LogPostParam.LOG_FILEPATH) or
                                           env_get_path(key=f"{APP_PREFIX}_LOGGING_FILEPATH",
                                                        def_value=__LOG_DEFAULT_FILEPATH)))
    logging_filepath.parent.mkdir(parents=True,
                                  exist_ok=True)
    _LOG_CONFIG[LogPostParam.LOG_LEVEL] = logging_level
    _LOG_CONFIG[LogPostParam.LOG_FORMAT] = logging_format
    _LOG_CONFIG[LogPostParam.LOG_STYLE] = logging_style
    _LOG_CONFIG[LogPostParam.LOG_TIMESTAMP] = logging_datetime
    _LOG_CONFIG[LogPostParam.LOG_FILEMODE] = logging_filemode
    _LOG_CONFIG[LogPostParam.LOG_FILEPATH] = logging_filepath

    # is there a logger ?
    global PYPOMES_LOGGER
    if PYPOMES_LOGGER:
        # yes, shut it down
        logging.shutdown()
        force_reset: bool = True
    else:
        # no
        force_reset: bool = False

    # start and configure the logger
    PYPOMES_LOGGER = logging.getLogger(name=__LOG_ID)
    # decide whether the logger's output is to be streamed
    if str(logging_filepath) == "stdout":
        logging.basicConfig(format=_LOG_CONFIG[LogPostParam.LOG_FORMAT],
                            datefmt=_LOG_CONFIG[LogPostParam.LOG_TIMESTAMP],
                            style=_LOG_CONFIG[LogPostParam.LOG_STYLE],
                            level=_LOG_CONFIG[LogPostParam.LOG_LEVEL],
                            force=force_reset)
    else:
        logging.basicConfig(filename=_LOG_CONFIG[LogPostParam.LOG_FILEPATH],
                            filemode=_LOG_CONFIG[LogPostParam.LOG_FILEMODE],
                            format=_LOG_CONFIG[LogPostParam.LOG_FORMAT],
                            datefmt=_LOG_CONFIG[LogPostParam.LOG_TIMESTAMP],
                            style=_LOG_CONFIG[LogPostParam.LOG_STYLE],
                            level=_LOG_CONFIG[LogPostParam.LOG_LEVEL],
                            force=force_reset)
    for handler in logging.root.handlers:
        handler.addFilter(filter=logging.Filter(__LOG_ID))


def logging_shutdown() -> None:
    """
    Invoke this function at shutdown.
    """
    global PYPOMES_LOGGER
    if PYPOMES_LOGGER:
        logging.shutdown()
        PYPOMES_LOGGER = None


def logging_get_entries(log_level: LogLevel = None,
                        log_from: datetime = None,
                        log_to: datetime = None,
                        log_threads: list[str] = None,
                        errors: list[str] = None) -> BytesIO:
    """
    Extract and return entries in the current logging file.

    Parameters specify criteria for log entry selection, and are optional.
    Intervals are inclusive (*[log_from, log_to]*).
    It is required that the current logging file be compliant with the default format,
    or that criteria for log entry selection not be specified.

    The current default format for the log is (field descriptions follow):
        {asctime} {levelname:1.1} {thread:5d} {module:20.20} {funcName:20.20} {lineno:3d} {message}
        *asctime*: timestamp, as YYYY-MM-DD hh:mm:ss
        *levelname:1.1*: first letter of the log level, in uppercase (N, D, I, W, E, C)
        *thread:5d*: first 5 digits of the thread id
        *module:20.20*: first 20 digits of the module name
        *funcName:20.20*: first 20 digits of the function name
        *lineno:3d* first 3 digits of the line number
        *message*: the log message

    :param log_level: the logging level (defaults to all levels)
    :param log_from: the initial timestamp (defaults to unspecified)
    :param log_to: the finaL timestamp (defaults to unspecified)
    :param log_threads: the threads originating the log entries (defaults to all threads)
    :param errors: incidental error messages
    :return: the logging entries meeting the specified criteria
    """
    # initialize the return variable
    result: BytesIO | None = None

    # verify whether inspecting the log entries is possible
    if _LOG_CONFIG[LogPostParam.LOG_FORMAT] == __LOG_DEFAULT_FORMAT or not \
            (log_level or log_from or log_to or log_threads):
        result = BytesIO()
        filepath: Path = _LOG_CONFIG[LogPostParam.LOG_FILEPATH]
        with filepath.open() as f:
            line: str = f.readline()
            while line:
                items: list[str] = line.split(sep=None,
                                              maxsplit=4)
                msg_level: int = LogLevel.CRITICAL \
                    if not log_level or len(items) < 3 \
                    else __get_level_value(log_label=items[2])
                if (not log_level or msg_level >= log_level) and \
                   (not log_threads or (len(items) > 3 and items[3] in log_threads)):
                    if len(items) > 1 and (log_from or log_to):
                        timestamp: datetime = datetime_parse(f"{items[0]} {items[1]}")
                        if not (timestamp or
                                ((not log_from or timestamp >= log_from) and
                                 (not log_to or timestamp <= log_to))):
                            result.write(line.encode())
                    else:
                        result.write(line.encode())
                line = f.readline()
    elif isinstance(errors, list):
        errors.append("It is not possible to apply level, timestamp "
                      "or threads criteria to filter log entries, "
                      "as the log format has been customized")

    return result


def logging_send_entries(args: dict[str, Any]) -> Response:
    """
    Retrieve from the log file, and send in response, the entries matching the criteria specified in *args*.

    :param args: the criteria for filtering the records to be returned
    :return: file containing the log entries requested
    """
    # declare the return variable
    result: Response

    # initialize the error messages list
    errors: list[str] = []

    # obtain the logging level (defaults to current level)
    log_level: LogLevel = validate_enum(source=args,
                                        attr=LogPostParam.LOG_LEVEL,
                                        enum_class=LogLevel,
                                        default=_LOG_CONFIG[LogPostParam.LOG_LEVEL],
                                        errors=errors)
    # obtain the thread id
    log_threads: list[str] = str_as_list(args.get(LogGetParam.LOG_THREADS))

    # obtain the  timestamps
    log_from: datetime = datetime_parse(dt_str=args.get(LogGetParam.LOG_FROM_DATETIME))
    log_to: datetime = datetime_parse(dt_str=args.get(LogGetParam.LOG_TO_DATETIME))

    if not log_from and not log_to:
        last_days: str = args.get(LogGetParam.LOG_LAST_DAYS, "0")
        last_hours: str = args.get(LogGetParam.LOG_LAST_HOURS, "0")
        offset_days: int = int(last_days) if last_days.isdigit() else 0
        offset_hours: int = int(last_hours) if last_hours.isdigit() else 0
        if offset_days or offset_hours:
            log_from = datetime.now() - timedelta(days=offset_days,
                                                  hours=offset_hours)
    # retrieve the log entries
    log_entries: BytesIO = logging_get_entries(log_level=log_level,
                                               log_from=log_from,
                                               log_to=log_to,
                                               log_threads=log_threads,
                                               errors=errors)
    if not errors:
        # return the log entries requested
        log_file = args.get(LogGetParam.LOG_FILENAME)
        log_entries.seek(0)
        result = send_file(path_or_file=log_entries,
                           mimetype=Mimetype.TEXT,
                           as_attachment=log_file is not None,
                           download_name=log_file)
    else:
        # report the failure
        result = Response(response=json.dumps(obj={"errors": errors}),
                          status=400,
                          mimetype=Mimetype.JSON)

    return result


# @flask_app.route(rule="/logging",
#                  methods=["GET", "POST"])
def service_logging() -> Response:
    """
    Entry pointy for configuring and retrieving the execution log of the system.

    The *GET* operation has a set of optional criteria, used to filter the records to be returned.
    They are specified according to the pattern
    *log-filename=<string>&log-level=<debug|info|warning|error|critical>&
    log-from_datetime=YYYYMMDDhhmmss&log-to-datetime=YYYYMMDDhhmmss&log-last_days=<n>&log-last_hours=<n>>*:
      - *log-filename*: the filename for saving the downloaded the data (if omitted, browser displays the data)
      - *log-level*: the logging level of the entries (defaults to *debug*)
      - *log-thread*: the thread originating the log entries (defaults to all threads)
      - *log-from-datetime*: the start timestamp
      - *log-to-datetime*: the finish timestamp
      - *log-last-days*: how many days before current date
      - *log-last-hours*: how may hours before current time

    The *POST* operation configures and starts/restarts the logger. These are the optional query parameters:
      - *log-filepath*: path for the log file
      - *log-filemode*: the mode for log file opening (a- append, w- truncate)
      - *log-level*: the logging level (*debug*, *info*, *warning*, *error*, *critical*)
      - *log-format*: the information and formats to be written to the log
      - *log-style*: the style used for building the 'log-format' parameter
      - *log-timestamp*: the format for displaying the date and time (defaults to YYYY-MM-DD HH:MM:SS)
    For omitted parameters, current existing parameter values are used, possibly obtained from environment variables.
    If *log-filepath* has the special value *stdout*, the log entries are streamed to the standard output,
    rather the written to a file, in which case *log-filemode* is ignored.

    :return: the requested log data, on *GET*, or the operation status, on *POST*
    """
    # retrieve the request parameters
    args: dict[str, Any] = dict(request.get_json(silent=True) or request.values or {})

    # log the request
    PYPOMES_LOGGER.debug(msg=logging_log_init(req=request))

    # validate the request parameters
    errors: list[str] = []
    if args:
        enum_class: Any = LogGetParam if request.method == "GET" else LogPostParam
        __assert_params(params=list(map(str, enum_class)),
                        args=args,
                        errors=errors)
    # run the request
    result: Response
    if errors:
        reply_err: dict = {"errors": validate_format_errors(errors=errors)}
        result = jsonify(reply_err)
        result.status_code = 400
    elif request.method == "GET":
        # retrieve the log
        result = logging_send_entries(args=args)
    else:
        # reconfigure the log
        logging_startup(args=args)
        reply: dict[str, Any] = {
            "status": "Log restarted",
            "configuration": dict_jsonify(source=logging_get_params())
        }
        result = jsonify(reply)

    # log the response
    PYPOMES_LOGGER.info(msg=f"Response {result}")

    return result


def logging_get_param(key: LogPostParam) -> Any:
    """
    Return the current value for logging parameter *key*.

    :param key: the reference parameter
    :return: the current value of the logging parameter
    """
    return _LOG_CONFIG.get(key)


def logging_get_params() -> dict[str, Any]:
    """
    Return the current logging parameters as a *dict*.

    Note that value associated with parameter *LogParam.LOG_FILEPATH* is not serializable.

    :return: the current logging parameters
    """
    return {str(k): v for (k, v) in _LOG_CONFIG.items()}


def logging_log_init(req: Request) -> str:
    """
    Build the information on the start of an HTTP request for logging.

    :param req: the reference HTTP request
    :return: the information to be written to the log
    """
    # retrieve the request arguments
    args: dict[str, Any] = dict(request.get_json(silent=True) or {})
    args.update(request.values or {})

    origin: str = req.headers.get(key="X-Forwarded-For",
                                  default=req.remote_addr)
    data: str = json.dumps(obj=args,
                           ensure_ascii=False)

    return f"Request {req.method}:{req.path}, from {origin}; {data}"


def __assert_params(params: list[str],
                    args: dict,
                    errors: list[str]) -> None:
    """
    Assert that the provided parameters are acceptable.

    :param errors: incidental errors
    :param params: acceptable parameters
    :param args: provided parameters and respective values
    """
    for key in args:
        if key not in params:
            # 122: Attribute is unknown or invalid in this context
            errors.append(validate_format_error(122,  # noqa: PERF401
                                                f"@{key}"))


def __get_level_value(log_label: str) -> int:
    """
    Translate the log severity *log_label* into the logging's internal severity value.

    :param log_label: the string log severity
    :return: the internal logging severity value
    """
    result: int
    match log_label.lower():
        case LogLevel.DEBUG.name | "d":
            result = LogLevel.DEBUG          # 10
        case LogLevel.INFO.name | "i":
            result = LogLevel.INFO           # 20
        case LogLevel.WARNING.name | "w":
            result = LogLevel.WARNING        # 30
        case LogLevel.ERROR | "e":
            result = LogLevel.ERROR          # 40
        case LogLevel.CRITICAL | "c":
            result = LogLevel.CRITICAL       # 50
        case _:
            result = LogLevel.NOTSET         # 0

    return result


# initialize the logger
logging_startup()
