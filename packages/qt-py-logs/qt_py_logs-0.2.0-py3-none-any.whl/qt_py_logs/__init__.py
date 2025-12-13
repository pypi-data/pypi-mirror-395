"""
qt_py_logs package initializer.

This module re-exports the primary public API of the package so consumers can
import the logging helpers directly from the package root.

Purpose:
- QTlogger: the package's main logger class intended for use in applications.
- SetupLogger: a convenience/helper class to configure logging (handlers, formatters,
    destinations, and Qt-specific integration) before creating or using QTlogger.

Notes:
- The module defines __all__ = ["QTlogger", "SetupLogger"] to make the public API
    explicit for `from qt_py_logs import *`.
- See the implementations of qt_py_logs.logger for full documentation of each class
    and available configuration options.
"""

from .logger import QTlogger, SetupLogger

__all__ = ["QTlogger", "SetupLogger"]
