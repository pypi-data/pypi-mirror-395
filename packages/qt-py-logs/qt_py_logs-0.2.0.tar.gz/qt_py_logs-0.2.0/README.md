# QT Py Logs

A Python client for publishing log messages to an MQTT broker, designed to work with the [QTLogs project](https://github.com/ausward/QTLogs). This package provides a simple, singleton logger that can be used across a Python application to send structured log messages to a specified MQTT topic.

## Installation

Install the package using poetry:

```bash
poetry add qt-py-logs
```

Or using pip:

```bash
pip install qt-py-logs
```

## Usage

The `SetupLogger` function allows you to configure the logger. You can either pass in all the configuration details directly as arguments or provide a path to a YAML configuration file.

### Option 1: Configuring with Python arguments

Set up the logger with your MQTT broker details by passing the `topic`, `broker`, `port`, and `source` directly:

```python
from qt_py_logs import SetupLogger

logger = SetupLogger(
    topic="your/mqtt/topic",
    broker="your_mqtt_broker.com",
    port=1883,
    source="your_application_name"
)
```

### Option 2: Configuring with a YAML file

Alternatively, you can configure the logger using a YAML file. Create a `config.yaml` file (or any other name) with the following structure:

```yaml
topic: "your/mqtt/topic"
broker: "your_mqtt_broker.com"
port: 1883
source: "your_application_name"
```

Then, set up the logger by providing the path to your YAML configuration file using the `config_path` argument:

```python
from qt_py_logs import SetupLogger

logger = SetupLogger(config_path="path/to/your/config.yaml")
```

The logger will automatically watch for changes in the YAML file and reload the configuration in real-time, so you don't need to restart your application.

Once the logger is set up using either method, you can use the logger instance to log messages from anywhere in your application:

```python
from qt_py_logs import QTlogger

# Get the logger instance
logger = QTlogger()

# Log a message
logger.log("INFO", "This is an informational message.")
logger.log("ERROR", "This is an error message.")

# If you want to add additional fields to the log message
extra_data = {"user_id": 1234, "operation": "data_processing"}
logger.log("DEBUG", "This is a debug message with extra data.", Extra=extra_data)
```

The log messages will be published to the specified MQTT topic in a JSON format:

```json
{
    "from": "your_application_name",
    "payload": "This is an informational message.",
    "level": "INFO",
    "timestamp": "2025-11-24 10:00:00",
    "caller": "your_function_name"
}
```

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License. See the [LICENSE](LICENSE) file for details.
