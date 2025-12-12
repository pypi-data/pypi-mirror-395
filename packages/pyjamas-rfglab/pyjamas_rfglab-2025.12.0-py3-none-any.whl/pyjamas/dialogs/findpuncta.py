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

from pyjamas.pjscore import PyJAMAS
from pyjamas.rimage.rimutils import rimutils


class FindPunctaDialog(object):

    first_slice: int = -1
    last_slice: int = -1
    mean_filter_width: int = -1
    difference_threshold: float = -1.
    max_size_merge: int = -1

    def __init__(self, pjs: PyJAMAS):
        super().__init__()

        self.pjs = pjs

    def setupUi(self, Dialog, first_slice: int = None, last_slice: int = None, mean_filter_width: int = None,
                difference_threshold: float = None, max_size_merge: int = None):
        if FindPunctaDialog.first_slice < 0:
            FindPunctaDialog.first_slice = first_slice or 0

        if FindPunctaDialog.last_slice < 0:
            FindPunctaDialog.last_slice = last_slice or 1

        if FindPunctaDialog.mean_filter_width < 1:
            FindPunctaDialog.mean_filter_width = rimutils.WATER_HPFILTER_WIDTH
        else:
            FindPunctaDialog.mean_filter_width = mean_filter_width

        if FindPunctaDialog.difference_threshold < 0:
            FindPunctaDialog.difference_threshold = rimutils.WATER_POSTHPFILTER_THRESHOLD
        else:
            FindPunctaDialog.difference_threshold = difference_threshold

        if FindPunctaDialog.max_size_merge < 1:
            FindPunctaDialog.max_size_merge = rimutils.WATER_MAX_SIZE_MERGE
        else:
            FindPunctaDialog.max_size_merge = max_size_merge

        self.dialog = Dialog
        Dialog.setObjectName("Dialog")
        Dialog.resize(609, 206)
        self.ok_buttonbox = QtWidgets.QDialogButtonBox(parent=Dialog)
        self.ok_buttonbox.setGeometry(QtCore.QRect(230, 160, 341, 32))
        self.ok_buttonbox.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.ok_buttonbox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Cancel|QtWidgets.QDialogButtonBox.StandardButton.Ok)
        self.ok_buttonbox.setObjectName("ok_buttonbox")
        self.input_label = QtWidgets.QLabel(parent=Dialog)
        self.input_label.setGeometry(QtCore.QRect(30, 70, 111, 16))
        self.input_label.setObjectName("input_label")
        self.first_slice_spinbox = QtWidgets.QSpinBox(parent=Dialog)
        self.first_slice_spinbox.setGeometry(QtCore.QRect(105, 28, 104, 26))
        self.first_slice_spinbox.setMinimum(1)
        self.first_slice_spinbox.setMaximum(last_slice)
        self.first_slice_spinbox.setValue(first_slice)
        self.first_slice_spinbox.setObjectName("first_slice_spinbox")
        self.last_slice_spinbox = QtWidgets.QSpinBox(parent=Dialog)
        self.last_slice_spinbox.setGeometry(QtCore.QRect(286, 26, 104, 26))
        self.last_slice_spinbox.setMinimum(1)
        self.last_slice_spinbox.setMaximum(last_slice)
        self.last_slice_spinbox.setValue(first_slice)
        self.last_slice_spinbox.setObjectName("last_slice_spinbox")
        self.first_slice_label = QtWidgets.QLabel(parent=Dialog)
        self.first_slice_label.setGeometry(QtCore.QRect(35, 30, 101, 16))
        self.first_slice_label.setObjectName("first_slice_label")
        self.last_slice_label = QtWidgets.QLabel(parent=Dialog)
        self.last_slice_label.setGeometry(QtCore.QRect(220, 30, 101, 16))
        self.last_slice_label.setObjectName("last_slice_label")
        self.mean_width_slider = QtWidgets.QSlider(parent=Dialog)
        self.mean_width_slider.setGeometry(QtCore.QRect(170, 67, 341, 22))
        self.mean_width_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.mean_width_slider.setMinimum(2)
        self.mean_width_slider.setMaximum(rimutils.WATER_HPFILTER_WIDTH_MAX)
        self.mean_width_slider.setValue(FindPunctaDialog.mean_filter_width)
        self.mean_width_slider.valueChanged.connect(lambda: (self.mean_width_edit.setText(str(self.mean_width_slider.value()))))
        self.mean_width_slider.sliderReleased.connect(self._update_mean_width_slider)
        self.mean_width_slider.setObjectName("mean_width_slider")
        self.diff_threshold_slider = QtWidgets.QSlider(parent=Dialog)
        self.diff_threshold_slider.setGeometry(QtCore.QRect(170, 97, 341, 22))
        self.diff_threshold_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.diff_threshold_slider.setMinimum(1)
        self.diff_threshold_slider.setMaximum(self.pjs.imagedata.max()-self.pjs.imagedata.min())
        self.diff_threshold_slider.setValue(FindPunctaDialog.difference_threshold)
        self.diff_threshold_slider.valueChanged.connect(
            lambda: (self.diff_threshold_edit.setText(str(self.diff_threshold_slider.value()))))
        self.diff_threshold_slider.sliderReleased.connect(self._update_diff_threshold_slider)
        self.diff_threshold_slider.setObjectName("diff_threshold_slider")
        self.input_label_2 = QtWidgets.QLabel(parent=Dialog)
        self.input_label_2.setGeometry(QtCore.QRect(30, 100, 131, 16))
        self.input_label_2.setObjectName("input_label_2")
        self.input_label_3 = QtWidgets.QLabel(parent=Dialog)
        self.input_label_3.setGeometry(QtCore.QRect(30, 130, 131, 16))
        self.input_label_3.setObjectName("input_label_3")
        self.max_size_slider = QtWidgets.QSlider(parent=Dialog)
        self.max_size_slider.setGeometry(QtCore.QRect(170, 127, 341, 22))
        self.max_size_slider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.max_size_slider.setMinimum(1)
        self.max_size_slider.setMaximum(rimutils.WATER_MAX_SIZE_MERGE_MAX)
        self.max_size_slider.setValue(FindPunctaDialog.max_size_merge)
        self.max_size_slider.valueChanged.connect(
            lambda: (self.max_size_edit.setText(str(self.max_size_slider.value()))))
        self.max_size_slider.sliderReleased.connect(self._update_max_size_slider)
        self.max_size_slider.setObjectName("max_size_slider")
        self.mean_width_edit = QtWidgets.QLineEdit(parent=Dialog)
        self.mean_width_edit.setGeometry(QtCore.QRect(521, 68, 61, 21))
        self.mean_width_edit.textEdited.connect(self._set_new_mean_width_slider_value)
        self.mean_width_edit.editingFinished.connect(self._update_mean_width_edit)
        self.mean_width_edit.setText(str(FindPunctaDialog.mean_filter_width))
        self.mean_width_edit.setObjectName("mean_width_edit")
        self.diff_threshold_edit = QtWidgets.QLineEdit(parent=Dialog)
        self.diff_threshold_edit.setGeometry(QtCore.QRect(520, 100, 61, 21))
        self.diff_threshold_edit.setText(str(FindPunctaDialog.difference_threshold))
        self.diff_threshold_edit.textEdited.connect(self._set_new_diff_threshold_slider_value)
        self.diff_threshold_edit.editingFinished.connect(self._update_diff_threshold_edit)
        self.diff_threshold_edit.setObjectName("diff_threshold_edit")
        self.max_size_edit = QtWidgets.QLineEdit(parent=Dialog)
        self.max_size_edit.setGeometry(QtCore.QRect(520, 130, 61, 21))
        self.max_size_edit.setText(str(FindPunctaDialog.max_size_merge))
        self.max_size_edit.textEdited.connect(self._set_new_max_size_slider_value)
        self.max_size_edit.editingFinished.connect(self._update_max_size_edit)
        self.max_size_edit.setObjectName("max_size_edit")

        self.retranslateUi(Dialog)
        self.ok_buttonbox.accepted.connect(self.accept)
        self.ok_buttonbox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self._old_annotations = self.pjs.copy_annotations()
        self._clean_n_run_water()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Find puncta"))
        self.input_label.setText(_translate("Dialog", "mean filter width"))
        self.first_slice_label.setText(_translate("Dialog", "first slice"))
        self.last_slice_label.setText(_translate("Dialog", "last slice"))
        self.input_label_2.setText(_translate("Dialog", "difference threshold"))
        self.input_label_3.setText(_translate("Dialog", "maximum merge size"))

    def parameters(self):
        FindPunctaDialog.first_slice = self.first_slice_spinbox.value()
        FindPunctaDialog.last_slice = self.last_slice_spinbox.value()
        FindPunctaDialog.mean_filter_width = self.mean_width_slider.value()
        FindPunctaDialog.difference_threshold = self.diff_threshold_slider.value()
        FindPunctaDialog.max_size_merge = self.max_size_slider.value()

        return {
            'first_slice': FindPunctaDialog.first_slice,
            'last_slice': FindPunctaDialog.last_slice,
            'mean_filter_width': FindPunctaDialog.mean_filter_width,
            'difference_threshold': FindPunctaDialog.difference_threshold,
            'max_size_merge': FindPunctaDialog.max_size_merge,
        }

    def _update_max_size_slider(self):
        self.max_size_edit.setText(str(self.max_size_slider.value()))

        self._clean_n_run_water()

        return True
    
    def _set_new_max_size_slider_value(self):
        try:
            self.max_size_slider.setValue(int(self.mean_width_edit.text()))
        except ValueError:
            pass

        return True

    def _update_max_size_edit(self):
        self._set_new_max_size_slider_value()
        self._clean_n_run_water()

        return True

    def _update_mean_width_slider(self):
        self.mean_width_edit.setText(str(self.mean_width_slider.value()))

        self._clean_n_run_water()

        return True

    def _set_new_mean_width_slider_value(self):
        try:
            self.mean_width_slider.setValue(int(self.mean_width_edit.text()))
        except ValueError:
            pass

        return True

    def _update_mean_width_edit(self):
        self._set_new_mean_width_slider_value()
        self._clean_n_run_water()

        return True

    def _update_diff_threshold_slider(self):
        self.diff_threshold_edit.setText(str(self.diff_threshold_slider.value()))

        self._clean_n_run_water()

        return True

    def _set_new_diff_threshold_slider_value(self):
        try:
            self.diff_threshold_slider.setValue(int(self.diff_threshold_edit.text()))
        except ValueError:
            pass

        return True

    def _update_diff_threshold_edit(self):
        self._set_new_diff_threshold_slider_value()
        self._clean_n_run_water()

        return True

    def _clean_n_run_water(self):
        self.pjs.annotations.cbDeleteAllAnn()
        self._water()

        return True

    def _water(self):
        parameters = self.parameters()

        self.pjs.image.cbFindPuncta(self.pjs.curslice+1, self.pjs.curslice+1, parameters.get('mean_filter_width'),
                                    parameters.get('difference_threshold'),
                                    parameters.get('max_size_merge'), True)

        return True

    def accept(self):
        self.pjs.annotations.cbDeleteAllAnn()
        self.pjs.paste_annotations(self._old_annotations)
        #self._water()
        self.dialog.accept()

    def reject(self):
        self.pjs.annotations.cbDeleteAllAnn()
        self.pjs.paste_annotations(self._old_annotations)
        self.dialog.reject()
