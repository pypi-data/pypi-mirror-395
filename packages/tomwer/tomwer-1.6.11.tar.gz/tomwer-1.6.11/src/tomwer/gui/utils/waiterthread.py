# coding: utf-8

"""
This module is used to manage observations. Initially on files.
Observations are runned on a thread and run each n seconds.
They are manage by thread and signals
"""


import time

from silx.gui import qt


class QWaiterThread(qt.QThread):
    """simple thread wich wait for waitingTime to be finished"""

    def __init__(self, waitingTime):
        qt.QThread.__init__(self)
        self.waitingTime = waitingTime

    def run(self):
        time.sleep(self.waitingTime)
