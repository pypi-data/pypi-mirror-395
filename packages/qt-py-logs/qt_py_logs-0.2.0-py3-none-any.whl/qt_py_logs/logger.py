"""
QTlogger: A singleton MQTT logger for publishing log messages. 
Allows configuration of MQTT broker, topic, and source identifier.
Supports logging messages with severity levels and additional context.

Meant to be used with QTlogs https://github.com/ausward/QTLogs
"""

import inspect
import json
import os
import time # Added import for time module
import threading
from typing import overload
import yaml
from paho.mqtt import publish
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class QTlogger:
    """ Singleton MQTT Logger for publishing log messages 
    to the specified MQTT broker and topic.
    """
    _instance = None
    topic: str
    broker: str
    port: int
    source: str
    _config_path: str = None
    _observer: Observer = None

    def __new__(cls, *args, **kwargs):
        """ Implement singleton pattern for QTlogger. """
        if cls._instance is None:
            cls._instance = super(QTlogger, cls).__new__(cls)
        return cls._instance

    def __init__(self, topic: str = None, broker: str = None, port: int = None, source: str = None, config_path: str = None):
        """
        Initialize or update the QTlogger's configuration.

        If configuration values are provided, the logger instance is updated.
        If no arguments are given, the existing configuration is maintained.

        Args:
            topic (str): MQTT topic to publish logs to.
            broker (str): MQTT broker address.
            port (int): MQTT broker port.
            source (str): Source identifier for the logger.
            config_path (str): Path to a YAML configuration file.
        """
        if self._observer:
            self._observer.stop()
            self._observer.join()

        if config_path:
            self._config_path = os.path.abspath(config_path)
            self._load_config()
            self._start_watcher()
        elif topic is not None:
            self.topic = topic
            self.broker = broker
            self.port = port
            self.source = source

    def _load_config(self):
        with open(self._config_path, 'r') as f:
            config = yaml.safe_load(f)
        self.topic = config['topic']
        self.broker = config['broker']
        self.port = config['port']
        self.source = config['source']

    def _start_watcher(self):
        event_handler = ConfigChangeHandler(self)
        self._observer = Observer()
        self._observer.schedule(event_handler, os.path.dirname(self._config_path), recursive=False)
        self._observer.daemon = True
        self._observer.start()

    def _log(self, message: str):
        """ Internal method to publish log messages to the MQTT broker."""
        # Check if logger is configured before attempting to publish
        if not all(hasattr(self, attr) for attr in ['topic', 'broker', 'port']):
            print("Error: Logger not configured. Please call SetupLogger first.")
            return
        publish.single(self.topic, payload=message, hostname=self.broker, port=self.port)

    def __print__(self):
        """ Print the current configuration of the logger. """
        if not all(hasattr(self, attr)
                for attr in ['topic', 'broker', 'port', 'source']):
            return "MQTT Logger is not configured."
        return f"MQTT Logger Configuration:\n\
        Topic: {self.topic}\n Broker: {self.broker}\n\
        Port: {self.port}\n Source: {self.source}"

    def log(self, level: str, message: str, extra_data: dict = None):
        """ Log a message with a given severity level.
        Args:
            level (str): Severity level of the log (e.g., 'INFO', 'ERROR').
            message (str): The log message.
            extra_data (dict, optional): Additional contextual information to include in the log.
        """
        caller_frame = inspect.stack()
        caller_function = str(caller_frame[1].frame)
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        if extra_data:
            json_message = {
                "from": self.source,
                "payload": message,
                "level": level,
                "timestamp": current_time,
                "caller": caller_function,
                "extra": json.dumps(extra_data)
            }
        else:
            json_message = {
                "from": self.source,
                "payload": message,
                "level": level,
                "timestamp": current_time,
                "caller": caller_function
            }
        threading.Thread(target=self._log, args=(json.dumps(json_message),)).start()


class ConfigChangeHandler(FileSystemEventHandler):
    def __init__(self, logger: QTlogger):
        self._logger = logger

    def on_modified(self, event):
        if not event.is_directory and os.path.abspath(event.src_path) == self._logger._config_path:
            self._logger._load_config()


@overload
def SetupLogger(topic:str, broker:str, port:int, source:str) -> QTlogger:
    ...

@overload
def SetupLogger(config_path: str) -> QTlogger:
    ...

def SetupLogger(topic:str = None, broker:str = None, port:int = None, source:str = None, config_path: str = None) -> QTlogger:
    """
    Configure and retrieve the QTlogger singleton instance.

    This function can be called multiple times to re-configure the logger.
    It can be called with either the topic, broker, port, and source, or with a path to a YAML configuration file.

    Args:
        topic (str): MQTT topic to publish logs to.
        broker (str): MQTT broker address.
        port (int): MQTT broker port.
        source (str): Source identifier for the logger.
        config_path (str): Path to a YAML configuration file.

    Returns:
        QTlogger: The configured singleton logger instance.
    """
    if config_path:
        logger = QTlogger(config_path=config_path)
    else:
        logger = QTlogger(topic, broker, port, source)
    return logger
