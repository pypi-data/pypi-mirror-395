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
class TextEditDialog(object):
    def __init__(self, text: str = '', title: str = ''):
        super().__init__()
        self.dialog = QtWidgets.QDialog()
        self.setupUi()
        self.textEdit.setPlainText(text)
        self.dialog.setWindowTitle(title)
        self.result_value = False

    def setupUi(self):
        self.dialog.setObjectName("Dialog")
        self.dialog.resize(800, 489)
        self.okButton = QtWidgets.QPushButton(self.dialog)
        self.okButton.setObjectName("okButton")
        self.cancelButton = QtWidgets.QPushButton(self.dialog)
        self.cancelButton.setObjectName("cancelButton")
        self.textEdit = QtWidgets.QPlainTextEdit(self.dialog)
        self.textEdit.setObjectName("textEdit")

        self.retranslateUi()
        self.okButton.clicked.connect(self.ok_button)
        self.cancelButton.clicked.connect(self.cancel_button)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

        layout = QtWidgets.QGridLayout(self.dialog)
        layout.addWidget(self.textEdit, 0, 0, 1, 2)
        layout.addWidget(self.okButton, 1, 0, QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.cancelButton, 1, 1, QtCore.Qt.AlignmentFlag.AlignCenter)
        self.dialog.setLayout(layout)
        self.okButton.setFixedSize(113, 32)
        self.cancelButton.setFixedSize(113, 32)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.okButton.setText(_translate("Dialog", "Cool!"))
        self.cancelButton.setText(_translate("Dialog", "No way"))

    def show(self):
        self.dialog.exec()

    def ok_button(self) -> bool:
        self.dialog.close()
        self.result_value = True
        return True

    def cancel_button(self) -> bool:
        self.dialog.close()
        self.result_value = False
        return False

    def result(self) -> bool:
        return self.result_value

    def parameters(self) -> str:
        return self.textEdit.toPlainText()
