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
import inspect
from functools import partial
from typing import Optional, Tuple

from PyQt6 import QtCore, QtWidgets

from pyjamas.rimage.rimml.rimneuralnet import rimneuralnet
from pyjamas.rutils import RUtils


class NeuralNetDialog:
    positive_training_folder: str = ''
    save_folder: str = ''
    train_image_size: Tuple[int, int] = (0, 0)
    epochs: int = rimneuralnet.EPOCHS
    learning_rate: float = rimneuralnet.LEARNING_RATE
    mini_batch_size: int = rimneuralnet.BATCH_SIZE
    erosion_width: int = rimneuralnet.EROSION_WIDTH
    step_sz: Tuple[int, int] = rimneuralnet.STEP_SIZE
    validation_split: float = rimneuralnet.VALIDATION_SPLIT
    early_stopper: dict = rimneuralnet.EARLY_STOPPER
    lr_scheduler: dict = rimneuralnet.LR_SCHEDULER
    model_checkpoint: dict = rimneuralnet.MODEL_CHECKPOINT
    logging: dict = rimneuralnet.LOGGING

    generate_notebook: bool = False
    notebook_path: str = ''

    def __init__(self):
        super().__init__()

    def setupUi(self, NNet: QtWidgets.QDialog, parameters: Optional[dict] = None):
        attributes = inspect.getmembers(NeuralNetDialog, lambda a: not (inspect.isroutine(a)))
        attributes = [a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))]
        for key, value in attributes:
            if parameters is not None and parameters is not False and key in parameters:
                NeuralNetDialog.__setattr__(key, parameters[key])

        NNet.setObjectName("NNet")
        NNet.resize(614, 565)

        # ===================================== GroupBox for Folders ===================================================

        self.groupBox_2 = QtWidgets.QGroupBox(NNet)
        self.groupBox_2.setObjectName("groupBox_2")
        self.groupBox_2.setGeometry(30, 26, 551, 130)

        self.label_ptf = QtWidgets.QLabel(self.groupBox_2)
        self.label_ptf.setObjectName("label_ptf")
        self.label_ptf.setGeometry(31, 26, 141, 24)
        self.positive_training_folder_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.positive_training_folder_edit.setObjectName("positive_training_folder_edit")
        self.positive_training_folder_edit.setGeometry(220, 30, 261, 21)
        self.positive_training_folder_edit.setText(NeuralNetDialog.positive_training_folder)
        self.btnSavePositive = QtWidgets.QToolButton(self.groupBox_2)
        self.btnSavePositive.setObjectName("btnSavePositive")
        self.btnSavePositive.setGeometry(490, 30, 26, 22)
        self.btnSavePositive.clicked.connect(self._open_positive_folder_dialog)

        self.label_sf = QtWidgets.QLabel(self.groupBox_2)
        self.label_sf.setObjectName("label_sf")
        self.label_sf.setGeometry(31, 56, 141, 24)
        self.save_folder_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.save_folder_edit.setObjectName("save_folder_edit")
        self.save_folder_edit.setGeometry(220, 60, 261, 21)
        self.save_folder_edit.setText(NeuralNetDialog.save_folder)
        self.btnSaveSave = QtWidgets.QToolButton(self.groupBox_2)
        self.btnSaveSave.setObjectName("btnSavePositive")
        self.btnSaveSave.setGeometry(490, 60, 26, 22)
        self.btnSaveSave.clicked.connect(self._open_save_folder_dialog)

        self.cbGenerateNotebook = QtWidgets.QCheckBox(self.groupBox_2)
        self.cbGenerateNotebook.setObjectName("cbGenerateNotebook")
        self.cbGenerateNotebook.setGeometry(31, 86, 200, 24)
        self.cbGenerateNotebook.setChecked(NeuralNetDialog.generate_notebook)
        self.notebook_path_edit = QtWidgets.QLineEdit(self.groupBox_2)
        self.notebook_path_edit.setObjectName("notebook_path_edit")
        self.notebook_path_edit.setGeometry(220, 90, 261, 21)
        self.notebook_path_edit.setText(NeuralNetDialog.notebook_path)
        self.notebook_path_edit.setEnabled(NeuralNetDialog.generate_notebook)
        self.btnSaveNotebook = QtWidgets.QToolButton(self.groupBox_2)
        self.btnSaveNotebook.setObjectName("btnSaveNotebook")
        self.btnSaveNotebook.setGeometry(490, 90, 26, 22)
        self.btnSaveNotebook.clicked.connect(self._open_notebook_path_dialog)
        self.btnSaveNotebook.setEnabled(NeuralNetDialog.generate_notebook)
        self.cbGenerateNotebook.stateChanged.connect(partial(self._connect_check, self.cbGenerateNotebook,
                                                             [self.notebook_path_edit, self.btnSaveNotebook],
                                                             True))

        self.label_ptf.setEnabled(not self.cbGenerateNotebook.isChecked())
        self.positive_training_folder_edit.setEnabled(not self.cbGenerateNotebook.isChecked())
        self.btnSavePositive.setEnabled(not self.cbGenerateNotebook.isChecked())
        self.label_sf.setEnabled(not self.cbGenerateNotebook.isChecked())
        self.save_folder_edit.setEnabled(not self.cbGenerateNotebook.isChecked())
        self.btnSaveSave.setEnabled(not self.cbGenerateNotebook.isChecked())
        self.cbGenerateNotebook.stateChanged.connect(partial(self._connect_check, self.cbGenerateNotebook,
                                                             [self.label_ptf, self.positive_training_folder_edit,
                                                              self.btnSavePositive, self.label_sf,
                                                              self.save_folder_edit, self.btnSaveSave],
                                                             False))

        # ======================== GroupBox for Network Input Size and Step Size  ======================================

        self.groupBox_3 = QtWidgets.QGroupBox(NNet)
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setGeometry(30, 167, 251, 61)

        self.label_w = QtWidgets.QLabel(self.groupBox_3)
        self.label_w.setObjectName("label_w")
        self.label_w.setGeometry(31, 28, 141, 24)
        self.lnWidth = QtWidgets.QLineEdit(self.groupBox_3)
        self.lnWidth.setObjectName("lnWidth")
        self.lnWidth.setGeometry(70, 30, 31, 21)
        self.lnWidth.setText(str(NeuralNetDialog.train_image_size[1]))
        self.label_h = QtWidgets.QLabel(self.groupBox_3)
        self.label_h.setObjectName("label_h")
        self.label_h.setGeometry(120, 28, 141, 24)
        self.lnHeight = QtWidgets.QLineEdit(self.groupBox_3)
        self.lnHeight.setObjectName("lnHeight")
        self.lnHeight.setGeometry(170, 30, 31, 21)
        self.lnHeight.setText(str(NeuralNetDialog.train_image_size[0]))

        self.groupBox_6 = QtWidgets.QGroupBox(NNet)
        self.groupBox_6.setObjectName("groupBox_6")
        self.groupBox_6.setGeometry(330, 167, 251, 61)

        self.label_r = QtWidgets.QLabel(self.groupBox_6)
        self.label_r.setObjectName("label_r")
        self.label_r.setGeometry(31, 28, 141, 24)
        self.lnRow = QtWidgets.QLineEdit(self.groupBox_6)
        self.lnRow.setObjectName("lnRow")
        self.lnRow.setGeometry(70, 30, 31, 21)
        self.lnRow.setText(str(NeuralNetDialog.step_sz[0]))
        self.label_c = QtWidgets.QLabel(self.groupBox_6)
        self.label_c.setObjectName("label_c")
        self.label_c.setGeometry(120, 28, 141, 24)
        self.lnColumn = QtWidgets.QLineEdit(self.groupBox_6)
        self.lnColumn.setObjectName("lnColumn")
        self.lnColumn.setGeometry(180, 30, 31, 21)
        self.lnColumn.setText(str(NeuralNetDialog.step_sz[1]))

        # ================================ GroupBox for Other Parameters ===============================================

        self.groupBox_5 = QtWidgets.QGroupBox(NNet)
        self.groupBox_5.setObjectName("groupBox_5")
        self.groupBox_5.setGeometry(30, 249, 551, 100)

        self.label_lr = QtWidgets.QLabel(self.groupBox_5)
        self.label_lr.setObjectName("label_lr")
        self.label_lr.setGeometry(61, 31, 141, 16)
        self.lnEta = QtWidgets.QLineEdit(self.groupBox_5)
        self.lnEta.setObjectName("lnEta")
        self.lnEta.setGeometry(147, 27, 46, 21)
        self.lnEta.setText(str(NeuralNetDialog.learning_rate))
        self.label_bs = QtWidgets.QLabel(self.groupBox_5)
        self.label_bs.setObjectName("label_bs")
        self.label_bs.setGeometry(231, 31, 95, 16)
        self.lnBatchSz = QtWidgets.QLineEdit(self.groupBox_5)
        self.lnBatchSz.setObjectName("lnBatchSz")
        self.lnBatchSz.setGeometry(301, 27, 46, 21)
        self.lnBatchSz.setText(str(NeuralNetDialog.mini_batch_size))
        self.label_epochs = QtWidgets.QLabel(self.groupBox_5)
        self.label_epochs.setObjectName("label_epochs")
        self.label_epochs.setGeometry(376, 31, 45, 16)
        self.lnEpochs = QtWidgets.QLineEdit(self.groupBox_5)
        self.lnEpochs.setObjectName("lnEpochs")
        self.lnEpochs.setGeometry(426, 27, 41, 21)
        self.lnEpochs.setText(str(NeuralNetDialog.epochs))

        self.label_val = QtWidgets.QLabel(self.groupBox_5)
        self.label_val.setObjectName("label_val")
        self.label_val.setGeometry(111, 75, 141, 16)
        self.lnValSplit = QtWidgets.QLineEdit(self.groupBox_5)
        self.lnValSplit.setObjectName("lnValSplit")
        self.lnValSplit.setGeometry(201, 71, 46, 21)
        self.lnValSplit.setText(str(NeuralNetDialog.validation_split))
        self.label_ew = QtWidgets.QLabel(self.groupBox_5)
        self.label_ew.setObjectName("label_ew")
        self.label_ew.setGeometry(271, 75, 141, 16)
        self.lnErosionWidth = QtWidgets.QLineEdit(self.groupBox_5)
        self.lnErosionWidth.setObjectName("lnErosionWidth")
        self.lnErosionWidth.setGeometry(361, 71, 46, 21)
        self.lnErosionWidth.setText(str(NeuralNetDialog.erosion_width))

        # ============================== GroupBox with advanced options for Callbacks ==================================

        self.groupBox_7 = QtWidgets.QGroupBox(NNet)
        self.groupBox_7.setObjectName("groupBox_7")
        self.groupBox_7.setGeometry(30, 365, 551, 150)

        self.cbEarlyStopper = QtWidgets.QCheckBox(self.groupBox_7)
        self.cbEarlyStopper.setObjectName("cbEarlyStopper")
        self.cbEarlyStopper.setGeometry(31, 30, 250, 24)
        self.cbEarlyStopper.setChecked(NeuralNetDialog.early_stopper['active'])
        self.label_patience = QtWidgets.QLabel(self.groupBox_7)
        self.label_patience.setObjectName("label_patience")
        self.label_patience.setGeometry(250, 30, 141, 24)
        self.label_patience.setEnabled(NeuralNetDialog.early_stopper['active'])
        self.lnESPatience = QtWidgets.QLineEdit(self.groupBox_7)
        self.lnESPatience.setObjectName("lnESPatience")
        self.lnESPatience.setGeometry(325, 30, 46, 21)
        self.lnESPatience.setText(str(NeuralNetDialog.early_stopper['kwargs']['patience']))
        self.lnESPatience.setEnabled(NeuralNetDialog.early_stopper['active'])
        self.cbEarlyStopper.stateChanged.connect(partial(self._connect_check, self.cbEarlyStopper,
                                                         [self.label_patience, self.lnESPatience],
                                                         True))

        self.cbLRScheduler = QtWidgets.QCheckBox(self.groupBox_7)
        self.cbLRScheduler.setObjectName("cbLRScheduler")
        self.cbLRScheduler.setGeometry(31, 60, 250, 24)
        self.cbLRScheduler.setChecked(NeuralNetDialog.lr_scheduler['active'])
        self.label_lrpatience = QtWidgets.QLabel(self.groupBox_7)
        self.label_lrpatience.setObjectName("label_lrpatience")
        self.label_lrpatience.setGeometry(250, 60, 141, 24)
        self.label_lrpatience.setEnabled(NeuralNetDialog.lr_scheduler['active'])
        self.lnLRPatience = QtWidgets.QLineEdit(self.groupBox_7)
        self.lnLRPatience.setObjectName("lnLRPatience")
        self.lnLRPatience.setGeometry(325, 60, 46, 21)
        self.lnLRPatience.setText(str(NeuralNetDialog.lr_scheduler['kwargs']['patience']))
        self.lnLRPatience.setEnabled(NeuralNetDialog.lr_scheduler['active'])
        self.cbLRScheduler.stateChanged.connect(partial(self._connect_check, self.cbLRScheduler,
                                                        [self.label_lrpatience, self.lnLRPatience],
                                                        True))

        self.cbModelCheckpoint = QtWidgets.QCheckBox(self.groupBox_7)
        self.cbModelCheckpoint.setObjectName("cbModelCheckpoint")
        self.cbModelCheckpoint.setGeometry(31, 90, 250, 24)
        self.cbModelCheckpoint.setChecked(NeuralNetDialog.model_checkpoint['active'])
        self.cbCkptBestOnly = QtWidgets.QCheckBox(self.groupBox_7)
        self.cbCkptBestOnly.setObjectName("cbCkptBestOnly")
        self.cbCkptBestOnly.setGeometry(250, 90, 250, 24)
        self.cbCkptBestOnly.setMaximumWidth(175)
        self.cbCkptBestOnly.setChecked(NeuralNetDialog.model_checkpoint['kwargs']['save_best_only'])
        self.cbModelCheckpoint.stateChanged.connect(partial(self._connect_check, self.cbModelCheckpoint,
                                                            [self.cbCkptBestOnly], True))

        self.cbLogging = QtWidgets.QCheckBox(self.groupBox_7)
        self.cbLogging.setObjectName("cbLogging")
        self.cbLogging.setGeometry(31, 120, 200, 24)
        self.cbLogging.setChecked(NeuralNetDialog.logging['active'])

        # ======================================== Accept or Reject Buttons ============================================

        self.buttonBox = QtWidgets.QDialogButtonBox(NNet)
        self.buttonBox.setGeometry(240, 525, 341, 32)
        self.buttonBox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel | QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.retranslateUi(NNet)
        self.buttonBox.accepted.connect(NNet.accept)
        self.buttonBox.rejected.connect(NNet.reject)
        QtCore.QMetaObject.connectSlotsByName(NNet)

    def retranslateUi(self, CNN):
        _translate = QtCore.QCoreApplication.translate
        CNN.setWindowTitle(_translate("NNet", "Train network"))
        self.groupBox_2.setTitle(_translate("NNet", "Project files"))
        self.label_ptf.setText(_translate("NNet", "training image folder"))
        self.label_sf.setText(_translate("NNet", "save folder"))
        self.btnSavePositive.setText(_translate("NNet", "..."))
        self.btnSaveSave.setText(_translate("NNet", "..."))
        self.cbGenerateNotebook.setText(_translate("NNet", "generate training notebook"))
        self.btnSaveNotebook.setText(_translate("NNet", "..."))
        self.groupBox_3.setTitle(_translate("NNet", "Network input size"))
        self.label_w.setText(_translate("NNet", "width"))
        self.label_h.setText(_translate("NNet", "height"))
        self.groupBox_5.setTitle(_translate("NNet", "Other parameters"))
        self.label_epochs.setText(_translate("NNet", "epochs"))
        self.label_lr.setText(_translate("NNet", "learning rate"))
        self.groupBox_6.setTitle(_translate("NNet", "Step size (testing)"))
        self.label_r.setText(_translate("NNet", "rows"))
        self.label_c.setText(_translate("NNet", "columns"))
        self.label_bs.setText(_translate("NNet", "batch size"))
        self.label_ew.setText(_translate("NNet", "erosion width"))
        self.label_val.setText(_translate("NNet", "validation split"))
        self.groupBox_7.setTitle(_translate("NNet", "Advanced settings"))
        self.cbEarlyStopper.setText(_translate("NNet", "early stopping"))
        self.label_patience.setText(_translate("NNet", "patience"))
        self.cbLRScheduler.setText(_translate("NNet", "learning rate scheduler"))
        self.label_lrpatience.setText(_translate("NNet", "patience"))
        self.cbModelCheckpoint.setText(_translate("NNet", "save model checkpoints"))
        self.cbCkptBestOnly.setText(_translate("NNet", "save best weights only"))
        self.cbLogging.setText(_translate("NNet", "log training progress"))

    def parameters(self) -> dict:
        # os.path.join(self.positive_training_folder, '') adds a slash at the end of the filename.
        NeuralNetDialog.positive_training_folder = os.path.join(self.positive_training_folder_edit.text(), '')
        NeuralNetDialog.save_folder = os.path.join(self.save_folder_edit.text(), '')

        # Because of the U-Net architecture, input layer dimensions must be divisible by 16 to avoid issues.
        input_size = (int(self.lnHeight.text()), int(self.lnWidth.text()))
        height = (input_size[0] // 16) * 16 if input_size[0] % 16 else input_size[0]
        width = (input_size[1] // 16) * 16 if input_size[1] % 16 else input_size[1]
        NeuralNetDialog.train_image_size = (height, width)

        NeuralNetDialog.step_sz = (int(self.lnRow.text()), int(self.lnColumn.text()))
        NeuralNetDialog.epochs = int(self.lnEpochs.text())
        NeuralNetDialog.learning_rate = float(self.lnEta.text())
        NeuralNetDialog.mini_batch_size = int(self.lnBatchSz.text())
        NeuralNetDialog.erosion_width = int(self.lnErosionWidth.text())
        NeuralNetDialog.generate_notebook = self.cbGenerateNotebook.isChecked()
        NeuralNetDialog.notebook_path = self.notebook_path_edit.text()
        NeuralNetDialog.validation_split = float(self.lnValSplit.text())
        NeuralNetDialog.early_stopper['active'] = self.cbEarlyStopper.isChecked()
        NeuralNetDialog.early_stopper['kwargs']['patience'] = int(self.lnESPatience.text())
        NeuralNetDialog.lr_scheduler['active'] = self.cbLRScheduler.isChecked()
        NeuralNetDialog.lr_scheduler['kwargs']['patience'] = int(self.lnLRPatience.text())
        NeuralNetDialog.model_checkpoint['active'] = self.cbModelCheckpoint.isChecked()
        NeuralNetDialog.model_checkpoint['kwargs']['save_best_only'] = self.cbCkptBestOnly.isChecked()
        NeuralNetDialog.logging['active'] = self.cbLogging.isChecked()

        attributes = inspect.getmembers(NeuralNetDialog, lambda a: not (inspect.isroutine(a)))
        return dict([a for a in attributes if not (a[0].startswith('__') and a[0].endswith('__'))])

    def _open_positive_folder_dialog(self) -> bool:
        folder = RUtils.open_folder_dialog("Positive training folder", NeuralNetDialog.positive_training_folder)

        if folder == '' or folder is False or self.positive_training_folder_edit is None:
            return False

        self.positive_training_folder_edit.setText(folder)

        return True

    def _open_notebook_path_dialog(self) -> bool:
        start_folder = self.notebook_path_edit.text() if self.notebook_path_edit.text() != '' else self.positive_training_folder_edit.text() if self.positive_training_folder_edit.text() != '' else self.notebook_path
        folder = RUtils.open_folder_dialog(f"Results folder", start_folder)

        if folder == '' or folder is False:
            return False

        self.notebook_path_edit.setText(folder)

        return True

    def _open_save_folder_dialog(self) -> bool:
        folder = RUtils.open_folder_dialog("Save folder", self.save_folder)

        if folder == '' or folder is False or self.save_folder_edit is None:
            return False

        self.save_folder_edit.setText(folder)
        return True

    @staticmethod
    def _connect_check(leader: QtWidgets.QCheckBox, followers: list, enable_on_check: bool):
        for follower in followers:
            follower.setEnabled(leader.isChecked() == enable_on_check)
