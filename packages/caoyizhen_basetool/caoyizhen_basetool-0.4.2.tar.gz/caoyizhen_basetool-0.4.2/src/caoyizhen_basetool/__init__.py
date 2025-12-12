"""
The caoyizhen_basetool library provides a tool to help you to dealing with data in Python.
"""

from .file import read_file, save_file, add_suffix_file, return_to_jsonl, filter_data
from .process import BaseMultiThreading
from .utils import singleton, LoggerManager, base_logger