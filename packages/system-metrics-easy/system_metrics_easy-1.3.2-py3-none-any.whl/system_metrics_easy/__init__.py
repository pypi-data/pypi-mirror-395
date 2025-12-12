"""
Server Metrics Monitor
A comprehensive server monitoring tool that collects and sends system metrics to a Socket.IO server.
"""

__version__ = "1.3.1"
__author__ = "Moonsys"
__email__ = "admin@moonsys.co"

from .server_metrics import ServerMetrics, main

__all__ = ["ServerMetrics", "main"]
