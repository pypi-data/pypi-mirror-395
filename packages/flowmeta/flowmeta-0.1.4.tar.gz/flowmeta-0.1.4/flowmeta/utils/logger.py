"""Logging utilities for flowmeta"""

import sys
from datetime import datetime


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def print_colorful_message(message, color):
    """
    Print a colorful message to the console.
    
    Args:
        message (str): The message to be printed.
        color (str): The color code to be applied.
                     Choices are 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'.
    """
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
    }
    end_color = '\033[0m'
    if color not in colors:
        print("Invalid color. Please choose from 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white'.")
        return
    colored_message = f"{colors[color]}{message}{end_color}"
    print(colored_message)


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def log_info(message):
    """Print info message with timestamp"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] [INFO] {message}")


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def log_warning(message):
    """Print warning message in yellow"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print_colorful_message(f"[{timestamp}] [WARNING] {message}", "yellow")


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def log_error(message):
    """Print error message in red"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print_colorful_message(f"[{timestamp}] [ERROR] {message}", "red")


# FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline
# Author: Dongqiang Zeng
# Email: interlaken@smu.edu.cn
# Affiliation: Southern Medical University
# Last Modified: 2025-11-15
def log_success(message):
    """Print success message in green"""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print_colorful_message(f"[{timestamp}] [SUCCESS] {message}", "green")
