from pyjamas.rplugins.base import PJSPluginABC

# Useful imports if the plugin requires a sub-menu with multiple options.
from PyQt6 import QtWidgets, QtCore
from functools import partial


class PJSPlugin(PJSPluginABC):
    def name(self) -> str:
        return "Sample plugin package"

    def run(self, parameters: dict) -> bool:
        print(parameters['text'])
        self.pjs.statusbar.showMessage(parameters['text'])

        return True

    def build_menu(self):
        parent_menu = QtWidgets.QMenu(self.pjs.menuPlugins)
        parent_menu.setObjectName(self.name())
        parent_menu.setTitle(QtCore.QCoreApplication.translate('PyJAMAS', self.name()))

        self.pjs.addMenuItem(parent_menu, "Print 'Hello my friends!'", partial(self.run, {'text': "Hello my friends!"}))
        self.pjs.addMenuItem(parent_menu, "Print 'Howdy y'all!'", partial(self.run, {'text': "Howdy y'all!"}))

        self.menu = self.pjs.menuPlugins.addMenu(parent_menu)
