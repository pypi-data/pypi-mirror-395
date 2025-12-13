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

from datetime import datetime
import os
from typing import Optional

import nbformat as nbf
import numpy
from PyQt6 import QtWidgets

import pyjamas.dialogs as dialogs
from pyjamas.pjscore import PyJAMAS
from pyjamas.pjsthreads import ThreadSignals
from pyjamas.rcallbacks.rcallback import RCallback
from pyjamas.rimage.rimml.rimclassifier import rimclassifier
import pyjamas.rimage.rimml.rimlr as rimlr
import pyjamas.rimage.rimml.rimsvm as rimsvm
import pyjamas.rimage.rimml.rimunet as rimunet
import pyjamas.rimage.rimml.rimrescunet as rimrescunet
from pyjamas.rimage.rimml.rimneuralnet import rimneuralnet
from pyjamas.rutils import RUtils
from pyjamas.rimage.rimml.classifier_types import classifier_types


class RCBClassifiers(RCallback):
    COLAB_NOTEBOOK_APPENDIX: str = '_colab_notebook'

    def cbCreateLR(self, parameters: Optional[dict] = None, wait_for_thread: bool = False) -> bool:
        """
        Create a logistic regression classifier.

        :param parameters: dictionary containing the parameters to create a logistic regression classifier; a dialog opens if this parameter is set to None; keys are:

            ``positive_training_folder``:
                path to the folder containing positive training images, formatted as a string
            ``negative_training_folder``:
                path to the folder containing negative training images, formatted as a string
            ``hard_negative_training_folder``:
                path to the folder containing hard negative training images, formatted as a string
            ``histogram_of_gradients``:
                use the distribution of gradient orientations as image features, True or False
            ``train_image_size``:
                the number of rows and columns in the positive and negative training images, formatted as a tuple of two integers
            ``step_sz``:
                number of pixel rows and columns to skip when scanning test images for target structures, formatted as a tuple of two integers
            ``misclass_penalty_C``:
                penalty for misclassification of training samples, formatted as a float
        :param wait_for_thread: True if PyJAMAS must wait for the thread running this operation to complete, False otherwise.
        :return: True if the classifier was successfully created, False otherwise.
        """
        continue_flag = True

        if parameters is None or parameters is False:
            dialog = QtWidgets.QDialog()
            ui = dialogs.logregression.LRDialog()
            ui.setupUi(dialog)

            dialog.exec()
            dialog.show()

            continue_flag = dialog.result() == QtWidgets.QDialog.DialogCode.Accepted
            parameters = ui.parameters()

            dialog.close()

        if continue_flag:
            self.pjs.batch_classifier.image_classifier = rimlr.lr(parameters)
            self.launch_thread(self.pjs.batch_classifier.fit, {'stop': True}, finished_fn=self.finished_fn,
                               stop_fn=self.stop_fn, wait_for_thread=wait_for_thread)

            return True

        else:
            return False

    def cbCreateUNet(self, parameters: Optional[dict] = None, wait_for_thread: bool = False) -> bool:  # Handle IO errors.
        """
        Create a convolutional neural network with UNet architecture.

        :param parameters: dictionary containing the parameters to create a UNet; a dialog opens if this parameter is set to None; keys are:

            ``positive_training_folder``:
                path to the folder containing positive training images, formatted as a string
            ``train_image_size``:
                the number of rows and columns in the network input (train images will be scaled to this size) formatted as a tuple of two integers, both of the integers must be divisible by 16.
            ``step_sz``:
                number of pixel rows and columns to divide test images into, each subimage will be scaled to the network input size and processed, formatted as a tuple of two integers
            ``epochs``:
                maximum number of iterations over the training data, as an int
            ``learning_rate``:
                step size when updating the weights, as a float
            ``mini_batch_size``:
                size of mini batches, as an int
            ``erosion_width``:
                width of the erosion kernel to apply to the labeled image produced by the UNet, to separate touching objects, as an int
            ``generate_notebook``:
                whether a Jupyter notebook to create and train the UNet (e.g. in Google Colab) should be generated, as a bool (if True, the UNet will NOT be created)
            ``notebook_path``:
                where to store the Jupyter notebook if it must be created
        :param wait_for_thread: True if PyJAMAS must wait for the thread running this operation to complete, False otherwise.
        :return: True if the classifier was successfully created, False otherwise.
        """
        continue_flag = True

        if parameters is None or parameters is False:
            dialog = QtWidgets.QDialog()
            ui = dialogs.neuralnet.NeuralNetDialog()
            ui.setupUi(dialog)

            dialog.exec()
            dialog.show()

            continue_flag = dialog.result() == QtWidgets.QDialog.DialogCode.Accepted
            parameters = ui.parameters()

            dialog.close()

        if continue_flag:
            self.pjs.batch_classifier.image_classifier = rimunet.UNet(parameters)

            if not parameters.get('generate_notebook'):
                self.launch_thread(self.pjs.batch_classifier.fit, {'stop': True}, finished_fn=self.finished_fn,
                                   stop_fn=self.stop_fn, wait_for_thread=wait_for_thread)
            else:
                self._generate_neuralnet_notebook(parameters, classifier_types.UNET.value)

            return True

        else:
            return False

    def cbCreateReSCUNet(self, parameters: Optional[dict] = None, wait_for_thread: bool = False) -> bool:  # Handle IO errors.
        """
        Create a convolutional neural network with ReSCUNet architecture.

        :param parameters: dictionary containing the parameters to create a ReSCUNet; a dialog opens if this parameter is set to None; keys are:

            ``positive_training_folder``:
                path to the folder containing positive training images, formatted as a string
            ``train_image_size``:
                the number of rows and columns in the network input (train images will be scaled to this size) formatted as a tuple of two integers, both of the integers must be divisible by 16.
            ``step_sz``:
                number of pixel rows and columns to divide test images into, each subimage will be scaled to the network input size and processed, formatted as a tuple of two integers
            ``epochs``:
                maximum number of iterations over the training data, as an int
            ``learning_rate``:
                step size when updating the weights, as a float
            ``mini_batch_size``:
                size of mini batches, as an int
            ``erosion_width``:
                width of the erosion kernel to apply to the labeled image produced by the UNet, to separate touching objects, as an int
            ``concatenation_depth``:
                number of encoder blocks before previous segmentation mask and current image frame input streams are combined in the network
            ``generate_notebook``:
                whether a Jupyter notebook to create and train the UNet (e.g. in Google Colab) should be generated, as a bool (if True, the UNet will NOT be created)
            ``notebook_path``:
                where to store the Jupyter notebook if it must be created
            ``save_folder``:
                where to store resized images and weight maps, if empty the resized images and weight maps will not be saved
            ``resize_images_flag``:
                whether or not to resize images, resized images and weight_maps will be loaded from positive_training_folder if False
        :param wait_for_thread: True if PyJAMAS must wait for the thread running this operation to complete, False otherwise.
        :return: True if the classifier was successfully created, False otherwise.
        """
        continue_flag = True

        if parameters is None or parameters is False:
            dialog = QtWidgets.QDialog()
            ui = dialogs.rescuneuralnet.ReSCUNetDialog()
            ui.setupUi(dialog)

            dialog.exec()
            dialog.show()

            continue_flag = dialog.result() == QtWidgets.QDialog.DialogCode.Accepted
            parameters = ui.parameters()

            dialog.close()

        if continue_flag:
            self.pjs.batch_classifier.image_classifier = rimrescunet.ReSCUNet(parameters)

            if not parameters.get('generate_notebook'):
                self.launch_thread(self.pjs.batch_classifier.fit, {'stop': True}, finished_fn=self.finished_fn,
                                   stop_fn=self.stop_fn, wait_for_thread=wait_for_thread)
            else:
                self._generate_neuralnet_notebook(parameters, classifier_types.RESCUNET.value)

            return True

        else:
            return False

    def _generate_neuralnet_notebook(self, parameters: dict, architecture: classifier_types = classifier_types.UNET.value) -> bool:
        # Follow scheme of path generation from measure notebook from rcbbatchprocess._save_notebook
        path = parameters.get('notebook_path')

        # Create filename
        thenow = datetime.now()
        filename = thenow.strftime(
            f"{thenow.year:04}{thenow.month:02}{thenow.day:02}_{thenow.hour:02}{thenow.minute:02}{thenow.second:02}")
        filepath = os.path.join(path, filename)
        fname = RUtils.set_extension(filepath+RCBClassifiers.COLAB_NOTEBOOK_APPENDIX, PyJAMAS.notebook_extension)

        if architecture == classifier_types.UNET.value:
            template_fname = os.path.join(self.pjs.folder, "notebooks", "unet.ipynb")
        elif architecture == classifier_types.RESCUNET.value:
            template_fname = os.path.join(self.pjs.folder, "notebooks", "rescunet.ipynb")

        with open(template_fname, 'r') as f:
            template = nbf.read(f, as_version=4)

        for acell in template.cells:
            if acell.cell_type == 'code':
                acell.source = acell.source.replace('{{positive_training_folder}}', f"'{parameters.get('positive_training_folder')}'")
                acell.source = acell.source.replace('{{save_folder}}', f"'{parameters.get('save_folder')}'")
                acell.source = acell.source.replace('{{train_image_size}}', str(parameters.get('train_image_size')))
                acell.source = acell.source.replace('{{step_sz}}', str(parameters.get('step_sz')))
                acell.source = acell.source.replace('{{learning_rate}}', str(parameters.get('learning_rate')))
                acell.source = acell.source.replace('{{mini_batch_size}}', str(parameters.get('mini_batch_size')))
                acell.source = acell.source.replace('{{epochs}}', str(parameters.get('epochs')))
                acell.source = acell.source.replace('{{validation_split}}', str(parameters.get('validation_split')))
                acell.source = acell.source.replace('{{erosion_width}}', str(parameters.get('erosion_width')))
                acell.source = acell.source.replace('{{early_stopper}}', str(parameters.get('early_stopper')))
                acell.source = acell.source.replace('{{lr_scheduler}}', str(parameters.get('lr_scheduler')))
                acell.source = acell.source.replace('{{model_checkpoint}}', str(parameters.get('model_checkpoint')))
                acell.source = acell.source.replace('{{logging}}', str(parameters.get('logging')))
                acell.source = acell.source.replace('{{concatenation_level}}', str(parameters.get('concatenation_level')))

        with open(fname, 'w') as f:
            nbf.write(template, f)

        return True

    def cbCreateSVM(self, parameters: Optional[dict] = None, wait_for_thread: bool = False) -> bool:  # Handle IO errors.
        """
        Create a support vector machine classifier.

        :param parameters: dictionary containing the parameters to create a logistic regression classifier; a dialog opens if this parameter is set to None; keys are:

            ``positive_training_folder``:
                path to the folder containing positive training images, formatted as a string
            ``negative_training_folder``:
                path to the folder containing negative training images, formatted as a string
            ``hard_negative_training_folder``:
                path to the folder containing hard negative training images, formatted as a string
            ``histogram_of_gradients``:
                use the distribution of gradient orientations as image features, True or False
            ``train_image_size``:
                the number of rows and columns in the positive and negative training images, formatted as a tuple of two integers
            ``step_sz``:
                number of pixel rows and columns to skip when scanning test images for target structures, formatted as a tuple of two integers
            ``misclass_penalty_C``:
                penalty for misclassification of training samples, formatted as a float
            ``kernel_type``:
                type of kernel ('linear' or 'rbf')
        :param wait_for_thread: True if PyJAMAS must wait for the thread running this operation to complete, False otherwise.
        :return: True if the classifier was successfully created, False otherwise.
        """


        continue_flag = True

        if parameters is None or parameters is False:
            dialog = QtWidgets.QDialog()
            ui = dialogs.svm.SVMDialog()
            ui.setupUi(dialog)

            dialog.exec()
            dialog.show()

            continue_flag = dialog.result() == QtWidgets.QDialog.DialogCode.Accepted
            parameters = ui.parameters()

            dialog.close()

        if continue_flag:
            self.pjs.batch_classifier.image_classifier = rimsvm.svm(parameters)
            self.launch_thread(self.pjs.batch_classifier.fit, {'stop': True}, finished_fn=self.finished_fn,
                               stop_fn=self.stop_fn, wait_for_thread=wait_for_thread)

            return True

        else:
            return False

    def cbApplyClassifier(self, firstSlice: Optional[int] = None, lastSlice: Optional[int] = None,
                          wait_for_thread: bool = False) -> bool:    # Handle IO errors.
        """
        Apply the current classifier to detect objects in the open image.

        :param firstSlice: slice number for the first slice to use (minimum is 1); a dialog will open if this parameter is None.
        :param lastSlice: slice number for the last slice to use; a dialog will open if this parameter is None.
        :param wait_for_thread: True if PyJAMAS must wait for the thread running this operation to complete, False otherwise.
        :return: True if the classifier is applied, False if the process is cancelled.
        """
        if (firstSlice is False or firstSlice is None or lastSlice is False or lastSlice is None) and self.pjs is not None:
            dialog = QtWidgets.QDialog()
            ui = dialogs.timepoints.TimePointsDialog()

            lastSlice = 1 if self.pjs.n_frames == 1 else self.pjs.slices.shape[0]
            ui.setupUi(dialog, firstslice=self.pjs.curslice + 1, lastslice=lastSlice)

            dialog.exec()
            dialog.show()
            # If the dialog was closed by pressing OK, then run the measurements.
            continue_flag = dialog.result() == QtWidgets.QDialog.DialogCode.Accepted
            firstSlice, lastSlice = ui.parameters()

            dialog.close()
        else:
            continue_flag = True

        if continue_flag:
            if firstSlice <= lastSlice:
                theslicenumbers = numpy.arange(firstSlice - 1, lastSlice, dtype=int)
            else:
                theslicenumbers = numpy.arange(lastSlice - 1, firstSlice, dtype=int)

            self.launch_thread(self.apply_classifier, {'theslices': theslicenumbers, 'progress': True, 'stop': True},
                               finished_fn=self.finished_fn,  progress_fn=self.progress_fn, stop_fn=self.stop_fn,
                               wait_for_thread=wait_for_thread)

            return True
        else:
            return False

    def apply_classifier(self, theslices: numpy.ndarray, progress_signal: ThreadSignals,
                         stop_signal: ThreadSignals) -> bool:
        # Make sure that the slices are in a 1D numpy array.
        theslices = numpy.atleast_1d(theslices)

        if stop_signal is not None:
            stop_signal.emit("Applying classifier ...")

        if type(self.pjs.batch_classifier.image_classifier) is rimrescunet.ReSCUNet:
            self.pjs.batch_classifier.predict(self.pjs.slices, theslices, progress_signal, self.pjs.polylines,
                                              self.pjs.polyline_ids)
        else:
            self.pjs.batch_classifier.predict(self.pjs.slices, theslices, progress_signal)

        # For every slice ...
        for index in theslices:
            if type(self.pjs.batch_classifier.image_classifier) in [rimlr.lr, rimsvm.svm]:
                self.add_classifier_boxes(self.pjs.batch_classifier.box_arrays[index], index, False)
            elif type(self.pjs.batch_classifier.image_classifier) is rimrescunet.ReSCUNet:
                self.add_neuralnet_polylines(self.pjs.batch_classifier.object_arrays[index],
                                             self.pjs.batch_classifier.object_ids[index], index, False)
            elif type(self.pjs.batch_classifier.image_classifier) is rimunet.UNet:
                self.add_neuralnet_polylines(self.pjs.batch_classifier.object_arrays[index], slice_index=index,
                                             paint=False)
            elif type(self.pjs.batch_classifier.image_classifier) is rimrescunet.ReSCUNet:
                self.add_neuralnet_polylines(self.pjs.batch_classifier.object_arrays[index],
                                             self.pjs.batch_classifier.object_ids[index], index, False)
            else:
                self.pjs.statusbar.showMessage(f"Wrong classifier type.")
                return False

        return True

    def add_neuralnet_polylines(self, polylines: Optional[numpy.ndarray] = None, ids: Optional[numpy.ndarray] = None,
                                slice_index: Optional[int] = None, paint: bool = True) -> bool:
        if polylines is None or polylines is False or polylines.size == 0:
            return False

        if slice_index is None or slice_index is False:
            slice_index = self.pjs.curslice

        for p, aPoly in enumerate(polylines):
            if ids is None:
                self.pjs.addPolyline(aPoly, slice_index, paint=paint)
            else:
                self.pjs.addPolyline(aPoly, slice_index, theid=ids[p], paint=paint)

        return True

    def add_classifier_boxes(self, boxes: Optional[numpy.ndarray] = None, slice_index: Optional[int] = None,
                             paint: bool = True) -> bool:  # The first slice_index should be 0.
        if boxes is None or boxes is False or boxes == []:
            return False

        if slice_index is None or slice_index is False:
            slice_index = self.pjs.curslice

        for aBox in boxes:
            # Boxes stored as [minrow, mincol, maxrow, maxcol]
            self.pjs.addPolyline([[aBox[1], aBox[0]], [aBox[3], aBox[0]], [aBox[3], aBox[2]],
                                  [aBox[1], aBox[2]], [aBox[1], aBox[0]]], slice_index, paint=paint)

        return True

    def cbNonMaxSuppression(self, parameters: Optional[dict] = None, firstSlice: Optional[int] = None,
                            lastSlice: Optional[int] = None) -> bool:
        """
        Apply non-maximum suppression to remove redundant objects from an image.

        :param parameters: dictionary containing the parameters for non-maximum suppression; a dialog will open if this parameter is None; keys are:

            ``prob_threshold``:
                lower threshold for the probability that a detected object represents an instance of the positive training set (returned by the classifier), as a float
            ``iou_threshold``:
                maximum value for the intersection-over-union ratio for the area of two detected objects, as a float; 0.0 prevents any overlaps between objects, 1.0 allows full overlap
            ``max_num_objects``:
                maximum number of objects present in the image, as an integer; objects will be discarded from lowest to highest probability of the object representing an instance of the positive training set
        :param firstSlice: slice number for the first slice to use (minimum is 1); a dialog will open if this parameter is None.
        :param lastSlice: slice number for the last slice to use; a dialog will open if this parameter is None.
        :return: True if non-maximum suppression is applied, False if the process is cancelled.
        """

        if self.pjs.batch_classifier is None or type(self.pjs.batch_classifier.image_classifier) is rimunet.UNet:

            return False

        continue_flag = True

        if parameters is None or parameters is False:
            dialog = QtWidgets.QDialog()
            ui = dialogs.nonmax_suppr.NonMaxDialog(self.pjs)
            ui.setupUi(dialog)
            dialog.exec()
            dialog.show()

            continue_flag = dialog.result() == QtWidgets.QDialog.DialogCode.Accepted

            if continue_flag:
                parameters = ui.parameters()

            dialog.close()

        if not continue_flag:
            return False

        if (firstSlice is None or firstSlice is False) and (lastSlice is None or lastSlice is False):
            dialog = QtWidgets.QDialog()
            ui = dialogs.timepoints.TimePointsDialog()
            ui.setupUi(dialog, dialogs.timepoints.TimePointsDialog.firstSlice,
                       dialogs.timepoints.TimePointsDialog.lastSlice)

            dialog.exec()
            dialog.show()

            continue_flag = dialog.result() == QtWidgets.QDialog.DialogCode.Accepted

            if continue_flag:
                firstSlice, lastSlice = ui.parameters()

            dialog.close()

        if firstSlice <= lastSlice:
            theslicenumbers = numpy.arange(firstSlice - 1, lastSlice, dtype=int)
        else:
            theslicenumbers = numpy.arange(lastSlice - 1, firstSlice, dtype=int)

        self.pjs.batch_classifier.non_max_suppression(
            parameters.get('prob_threshold', rimclassifier.DEFAULT_PROB_THRESHOLD),
            parameters.get('iou_threshold', rimclassifier.DEFAULT_IOU_THRESHOLD),
            parameters.get('max_num_objects', rimclassifier.DEFAULT_MAX_NUM_OBJECTS),
            theslicenumbers
        )

        for index in theslicenumbers:
            self.pjs.annotations.cbDeleteSliceAnn(index)
            self.pjs.classifiers.add_classifier_boxes(self.pjs.batch_classifier.box_arrays[index][self.pjs.batch_classifier.good_box_indices[index]], index, True)

        self.pjs.repaint()

        return True

    def cbSetNeuralNetStepSize(self, step_sz: tuple = None) -> bool:
        """
        Set the step size for tiling over an input image when applying a convolutional neural network.
        If step_sz >= train_image_size no tiling occurs.

        :param step_sz: the step size (int, int) for tiling in the vertical and horizontal directions.
        :return: True if option is succesfully set, False otherwise.
        """
        ok_flag = True
        print(type(self.pjs.batch_classifier.image_classifier))
        if not issubclass(type(self.pjs.batch_classifier.image_classifier), rimneuralnet):
            print("Classifier must be a neural network.")
            return False

        if step_sz is None or not step_sz:
            # Read user input for step size and then prediction image size.
            step_sz_str, ok_flag = QtWidgets.QInputDialog.getText(None, 'Step Size',
                                                                   '(row, column) step size: ',
                                                                   QtWidgets.QLineEdit.EchoMode.Normal,
                                                                   f"{self.pjs.batch_classifier.image_classifier.step_sz}")
        if ok_flag:
            try:
                step_sz = eval(step_sz_str)
            except:
                print(f"Incorrect input tuple.")
                ok_flag = False

        if ok_flag:
            self.pjs.batch_classifier.image_classifier.step_sz = step_sz
            return True
        else:
            return False
