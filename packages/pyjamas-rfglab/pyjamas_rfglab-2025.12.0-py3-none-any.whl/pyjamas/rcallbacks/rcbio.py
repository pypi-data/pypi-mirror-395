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

import gzip
import os
import pickle
import tomlkit
import re
from typing import List, Optional, Tuple

import cv2
import numpy
from PyQt6 import QtWidgets, QtGui, QtCore
import scipy.io
import skimage.morphology as skm
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC

from pyjamas.external import pascal_voc_io
import pyjamas.rimage.rimcore as rimcore
from pyjamas.pjscore import PyJAMAS
from pyjamas.pjscore import undo_modes
from pyjamas.rcallbacks.rcallback import RCallback
from pyjamas.rimage.rimml.batchclassifier import BatchClassifier
from pyjamas.rimage.rimml.batchneuralnet import BatchNeuralNet
from pyjamas.rimage.rimml.rimclassifier import rimclassifier
from pyjamas.rimage.rimutils import rimutils
from pyjamas.rimage.rimml.rimlr import lr
from pyjamas.rimage.rimml.rimsvm import svm
from pyjamas.rimage.rimml.rimunet import UNet
from pyjamas.rutils import RUtils
from pyjamas.rimage.rimml.classifier_types import classifier_types
from pyjamas.dialogs.classifiertype import ClassifierTypeDialog
from pyjamas.dialogs.timepoints import TimePointsDialog
from pyjamas.rimage.rimml.batchrecurrentneuralnet import BatchRecurrentNeuralNet
from pyjamas.rimage.rimml.rimrescunet import ReSCUNet


class RCBIO(RCallback):
    FILENAME_BASE: str = "cell_"
    FILENAME_FIDUCIAL_LENGTH: int = 5
    DEFAULT_PICKLE_PROTOCOL: int = RUtils.DEFAULT_PICKLE_PROTOCOL

    def cbLoadTimeSeries(self, filename: Optional[str] = None, channel_method: Optional[rimutils.ChannelMethod] = None,
                         index: int = -1, message: str = "Load image ...") -> bool:
        """
        Load an image from file using rimutils.read_stack.

        :param filename: file to open.
        :param channel_method: for a multi-channel sequence, determines whether to open a channel or a slice.
        :param index: index of the channel or slice to open (with origin at 0).
        :param message: string to display as the dialog box title.
        :return: True if the image was loaded with no problems, False otherwise.
        """

        # Get file name.
        if filename is None or filename is False:
            fname = QtWidgets.QFileDialog.getOpenFileName(None, message, self.pjs.cwd,
                                                          filter='All files (*)')  # fname[0] is the full filename, fname[1] is the filter used.
            filename = fname[0]
            if filename == '':
                return False

        _, ext = os.path.splitext(filename)

        # Read image.
        theimage = rimutils.read_stack(filename, channel_method, index)
        if theimage is not None:
            self.pjs.slices = theimage
        else:
            self.pjs.statusbar.showMessage("That does not look like an image.")
            return False

        # Clear annotation undo stack.
        self.pjs.undo_stack.clear()

        # Store current working directory.
        self.pjs.cwd = os.path.dirname(filename)  # Path of loaded image.
        self.pjs.filename = filename

        # Initialize image and display.
        self.pjs.initImage()

        # Clear and reset classifier object arrays so that the classifier can be applied without reloading from file
        self.pjs.batch_classifier.reset_objects(self.pjs.n_frames)

        return True

    def cbLoadArray(self, image: numpy.ndarray) -> bool:
        """
        Load a numpy matrix as an image.

        :param image: the array to open.
        :return: True if the image was loaded with no problems, False otherwise.
        """
        if image is False or image is None:
            return False

        self.pjs.slices = image

        self.pjs.filename = 'animage'

        self.pjs.initImage()

        # Clear and reset classifier object arrays so that the classifier can be applied without reloading from file
        self.pjs.batch_classifier.reset_objects(self.pjs.n_frames)

    def cbLoadAnnotations(self, filenames: Optional[List[str]] = None, image_file: Optional[str] = None,
                          replace: bool = True, message: str = "Load annotations ...") -> bool:  # Handle IO errors
        """
        Loads PyJAMAS annotation files.

        :param filenames: paths to the files containing the annotations.
        :param image_file: path to an image to be loaded with the annotation file. None if no image is to be loaded. '' to create an empty image.
        :param replace: True if loaded annotations should replace existing ones, False if this is an additive load.
        :param message: string to display as the dialog box title.
        :return: True if the annotation file was loaded, False otherwise.
        """

        # Get file name.
        if filenames is None or filenames is False or filenames == []: # When the menu option is clicked on, for some reason that I do not understand, the function is called with filename = False, which causes a bunch of problems.
            dialog = QtWidgets.QFileDialog(None, message)
            dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)
            dialog.setDirectory(self.pjs.cwd)
            dialog.setNameFilter('PyJAMAS data (*' + PyJAMAS.data_extension + ')')
            dialog.exec()

            filenames = dialog.selectedFiles()
            if filenames is None or filenames == [] or filenames[0] == '':
                return False

        filenames.sort(key=RUtils.natural_sort)

        if image_file is not False and image_file is not None and image_file != '':
            self.pjs.io.cbLoadTimeSeries(image_file)

        # # Open file names and read annotations.
        fh = None
        maxid: int = 0

        if not replace:
            [allfiducials, allqpolygonfs, allpolyline_ids] = self.pjs.copy_annotations()
            allpolylines = RUtils.qpolygonfs2coordinatelists(allqpolygonfs)

            maxid = max([0] + [max(slice_ids) for slice_ids in allpolyline_ids if
                               slice_ids])  # the [0] ensures no error if there are no annotations.

        else:
            allfiducials = [[] for _ in range(self.pjs.n_frames)]
            allpolylines = [[] for _ in range(self.pjs.n_frames)]
            allpolyline_ids = [[] for _ in range(self.pjs.n_frames)]

        curfiducials: List[List[int]] = None
        curpolylines: List[List[int]] = None
        curpolyline_ids: List[List[int]] = None

        for fname in filenames:
            try:
                fh = gzip.open(fname, "rb")
                curfiducials = pickle.load(fh)
                curpolylines = pickle.load(fh)
                curpolyline_ids = pickle.load(fh)

            except (IOError, OSError) as ex:
                if fh is not None:
                    fh.close()
                print(ex)
                return False

            except EOFError as ex:
                if not curfiducials:
                    curfiducials = [[] for _ in range(self.pjs.n_frames)]
                    curpolylines = [[] for _ in range(self.pjs.n_frames)]
                    curpolyline_ids = [[] for _ in range(self.pjs.n_frames)]

                elif not curpolylines:
                    curpolylines = [[] for _ in range(self.pjs.n_frames)]
                    curpolyline_ids = [[] for _ in range(self.pjs.n_frames)]

                # this takes care of old annotation files with no polyline_ids.
                elif not curpolyline_ids:
                    curpolyline_ids = [[] for _ in range(len(curpolylines))]

                    for slice_index, slice_polylines in enumerate(curpolylines):
                        for thepolyline_index, thepolyline in enumerate(slice_polylines):
                            if thepolyline:
                                curpolyline_ids[slice_index].append(thepolyline_index + 1)

            for i in range(min(len(allfiducials), len(curfiducials))):
                allfiducials[i].extend(curfiducials[i])

            for i in range(min(len(allpolylines), len(curpolylines))):
                allpolylines[i].extend([apolylinelist for apolylinelist in curpolylines[i]])
                allpolyline_ids[i].extend((numpy.asarray(curpolyline_ids[i]) + maxid).tolist())

            max_id_list = [max(slice_ids) for slice_ids in curpolyline_ids if slice_ids]

            # this takes care of the scenario with no polylines defined on any slice
            if max_id_list:
                themaxid = max(max_id_list)
                maxid = max(maxid, themaxid)

        if image_file == '':  # Create a blank image.
            # Find maxx, maxy, and maxz, and create a numpy.ndarray with those dimensions + 1.
            maxz = len(allfiducials)
            maxx = 0
            maxy = 0

            # Fiducials and polylines are stored as (x, y) coordinates.
            # numpy.ndarrays are created with (slices, rows, cols).
            for slice_fiducials in allfiducials:
                for afiducial in slice_fiducials:
                    maxx = max(maxx, afiducial[0])
                    maxy = max(maxy, afiducial[1])

            for slice_polylines in allpolylines:
                for apolyline in slice_polylines:
                    for afiducial in apolyline:
                        maxx = max(maxx, afiducial[0])
                        maxy = max(maxy, afiducial[1])

            virtual_image = numpy.zeros((maxz, int(maxy + 1), int(maxx + 1)), dtype=int)
            self.pjs.io.cbLoadArray(virtual_image)

        # elif image_file is not False and image_file is not None:
        #    self.pjs.io.cbLoadTimeSeries(image_file)

        self.pjs.annotations.cbDeleteAllAnn()

        self.pjs.undo_stack.push(
            {'changetype': undo_modes.MULTI, 'frame': (0, self.pjs.n_frames), 'index': (True, True),
             'details': self.pjs.copy_annotations()})

        for slice_index, slice_fiducials in enumerate(allfiducials):
            for afiducial in slice_fiducials:
                self.pjs.addFiducial(int(afiducial[0]), int(afiducial[1]), slice_index, paint=False)

        for i, theframepolylines in enumerate(allpolylines):
            if i < self.pjs.n_frames:  # this allows opening annotation files with extra time poinnts.
                for j, thepolyline in enumerate(theframepolylines):
                    if thepolyline != []:
                        if self.pjs.close_all_polylines and thepolyline[0] != thepolyline[-1]:
                            thepolyline.append(thepolyline[0])
                        self.pjs.addPolyline(thepolyline, i, paint=False)
                        # self.pjs.polylines[i].append(thepolyline)
                        self.pjs.polyline_ids[i][-1] = allpolyline_ids[i][j]

        # self.pjs.image.cbZoom(0)
        self.pjs.repaint()

        # Modify current path.
        self.pjs.cwd = os.path.dirname(filenames[0])

        return True

    def cbSaveTimeSeries(self, filename: Optional[str] = None, message: str = "Save time series ...") -> bool:
        '''
        Save the current image (pjs.slices) as a grayscale, multi-page TIFF.

        :param filename: path to the destination file.
        :param message: string to display as the dialog box title.
        :return: True if the image was saved with no problems, False otherwise.
        '''

        # Get file name.
        if filename == '' or filename is False or filename is None:
            fname: tuple = QtWidgets.QFileDialog.getSaveFileName(None, message, self.pjs.cwd,
                                                          filter='TIFF files (*.tif *.tiff)')  # fname[0] is the full filename, fname[1] is the filter used.
            filename = fname[0]
        if filename == '':
            return False

        # Save image.
        rimutils.write_stack(filename, self.pjs.slices)
        self.pjs.statusbar.showMessage('Image saved: ' + filename)

        self.pjs.cwd = os.path.dirname(filename)  # Path of loaded image.
        self.pjs.filename = filename

        return True

    def cbImportMasks(self, filename: Optional[str] = None, message: str = "Load mask file ...") -> bool:
        """
        Load a mask image from file using rimutils.read_stack and convert the mask regions to polyline annotations.

        :param filename: file to open.
        :param message: string to display as the dialog box title.
        :return: True if the mask image was loaded with no problems, False otherwise.
        """

        # Get file name.
        if filename is None or filename is False:
            fname = QtWidgets.QFileDialog.getOpenFileName(None, message, self.pjs.cwd,
                                                          filter='All files (*)')  # fname[0] is the full filename, fname[1] is the filter used.
            filename = fname[0]
            if filename == '':
                return False

        _, ext = os.path.splitext(filename)

        # Read image.
        themask = rimutils.read_stack(filename)
        if themask is None:
            self.pjs.statusbar.showMessage("That does not look like an image.")
            return False

        # Store current working directory.
        self.pjs.cwd = os.path.dirname(filename)  # Path of loaded image.

        return self.add_masks_as_polylines(themask)

    def add_masks_as_polylines(self, mask: numpy.ndarray):
        if len(numpy.unique(mask)) == 2:
            is_binary = True
        elif len(numpy.unique(mask)) > 2:
            is_binary = False
        else:
            self.pjs.statusbar.showMessage("Could not interpret mask values as polylines.")
            return False

        if mask.ndim == 2:
            mask = mask[None, ...]

        for t, this_slice in enumerate(mask):
            if is_binary:
                labelled_slice = skm.label(this_slice)
            else:
                labelled_slice = this_slice
            for this_id in numpy.unique(labelled_slice[labelled_slice > 0]):  # add one polyline per mask region
                this_region = labelled_slice == this_id
                contour_array = numpy.asarray(rimutils.extract_contours(this_region), dtype=object)
                if len(contour_array) > 1:
                    self.pjs.statusbar.showMessage("Some polylines may be missing due to holes in the mask regions.")
                    continue
                else:
                    self.pjs.addPolyline(contour_array[0], t, theid=this_id)  # add the polyline to PyJAMAS
        return True

    def cbExportROIAndMasks(self, polyline: Optional[numpy.ndarray] = None, margin_size: int = 0) -> bool:
        """
        Save the image within an ROI, plus a second image containing a binary mask of any polylines within the ROI.

        :param polyline: ndarray with two columns containing the x, y coordinates of the ROI; if using a tracked polyline, ndarray with one element corresponding to the polyline index; if not provided, the function will prompt the user to select a polyline.
        :param margin_size: margin size in pixels for cropping around the polyline
        :return: True if the image is cropped, False otherwise.

        """
        if (polyline is None) | (numpy.array_equal(polyline, [])):
            thepolylines = self.pjs.polylines[self.pjs.curslice]

            if thepolylines == [] or thepolylines[0] == []:
                return False

            # prompt user to select polyline
            self.pjs.statusbar.showMessage('Select polygons.')
            self.pjs.annotation_mode = PyJAMAS.select_polyline_exportroi

            return True

        minx, miny, maxx, maxy = self.get_coordinate_bounds(coordinates=polyline, margin_size=margin_size)

        # Where to save?
        filenameext = self.generate_ROI_filename((minx, maxx), (miny, maxy), (self.pjs.curslice, self.pjs.curslice),
                                                 PyJAMAS.image_extensions[0], relative=True)
        filename, _ = os.path.splitext(filenameext)
        path_to_image: str = os.path.join(self.pjs.cwd, filename, "image", filenameext)
        path_to_mask: str = os.path.join(self.pjs.cwd, filename, "mask", filenameext)
        cwd = self.pjs.cwd

        # Save image.
        self.pjs.io.cbSaveROI(path_to_image, (minx, maxx), (miny, maxy), (self.pjs.curslice, self.pjs.curslice))

        # Export mask.
        self.pjs.io.cbExportCurrentAnnotationsBinaryImage(path_to_mask, numpy.array([[minx, miny], [maxx, maxy]]),
                                                          firstSlice=self.pjs.curslice + 1, lastSlice=self.pjs.curslice + 1)

        # Important, as cbSaveROI and cbExportCurrentAnnotationsBinaryImage may affect the cwd.
        self.pjs.cwd = cwd

        return True

    def cbSaveROI(self, filename: Optional[str] = None, x_range: Tuple[int, int] = False,
                  y_range: Tuple[int, int] = False, z_range: Tuple[int, int] = False,
                  message: str = "Save time series ...") -> bool:
        """
        Save a subregion of the image currently open (pjs.slices).

        :param filename: '' for automated naming based on coordinates. If None, a dialog will open. Make sure to provide an extension (defaults to PyJAMAS.image_extensions[0]).
        :param x_range: tuple containing the min and max X values to save. If False, take the coordinates of the first polyline defined on the image. If no polygons, use the entire image width.
        :param y_range: tuple containing the min and max Y values to save. If False, take the coordinates of the first polyline defined on the image. If no polygons, use the entire image height.
        :param z_range: tuple containing the min and max Z values to save. If False, use just the current Z.
        :param message: string to display as the dialog box title.
        :return: True if the image was properly saved, False otherwise.
        """

        # Check X, Y, and Z parameters or assign default values.
        if z_range is False:
            z_range = tuple([self.pjs.curslice, self.pjs.curslice])

        if x_range is False:
            thepolylines = self.pjs.polylines[self.pjs.curslice]
            if thepolylines == [] or thepolylines[0] == []:
                return False

            thepolyline = self.pjs.polylines[self.pjs.curslice][0].boundingRect()
            x_range = tuple([int(thepolyline.x()), int(thepolyline.x()+thepolyline.width())])
        if y_range is False and thepolylines != [] and thepolylines[0] != []:
            thepolylines = self.pjs.polylines[self.pjs.curslice]
            if thepolylines == [] or thepolylines[0] == []:
                return False

            thepolyline = self.pjs.polylines[self.pjs.curslice][0].boundingRect()
            y_range = tuple([int(thepolyline.y()), int(thepolyline.y() + thepolyline.height())])
        # Get file name.
        if filename is None or filename is False:
            fname: tuple = QtWidgets.QFileDialog.getSaveFileName(None, message, self.pjs.cwd,
                                                          filter='TIFF files (*.tif *.tiff)')  # fname[0] is the full filename, fname[1] is the filter used.
            filename = fname[0]
            if filename == '':
                return False

        elif filename == '':
            filename = self.generate_ROI_filename(x_range, y_range, z_range, PyJAMAS.image_extensions[0])
        # Make sure the file name has an extension (this is important to determine the image format in rimutils.write_stack.
        _, fext = os.path.splitext(filename)
        if fext == '':
            filename = RUtils.set_extension(filename, PyJAMAS.image_extensions[0])

        # Save image.
        rimutils.write_stack(filename,
                             self.pjs.slices[z_range[0]:z_range[1]+1, y_range[0]:y_range[1]+1, x_range[0]:x_range[1]+1])
        self.pjs.statusbar.showMessage('Image saved: ' + filename)

        self.pjs.cwd = os.path.dirname(filename)  # Path of loaded image.

        return True

    def cbSaveDisplay(self, filename: Optional[str] = None, message: str = "Save display ...") -> bool:
        """
        Save the PyJAMAS display, including annotations, as a colour image.

        :param filename: '' for automated naming based on the current image name (pjs.filename). If not provided, a dialog will open.
        :param message: string to display as the dialog box title.
        :return: True if the display was properly saved, False otherwise.
        """

        # Get file name.
        if filename is False or filename is None:
            fname: tuple = QtWidgets.QFileDialog.getSaveFileName(None, message, self.pjs.cwd,
                                                          filter='TIFF files (*.tif *.tiff)')  # fname[0] is the full filename, fname[1] is the filter used.
            filename = fname[0]
            if filename == '':
                return False

        elif filename == '':
            _, fname = os.path.split(self.pjs.filename)
            filename = os.path.join(self.pjs.cwd, fname)

        # Save image.
        self.capture_display(filename)

        self.pjs.statusbar.showMessage('Display saved: ' + filename)

        self.pjs.cwd = os.path.dirname(filename)  # Path of loaded image.

        return True

    def cbExportMovie(self, filename: Optional[str] = None, message: str = "Export movie with annotations ...") -> bool:
        """
        Save an avi file displaying the movie currently open and its annotations.
        The number of frames per second is determined by pjs.fps.

        :param filename: '' for automated naming based on the current image name (pjs.filename). If not provided, a dialog will open.
        :param message: string to display as the dialog box title.
        :return: True if the display was properly saved, False otherwise.
        """

        # Get file name.
        if filename is False or filename is None:
            fname: tuple = QtWidgets.QFileDialog.getSaveFileName(None, message, self.pjs.cwd,
                                                          filter='AVI (*.avi)')  # fname[0] is the full filename, fname[1] is the filter used.
            filename = fname[0]
            if filename == '':
                return False

        elif filename == '':
            _, fname = os.path.split(self.pjs.filename)
            filename = os.path.join(self.pjs.cwd, fname)

        # Save image.
        self.export_movie(filename)

        self.pjs.statusbar.showMessage('Movie exported: ' + filename)

        self.pjs.cwd = os.path.dirname(filename)  # Path of loaded image.

        return True

    def capture_display(self, filename: Optional[str] = None) -> QtGui.QImage:

        #pix_map: QtGui.QPixmap = self.pjs.gView.grab(self.pjs.gView.sceneRect().toRect())
        #pix_map: QtGui.QPixmap = self.pjs.gView.grab(QRect(0, 0, int(self.pjs.width * self.pjs.zoom_factors[self.pjs.zoom_index]), int(self.pjs.height * self.pjs.zoom_factors[self.pjs.zoom_index])))
        #pix_map: QtGui.QPixmap = self.pjs.gView.grab()
        #pix_map = pix_map.scaled(pix_map.width(), pix_map.height())

        self.pjs.gScene.clearSelection()
        self.pjs.gScene.setSceneRect(self.pjs.gScene.itemsBoundingRect())
        image: QtGui.QImage = QtGui.QImage(self.pjs.gScene.sceneRect().size().toSize(), QtGui.QImage.Format.Format_ARGB32)
        image.fill(QtCore.Qt.GlobalColor.transparent)
        painter: QtGui.QPainter = QtGui.QPainter(image)
        self.pjs.gScene.render(painter)

        if filename and filename is not None and filename != '':
            image.save(filename)

        return image

    def export_movie(self, filename: Optional[str] = None) -> list:
        curslice = self.pjs.curslice

        qimage_list = []

        for i in range(self.pjs.n_frames):
            self.pjs.image.cbGoTo(i)
            qimage_list.append(self.capture_display())


        self.pjs.image.cbGoTo(curslice)

        if filename and filename is not None and filename != '':
            fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')

            out = cv2.VideoWriter(filename, fourcc, self.pjs.fps, (self.pjs.width, self.pjs.height), True)

            for i in range(self.pjs.n_frames):
                a = rimutils.qimage2ndarray(qimage_list[i])

                # In some cases, particularly colour images with annotations, qimage2ndarray adds 2-3 rows of black
                # pixels at the top and left sides of the image. Here we remove them.
                h0: int = a.shape[0]-self.pjs.height
                w0: int = a.shape[1]-self.pjs.width
                gray_3c = cv2.merge([a[h0:, w0:, 0], a[h0:, w0:,  1], a[h0:, w0:, 2]])
                out.write(gray_3c.astype('uint8'))

            out.release()

        return qimage_list

    def cbSaveAnnotations(self, filename: Optional[str] = None, polylines: Optional[List] = None,
                          polyline_ids: Optional[List] = None,
                          fiducials: Optional[List] = None, pickle_protocol: int = DEFAULT_PICKLE_PROTOCOL,
                          message: str = "Save annotations ...") -> bool:  # Handle IO errors.
        """
        Save annotations on the current image in pjs format (pickled). These annotations CAN BE opened by PyJAMAS.

        :param filename: '' for automated naming based on the current image name (pjs.filename). If not provided, a dialog will open.
        :param polylines: list of polylines to save (one slice per time point, one QtGui.QPolygonF per polyline).
        :param polyline_ids: list of polylines ids to save (one slice per time point, one integer per polyline).
        :param fiducials: list of fiducials to save (one slice per time point, one row with [x, y] coordinates per fiducial (int)).
        :param pickle_protocol: integer indicating the pickle protocol to use for saving (defaults to RCBIO.DEFAULT_PICKLE_PROTOCOL).
        :param message: string to display as the dialog box title.
        :return: True if the annotations were saved, False otherwise.
        """

        # Get file name.
        if filename is None or filename is False or filename == '': # When the menu option is clicked on, for some reason that I do not understand, the function is called with filename = False, which causes a bunch of problems.
            fname = QtWidgets.QFileDialog.getSaveFileName(None, message, self.pjs.cwd,
                                                          filter='PyJAMAS data (*' + PyJAMAS.data_extension + ')')  # fname[0] is the full filename, fname[1] is the filter used.

            # If cancel ...
            filename = fname[0]
            if filename == '':
                return False

        elif filename == '':
            _, fname = os.path.split(self.pjs.filename)
            filename = os.path.join(self.pjs.cwd, fname)

        self.pjs.cwd = os.path.dirname(filename)

        if filename[-4:] != PyJAMAS.data_extension:
            filename = RUtils.set_extension(filename, PyJAMAS.data_extension)

        if not polylines:
            polylines = self.pjs.polylines

        if not polyline_ids:
            polyline_ids = self.pjs.polyline_ids

        if not fiducials:
            fiducials = self.pjs.fiducials

        # Prepare polygons to be stored: pickle does not support QPolygonF, so we convert the polygons to a list.
        # We store the polygons as QPolygonF because QGraphicsScene does have an addPolygon method that takes a
        # QPolygonF as the parameter.
        polyline_list = RUtils.qpolygonfs2coordinatelists(polylines)

        # Open file for writing.
        fh = None

        with gzip.open(filename, "wb") as fh:
            pickle.dump(fiducials, fh, protocol=pickle_protocol)
            pickle.dump(polyline_list, fh, protocol=pickle_protocol)
            pickle.dump(polyline_ids, fh, protocol=pickle_protocol)

        self.pjs.cwd = os.path.dirname(filename)

        self.pjs.statusbar.showMessage(f"Saved {filename}.")

        return True

    def cbExportCurrentAnnotationsBinaryImage(self, filename: Optional[str] = None,
                                              polyline: Optional[numpy.ndarray] = None,
                                              firstSlice: Optional[int] = None, lastSlice: Optional[int] = None,
                                              message: str = "Save annotations ...") -> bool:
        """
        Save current slice annotations as a binary image displaying one mask per object.

        :param filename: '' for automated naming based on the current image name (pjs.filename). If not provided, a dialog will open.
        :param polyline: ndarray with two columns containing the x, y coordinates of the ROI; if None or empty array, use the entire image as ROI.
        :param firstSlice: slice number for the first slice to use (minimum is 1); a dialog will open if this parameter is None.
        :param lastSlice: slice number for the last slice to use; a dialog will open if this parameter is None.
        :param message: string to display as the dialog box title.
        :return:
        """
        # Get file name.
        if filename is None or filename is False:  # When the menu option is clicked on, for some reason that I do not understand, the function is called with filename = False, which causes a bunch of problems.
            fname = QtWidgets.QFileDialog.getSaveFileName(None, message,
                                                          self.pjs.cwd,
                                                          filter='image file (*' + PyJAMAS.image_extensions[0] + ')')  # fname[0] is the full filename, fname[1] is the filter used.

            # If cancel ...
            filename = fname[0]
            if filename == '':
                return False

        elif filename == '':
            _, fname = os.path.split(self.pjs.filename)
            filename = os.path.join(self.pjs.cwd, fname)

        self.pjs.cwd = os.path.dirname(filename)

        if filename[-4:] not in PyJAMAS.image_extensions:
            filename = RUtils.set_extension(filename, PyJAMAS.image_extensions[0])

        # Get the slices to use.
        if (firstSlice is False or firstSlice is None or lastSlice is False or lastSlice is None) and self.pjs is not None:
            dialog = QtWidgets.QDialog()
            ui = TimePointsDialog()

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

        if (polyline is None) | (numpy.array_equal(polyline, [])) | (polyline is False):
            minx = 0
            miny = 0
            maxx = self.pjs.width - 1
            maxy = self.pjs.height - 1
        else:
            minx, miny, maxx, maxy = self.get_coordinate_bounds(coordinates=polyline)

        # Transform annotations to export only the ones within the ROI (but not the ROI itself!).
        transform = QtGui.QTransform()
        transform.translate(-minx, -miny)

        # Transform using a one pixel less wide and less tall size such that the polyline that determines the ROI
        # (if there was one) is not included in the regions within the image.
        _, new_polylines, _ = self.transform_annotations(transform, (maxx - minx - 1, maxy - miny - 1))

        if continue_flag:
            if firstSlice <= lastSlice:
                thepolylines = new_polylines[firstSlice - 1:lastSlice]
            else:
                thepolylines = new_polylines[lastSlice:firstSlice]
        else:
            return False

        mask_image = numpy.zeros((len(thepolylines), maxy - miny + 1, maxx - minx + 1), dtype=bool)
        for t, these_polylines in enumerate(thepolylines):
            mask_image[t] = rimutils.mask_from_polylines((maxy - miny + 1, maxx - minx + 1), these_polylines, self.pjs.brush_size)
        if firstSlice == lastSlice:  # Reduce dimensions if the mask should only be one slice
            mask_image = mask_image[0]
        rimutils.write_stack(filename, mask_image)

        self.pjs.statusbar.showMessage(f"Saved {filename}.")

        return True

    def cbSaveClassifier(self, filename: Optional[str] = None,
                         theclassifier: Optional[rimclassifier] = None,
                         message: str = "Save classifier ...") -> bool:  # Handle IO errors.
        """
        Save current classifier (pickled).

        :param filename: '' for automated naming based on the current image name (pjs.filename). If not provided, a dialog will open.
        :param theclassifier: True if the classifier saved, False otherwise.
        :param message: string to display as the dialog box title.
        :return: True if the classifier was saved, False otherwise.
        """

        if theclassifier is None or theclassifier is False:
            if self.pjs.batch_classifier.image_classifier is None:
                return False
            else:
                theclassifier = self.pjs.batch_classifier.image_classifier

        # Get file name.
        if filename is None or filename is False:  # When the menu option is clicked on, for some reason that I do not understand, the function is called with filename = False, which causes a bunch of problems.
            fname = QtWidgets.QFileDialog.getSaveFileName(None, message, self.pjs.cwd,
                                                          filter='PyJAMAS classifier (*' + PyJAMAS.classifier_extension + ')')  # fname[0] is the full filename, fname[1] is the filter used.

            # If cancel ...
            filename = fname[0]
            if filename == '':
                return False

        elif filename == '':
            _, fname = os.path.split(self.pjs.filename)
            filename = os.path.join(self.pjs.cwd, fname)

        if filename[-4:] != PyJAMAS.classifier_extension:
            filename = RUtils.set_extension(filename, PyJAMAS.classifier_extension)

        self.pjs.cwd = os.path.dirname(filename)

        theclassifier.save(filename)

        self.pjs.statusbar.showMessage(f'Saved classifier {filename}.')

        return True

    def cbLoadClassifier(self, filename: Optional[str] = None,
                         message: str = "Load classifier ...") -> bool:  # Handle IO errors
        """
        Load a classifier from disk.

        :param filename: name of the file containing a pickled classifier to be loaded.
        :param message: string to display as the dialog box title.
        :return: True if the classifier was loaded, False otherwise.
        """

        filename = self.load_classifier(filename, message)

        if filename is None:
            return False

        # Modify current path.
        self.pjs.cwd = os.path.dirname(filename)

        self.pjs.statusbar.showMessage(f"Classifier {filename} loaded.")

        return True

    def load_classifier(self, filename: Optional[str] = None, message: str = "Load classifier ...") -> str:
        # Get file name.
        if filename is None or filename is False:
            fname = QtWidgets.QFileDialog.getOpenFileName(None, message, self.pjs.cwd,
                                                          filter='PyJAMAS classifier (*' + PyJAMAS.classifier_extension + ')')  # fname[0] is the full filename, fname[1] is the filter used.
            filename = fname[0]
            if filename == '':
                return None

        # Open file name and read classifier.
        fh = None
        theparameters: dict = None

        try:
            fh = gzip.open(filename, "rb")
            theparameters = pickle.load(fh)
            fh.close()

        except (IOError, OSError) as ex:
            if fh is not None:
                fh.close()

            print(ex)
            return None

        if theparameters is None:
            return None

        theclassifier = theparameters.get('classifier', None)
        classifier_type = theparameters.get('classifier_type', None)

        classifier_identities = set(thetype.value for thetype in classifier_types)
        loading = True
        while loading:  # Ask for classifier type until successfully built or cancelled
            try:
                if classifier_type == classifier_types.SUPPORT_VECTOR_MACHINE.value and type(theclassifier) == SVC:
                    self.pjs.batch_classifier = BatchClassifier(self.pjs.n_frames, svm(theparameters))
                elif classifier_type == classifier_types.LOGISTIC_REGRESSION.value and type(theclassifier) == LogisticRegression:
                    self.pjs.batch_classifier = BatchClassifier(self.pjs.n_frames, lr(theparameters))
                elif classifier_type == classifier_types.UNET.value and type(theclassifier) == list:
                    self.pjs.batch_classifier = BatchNeuralNet(self.pjs.n_frames, UNet(theparameters))
                elif classifier_type == classifier_types.RESCUNET.value and type(theclassifier) == list:
                    concatenation_level = theparameters.get('concatenation_level', None)
                    if concatenation_level is None:  # compatibility with older classifiers without concatenation_level
                        build_success = False  # Iterate over possible values to find proper construction
                        concatenation_level = 0
                        while not build_success and concatenation_level <= 4:
                            try:
                                theparameters['concatenation_level'] = concatenation_level
                                self.pjs.batch_classifier = BatchRecurrentNeuralNet(self.pjs.n_frames, ReSCUNet(theparameters))
                                build_success = True
                            except:
                                concatenation_level += 1
                        if not build_success:
                            raise TypeError("Wrong classifier type.")
                    else:
                        self.pjs.batch_classifier = BatchRecurrentNeuralNet(self.pjs.n_frames, ReSCUNet(theparameters))
                else:
                    raise TypeError("Wrong classifier type.")
                loading = False  # Passed through if/else's without error so the classifier was loaded, exit the loop

            except:  # Classifier type non-existent, unknown, or incorrect
                dialog = QtWidgets.QDialog()
                ui = ClassifierTypeDialog()
                ui.setupUi(dialog, classifier_type=classifier_types.UNKNOWN.value)
                dialog.exec()
                dialog.show()
                continue_flag = dialog.result() == QtWidgets.QDialog.DialogCode.Accepted
                classifier_type = ui.parameters()
                dialog.close()
                if not continue_flag:
                    self.pjs.statusbar.showMessage("Unknown classifier type.")
                    loading = False  # User cancelled loading, exit loop and return None as filename
                    filename = None

        return filename

    def cbExportPolylineAnnotations(self, folder_name: Optional[str] = None) -> bool:
        """
        Set PyJAMAS' annotation mode such that when a fiducial is clicked on, its containing polyline -over time- is stored in a new PyJAMAS annotation file (pickled).

        :param folder_name: folder where annotation files will be stored.
        :return: True if the annotation mode was changed, False otherwise.
        """
        if folder_name is not None and folder_name is not False:  # When the menu option is clicked on, for some reason that I do not understand, the function is called with filename = False, which causes a bunch of problems.
            self.pjs.cwd = folder_name

        self.pjs.annotation_mode = PyJAMAS.export_fiducial_polyline
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.CursorShape.CrossCursor)

        return True

    def export_polyline_annotations(self, x: int, y: int) -> bool:
        # Make sure the fiducial is in the list.
        assert [x, y] in self.pjs.fiducials[self.pjs.curslice], "Fiducial not found!"

        # Identify the fiducial.
        fiducial_index: int = self.pjs.fiducials[self.pjs.curslice].index([x, y])

        # List of polygons and fiducials for new annotation file.
        fiducial_list: list = [[] for _ in range(self.pjs.n_frames)]
        polyline_list: list = [[] for _ in range(self.pjs.n_frames)]
        polyline_id_list: list = [[] for _ in range(self.pjs.n_frames)]

        # If no polyline encloses the fiducial, return False.
        found_one_polyline: bool = False

        # In every image:
        for slice in range(self.pjs.n_frames):
            # If there are enough fiducials and any polylines.
            if self.pjs.fiducials[slice] and fiducial_index < len(self.pjs.fiducials[slice]) and self.pjs.polylines[slice]:
                # Store the fiducial.
                fiducial_list[slice].append(self.pjs.fiducials[slice][fiducial_index])

                # Find the first polygon that contains the fiducial and store it as well.
                thefiducial: list = self.pjs.fiducials[slice][fiducial_index]
                thepolylines: list = [one_polyline for one_polyline in self.pjs.polylines[slice]]

                for index_polyline, one_polyline in enumerate(thepolylines):
                    if one_polyline.containsPoint(QtCore.QPointF(thefiducial[0], thefiducial[1]), QtCore.Qt.FillRule.OddEvenFill):
                        polyline_list[slice].append(self.pjs.polylines[slice][index_polyline])
                        polyline_id_list[slice].append(self.pjs.polyline_ids[slice][index_polyline])
                        found_one_polyline = True
                        break

        # Save new annotation file.
        if found_one_polyline:
            filename: str = os.path.join(self.pjs.cwd, self.FILENAME_BASE + str(fiducial_index+1).zfill(self.FILENAME_FIDUCIAL_LENGTH))
            self.pjs.io.cbSaveAnnotations(filename, polyline_list, polyline_id_list, fiducial_list)

        return True

    def export_all_polyline_annotations(self, slice_index: int = 0) -> bool:
        if slice_index < 0 or slice_index >= self.pjs.slices.shape[0]:
            return False

        for afidu in self.pjs.fiducials[slice_index]:
            self.export_polyline_annotations(afidu[0], afidu[1])

        return True

    def cbExportAllPolylineAnnotations(self, folder_name: Optional[str] = None,
                                       message: str = "Export files to folder ...") -> bool:
        """
        Exports each polyline in the image containing a fiducial into a single PyJAMAS annotation file - including polylines containing the same fiducial in other slices.

        :param folder_name: folder where annotation files will be stored.
        :param message: string to display as the dialog box title.
        :return: True if the export process completed normally, False otherwise.
        """
        if folder_name == '' or folder_name is False or folder_name is None: # When the menu option is clicked on, for some reason that I do not understand, the function is called with filename = False, which causes a bunch of problems.
            folder_name = QtWidgets.QFileDialog.getExistingDirectory(None, message, self.pjs.cwd)

        # If cancel ...
        if folder_name == '':
            return False

        if os.path.exists(folder_name):
            self.pjs.cwd = os.path.abspath(folder_name)
            self.export_all_polyline_annotations(self.pjs.curslice)

            self.pjs.statusbar.showMessage(f"Done!")

            return True

        else:
            return False

    def cbImportSIESTAAnnotations(self, filenames: Optional[List[str]] = None,
                                  image_file: Optional[str] = None, replace: bool = True,
                                  message: str = "Load annotations ...") -> bool:
        """
        Read Matlab-based annotations into PyJAMAS..

        :param filenames: path to the files that will contain the Matlab-based annotations.
        :param image_file: path to an image that can be loaded with the Matlab-based annotations. '' to use an empty image.
        :param replace: True if loaded annotations should replace existing ones, False if this is an additive load.
        :param message: string to display as the dialog box title.
        :return: True if the annotation file was properly loaded, False otherwise.
        """
        # Get file name.
        if filenames is None or filenames is False or filenames == []: # When the menu option is clicked on, for some reason that I do not understand, the function is called with filename = False, which causes a bunch of problems.
            dialog = QtWidgets.QFileDialog(None, message)
            dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFiles)
            dialog.setDirectory(self.pjs.cwd)
            dialog.setNameFilter('SIESTA annotations (*.mat)')
            dialog.exec()

            filenames = dialog.selectedFiles()
            if filenames is None or filenames == [] or filenames[0] == '':
                return False

        filenames.sort(key=RUtils.natural_sort)

        # # Open file names and read annotations.
        maxid: int = 0

        if not replace:
            [allfiducials, allqpolygonfs, allpolyline_ids] = self.pjs.copy_annotations()
            allpolylines = RUtils.qpolygonfs2coordinatelists(allqpolygonfs)

            maxid = max([0] + [max(slice_ids) for slice_ids in allpolyline_ids if
                               slice_ids])  # the [0] ensures no error if there are no annotations.

        else:
            allfiducials = [[] for _ in range(self.pjs.n_frames)]
            allpolylines = [[] for _ in range(self.pjs.n_frames)]
            allpolyline_ids = [[] for _ in range(self.pjs.n_frames)]

        curfiducials: List[List[int]] = None
        curpolylines: List[List[int]] = None
        curpolyline_ids: List[List[int]] = None

        for fname in filenames:
            try:
                matlabVars = scipy.io.loadmat(fname, struct_as_record=False)
            except (IOError, OSError) as ex:
                print(ex)
                return False

            ud = matlabVars['ud'][0][0]

            if ud.rfiducials.size > 0:
                curfiducials = numpy.asarray(numpy.transpose(ud.rfiducials, [2, 0, 1]), dtype=int)
            else:
                curfiducials = [[] for _ in range(self.pjs.n_frames)]

            if ud.rpolygons.size > 0:
                curpolylines = numpy.transpose(ud.rpolygons, [2, 0, 1])
            else:
                curpolylines = [[] for _ in range(self.pjs.n_frames)]

            curpolyline_ids = [[] for _ in range(self.pjs.n_frames)]

            for slice_index, slice_polylines in enumerate(curpolylines):
                for thepolyline_index, thepolyline in enumerate(slice_polylines):
                    if thepolyline[0].size > 0:
                        curpolyline_ids[slice_index].append(thepolyline_index + 1)

            for i in range(len(allfiducials)):
                allfiducials[i].extend(curfiducials[i])

            for i in range(len(allpolylines)):
                allpolylines[i].extend([apolylinearray[0].tolist() for apolylinearray in curpolylines[i]])
                allpolyline_ids[i].extend((numpy.asarray(curpolyline_ids[i]) + maxid).tolist())

            themaxid = max([max(slice_ids) for slice_ids in curpolyline_ids if slice_ids])
            maxid = max(maxid, themaxid)

        if image_file == '':  # Create a blank image.
            # Find maxx, maxy, and maxz, and create a numpy.ndarray with those dimensions + 1.
            maxz = len(allfiducials)
            maxx = 0
            maxy = 0

            # Fiducials and polylines are stored as (x, y) coordinates.
            # numpy.ndarrays are created with (slices, rows, cols).
            for slice_fiducials in allfiducials:
                for afiducial in slice_fiducials:
                    maxx = max(maxx, afiducial[0])
                    maxy = max(maxy, afiducial[1])

            for slice_polylines in allpolylines:
                for apolyline in slice_polylines:
                    for afiducial in apolyline:
                        maxx = max(maxx, afiducial[0])
                        maxy = max(maxy, afiducial[1])

            virtual_image = numpy.zeros((maxz, int(maxy + 1), int(maxx + 1)), dtype=int)
            self.pjs.io.cbLoadArray(virtual_image)

        elif image_file is not False and image_file is not None:
            self.pjs.io.cbLoadTimeSeries(image_file)

        self.pjs.annotations.cbDeleteAllAnn()

        self.pjs.undo_stack.push(
            {'changetype': undo_modes.MULTI, 'frame': (0, self.pjs.n_frames), 'index': (True, True),
             'details': self.pjs.copy_annotations()})

        for slice_index, slice_fiducials in enumerate(allfiducials):
            for afiducial in slice_fiducials:
                if afiducial[-1] >= 0:
                    self.pjs.addFiducial(int(afiducial[0]), int(afiducial[1]), slice_index, paint=False)

        for i, theframepolylines in enumerate(allpolylines):
            if i < self.pjs.n_frames:
                for thepolyline in theframepolylines:
                    if thepolyline != [] and thepolyline != [[]]:  # the condition comparing to [[]] is for an edge case with bad user annotations in siesta.
                        if self.pjs.close_all_polylines and thepolyline[0] != thepolyline[-1]:
                            thepolyline.append(thepolyline[0])
                        self.pjs.addPolyline(thepolyline, i, paint=False)

        self.pjs.repaint()

        # Modify current path.
        self.pjs.cwd = os.path.dirname(filenames[0])

        return True


    def cbExportSIESTAAnnotations(self, filename: Optional[str] = None,
                                  message: str = "Export SIESTA annotations ...") -> bool:
        """
        Export annotations in Matlab format. These annotations can be read by both Matlab and Python.
        See https://www.mathworks.com/help/matlab/matlab_external/handling-data-returned-from-python.html for details.

        Something important here is to send float arrays to Matlab, otherwise there are errors when
        Matlab tries to conduct certain operations on the arrays.

        :param filename: name of the file used to store the annotations.
        :param message: string to display as the dialog box title.
        :return: True if the annotations are exported, False otherwise.
        """

        # Get file name.
        if filename is None or filename is False:  # When the menu option is clicked on, for some reason that I do not understand, the function is called with filename = False, which causes a bunch of problems.
            fname = QtWidgets.QFileDialog.getSaveFileName(None, message,
                                                          self.pjs.cwd,
                                                          filter='SIESTA annotations (*.mat)')  # fname[0] is the full filename, fname[1] is the filter used.
            # If cancel ...
            filename = fname[0]
            if filename == '':
                return False
        elif filename == '':
            _, fname = os.path.split(self.pjs.filename)
            filename = os.path.join(self.pjs.cwd, fname)

        # Modify current path.
        self.pjs.cwd = os.path.dirname(filename)

        # Find max number of fiducials and polygons in any frame.
        rnfiducials = numpy.zeros(self.pjs.n_frames, dtype=float)
        max_n_polylines = 0
        for iSlice, thefiducials in enumerate(self.pjs.fiducials):
            rnfiducials[iSlice] = len(thefiducials)
            if len(self.pjs.polylines[iSlice]) > max_n_polylines:
                max_n_polylines = len(self.pjs.polylines[iSlice])

        # Create the fiducial array to send to Matlab.
        max_n_fiducials = numpy.amax(rnfiducials)
        rfiducials = -1. * numpy.ones([int(max_n_fiducials), 3, self.pjs.n_frames], dtype=float)

        # rpolylines is a list, which in Matlab is a cell.
        # The right dimensions are (max_n_fiducials, 1, self.pjs.n_frames)
        # Need to add the singlet second dimensions. The order of the square brackets is critical here.
        rpolylines = [[[[] for _ in range(self.pjs.n_frames)]] for _ in range(max_n_polylines)]

        for iSlice, thefiducials in enumerate(self.pjs.fiducials):
            if thefiducials:
                thefiducials_array = numpy.asarray(thefiducials, dtype=float)
                rfiducials[0:thefiducials_array.shape[0], 0:2, iSlice] = thefiducials_array
                rfiducials[0:thefiducials_array.shape[0], 2, iSlice] = float(iSlice)

            thepolylines = self.pjs.polylines[iSlice]

            if thepolylines:
                for iPoly, thePoly in enumerate(thepolylines):
                    theintpoly = [[float(pnt.x()), float(pnt.y())] for pnt in thePoly]

                    rpolylines[iPoly][0][iSlice] = theintpoly

        imsize = [float(self.pjs.width), float(self.pjs.height), float(self.pjs.n_frames)]

        # Build dictionary with the variables. Dictionaries are converted to structs
        ud = {
            'rfiducials': rfiducials,
            'rpolygons': rpolylines,
            'rnfiducials': rnfiducials,
            'imsize': imsize,
        }

        # Open file name and save annotations.
        try:
            scipy.io.savemat(filename, {'ud': ud}, appendmat=True)
        except (IOError, OSError) as ex:
            print(ex)
            return False

        # Modify current path.
        self.pjs.cwd = os.path.dirname(filename)

        self.pjs.statusbar.showMessage(f'Exported annotations to {filename}.')

        return True

    def cbLoadConfig(self, filename: Optional[str] = None, message: Optional[str] = "Load config file ..."):
        """
                Load a configuration file using tomlkit.

                :param filename: file to open.
                :param message: string to display as the dialog box title.
                :return: True if the config file was loaded with no problems, False otherwise.
                """

        # Get file name.
        if filename is None or filename is False:
            file_dialog = QtWidgets.QFileDialog(None, message, self.pjs.config_path, filter="Config files (*.toml)")
            file_dialog.setFileMode(file_dialog.FileMode.ExistingFile)
            file_dialog.exec()
            filename = file_dialog.selectedFiles()[0]
            if filename == '':
                return False

        self.pjs.cwd = os.path.dirname(filename)
        try:
            with open(filename, 'r') as f:
                self.pjs.config = tomlkit.load(f)
            self.update_options()
            self.update_key_bindings()
            return True
        except FileNotFoundError:
            self.pjs.statusbar.showMessage("Could not find specified file.")
            return False

    def update_options(self):
        """ Updates values for options using the values from self.pjs.config"""
        for this_key in self.pjs.config['options'].keys():
            if getattr(self.pjs, this_key, None) is not None:
                setattr(self.pjs, this_key, self.pjs.config['options'][this_key])
        return True

    def update_key_bindings(self):
        """Updates values for key bindings using the values from self.pjs.config"""
        curr_bindings = self.pjs.get_key_bindings()
        new_bindings = curr_bindings.copy()

        # Get a translation dictionary to go from option names to config names (lowercase, replace spaces with _)
        translation_dict = {}
        for menu_name, this_menu in curr_bindings.items():
            menu_keys = this_menu.keys()
            translated_keys = []
            for this_key in menu_keys:
                this_key = re.sub(r'\s+', '_', this_key.strip())
                this_key = re.sub('[^A-Za-z0-9_]+', '', this_key).lower()
                if this_key.endswith('_'):
                    this_key = this_key[:-1]
                translated_keys.append(this_key)
            translation_dict[menu_name] = translated_keys

        for this_action, this_shortcut in self.pjs.config['key_bindings'].items():
            for menu_name, this_menu in curr_bindings.items():
                if this_action in translation_dict[menu_name]:
                    this_key = list(this_menu.keys())[translation_dict[menu_name].index(this_action)]
                    new_bindings[menu_name][this_key] = this_shortcut
                    break
        return self.pjs.options.configure_key_bindings(new_bindings)

    def cbSaveConfig(self, filename: Optional[str] = None, message: Optional[str] = "Save config file ..."):
        """
                Save the current pjs.config as a .toml file.

                :param filename: filepath to save to.
                :param message: string to display as the dialog box title.
                :return: True if the config file was saved with no problems, False otherwise.
                """

        # Get file name.
        if filename is None or filename is False or filename == '':
            file_dialog = QtWidgets.QFileDialog(None, message, self.pjs.config_path, filter="Config files (*.toml)")
            file_dialog.setFileMode(file_dialog.FileMode.AnyFile)
            file_dialog.setAcceptMode(file_dialog.AcceptMode.AcceptSave)
            file_dialog.exec()
            filename = file_dialog.selectedFiles()[0]

        if filename == '':
            filename = self.pjs.config_path

        self.pjs.config_path = filename

        if os.path.splitext(filename)[1] != ".toml":
            filename = RUtils.set_extension(filename, ".toml")

        self.update_config()
        return self.save_config(filename)
    
    def update_config(self) -> bool:
        # Update options fields
        for this_key in self.pjs.config["options"].keys():
            this_val = getattr(self.pjs, this_key, None)
            if this_val is not None:
                self.pjs.config["options"][this_key] = this_val

        # Update keyboard shortcuts
        for this_menu in self.pjs.menubar.children():
            if type(this_menu) == QtWidgets.QToolButton:
                continue
            these_actions = self.pjs.get_menu_children(this_menu)
            for this_action in these_actions:
                self.pjs.config["key_bindings"][
                    re.sub('[^A-Za-z0-9_]+', '', this_action.objectName())] = this_action.shortcut().toString()

        return True
    
    def save_config(self, fpath: str) -> bool:
        try:
            with open(fpath, 'w') as f:
                tomlkit.dump(self.pjs.config, f)
        except:
            self.pjs.statusbar.showMessage("Failed writing the config file.")
            return False
        return True
    