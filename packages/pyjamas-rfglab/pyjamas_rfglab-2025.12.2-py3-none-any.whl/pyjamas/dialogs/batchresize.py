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

from typing import Optional

from PyQt6 import QtCore, QtWidgets

from pyjamas.rutils import RUtils


class BatchResizeDialog(object):
    input_folder: str = None
    save_folder: str = None
    recurr: bool = None
    im_size: tuple = None

    def __init__(self):
        super().__init__()

    def setupUi(self, Dialog, parameters: Optional[dict] = None):

        if (parameters is None or parameters is False) and BatchResizeDialog.input_folder is None:
            parameters = {'input_folder': '',
                          'save_folder': '',
                          'recurr': True,
                          'im_size': (512, 512)}

        if parameters is not None and parameters is not False:
            BatchResizeDialog.input_folder = parameters.get('input_folder')
            BatchResizeDialog.save_folder = parameters.get('save_folder')
            BatchResizeDialog.recurr = parameters.get('recurr')
            BatchResizeDialog.im_size = parameters.get('im_size')

        Dialog.setObjectName("Dialog")
        Dialog.resize(450, 180)
        self.buttonsOkCancel = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonsOkCancel.setGeometry(QtCore.QRect(140, 140, 200, 32))
        self.buttonsOkCancel.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonsOkCancel.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonsOkCancel.setObjectName("buttonsOkCancel")

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 15, 131, 16))
        self.label.setObjectName("label")
        
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 50, 131, 16))
        self.label_2.setObjectName("label_2")
       
        self.leInputFolder = QtWidgets.QLineEdit(Dialog)
        self.leInputFolder.setGeometry(QtCore.QRect(110, 15, 271, 21))
        self.leInputFolder.setObjectName("leInputFolder")
        
        self.leSaveFolder = QtWidgets.QLineEdit(Dialog)
        self.leSaveFolder.setGeometry(QtCore.QRect(110, 50, 271, 21))
        self.leSaveFolder.setObjectName("leSaveFolder")
        
        self.pbInputFolder = QtWidgets.QPushButton(Dialog)
        self.pbInputFolder.setGeometry(QtCore.QRect(390, 10, 51, 32))
        self.pbInputFolder.setObjectName("pbInputFolder")
        self.pbInputFolder.clicked.connect(self._open_input_folder_dialog)
        
        self.pbSaveFolder = QtWidgets.QPushButton(Dialog)
        self.pbSaveFolder.setGeometry(QtCore.QRect(390, 45, 51, 32))
        self.pbSaveFolder.setObjectName("pbSaveFolder")
        self.pbSaveFolder.clicked.connect(self._open_save_folder_dialog)
    
        self.cbRecurrFlag = QtWidgets.QCheckBox(Dialog)
        self.cbRecurrFlag.setGeometry(QtCore.QRect(20, 110, 150, 20))
        self.cbRecurrFlag.setObjectName("cbRecurrFlag")

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 80, 190, 20))
        self.label_3.setObjectName("label_3")
        self.leImSize = QtWidgets.QLineEdit(Dialog)
        self.leImSize.setGeometry(QtCore.QRect(210, 80, 71, 21))
        self.leImSize.setObjectName("leImSize")

        self.buttonsOkCancel.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.leInputFolder.raise_()
        self.leSaveFolder.raise_()
        self.pbInputFolder.raise_()
        self.pbSaveFolder.raise_()
        self.cbRecurrFlag.raise_()
        self.leImSize.raise_()

        self.retranslateUi(Dialog)
        self.buttonsOkCancel.accepted.connect(Dialog.accept)
        self.buttonsOkCancel.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Batch Resize"))
        self.label.setText(_translate("Dialog", "input folder"))
        self.leInputFolder.setText(BatchResizeDialog.input_folder)
        self.label_2.setText(_translate("Dialog", "save folder"))
        self.leSaveFolder.setText(BatchResizeDialog.save_folder)
        self.pbInputFolder.setText(_translate("Dialog", "..."))
        self.pbSaveFolder.setText(_translate("Dialog", "..."))
        self.cbRecurrFlag.setText(_translate("Dialog", "search in subfolders"))
        self.cbRecurrFlag.setChecked(BatchResizeDialog.recurr)
        self.label_3.setText(_translate("Dialog", "new image size (height, width)"))
        self.leImSize.setText(str(BatchResizeDialog.im_size))

    def parameters(self) -> dict:
        BatchResizeDialog.input_folder: str = self.leInputFolder.text()
        BatchResizeDialog.save_folder: str = self.leSaveFolder.text()
        BatchResizeDialog.recurr: bool = self.cbRecurrFlag.isChecked()
        try:
            BatchResizeDialog.im_size = eval(self.leImSize.text())
        except:
            print(f"Incorrect input tuple.")
            BatchResizeDialog.im_size = (512, 512)

        return {
            'input_folder': BatchResizeDialog.input_folder,
            'save_folder': BatchResizeDialog.save_folder,
            'recurr': BatchResizeDialog.recurr,
            'im_size': BatchResizeDialog.im_size
        }

    def _open_input_folder_dialog(self) -> bool:
        start_folder = self.leInputFolder.text() if self.leInputFolder.text() != '' else BatchResizeDialog.input_folder
        folder = RUtils.open_folder_dialog(f"Input folder", start_folder)

        if folder == '' or folder is False:
            return False

        self.leInputFolder.setText(folder)

        return True

    def _open_save_folder_dialog(self) -> bool:
        start_folder = self.leSaveFolder.text() if self.leSaveFolder.text() != '' else BatchResizeDialog.save_folder
        folder = RUtils.open_folder_dialog(f"Save folder", start_folder)

        if folder == '' or folder is False:
            return False

        self.leSaveFolder.setText(folder)

        return True

