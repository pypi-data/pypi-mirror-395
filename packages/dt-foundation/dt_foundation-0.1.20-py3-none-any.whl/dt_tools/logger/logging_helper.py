"""
Logging helper methods for loguru. (https://github.com/Delgan/loguru)

Example::

    import dt_tools.logger.logging_helper as lh
    from loguru import logger as LOGGER

    log_file = './mylog.log'

    # File logger
    f_handle = lh.configure_logger(log_target=log_file, log_level="DEBUG")
    # Console logger
    c_handle - lh.configure_logger()

    LOGGER.debug('this should only show up in file logger')
    LOGGER.info('this should show up in file logger and console')

"""
import functools
import inspect
import logging
import sys
import time
from typing import Dict, List

from loguru import logger as LOGGER

# Format variables:
# Variable    Description
# ----------- ------------------------------------------------------------
# elapsed     The time elapsed since the start of the program
# exception   The formatted exception if any, None otherwise
# extra       The dict of attributes bound by the user (see bind())
# file        The file where the logging call was made
# function    The function from which the logging call was made
# level       The severity used to log the message
# line        The line number in the source code
# message     The logged message (not yet formatted)
# module      The module where the logging call was made
# name        The __name__ where the logging call was made
# process     The process in which the logging call was made
# thread      The thread in which the logging call was made
# time        The aware local time when the logging call was made

DEFAULT_FILE_LOGFMT = "<green>{time:MM/DD/YY HH:mm:ss}</green> |<level>{level: <8}</level>|<cyan>{file:18}</cyan>|<cyan>{line:4}</cyan>| <level>{message}</level>"
"""For file logging, format- timestamp \|level\|method name\|lineno\|message"""

DEFAULT_CONSOLE_LOGFMT = "<level>{message}</level>"
"""For console logging, format- message"""

DEFAULT_DEBUG_LOGFMT =  "<green>{time:HH:mm:ss}</green> |<level>{level: <8}</level>|<cyan>{module:20}</cyan>|<cyan>{line:4}</cyan>| <level>{message}</level>"
"""For console/file logging, timestamp \|level\|method name\|lineno\|message"""

DEFAULT_DEBUG_LOGFMT2 =  "<green>{time:HH:mm:ss}</green> |<level>{level: <8}</level>|<yellow>{name:15}|{module:20}|{line:4}</yellow>| <level>{message}</level>"
"""For console/file logging, timestamp \|level\|method name\|lineno\|message"""

def configure_logger(log_target = sys.stderr, 
                     log_level: str = "INFO", 
                     log_format: str = None, 
                     brightness: bool = False, 
                     log_handle: int = 0, 
                     enqueue: bool = False,
                     propogate_loggers: List[str] = None,
                     enable_loggers: List[str] = None,
                     disable_loggers: List[str] = None,
                     **kwargs) -> int:
    """
    Configure logger via loguru.

     - should be done once for each logger (console, file,..)
     - if reconfiguring a logger, pass the log_handle
    
    Parameters:
        log_target: defaults to stderr, but can supply filename as well (default console/stderr)
        log_level : TRACE|DEBUG|INFO(dflt)|ERROR|CRITICAL (default INFO)
        log_format: format for output log line (loguru default)
        brightness: console messages bright or dim (default False)
        log_handle: handle of log being re-initialized. (default 0)
        enqueue   : to avoid collisions on the log in muti-processing applications. 
            See is_complete() and wait_for_complete().
        propogate_loggers: list of (legacy) loggers to propogate this configuration to.
        enable_loggers: list of loggers to enable messages from
        disable_loggers: list of loggers to disable messages from
        other     : keyword args related to loguru logger.add() function
            see: https://loguru.readthedocs.io/en/stable/api/logger.html#loguru._logger.Logger.add            

    Example::

        import dt_tools.logger.logging_helper as lh
        from loguru import logger as LOGGER

        log_file = './mylog.log'

        f_handle = lh.configure_logger(log_target=log_file, log_level="DEBUG")
        c_handle - lh.configure_logger()

        LOGGER.debug('this should only show up in file logger')
        LOGGER.info('this should show up in file logger and console')

    Returns:
        logger_handle_id: integer representing logger handle
    """
    # Ideas from: https://medium.com/@muh.bazm/how-i-unified-logging-in-fastapi-with-uvicorn-and-loguru-6813058c48fc
    try:
        if log_handle >= 0:
            # Remove specific handler
            LOGGER.remove(log_handle)
            LOGGER.trace(f'removed handler: {log_handle}')            
    except Exception as ex:
        if 'There is no existing' not in str(ex):
            LOGGER.error(f'configure_logger(): {ex}')

    # Intercept standard logging
    logging.basicConfig(handlers=[_InterceptHandler()], level=0, force=True)    

    if brightness is not None:
        set_log_levels_brightness(brightness)
        
    if log_format is None:
        # Set format based on type of logger (file vs console)        
        log_format = DEFAULT_FILE_LOGFMT if isinstance(log_target, str) else DEFAULT_CONSOLE_LOGFMT

    hndl = LOGGER.add(sink=log_target, 
                      level=log_level, 
                      format=log_format, 
                      enqueue=enqueue,
                      diagnose=True, 
                      **kwargs)
    # NOTE: This adds a new variable to LOGGER so current log level can be determined.
    LOGGER.log_level = log_level

    if propogate_loggers is not None:
        _propogate_loggers(propogate_loggers)
    if enable_loggers is not None:
        _enable_loggers(enable_loggers)
    if disable_loggers is not None:
        _disable_loggers(disable_loggers)

    if not hasattr(LOGGER, 'is_complete'):
        setattr(LOGGER, 'is_complete', is_complete)
    if not hasattr(LOGGER, 'waitfor_complete'):
        setattr(LOGGER, 'waitfor_complete', waitfor_complete)

    return hndl

class _InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        # Get corresponding Loguru level
        level: str | int
        try:
            level = LOGGER.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller to get correct stack depth
        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        LOGGER.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage()
        )

        
# =============================================================================================
def _propogate_loggers(loggers: list[str]) -> bool:
    for lgr_name in [x for x in loggers if x.strip() != '']:
        logging_logger = logging.getLogger(lgr_name)
        logging_logger.handlers = []
        logging_logger.propagate = True
        LOGGER.trace(f'- propogate set for {lgr_name}')

    return True

def _enable_loggers(loggers: list[str]) -> bool:
    for lgr in [x for x in loggers if x.strip() != '']:
        LOGGER.enable(lgr)
        LOGGER.trace(f'- logging enabled for {lgr}')

    return True

def _disable_loggers(loggers: list[str]) -> bool:
    for lgr in [x for x in loggers if x.strip() != '']:
        LOGGER.disable(lgr)
        LOGGER.trace(f'- logging disabled for {lgr}')

    return True


# =============================================================================================
def _print_log_level_definitions():
    for lvl in ['TRACE','DEBUG','INFO','SUCCESS','WARNING','ERROR','CRITICAL']:
        LOGGER.log(lvl, LOGGER.level(lvl))
    while not LOGGER.complete():
        pass

def set_log_levels_brightness(on: bool = True):
    """
    Set brighness of console log messages

    Args:
        on (bool, optional): True messages are bold (bright), False messages are dimmer. Defaults to True.
    """
    for lvl in ['TRACE','DEBUG','INFO','SUCCESS','WARNING','ERROR','CRITICAL']:
        color = LOGGER.level(lvl).color
        if on and '<bold>' not in color:
            color = f'{color}<bold>'
        elif not on:
            color = color.replace('<bold>', '')
        LOGGER.level(lvl, color=color)

def is_complete() -> bool:
    """
    Check if any log output is pending.

    Returns:
        bool: True if enqueue buffer is empty, else False (i.e. pending log lines)
    """
    return LOGGER.complete()

def waitfor_complete():
    """
    If logger has enqueue set, wait for any pending log lines to 
    be written before continuing.
    """
    while not LOGGER.complete():
        time.sleep(.1)

# =============================================================================================
def disable_non_loguru_loggers():
    loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    for lgr in loggers:
       logging.getLogger(lgr.name).disabled = True

def enable_non_loguru_loggers(logger_names: List[str]):
    for lgr in logger_names:
        logging.getLogger(lgr).disabled = False

def get_non_loguru_loggers() -> List[Dict[str, Dict]]:
    logger_list = []
    # loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
    loggers = [logging.getLogger(name) for name in logging.RootLogger.manager.loggerDict]
    for lgr in loggers:
        lgr.level
        entry = {
            "name": lgr.name,
            "disabled": lgr.disabled, 
            "parent": lgr.parent.name,
            "filters": lgr.filters,
            "handlers": lgr.handlers,
            "level": lgr.level,
            "elevel": lgr.getEffectiveLevel(),
        }
        logger_list.append(entry)
    
    return logger_list

# =============================================================================================
# == Logging Decorators =======================================================================
# =============================================================================================
def logger_wraps(*, entry=True, exit=True, level="DEBUG"):
    """
    function decorator wrapper to log entry and exit

    When decorator enabled, messages will automatically be included in the the log:
    Example::    

        @logger_wraps()
        def foo(a, b, c):
            logger.info("Inside the function")
            return a * b * c 

    """
    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            logger_ = LOGGER.opt(depth=1)
            if entry:
                logger_.log(level, "Entering '{}' (args={}, kwargs={})", name, args, kwargs)
            result = func(*args, **kwargs)
            if exit:
                logger_.log(level, "Exiting '{}' (result={})", name, result)
            return result

        return wrapped

    return wrapper

def timer_wraps(*, level="DEBUG"):
    """
    function decorator wrapper to log function execution time

    Example::

        @timer_wraps(level='INFO')
        def foo(a,b,c):
          logger.info('inside the function')
          time.sleep(1)
          return a * b * c

    """
    def wrapper(func):
        name = func.__name__

        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            """time_wrapper's doc string"""
            start = time.perf_counter()
            result = func(*args, **kwargs)
            time_elapsed = time.perf_counter() - start
            LOGGER.info(f"TIMER: Function: {name}, Time: {time_elapsed:.3f} seconds")
            return result
        return wrapped
    
    return wrapper


if __name__ == "__main__":
    import dt_tools.cli.demos.dt_foundation_demo as module
    module.demo()
