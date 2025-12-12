from functools import partial
from typing import Optional
from PyQt6 import QtCore, QtWidgets, QtGui
from functools import partial
import time


class ConfigureKeyBindingsDialog(QtWidgets.QWidget):
    key_configs: dict = None
    searching: bool = False
    bttn: QtWidgets.QPushButton = None
    menu: str = None
    option: str = None
    dialog: QtWidgets.QDialog = None

    def __init__(self):
        super().__init__()

    def setupUi(self, Dialog: QtWidgets.QDialog, key_configs: dict):
        self.key_configs = key_configs
        self.dialog = Dialog

        self.gScene = QtWidgets.QGraphicsScene(self.dialog)
        self.gScene.setSceneRect(0, 0, 1183, 761)
        self.gScene.setObjectName('gScene')

        self.gView = QtWidgets.QGraphicsView(self.gScene)
        self.gView.setObjectName('gView')
        self.gView.installEventFilter(self)

        self.dialog.setObjectName("Dialog")
        self.dialog.resize(600, 500)
        self.buttonsOkCancel = QtWidgets.QDialogButtonBox(self.dialog)
        self.buttonsOkCancel.setGeometry(QtCore.QRect(0, 460, 560, 32))
        self.buttonsOkCancel.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonsOkCancel.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonsOkCancel.setObjectName("buttonsOkCancel")

        self.TabBox = QtWidgets.QTabWidget(self.dialog)
        self.TabBox.setGeometry(QtCore.QRect(20, 20, 560, 430))
        self.TabBox.setObjectName("tab_box")

        self.menu_groupboxes = {}
        self.menu_scrollareas = {}
        self.option_labels = {}
        self.option_pbs = {}

        for this_menu in self.key_configs.keys():
            menu_configs = self.key_configs[this_menu]
            self.menu_groupboxes[this_menu] = QtWidgets.QGroupBox()
            self.menu_groupboxes[this_menu].setGeometry(QtCore.QRect(0, 0, 560, 430))
            self.menu_groupboxes[this_menu].setObjectName(f"menu_groupbox_{this_menu}")

            column_form = QtWidgets.QFormLayout()
            column_form.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignLeft)
            column_form.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
            column_form.setObjectName(f"{this_menu}_columns")

            self.option_labels[this_menu] = {}
            self.option_pbs[this_menu] = {}
            for menu_option in menu_configs.keys():
                self.option_labels[this_menu][menu_option] = QtWidgets.QLabel(menu_option)
                self.option_pbs[this_menu][menu_option] = QtWidgets.QPushButton()
                self.option_pbs[this_menu][menu_option].setFixedSize(QtCore.QSize(100, 30))
                self.option_pbs[this_menu][menu_option].clicked.connect(
                    partial(self.button_clicked, self.option_pbs[this_menu][menu_option], this_menu, menu_option))
                column_form.addRow(self.option_pbs[this_menu][menu_option],
                                   self.option_labels[this_menu][menu_option])

            self.menu_groupboxes[this_menu].setLayout(column_form)
            self.menu_scrollareas[this_menu] = QtWidgets.QScrollArea()
            self.menu_scrollareas[this_menu].setWidget(self.menu_groupboxes[this_menu])
            self.menu_scrollareas[this_menu].setWidgetResizable(True)
            self.menu_scrollareas[this_menu].setFixedHeight(400)

            self.TabBox.addTab(self.menu_scrollareas[this_menu], this_menu)

        self.retranslateUi()
        self.buttonsOkCancel.accepted.connect(self.dialog.accept)
        self.buttonsOkCancel.rejected.connect(self.dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.dialog.setWindowTitle(_translate("Dialog", "Configure key bindings"))

        for this_menu in self.key_configs.keys():
            for menu_option, option_shortcut in zip(self.key_configs[this_menu].keys(),
                                                    self.key_configs[this_menu].values()):
                self.option_labels[this_menu][menu_option].setText(_translate("Dialog", menu_option))
                self.option_pbs[this_menu][menu_option].setText(_translate("Dialog", option_shortcut))

    def parameters(self) -> dict:
        for this_menu in self.key_configs.keys():
            for menu_option in self.key_configs[this_menu].keys():
                self.key_configs[this_menu][menu_option] = self.option_pbs[this_menu][menu_option].text()

        ConfigureKeyBindingsDialog.key_configs: dict = self.key_configs
        return ConfigureKeyBindingsDialog.key_configs

    def button_clicked(self, bttn: QtWidgets.QPushButton, menu: str, option: str):
        _translate = QtCore.QCoreApplication.translate
        bttn.setText(_translate('Dialog', '...'))
        self.gView.grabKeyboard()
        self.bttn = bttn
        self.menu = menu
        self.option = option
        self.searching = True

    def eventFilter(self, source, event: QtCore.QEvent):
        modifier_keys = [QtCore.Qt.Key.Key_Shift, QtCore.Qt.Key.Key_Alt,
                         QtCore.Qt.Key.Key_Control, QtCore.Qt.Key.Key_Meta]
        if type(source) == QtWidgets.QGraphicsView and self.searching:
            if event.type() == QtCore.QEvent.Type.KeyPress:
                if event.key() not in modifier_keys:
                    if event.key() == QtCore.Qt.Key.Key_Escape:
                        self.finish_search("")
                    else:
                        self.finish_search(QtGui.QKeySequence(event.keyCombination()).toString())
                        return True
        return False

    def finish_search(self, key_string: str):
        self.searching = False
        if self.bttn is not None:
            if key_string != "":  # If not empty string, replace matching shortcuts with empty strings
                for this_menu in self.key_configs.keys():
                    for this_option in self.key_configs[this_menu].keys():
                        if self.key_configs[this_menu][this_option] == key_string:
                            self.key_configs[this_menu][this_option] = ""
            self.key_configs[self.menu][self.option] = key_string
        self.retranslateUi()
