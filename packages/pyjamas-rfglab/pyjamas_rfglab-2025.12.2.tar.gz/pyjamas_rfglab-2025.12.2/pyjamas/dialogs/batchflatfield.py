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

import os
from typing import List, Optional, Tuple

from PyQt6 import QtCore, QtWidgets

from pyjamas.rutils import RUtils


class BatchFlatFieldCorrectionDialog(object):
    BG_MODES: List[str] = ['none', 'mode']
    MAX_DIM: int = 1200

    input_folder: str = None
    darkfield_file: str = None
    flatfield_file: str = None
    crop_dims: Tuple[int, int] = (MAX_DIM//2, MAX_DIM//2)
    input_substr: str = ''
    file_suffix: str = None
    bg_mode: str = BG_MODES[-1]

    def setupUi(self, Dialog, parameters: Optional[dict] = None):
        from pyjamas.rcallbacks.rcbbatchprocess import RCBBatchProcess

        if (parameters is None or parameters is False) and BatchFlatFieldCorrectionDialog.input_folder is None:
            parameters = RCBBatchProcess._default_batchflatfield_parameters()

        if parameters is not None and parameters is not False:
            BatchFlatFieldCorrectionDialog.input_folder = parameters.get('input_folder')
            BatchFlatFieldCorrectionDialog.darkfield_file = parameters.get('darkfield_file')
            BatchFlatFieldCorrectionDialog.flatfield_file = parameters.get('flatfield_file')
            BatchFlatFieldCorrectionDialog.crop_dims = parameters.get('crop_dims')
            BatchFlatFieldCorrectionDialog.bg_mode = parameters.get('bg_mode')
            BatchFlatFieldCorrectionDialog.input_substr = parameters.get('input_substr')
            BatchFlatFieldCorrectionDialog.file_suffix = parameters.get('file_suffix')

        Dialog.setObjectName("Dialog")
        Dialog.resize(609, 303)
        self.ok_buttonbox = QtWidgets.QDialogButtonBox(parent=Dialog)
        self.ok_buttonbox.setGeometry(QtCore.QRect(230, 250, 341, 32))
        self.ok_buttonbox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.ok_buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.ok_buttonbox.setObjectName("ok_buttonbox")
        self.input_lineedit = QtWidgets.QLineEdit(parent=Dialog)
        self.input_lineedit.setGeometry(QtCore.QRect(160, 30, 341, 21))
        self.input_lineedit.setObjectName("input_lineedit")
        self.input_button = QtWidgets.QPushButton(parent=Dialog)
        self.input_button.setGeometry(QtCore.QRect(510, 25, 61, 32))
        self.input_button.setObjectName("input_button")
        self.input_button.clicked.connect(self._open_input_folder_dialog)
        self.input_label = QtWidgets.QLabel(parent=Dialog)
        self.input_label.setGeometry(QtCore.QRect(40, 33, 91, 16))
        self.input_label.setObjectName("input_label")
        self.darfield_label = QtWidgets.QLabel(parent=Dialog)
        self.darfield_label.setGeometry(QtCore.QRect(40, 68, 101, 16))
        self.darfield_label.setObjectName("darfield_label")
        self.darkfield_lineedit = QtWidgets.QLineEdit(parent=Dialog)
        self.darkfield_lineedit.setGeometry(QtCore.QRect(160, 65, 341, 21))
        self.darkfield_lineedit.setObjectName("darkfield_lineedit")
        self.darkfield_button = QtWidgets.QPushButton(parent=Dialog)
        self.darkfield_button.setGeometry(QtCore.QRect(510, 60, 61, 32))
        self.darkfield_button.setObjectName("darkfield_button")
        self.darkfield_button.clicked.connect(self._open_darkfile_dialog)
        self.flatfield_lineedit = QtWidgets.QLineEdit(parent=Dialog)
        self.flatfield_lineedit.setGeometry(QtCore.QRect(160, 97, 341, 21))
        self.flatfield_lineedit.setObjectName("flatfield_lineedit")
        self.flatfield_button = QtWidgets.QPushButton(parent=Dialog)
        self.flatfield_button.setGeometry(QtCore.QRect(510, 92, 61, 32))
        self.flatfield_button.setObjectName("flatfield_button")
        self.flatfield_button.clicked.connect(self._open_flatfile_dialog)
        self.flatfield_label = QtWidgets.QLabel(parent=Dialog)
        self.flatfield_label.setGeometry(QtCore.QRect(40, 100, 101, 16))
        self.flatfield_label.setObjectName("flatfield_label")
        self.cropdim_label = QtWidgets.QLabel(parent=Dialog)
        self.cropdim_label.setGeometry(QtCore.QRect(40, 130, 101, 16))
        self.cropdim_label.setObjectName("cropdim_label")
        self.rowdim_spinbox = QtWidgets.QSpinBox(parent=Dialog)
        self.rowdim_spinbox.setGeometry(QtCore.QRect(210, 128, 104, 26))
        self.rowdim_spinbox.setObjectName("rowdim_spinbox")
        self.rowdim_spinbox.setRange(0, BatchFlatFieldCorrectionDialog.MAX_DIM)
        self.coldim_spinbox = QtWidgets.QSpinBox(parent=Dialog)
        self.coldim_spinbox.setGeometry(QtCore.QRect(391, 126, 104, 26))
        self.coldim_spinbox.setObjectName("coldim_spinbox")
        self.coldim_spinbox.setRange(0, BatchFlatFieldCorrectionDialog.MAX_DIM)
        self.rowdim_label = QtWidgets.QLabel(parent=Dialog)
        self.rowdim_label.setGeometry(QtCore.QRect(170, 130, 50, 16))
        self.rowdim_label.setObjectName("rowdim_label")
        self.coldim_label = QtWidgets.QLabel(parent=Dialog)
        self.coldim_label.setGeometry(QtCore.QRect(330, 130, 50, 16))
        self.coldim_label.setObjectName("coldim_label")
        self.background_label = QtWidgets.QLabel(parent=Dialog)
        self.background_label.setGeometry(QtCore.QRect(40, 163, 101, 16))
        self.background_label.setObjectName("background_label")
        self.background_combo = QtWidgets.QComboBox(parent=Dialog)
        self.background_combo.setGeometry(QtCore.QRect(160, 159, 131, 26))
        self.background_combo.setObjectName("background_combo")
        for amode in BatchFlatFieldCorrectionDialog.BG_MODES:
            self.background_combo.addItem(amode)
        self.inputsubstr_label = QtWidgets.QLabel(parent=Dialog)
        self.inputsubstr_label.setGeometry(QtCore.QRect(40, 203, 101, 16))
        self.inputsubstr_label.setObjectName("inputsubstr_label")
        self.inputsubstr_lineedit = QtWidgets.QLineEdit(parent=Dialog)
        self.inputsubstr_lineedit.setGeometry(QtCore.QRect(160, 200, 120, 21))
        self.inputsubstr_lineedit.setText("")
        self.inputsubstr_lineedit.setObjectName("inputsubstr_lineedit")
        self.suffix_label = QtWidgets.QLabel(parent=Dialog)
        self.suffix_label.setGeometry(QtCore.QRect(320, 203, 101, 16))
        self.suffix_label.setObjectName("suffix_label")
        self.suffix_lineedit = QtWidgets.QLineEdit(parent=Dialog)
        self.suffix_lineedit.setGeometry(QtCore.QRect(440, 200, 120, 21))
        self.suffix_lineedit.setText("")
        self.suffix_lineedit.setObjectName("suffix_lineedit")

        self.retranslateUi(Dialog)
        self.ok_buttonbox.accepted.connect(Dialog.accept) # type: ignore
        self.ok_buttonbox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Batch Correct"))
        self.input_button.setText(_translate("Dialog", "..."))
        self.input_label.setText(_translate("Dialog", "input folder"))
        self.darfield_label.setText(_translate("Dialog", "darkfield image"))
        self.darkfield_button.setText(_translate("Dialog", "..."))
        self.flatfield_button.setText(_translate("Dialog", "..."))
        self.flatfield_label.setText(_translate("Dialog", "flatfield image"))
        self.cropdim_label.setText(_translate("Dialog", "crop dimensions"))
        self.rowdim_label.setText(_translate("Dialog", "rows"))
        self.coldim_label.setText(_translate("Dialog", "columns"))
        self.background_label.setText(_translate("Dialog", "background"))
        self.inputsubstr_label.setText(_translate("Dialog", "input substring"))
        self.suffix_label.setText(_translate("Dialog", "output file suffix"))

        self.input_lineedit.setText(BatchFlatFieldCorrectionDialog.input_folder)
        self.darkfield_lineedit.setText(BatchFlatFieldCorrectionDialog.darkfield_file)
        self.flatfield_lineedit.setText(BatchFlatFieldCorrectionDialog.flatfield_file)
        self.rowdim_spinbox.setValue(BatchFlatFieldCorrectionDialog.crop_dims[0])
        self.coldim_spinbox.setValue(BatchFlatFieldCorrectionDialog.crop_dims[1])
        self.background_combo.setCurrentIndex(BatchFlatFieldCorrectionDialog.BG_MODES.index(BatchFlatFieldCorrectionDialog.bg_mode))
        self.inputsubstr_lineedit.setText(BatchFlatFieldCorrectionDialog.input_substr)
        self.suffix_lineedit.setText(BatchFlatFieldCorrectionDialog.file_suffix)

    def parameters(self) -> dict:
        BatchFlatFieldCorrectionDialog.input_folder = self.input_lineedit.text()
        BatchFlatFieldCorrectionDialog.darkfield_file = self.darkfield_lineedit.text()
        BatchFlatFieldCorrectionDialog.flatfield_file = self.flatfield_lineedit.text()
        BatchFlatFieldCorrectionDialog.crop_dims = (self.rowdim_spinbox.value(), self.coldim_spinbox.value())
        BatchFlatFieldCorrectionDialog.bg_mode = self.BG_MODES[self.background_combo.currentIndex()]
        BatchFlatFieldCorrectionDialog.file_suffix = self.suffix_lineedit.text()
        BatchFlatFieldCorrectionDialog.input_substr = self.inputsubstr_lineedit.text()

        return {
            'input_folder': BatchFlatFieldCorrectionDialog.input_folder,
            'darkfield_file': BatchFlatFieldCorrectionDialog.darkfield_file,
            'flatfield_file': BatchFlatFieldCorrectionDialog.flatfield_file,
            'crop_dims': BatchFlatFieldCorrectionDialog.crop_dims,
            'bg_mode': BatchFlatFieldCorrectionDialog.bg_mode,
            'input_substr': BatchFlatFieldCorrectionDialog.input_substr,
            'file_suffix': BatchFlatFieldCorrectionDialog.file_suffix,
        }

    def _open_input_folder_dialog(self) -> bool:
        start_folder = self.input_lineedit.text() if self.input_lineedit.text() != '' else BatchFlatFieldCorrectionDialog.input_folder
        folder = RUtils.open_folder_dialog(f"Input folder", start_folder)

        if folder == '' or folder is False:
            return False

        self.input_lineedit.setText(folder)

        return True

    def _open_darkfile_dialog(self) -> bool:
        start_folder, _ = os.path.split(self.darkfield_lineedit.text())
        if start_folder == '':
            start_folder = os.path.split(BatchFlatFieldCorrectionDialog.darkfield_file)
        fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Dark field file ...',
                                                      BatchFlatFieldCorrectionDialog.input_folder,
                                                      filter='TIFF files (*.tif *.tiff)')

        self.darkfield_lineedit.setText(fname[0])

        return True

    def _open_flatfile_dialog(self) -> bool:
        start_folder, _ = os.path.split(self.flatfield_lineedit.text())
        if start_folder == '':
            start_folder = os.path.split(BatchFlatFieldCorrectionDialog.flatfield_file)
        fname = QtWidgets.QFileDialog.getOpenFileName(None, 'Flat field file ...',
                                                      BatchFlatFieldCorrectionDialog.input_folder,
                                                      filter='TIFF files (*.tif *.tiff)')

        self.flatfield_lineedit.setText(fname[0])

        return True
