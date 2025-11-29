import logging
from datetime import datetime
import inspect

class Logging():
    def __init__(self, name="automation_log"):
        self.name = name
        logger_name = inspect.stack()[1][3]
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.DEBUG)
        self.logname = self.getlogname()

    def logger(self):
        fh = logging.FileHandler('..\\Logs\\{}'.format(self.logname), mode='w')
        fh.setLevel(logging.CRITICAL)
        ch = logging.StreamHandler()
        format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                   datefmt='%d-%m-%y %I:%M:%S %p')
        fh.setFormatter(format)
        ch.setFormatter(format)
        self.logger.addHandler(fh)
        self.logger.addHandler(ch)
        return  self.logger

    def getlogname(self):
        trail = datetime.strftime(datetime.now(), "%Y-%m-%d_%I%M%S%p")
        return self.name + trail + ".log"


# def logging_function():
#     logger.debug("Hello this is debug message")
#     logger.info("Hello this is info message")
#     logger.warning("Hello this is warning message")
#     logger.error("Hello this is error message")
#     logger.critical("Hello this is critical message")
# logging_function()