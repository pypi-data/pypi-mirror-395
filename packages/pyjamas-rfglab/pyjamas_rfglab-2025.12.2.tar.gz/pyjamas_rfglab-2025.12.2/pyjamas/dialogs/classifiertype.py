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

from typing import Tuple

from PyQt6 import QtCore, QtWidgets
from pyjamas.rimage.rimml.classifier_types import classifier_types


class ClassifierTypeDialog(object):
    # These are class variables so that, when their values change, they change, and next time the same dialog is
    # open, the most recent values are preserved.
    classifier_type = classifier_types.UNKNOWN.value

    def __init__(self):
        super().__init__()

    def setupUi(self, Dialog, classifier_type: str = classifier_types.UNKNOWN.value):

        classifier_identities = set(thetype.value for thetype in classifier_types)
        if classifier_type not in classifier_identities:
            self.classifier_type = classifier_types.UNKNOWN.value
        else:
            self.classifier_type = classifier_type

        Dialog.setObjectName("Dialog")
        Dialog.resize(210, 100)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Ignored, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-160, 60, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(20, 20, 170, 30))
        self.comboBox.addItems(classifier_identities)
        self.comboBox.setCurrentText(self.classifier_type)
        self.comboBox.setObjectName("combobox")

        self.retranslateUi(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.buttonBox.accepted.connect(Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Select classifier type"))

    def parameters(self) -> Tuple[int, int]:
        ClassifierTypeDialog.classifier_type = self.comboBox.currentText()

        return ClassifierTypeDialog.classifier_type
