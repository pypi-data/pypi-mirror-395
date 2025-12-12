# coding: utf-8

"""
This module is used to manage observations. Initially on files.
Observations are runned on a thread and run each n seconds.
They are manage by thread and signals
"""

from time import time


class Timer:
    def __init__(self, title):
        self.title = title

    def __enter__(self):
        self._start_time = time()

    def __exit__(self, type, value, traceback):
        exec_time = time() - self._start_time
        print(f"{self.title} exec time: {exec_time} s")
