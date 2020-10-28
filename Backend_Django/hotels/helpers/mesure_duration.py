import time
import logging
import coloredlogs

logger = logging.getLogger(__name__)

class MeasureDuration:
    def __init__(self,message):
        self.start = None
        self.end = None
        self.message = message
 
    def __enter__(self):
        self.start = time.time()
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end = time.time()
        logger.info("%s -> Time taken: %sms" % (self.message, str(self.duration())))
 
    def duration(self):
        return round((self.end - self.start) * 1000,2)
