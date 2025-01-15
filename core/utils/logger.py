import io
import logging

class OnlyWarningsFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.WARNING

class OnlyErrorsFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.ERROR

class OnlyInfoFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.INFO

repaired_msg = '{dataSource}, {monumentName}, {localityName}, {errorReason}, {operation}'
excluded_msg = '{dataSource}, {monumentName}, {localityName}, {errorReason}'
succeded_msg = 'Dato insertado: {monumentName}'

repaired_stream = io.StringIO()
excluded_stream = io.StringIO()
succeded_stream = io.StringIO()

class MyLogger:
    _logger = None
    repaired_counter = 0
    excluded_counter = 0
    succeded_counter = 0

    def __init__(self):
        if MyLogger._logger is None:
            repaired_file_handler = logging.StreamHandler(repaired_stream)
            repaired_file_handler.setLevel(logging.WARNING)
            repaired_file_handler.addFilter(OnlyWarningsFilter())

            excluded_file_handler = logging.StreamHandler(excluded_stream)
            excluded_file_handler.setLevel(logging.ERROR)
            excluded_file_handler.addFilter(OnlyErrorsFilter())

            succeded_file_handler = logging.StreamHandler(succeded_stream)
            succeded_file_handler.setLevel(logging.INFO)
            succeded_file_handler.addFilter(OnlyInfoFilter())

            MyLogger._logger = logging.getLogger(__name__)
            MyLogger._logger.addHandler(repaired_file_handler)
            MyLogger._logger.addHandler(excluded_file_handler)
            MyLogger._logger.addHandler(succeded_file_handler)
            MyLogger._logger.setLevel(logging.INFO)

        self.logger = MyLogger._logger

    def log_repaired(self, dataSource, monumentName, localityName, errorReason, operation):
        self.logger.warning(repaired_msg.format(dataSource=dataSource, monumentName=monumentName, localityName=localityName, errorReason=errorReason, operation=operation))
        MyLogger.repaired_counter += 1
    
    def log_excluded(self, dataSource, monumentName, localityName, errorReason):
        self.logger.error(excluded_msg.format(dataSource=dataSource, monumentName=monumentName, localityName=localityName, errorReason=errorReason))
        MyLogger.excluded_counter += 1
    
    def log_succeded(self, monumentName):
        self.logger.info(succeded_msg.format(monumentName=monumentName))
        MyLogger.succeded_counter += 1

    @classmethod
    def get_counts(cls):
        print(f'Repaired: {cls.repaired_counter}')
        print(f'Excluded: {cls.excluded_counter}')
        print(f'Succeded: {cls.succeded_counter}')