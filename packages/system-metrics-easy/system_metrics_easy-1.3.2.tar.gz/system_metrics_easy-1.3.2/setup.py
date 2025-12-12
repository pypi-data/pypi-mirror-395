#!/usr/bin/env python3
"""
Setup script for Server Metrics Monitor
"""

from setuptools import setup, find_packages
import os


# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "Server Metrics Monitor - A comprehensive server monitoring tool"


# Dependencies are now defined in pyproject.toml
def get_requirements():
    return [
        "bidict==0.23.1",
        "certifi==2025.8.3",
        "charset-normalizer==3.4.3",
        "python-dotenv==1.1.1",
        "h11==0.16.0",
        "idna==3.10",
        "psutil==7.1.0",
        "python-engineio==4.12.2",
        "python-socketio==5.13.0",
        "requests==2.32.5",
        "simple-websocket==1.1.0",
        "urllib3==2.5.0",
        "websocket-client>=1.0.0",  # For WebSocket transport support
        "wsproto==1.2.0",
    ]


setup(
    name="system-metrics-easy",
    version="1.3.2",
    author="Moonsys",
    author_email="admin@moonsys.co",
    description="A comprehensive server monitoring tool that collects and sends system metrics to a Socket.IO server",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/hamzaig/system-metrics-easy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=get_requirements(),
    entry_points={
        "console_scripts": [
            "system-metrics-easy=system_metrics_easy.server_metrics:main",  # Use the main script directly
        ],
    },
    keywords="server monitoring metrics system stats cpu memory disk network gpu socketio",
    project_urls={
        "Bug Reports": "https://github.com/hamzaig/system-metrics-easy/issues",
        "Source": "https://github.com/hamzaig/system-metrics-easy",
        "Documentation": "https://github.com/hamzaig/system-metrics-easy#readme",
    },
    include_package_data=True,
    zip_safe=False,
)
