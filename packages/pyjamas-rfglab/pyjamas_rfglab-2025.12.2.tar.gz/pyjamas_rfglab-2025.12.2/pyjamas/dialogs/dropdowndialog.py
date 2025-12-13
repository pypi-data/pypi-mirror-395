"""
    PyJAMAS is Just A More Awesome Siesta
    Copyright (C) 2018  Rodrigo Fernandez-Gonzalez (rodrigo.fernandez.gonzalez@utoronto.ca)

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from PyQt6 import QtCore, QtWidgets


class DropDownDialog(object):
    text = ''
    index = None
    accepted = False

    def __init__(self, items: list = [], title: str = ''):
        super().__init__()
        self.dialog = QtWidgets.QDialog()
        self.setupUi(self.dialog)
        self.comboBox.addItems(items)
        self.dialog.setWindowTitle(title)

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(200, 100)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 50, 160, 30))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(
            QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.setGeometry(QtCore.QRect(10, 10, 180, 30))

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.ok_button)
        self.buttonBox.rejected.connect(self.cancel_button)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate

    def show(self):
        self.dialog.exec()

    def ok_button(self) -> bool:
        self.dialog.close()
        self.accepted = True
        return True

    def cancel_button(self) -> bool:
        self.dialog.close()
        self.accepted = False
        return False

    def result(self) -> bool:
        return self.accepted

    def parameters(self) -> str:
        self.text = self.comboBox.currentText()
        self.index = self.comboBox.currentIndex()

        return {'text': self.text,
                'index': self.index}
