import os
import uuid
from datetime import datetime
from enum import Enum
from fluent import sender, event

class FluentConf:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    
class LogLevel(Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    ERROR = 'ERROR'

class Logger:
    def __init__(self, application_name, trace_id, file):
        self.file = file
        self.application_name = application_name
        self.trace_id = trace_id
        self.fluent = None

    def init_fluent(self, level: LogLevel, fluent: FluentConf):
        if not fluent:
            raise Exception('Конфиг пустой')
            return
        
        sender.fluent = fluent
        sender.setup(level, host=fluent.host, port=fluent.port)


    def debug(self, message):
        self.__log(LogLevel.DEBUG, message)

    def log(self, message):
        self.__log(LogLevel.INFO, message)

    def error(self, message, b_raise=True):
        self.__log(LogLevel.ERROR, message, b_raise)

    def __log(self, level: LogLevel, message, b_raise=False):
        """
        Parameters
        ----------
        level: LogLevel 
            уровень DEBUG INFO ERROR
        message : str
            входная строка

        Raises
        -------
        Exception
            Исключение при записи в лог-файл
        """
        datetime_string = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f'{level.name} {datetime_string}: {message}'
        print(message)

        file = self.file
        try:
            # Создаем директорию, если она не существует
            dir = os.path.dirname(file)
            if dir:  # Если путь содержит директорию
                os.makedirs(dir, exist_ok=True)

            with open(file, 'a', encoding='utf-8') as f:
                f.write(message + '\n')
        except Exception as e:
            print(f'Ошибка записи в лог-файл {file}: {e}')

        if self.fluent:
            event.Event(level.name, {
                # "id": f"etl.{self.application_name}.{uuid.uuid4()}",
                "@timestamp": datetime_string,
                "level":  level.name,
                "userId": "",
                "traceId": self.trace_id,
                "host": "",
                "requestMethod": "",
                "requestStatusCode": "",
                "controller": "",
                "function": "",
                "requestUrl": "",
                "requestBody": "",
                "threadId": "",
                "logger": 'ETL',
                "message": message,
                "exception": "",
                "srcIp0v4": 127,
                "srcIp1v4": 0,
                "srcIp2v4": 0,
                "srcIp3v4": 1,
                "dstHost": "",
                "userExtId": "",
                "other": ""
            })

        if b_raise:
            raise Exception(message)
        

    