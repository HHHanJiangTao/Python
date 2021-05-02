import os
import time
import logging


class Log:
    def __init__(self,
        log_id="log_%s" % time.time(),
        file_mode="w",
        file_level=logging.INFO,
        file_enable=True,
        stream_level=logging.INFO,
        stream_enable=True):
        """Log

        @param log_id: id for log
        @param file_mode: log file operate mode "a+" "w" etc.
        @param file_level: file log level
        @param file_enable: file log enable
        @param stream_level: stream log level
        @param stream_enable: stream log enable
        """
        self.logger = logging.getLogger(log_id)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        log_handler = list()
        if file_enable:
            log_file = os.path.join(os.getcwd(), 'log', '%s.log' % (log_id))
            if not os.path.isdir(os.path.join(os.getcwd(), 'log')):
                os.makedirs(os.path.join(os.getcwd(), 'log'))
            file_handler = logging.FileHandler(log_file, file_mode, encoding='utf-8')
            file_handler.setLevel(file_level)
            file_handler.setFormatter(formatter)
            log_handler.append(file_handler)

        if stream_enable:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(stream_level)
            stream_handler.setFormatter(formatter)
            log_handler.append(stream_handler)

        for handler in log_handler:
            self.logger.addHandler(handler)

    def debug(self, *args, **kwds):
        self.logger.debug(*args, **kwds)
 
    def info(self, *args, **kwds):
        self.logger.info(*args, **kwds)
 
    def warning(self, *args, **kwds):
        self.logger.warning(*args, **kwds)
 
    def error(self, *args, **kwds):
        self.logger.error(*args, **kwds)

STREAM_INFO_INSTANCE = Log(file_enable=False)