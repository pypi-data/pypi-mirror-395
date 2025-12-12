from __future__ import annotations

from orangewidget import settings


class CallbackSettingsHandler(settings.SettingsHandler):
    """
    Settings handler used to call some callback before packing data (so before)
    saving orange :class:`Setting`
    """

    def __init__(self):
        super(CallbackSettingsHandler, self).__init__()
        self.__callbacks = []

    def addCallback(self, _callback):
        self.__callbacks.append(_callback)

    def removeCallback(self, callback):
        self.__callbacks.remove(callback)

    def pack_data(self, widget):
        """"""
        for callback in self.__callbacks:
            callback()
        return super(CallbackSettingsHandler, self).pack_data(widget)
