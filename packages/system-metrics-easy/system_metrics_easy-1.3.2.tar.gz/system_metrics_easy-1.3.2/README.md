# System Metrics Easy

[![PyPI version](https://badge.fury.io/py/system-metrics-easy.svg)](https://badge.fury.io/py/system-metrics-easy)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A professional server monitoring solution that collects comprehensive system metrics and transmits them in real-time to your monitoring infrastructure. Built for production environments with enterprise-grade reliability and cross-platform support.

## 🚀 Quick Start

### Installation

```bash
pip install system-metrics-easy
```

### Basic Usage

```bash
# Start monitoring (interactive setup)
system-metrics-easy

# Check status
system-metrics-easy --status

# Stop monitoring
system-metrics-easy --stop
```

## 📊 Metrics Collected

### System Information

- **Hostname & OS**: System identification and platform details
- **Architecture**: CPU architecture and system specifications
- **Uptime**: System boot time and uptime statistics
- **Python Environment**: Runtime version and monitor version

### CPU Performance

- **Total CPU Usage**: Overall system CPU utilization percentage
- **Per-Core Usage**: Individual CPU core utilization
- **Load Average**: 1-minute, 5-minute, and 15-minute load averages
- **Core Count**: Number of available CPU cores

### Memory Management

- **RAM Usage**: Total, used, free, and available memory
- **Memory Percentage**: Current memory utilization
- **Swap Statistics**: Swap memory usage and percentage

### Storage Monitoring

- **Disk Usage**: All mounted filesystems and partitions
- **Space Utilization**: Total, used, and free disk space
- **Usage Percentages**: Per-partition utilization rates

### Network Activity

- **Throughput**: Real-time network traffic per second
- **Interface Statistics**: Per-network-interface metrics
- **Total Traffic**: Cumulative bytes sent and received

### GPU Performance

- **NVIDIA GPUs**: Utilization, memory usage, temperature
- **Apple Silicon**: GPU information and memory details
- **AMD GPUs**: ROCm-based performance metrics
- **Intel GPUs**: Basic GPU detection and statistics

## 🔧 Configuration Options

### Interactive Setup

When you run `system-metrics-easy` without parameters, it will guide you through:

1. **Collection Interval**: How often to collect metrics (default: 10 seconds)
2. **Server Identification**: Unique name for this server
3. **Automatic Background Start**: Option to run as background service

### Environment Variables

Configure automatically using environment variables:

```bash
export TIME_INTERVAL=10                    # Collection interval in seconds
export SERVER_ID=production-server-01      # Unique server identifier
```

### Command Line Options

```bash
# Interactive setup and start
system-metrics-easy

# Check if monitoring is running
system-metrics-easy --status

# Stop background monitoring
system-metrics-easy --stop

# View recent logs
tail -f system-metrics-easy.log
```

## 📡 Real-Time Data Transmission

The monitor emits comprehensive metrics data in real-time with the following structure:

### Event: `server-stats`

```json
{
  "timestamp": 1640995200.0,
  "formatted_time": "2022-01-01 12:00:00",
  "server_id": "production-server-01",
  "system_info": {
    "hostname": "server-01",
    "os": "Linux 5.4.0",
    "architecture": "x86_64",
    "python_version": "3.9.7",
    "monitor_version": "1.3.1",
    "uptime_seconds": 86400.5,
    "boot_time": "2022-01-01 00:00:00"
  },
  "cpu": {
    "total": 45.2,
    "per_core": [42.1, 48.3, 44.8, 46.0],
    "core_count": 4,
    "load_average": {
      "1min": 1.2,
      "5min": 1.1,
      "15min": 1.0
    }
  },
  "memory": {
    "total_gb": 16.0,
    "used_gb": 8.5,
    "free_gb": 7.5,
    "available_gb": 7.2,
    "used_percent": 53.1,
    "swap_total_gb": 2.0,
    "swap_used_gb": 0.1,
    "swap_percent": 5.0
  },
  "disk": [
    {
      "device": "/dev/sda1",
      "mountpoint": "/",
      "fstype": "ext4",
      "total_gb": 500.0,
      "used_gb": 250.0,
      "free_gb": 250.0,
      "used_percent": 50.0
    }
  ],
  "network": [
    {
      "interface": "eth0",
      "bytes_sent_per_sec": 1024000,
      "bytes_recv_per_sec": 2048000,
      "mb_sent_per_sec": 0.98,
      "mb_recv_per_sec": 1.95,
      "total_sent_gb": 1024.5,
      "total_recv_gb": 2048.7
    }
  ],
  "gpu": [
    {
      "gpu_id": "0",
      "name": "NVIDIA GeForce RTX 3080",
      "type": "NVIDIA",
      "utilization_percent": 75.0,
      "memory_used_mb": 4096,
      "memory_total_mb": 10240,
      "temperature_c": 65,
      "memory_used_gb": 4.0,
      "memory_total_gb": 10.0,
      "memory_usage_percent": 40.0
    }
  ],
  "cuda_processes": {
    "message": "No active CUDA processes"
  }
}
```

## 🛠️ System Requirements

### Minimum Requirements

- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows
- **Memory**: 50MB RAM
- **Disk Space**: 10MB

### Dependencies

- **psutil**: System metrics collection
- **python-socketio**: Real-time communication
- **python-dotenv**: Configuration management

### Optional GPU Support

- **NVIDIA**: nvidia-smi (included with NVIDIA drivers)
- **AMD**: ROCm tools (rocm-smi or amd-smi) with comprehensive metrics
- **Apple Silicon**: Native macOS support
- **Intel**: Multi-method detection (intel_gpu_top, sysfs, lspci)

## 🔄 Background Service Management

### Automatic Background Operation

The monitor automatically handles background operation:

```bash
# Start as background service
system-metrics-easy

# The service will:
# - Start in background automatically
# - Create PID file for management
# - Log all activity to system-metrics-easy.log
# - Handle process lifecycle
```

### Service Management Commands

```bash
# Check service status
system-metrics-easy --status

# Stop service
system-metrics-easy --stop

# View service logs
tail -f system-metrics-easy.log

# Check service PID
cat system-metrics-easy.pid
```

## 🔒 Production Features

### Reliability & Error Handling

- **Automatic Reconnection**: Smart reconnection with exponential backoff
- **Failure Detection**: Automatic exit after consecutive failures
- **Graceful Shutdown**: Clean process termination with signal handling
- **Resource Management**: Memory and CPU usage optimization

### Security & Performance

- **Input Validation**: Comprehensive data sanitization
- **Resource Limits**: CPU and memory usage caps
- **Safe Execution**: Protected subprocess execution with timeouts
- **Error Recovery**: Graceful degradation on system errors

### Monitoring & Logging

- **Comprehensive Logging**: Detailed activity and error logs
- **Status Monitoring**: Real-time service health checks
- **Performance Tracking**: Monitor version and system information
- **Debug Information**: Detailed error messages and troubleshooting

## 📋 Platform Support

| Platform    | CPU     | Memory  | Disk    | Network | GPU              |
| ----------- | ------- | ------- | ------- | ------- | ---------------- |
| **Linux**   | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ All Types     |
| **macOS**   | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ Apple Silicon |
| **Windows** | ✅ Full | ✅ Full | ✅ Full | ✅ Full | ✅ NVIDIA/Intel  |

## 🚀 Advanced Usage

### Custom Configuration

```bash
# Set custom collection interval
export TIME_INTERVAL=5

# Set custom server identifier
export SERVER_ID=web-server-01

# Start with custom settings
system-metrics-easy
```

### Integration Examples

```python
# Python integration example
import socketio

sio = socketio.Client()

@sio.event
def server_stats(data):
    print(f"Server {data['server_id']} CPU: {data['cpu']['total']}%")
    print(f"Memory usage: {data['memory']['used_percent']}%")

sio.connect('https://your-monitoring-server.com')
```

## 📈 Performance Characteristics

- **Collection Overhead**: < 1% CPU usage
- **Memory Footprint**: ~50MB RAM
- **Network Bandwidth**: ~1KB per transmission
- **Transmission Frequency**: Configurable (default: 10 seconds)
- **Data Retention**: Real-time streaming (no local storage)

## 🔧 Troubleshooting

### Common Issues

**Service won't start:**

```bash
# Check logs
cat system-metrics-easy.log

# Verify Python installation
python --version

# Check dependencies
pip list | grep system-metrics-easy
```

**No metrics data:**

```bash
# Check service status
system-metrics-easy --status

# Restart service
system-metrics-easy --stop
system-metrics-easy
```

**Connection issues:**

```bash
# Check network connectivity
ping your-monitoring-server.com

# Verify server configuration
system-metrics-easy --status
```

## 📚 API Reference

### Socket.IO Events

| Event          | Direction       | Description            |
| -------------- | --------------- | ---------------------- |
| `server-stats` | Client → Server | System metrics data    |
| `connect`      | Bidirectional   | Connection established |
| `disconnect`   | Bidirectional   | Connection lost        |

### Data Schema

All metrics follow a consistent JSON schema with:

- **Timestamp**: Unix timestamp and formatted time
- **Server ID**: Unique server identifier
- **System Info**: Basic system information
- **Performance Metrics**: CPU, memory, disk, network, GPU data

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Support

- **Documentation**: [GitHub Wiki](https://github.com/hamzaig/system-metrics-easy/wiki)
- **Issues**: [GitHub Issues](https://github.com/hamzaig/system-metrics-easy/issues)
- **Discussions**: [GitHub Discussions](https://github.com/hamzaig/system-metrics-easy/discussions)

## 📝 Changelog

### Version 1.3.1 (Latest)

- **FIXED**: NVIDIA H200 GPU detection issue - improved CSV parsing to handle GPU names with commas
- **IMPROVED**: Added JSON format support for nvidia-smi (more reliable parsing)
- **IMPROVED**: Enhanced CSV parsing using Python's csv module (handles quoted fields properly)
- **FIXED**: Better compatibility with all NVIDIA GPU models including H200

### Version 1.3.0

- **NEW**: Enhanced AMD GPU support with rocm-smi and amd-smi compatibility
- **NEW**: Comprehensive Intel GPU detection (intel_gpu_top, sysfs, lspci)
- **IMPROVED**: Flexible JSON parsing for different GPU tool versions
- **IMPROVED**: Better fallback mechanisms for GPU detection
- **FIXED**: Improved error handling for missing GPU tools
- **ADDED**: Support for multiple AMD GPU detection methods

### Version 1.2.0

- **NEW**: Hardcoded backend URL for simplified deployment
- **FIXED**: CPU monitoring accuracy improvements
- **IMPROVED**: Enhanced error handling and reliability
- **ADDED**: Monitor version tracking in system information

### Version 1.1.2

- **IMPROVED**: WebSocket transport support
- **ENHANCED**: Better real-time communication performance

### Version 1.1.1

- **FIXED**: Windows compatibility improvements
- **IMPROVED**: Cross-platform console output

### Version 1.1.0

- **NEW**: Direct execution mode
- **NEW**: Smart reconnection with failure tracking
- **IMPROVED**: Enhanced reliability and error handling

---

**System Metrics Easy** - Professional server monitoring made simple.

_Built with ❤️ by [Moonsys](https://github.com/hamzaig)_
