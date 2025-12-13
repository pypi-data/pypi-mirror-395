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

import copy
from functools import partial
import os
import re

os.environ['KERAS_BACKEND'] = 'torch'

import sys
from typing import List, Tuple, Optional
from enum import IntEnum
import tomlkit

import numpy
from PyQt6 import QtCore, QtGui, QtWidgets
from skimage.measure import points_in_poly

from pyjamas.dragdropmainwindow import DragDropMainWindow
from pyjamas.rannotations.rvector2d import RVector2D
import pyjamas.rimage.rimcore as rimcore
from pyjamas.rimage.rimml.batchml import BatchML
from pyjamas.rimage.rimml.batchclassifier import BatchClassifier
from pyjamas.rimage.rimml.batchneuralnet import BatchNeuralNet
import pyjamas.rimage.rimml.rimlr as rimlr
import pyjamas.rimage.rimml.rimsvm as rimsvm
import pyjamas.rimage.rimml.rimunet as rimunet
from pyjamas.rimage.rimutils import rimutils
from pyjamas.rutils import RUtils, SizedStack
from pyjamas.version import __version__


class undo_modes(IntEnum):
    # Undo change types.
    FIDUCIAL_ADDED: int = 0
    FIDUCIAL_DELETED: int = 1
    POLYLINE_ADDED: int = 2
    POLYLINE_DELETED: int = 3
    POLYLINE_REPLACED: int = 4
    MULTI: int = 5
    IMAGE: int = 6


class PyJAMAS(QtCore.QObject):
    '''
    PyJAMAS is Just A More Awesome Siesta.

    Uses calendar versioning (https://calver.org).
    Format: YYYY.M.minor

    YYYY - Full year - 2006, 2016, 2106
    M - Short month - 6, 16, 10
    minor - minor version number, starts at 0 for a given YYYY.M combination.


    PyJAMAS() creates a PyJAMAS user interface.

    '''

    # Logo path.
    logo_filename = 'pyjamas.tif'
    folder = os.path.split(__file__)[0]
    logo_path = os.path.join(folder, logo_filename)

    # Config path
    config_filename = 'config.toml'
    config_path = os.path.join(folder, config_filename)
    default_config_filename = 'default_config.toml'
    default_config_path = os.path.join(folder, default_config_filename)

    # Annotation modes.
    no_annotations: int = 0
    fiducial_annotations: int = 1
    rectangle_annotations: int = 2
    polyline_annotations: int = 3
    livewire_annotations: int = 4
    move_polyline: int = 5
    export_fiducial_polyline: int = 6
    delete_fiducials_outside_polyline: int = 7
    delete_fiducials_inside_polyline: int = 8
    copy_polyline: int = 9
    select_polyline_crop: int = 10
    select_polyline_exportroi: int = 11
    select_polyline_kymo: int = 12
    inflate_balloon: int = 13
    select_polyline_erosion_dilation: int = 14
    fiducial_highlight_modes = [fiducial_annotations, export_fiducial_polyline]
    polyline_highlight_modes = [rectangle_annotations, polyline_annotations, livewire_annotations, move_polyline,
                                delete_fiducials_outside_polyline, delete_fiducials_inside_polyline, copy_polyline,
                                select_polyline_crop, select_polyline_exportroi, select_polyline_kymo, inflate_balloon,
                                select_polyline_erosion_dilation]

    # Data file extension.
    data_extension: str = '.pjs'
    matlab_extension: str = '.mat'
    image_extensions: Tuple[str] = rimcore.rimage.image_extensions
    plugin_extension: str = '.py'
    config_extension: str = '.toml'
    notebook_extension: str = '.ipynb'
    classifier_extension: str = '.cfr'
    backgroundimage_extension: str = '.bg'

    # Plotting constants.
    fiducial_color = QtCore.Qt.GlobalColor.magenta
    polyline_color = QtCore.Qt.GlobalColor.green
    trajectory_color = QtCore.Qt.GlobalColor.cyan
    vector_color = QtCore.Qt.GlobalColor.darkCyan
    highlight_color = QtCore.Qt.GlobalColor.blue
    fiducial_radius: int = 6
    fiducial_brush_style: QtGui.QBrush = QtGui.QBrush()  # No fill for fiducials (open circles).
    polyline_brush_style: QtGui.QBrush = QtGui.QBrush()
    fiducial_font: QtGui.QFont = QtGui.QFont('Arial', 8)

    # default options
    brush_size: int = 3
    display_fiducial_ids: bool = False
    fps: int = 7
    cwd: str = os.getcwd()
    margin_size: int = 0
    balloon_crop_size: int = 50
    crop_tracked_polyline: bool = False
    darktheme: bool = False
    close_all_polylines: bool = False
    livewire_margin: int = 5
    livewire_gaussian_sigma: float = 5.0
    livewire_shortest_path_fn: str = 'Dijkstra'

    zoom_factors: tuple = (1., 2., 4., 8., .125, .25, .5)

    undo_stack_size: int = 50

    # Read version.
    __version__: str = __version__

    def __init__(self):
        self.initData()  # Initialize object variables.
        self.setupUI()  # Build the GUI.

    def setupUI(self):
        self.app = QtWidgets.QApplication(sys.argv)

        import pyjamas.pjseventfilter as pjseventfilter
        import pyjamas.rcallbacks as rcallbacks

        QtCore.QObject.__init__(self)
        self.MainWindow = DragDropMainWindow()

        self.MainWindow.dropped.connect(self.file_dropped)

        self.MainWindow.setObjectName('PyJAMAS')
        self.MainWindow.resize(1183, 761)
        self.MainWindow.setWindowTitle('PyJAMAS')
        # Windows app icon.
        #self.pjsIcon = QtGui.QIcon('pyjamas.ico')
        #self.MainWindow.setWindowIcon(self.pjsIcon)

        self.gScene = QtWidgets.QGraphicsScene(self.MainWindow)
        self.gScene.setSceneRect(0, 0, 1183, 761)
        self.gScene.setObjectName('gScene')

        self.gView = QtWidgets.QGraphicsView(self.gScene)
        self.gView.setObjectName('gView')
        self.gView.setMouseTracking(
            True)  # This here is necessary so that MouseMove events are triggered when no mouse buttons are pressed.
        self.filter = pjseventfilter.PJSEventFilter(self)
        self.gView.viewport().installEventFilter(self.filter)  # Capture mouse, but not keypress events.
        self.gView.installEventFilter(self.filter)  # Captures key press events but not mouse ones.
        self.MainWindow.setCentralWidget(self.gView)

        self.timeSlider = QtWidgets.QSlider(self.MainWindow)
        self.timeSlider.setGeometry(QtCore.QRect(0, 0, 1183, 22))
        self.timeSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.timeSlider.setObjectName("timeSlider")

        self.darktheme: bool = self.config["options"].get("darktheme", PyJAMAS.darktheme)

        self.menubar = QtWidgets.QMenuBar(self.MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1183, 22))
        self.menubar.setObjectName('menubar')
        self.menuIO = QtWidgets.QMenu(self.menubar)
        self.menuIO.setObjectName('menuIO')
        self.menuOptions = QtWidgets.QMenu(self.menubar)
        self.menuOptions.setObjectName('menuOptions')
        self.menuImage = QtWidgets.QMenu(self.menubar)
        self.menuImage.setObjectName('menuImage')
        self.menuClassifiers = QtWidgets.QMenu(self.menuImage)
        self.menuClassifiers.setObjectName('menuClassifiers')
        self.menuAnnotations = QtWidgets.QMenu(self.menubar)
        self.menuAnnotations.setObjectName('menuAnnotations')
        self.menuMeasurements = QtWidgets.QMenu(self.menubar)
        self.menuMeasurements.setObjectName('menuMeasurements')
        self.menuBatch = QtWidgets.QMenu(self.menubar)
        self.menuBatch.setObjectName('menuBatch')
        self.menuPlugins = QtWidgets.QMenu(self.menubar)
        self.menuPlugins.setObjectName('menuPlugins')
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName('menuHelp')
        self.MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusbar.setObjectName('statusbar')
        self.MainWindow.setStatusBar(self.statusbar)

        self.threadpool = QtCore.QThreadPool()
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.io = rcallbacks.rcbio.RCBIO(self)
        self.options = rcallbacks.rcboptions.RCBOptions(self)
        self.image = rcallbacks.rcbimage.RCBImage(self)
        self.classifiers = rcallbacks.rcbclassifiers.RCBClassifiers(self)
        self.annotations = rcallbacks.rcbannotations.RCBAnnotations(self)
        self.measurements = rcallbacks.rcbmeasure.RCBMeasure(self)
        self.batch = rcallbacks.rcbbatchprocess.RCBBatchProcess(self)
        self.plugins = rcallbacks.rcbplugins.RCBPlugins(self)
        self.about = rcallbacks.rcbabout.RCBAbout(self)

        # Time slider and default image
        self.timeSlider.valueChanged.connect(self.image.cbTimeSlider)
        self.io.cbLoadTimeSeries(PyJAMAS.logo_path)
        self.cwd = self.config["options"].get("cwd", PyJAMAS.cwd)  # so cwd is not overwritten when default image is loaded
        if self.cwd == "":  # Default config loaded
            self.cwd = os.getcwd()

        # IO MENU ----------------------------------------------------------------------
        # Load image action
        self.addMenuItem(self.menuIO, 'Load image ...', self.io.cbLoadTimeSeries)

        # Save time-lapse.
        self.addMenuItem(self.menuIO, 'Save image ...', self.io.cbSaveTimeSeries)

        # Save time-lapse, but only ROI inside the polygon.
        self.addMenuItem(self.menuIO, 'Save image in polyline to working folder',
                         partial(self.io.cbSaveROI, filename=''))

        self.menuIO.addSeparator()

        # Load annotations.
        self.addMenuItem(self.menuIO, 'Load annotations ...', self.io.cbLoadAnnotations)

        self.addMenuItem(self.menuIO, 'Load annotations (additive) ...',
                         lambda: self.io.cbLoadAnnotations(replace=False))

        # Save annotations.
        self.addMenuItem(self.menuIO, 'Save annotations ...', self.io.cbSaveAnnotations)

        self.addMenuItem(self.menuIO, 'Export individual fiducial-polyline annotations',
                         self.io.cbExportPolylineAnnotations)

        self.addMenuItem(self.menuIO, 'Export ALL fiducial-polyline annotations ...',
                         self.io.cbExportAllPolylineAnnotations)

        self.menuIO.addSeparator()

        self.addMenuItem(self.menuIO, 'Load classifier ...', self.io.cbLoadClassifier)

        self.addMenuItem(self.menuIO, 'Save current classifier ...', self.io.cbSaveClassifier)

        self.menuIO.addSeparator()

        self.addMenuItem(self.menuIO, 'Import mask as polylines ...', self.io.cbImportMasks)

        # Export roi and  masks.
        self.addMenuItem(self.menuIO, 'Export ROI and binary masks ...',
                         partial(self.io.cbExportROIAndMasks, polyline=None))

        # Export binary image roi.
        self.addMenuItem(self.menuIO, 'Export current ROIs as binary image ...',
                         self.io.cbExportCurrentAnnotationsBinaryImage)

        self.menuIO.addSeparator()

        # Import SIESTA annotations.
        self.addMenuItem(self.menuIO, 'Import SIESTA annotations ...', self.io.cbImportSIESTAAnnotations)

        # Add SIESTA annotations.
        self.addMenuItem(self.menuIO, 'Import SIESTA annotations (additive) ...',
                         lambda: self.io.cbImportSIESTAAnnotations(replace=False))

        # Export SIESTA annotations.
        self.addMenuItem(self.menuIO, 'Export SIESTA annotations ...', self.io.cbExportSIESTAAnnotations)

        self.menuIO.addSeparator()

        # Save display.
        self.addMenuItem(self.menuIO, 'Save display ...', self.io.cbSaveDisplay)

        # Save annotations movie.
        self.addMenuItem(self.menuIO, 'Export movie with annotations ...', self.io.cbExportMovie)

        self.menubar.addMenu(self.menuIO)

        self.menuIO.addSeparator()

        # Load configuration from file.
        self.addMenuItem(self.menuIO, 'Load config ...', self.io.cbLoadConfig)

        # Save configuration to file.
        self.addMenuItem(self.menuIO, 'Save config ...', self.io.cbSaveConfig)

        # OPTIONS MENU ----------------------------------------------------------------------
        # Set brush size.

        self.addMenuItem(self.menuOptions, 'Undo', self.options.cbUndo)

        self.menuOptions.addSeparator()

        self.addMenuItem(self.menuOptions, 'Brush size ...', self.options.cbSetBrushSize)

        self.addMenuItem(self.menuOptions, 'Crop margins ...', self.options.cbSetMarginSize)

        self.addMenuItem(self.menuOptions, 'Frames per sec ...',
                         self.options.cbFramesPerSec)

        self.addMenuItem(self.menuOptions, 'Working folder ...', self.options.cbSetCWD)

        self.menuOptions.addSeparator()

        self.addMenuItem(self.menuOptions, 'Balloon crop size ...', self.options.cbSetImageProcessingCropSize)

        self.addMenuItem(self.menuOptions, 'LiveWire Gaussian smoothing ...', self.options.cbSetLiveWireSmoothGaussian)

        self.addMenuItem(self.menuOptions, 'LiveWire shortest path function ...', self.options.cbSetLivewireShortestPathFunction)

        self.menuOptions.addSeparator()

        self.addMenuItem(self.menuOptions, 'Close all loaded polylines', self.options.cbCloseAllPolylines)

        self.addMenuItem(self.menuOptions, 'Display fiducial and polyline ids', self.options.cbDisplayFiducialIDs)

        self.addMenuItem(self.menuOptions, 'Toggle crop tracked polyline', self.options.cbCropTracked)

        self.addMenuItem(self.menuOptions, 'Toggle highlighting objects under cursor',
                         self.options.cbToggleHighlightOnHover)

        self.addMenuItem(self.menuOptions, 'Change dilation/erosion footprint', self.options.cbChangeFootprint)

        self.menuOptions.addSeparator()

        self.addMenuItem(self.menuOptions, 'Dark/light display theme', self.options.cbChangeDisplayTheme)

        self.menuOptions.addSeparator()

        self.addMenuItem(self.menuOptions, 'Change key bindings ...', self.options.cbChangeKeyBindings)

        self.menubar.addMenu(self.menuOptions)

        # IMAGE MENU ----------------------------------------------------------------------

        # Adjust contrast
        self.addMenuItem(self.menuImage, 'Adjust contrast ...', self.image.cbAdjustContrast)

        self.menuImage.addSeparator()

        # Rotate image CW.
        self.addMenuItem(self.menuImage, 'Play sequence', self.image.cbPlay)

        self.menuImage.addSeparator()

        self.addMenuItem(self.menuImage, 'Rotate 90 degree clockwise',
                         partial(self.image.cbRotateImage, direction=rcallbacks.rcbimage.RCBImage.CW))

        # Rotate image CCW.
        self.addMenuItem(self.menuImage, 'Rotate 90 degree counter-clockwise',
                         partial(self.image.cbRotateImage, direction=rcallbacks.rcbimage.RCBImage.CCW))

        # Flip left-right.
        self.addMenuItem(self.menuImage, 'Flip left-right',
                         partial(self.image.cbFlipImage, direction=rcallbacks.rcbimage.RCBImage.LEFT_RIGHT))

        # Flip top-bottom.
        self.addMenuItem(self.menuImage, 'Flip up-down',
                         partial(self.image.cbFlipImage, direction=rcallbacks.rcbimage.RCBImage.UP_DOWN))

        self.menuImage.addSeparator()

        # Invert image.
        self.addMenuItem(self.menuImage, 'Invert image', self.image.cbInvertImage)

        # Smoothen image.
        self.addMenuItem(self.menuImage, 'Gaussian smoothing ...', self.image.cbGaussianImage)

        # Gradient.
        self.addMenuItem(self.menuImage, 'Gradient', self.image.cbGradientImage)

        # Maximum intensity projection.
        self.addMenuItem(self.menuImage, 'Maximum intensity projection',
                         partial(self.image.cbProjectImage, projection_type=rcallbacks.rcbimage.projection_types.MAX))

        # Sum intensity projection.
        self.addMenuItem(self.menuImage, 'Sum intensity projection',
                         partial(self.image.cbProjectImage, projection_type=rcallbacks.rcbimage.projection_types.SUM))

        self.menuImage.addSeparator()

        self.addMenuItem(self.menuImage, 'Register image', self.image.cbRegisterImage)

        self.addMenuItem(self.menuImage, 'Rescale image ...', self.image.cbRescaleImage)

        self.menuImage.addSeparator()
        # Zoom action.
        self.addMenuItem(self.menuImage, 'Zoom', self.image.cbZoom)

        # Crop action.
        self.addMenuItem(self.menuImage, 'Crop', partial(self.image.cbCrop, polyline=None))

        # Kymograph.
        self.addMenuItem(self.menuImage, 'Kymograph', partial(self.image.cbKymograph, polyline=None))

        # Orthogonal views.
        self.addMenuItem(self.menuImage, 'Orthogonal views', self.image.cbOrthogonalViews)

        self.menuImage.addSeparator()

        # Find seeds.
        self.addMenuItem(self.menuImage, 'Find seeds ...', self.image.cbFindSeeds)

        # Add fiducials in the centre of polylines.
        self.addMenuItem(self.menuImage, 'Add seeds in polyline centroids ...', self.image.cbCentroidSeeds)

        # Propagate seeds.
        self.addMenuItem(self.menuImage, 'Propagate seeds ...', self.image.cbPropagateSeeds)

        # Expand seeds.
        self.addMenuItem(self.menuImage, 'Expand seeds ...', self.image.cbExpandSeeds)

        # Expand and propagate seeds.
        self.addMenuItem(self.menuImage, 'Expand and propagate seeds ...', self.image.cbExpandNPropagateSeeds)

        # Propagate and expand balloons.
        self.addMenuItem(self.menuImage, 'Propagate balloons ...', self.image.cbPropagateBalloons)

        # Find puncta.
        self.addMenuItem(self.menuImage, 'Find puncta ...', self.image.cbFindPuncta)

        # Classifiers.
        self.menuImage.addMenu(self.menuClassifiers)
        # -- Display Classifier: YellowBrick?
        self.addMenuItem(self.menuClassifiers, 'Create and train logistic regression model ...',
                         self.classifiers.cbCreateLR)
        self.addMenuItem(self.menuClassifiers, 'Create and train support vector machine ...',
                         self.classifiers.cbCreateSVM)
        # self.addMenuItem(self.menuClassifiers, 'Create and train convolutional neural network ...', None,
        #                 self.classifiers.cbCreateCNN)
        self.addMenuItem(self.menuClassifiers, 'Create and train UNet ...', self.classifiers.cbCreateUNet)
        self.addMenuItem(self.menuClassifiers, 'Create and train ReSCUNet ...', self.classifiers.cbCreateReSCUNet)

        # -- Decision Trees

        self.menuClassifiers.addSeparator()

        self.addMenuItem(self.menuClassifiers, 'Apply classifier ...', self.classifiers.cbApplyClassifier)

        self.addMenuItem(self.menuClassifiers, 'Apply classifier to current slice ...',
                         lambda: self.classifiers.cbApplyClassifier(firstSlice=self.curslice + 1, lastSlice=self.curslice + 1))

        self.menuClassifiers.addSeparator()

        self.addMenuItem(self.menuClassifiers, 'Non-maximum suppression ...', self.classifiers.cbNonMaxSuppression)

        self.addMenuItem(self.menuClassifiers, 'Segment detected objects ...', self.image.cbSegmentDetectedObjects)

        self.addMenuItem(self.menuClassifiers, 'Change neural net step size ...',
                         self.classifiers.cbSetNeuralNetStepSize)

        self.menuImage.addSeparator()

        # Next image action
        self.addMenuItem(self.menuImage, 'Next frame', self.image.cbNextFrame)

        # Previous image action
        self.addMenuItem(self.menuImage, 'Previous frame', self.image.cbPrevFrame)

        # Beginning and end actions
        self.addMenuItem(self.menuImage, 'Go to beginning', partial(self.image.cbGoTo, slice_index=0))
        self.addMenuItem(self.menuImage, 'Go to end', partial(self.image.cbGoTo, slice_index=-1))

        self.menuImage.addSeparator()

        # Display info.
        self.addMenuItem(self.menuImage, 'Display info', self.image.cbDisplayInfo)

        self.menubar.addMenu(self.menuImage)

        # ANNOTATIONS MENU ----------------------------------------------------------------------
        # No annotations.
        self.addMenuItem(self.menuAnnotations, 'No annotations', self.annotations.cbNoAnn)

        self.addMenuItem(self.menuAnnotations, 'Hide/display annotations', self.annotations.cbHideAnn)

        # Fiducials
        self.addMenuItem(self.menuAnnotations, 'Fiducials', self.annotations.cbFiducials)

        # Rectangles
        self.addMenuItem(self.menuAnnotations, 'Rectangles', self.annotations.cbRectangles)

        # Polylines
        self.addMenuItem(self.menuAnnotations, 'Polylines', self.annotations.cbPolylines)

        # Livewire
        self.addMenuItem(self.menuAnnotations, 'LiveWire', self.annotations.cbLiveWire)

        # Balloon
        self.addMenuItem(self.menuAnnotations, 'Balloon', self.annotations.cbInflateBalloon)

        self.menuAnnotations.addSeparator()

        # Copy and paste polyline
        self.addMenuItem(self.menuAnnotations, 'Copy polyline', self.annotations.cbCopyPolyline)

        self.addMenuItem(self.menuAnnotations, 'Paste polyline', self.annotations.cbPastePolyline)

        # Move polyline.
        self.addMenuItem(self.menuAnnotations, 'Move polyline', self.annotations.cbMovePolyline)

        # Dilate/erode polyline
        self.addMenuItem(self.menuAnnotations, 'Dilate/Erode polyline', self.annotations.cbDilateErodePolyline)

        self.menuAnnotations.addSeparator()

        self.addMenuItem(self.menuAnnotations, 'Track fiducials ...', self.annotations.cbTrackFiducials)

        self.menuAnnotations.addSeparator()

        # Delete polylines on the current image.
        self.addMenuItem(self.menuAnnotations, 'Delete polylines on current frame', self.annotations.cbDeleteSlicePoly)

        # Delete fiducials on current image.
        self.addMenuItem(self.menuAnnotations, 'Delete fiducials on current frame',
                         self.annotations.cbDeleteSliceFiducials)

        # Delete annotations on the current image.
        self.addMenuItem(self.menuAnnotations, 'Delete all annotations on current frame',
                         self.annotations.cbDeleteSliceAnn)

        # Delete ALL annotations.
        self.addMenuItem(self.menuAnnotations, 'Delete all annotations in the sequence',
                         self.annotations.cbDeleteAllAnn)

        # Delete ALL fiducials.
        self.addMenuItem(self.menuAnnotations, 'Delete all fiducials in the sequence',
                         self.annotations.cbDeleteAllFiducials)

        # Delete fiducials OUTSIDE polyline.
        self.addMenuItem(self.menuAnnotations, 'Delete fiducials outside polyline',
                         self.annotations.cbDeleteFiducialsOutsidePoly)

        self.menubar.addMenu(self.menuAnnotations)

        # Delete fiducials INSIDE polyline.
        self.addMenuItem(self.menuAnnotations, 'Delete fiducials inside polyline',
                         self.annotations.cbDeleteFiducialsInsidePoly)

        self.menubar.addMenu(self.menuAnnotations)

        # MEASUREMENTS MENU --------------------------------------------------------------------
        self.addMenuItem(self.menuMeasurements, 'Measure polylines ...', self.measurements.cbMeasurePoly)

        self.menubar.addMenu(self.menuMeasurements)

        # BATCH MENU ---------------------------------------------------------------------------
        # Max project and concatenate.
        self.addMenuItem(self.menuBatch, "Max project and concatenate ...",
                         partial(self.batch.cbBatchProjectConcat, projection_type=rcallbacks.rcbimage.projection_types.MAX))

        # Sum project and concatenate.
        self.addMenuItem(self.menuBatch, "Sum project and concatenate ...",
                         partial(self.batch.cbBatchProjectConcat, projection_type=rcallbacks.rcbimage.projection_types.SUM))

        # Resize images.
        self.addMenuItem(self.menuBatch, "Resize images ...", self.batch.cbBatchResize)

        # Resize images.
        self.addMenuItem(self.menuBatch, "Correct images ...", self.batch.cbBatchFlatFieldCorrection)

        self.menuBatch.addSeparator()

        # Measure.
        self.addMenuItem(self.menuBatch, "Measure ...", self.batch.cbMeasureBatch)

        self.menubar.addMenu(self.menuBatch)

        # PLUGINS MENU ---------------------------------------------------------------------------
        # Install plugin.
        self.addMenuItem(self.menuPlugins, "Install plugin ...", self.plugins.cbInstallPlugin)

        # Uninstall plugin.
        self.addMenuItem(self.menuPlugins, "Uninstall plugin ...", self.plugins.cbUninstallPlugin)

        self.menuPlugins.addSeparator()

        self.plugins.cbLoadPlugins()

        self.menubar.addMenu(self.menuPlugins)

        # PyJAMAS MENU ---------------------------------------------------------------------------
        # About.
        self.addMenuItem(self.menuHelp, "About", self.about.cbAbout)

        self.menubar.addMenu(self.menuHelp)

        self.menubar.setNativeMenuBar(True)
        self.retranslateUi()

        # Init UI.
        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

        self.gView.show()
        self.MainWindow.show()

    def initData(self) -> bool:
        # Load the config file
        try:
            with open(self.config_path, 'r') as f:
                self.config = tomlkit.load(f)
        except FileNotFoundError:
            with open(self.default_config_path, 'r') as f:
                self.config = tomlkit.load(f)

        self._imageItem = None  # pixmap containing the image currently being displayed.
        self.zoom_index = 0  # index into PyJAMAS.zoom_factors to establish the zoom level.
        self.brush_size: int = self.config["options"].get("brush_size", PyJAMAS.brush_size)  # brush size to paint polylines
        self.show_annotations: bool = True  # display or not annotations.
        self.display_fiducial_ids: bool = self.config["options"].get("display_fiducial_ids", PyJAMAS.display_fiducial_ids)  # display an identifier next to each fiducial
        self.margin_size: int = self.config["options"].get("margin_size", PyJAMAS.margin_size)  # margin size for cropping
        self.crop_tracked_polyline: bool = self.config["options"].get("crop_tracked_polyline", PyJAMAS.crop_tracked_polyline)  # crop function takes polyline on one slice or all slices
        self.fps: int = self.config["options"].get("fps", PyJAMAS.fps)  # frames per second used to play the current sequence or when exporting as a movie
        self.close_all_polylines: bool = self.config["options"].get("close_all_polylines", PyJAMAS.close_all_polylines)  # close all polylines loaded from file or load as open polylines those whose first and last point are not the same
        self.annotation_mode = PyJAMAS.no_annotations
        self.batch_classifier: BatchML = None
        self.gaussian_sigma: float = 0.0
        self.scale_factor: Tuple[float, float] = (1.0, 1.0)
        self.balloon_crop_size: int = self.config["options"].get("balloon_crop_size", PyJAMAS.balloon_crop_size)  # crop size used to inflate balloons

        self.livewire_margin: int = self.config["options"].get("livewire_margin", PyJAMAS.livewire_margin)
        self.livewire_gaussian_sigma: float = self.config["options"].get("livewire_gaussian_sigma", PyJAMAS.livewire_gaussian_sigma)
        self.livewire_shortest_path_fn: str = self.config["options"].get("livewire_shortest_path_fn", PyJAMAS.livewire_shortest_path_fn)
        self.highlight_on_hover: bool = self.config["options"].get("highlight_on_hover", True)  # whether to highlight the object under the cursor
        self.footprint: str = self.config["options"].get("footprint", "disk")
        self.active_element = None  # will hold the scene element that is under the mouse (for changing colour on hover)

        self.min_pix_percentile: int = 0  # Lowest percentile of the pixel values to map to display value 0.
        self.max_pix_percentile: int = 100  # Highest percentile of the pixel values to map to display value 255.

        self.pjs_path, _ = os.path.split(os.path.realpath(__file__))
        self.plugin_list: List = []
        self.plugin_path_list: List = []
        self.plugin_path: str = os.path.join(self.pjs_path, 'plugins')
        sys.path.append(self.plugin_path)

        self._poly_ = []  # Stores polyline coordinates while they are being drawn. Dunder (__a__) is reserved for special methods (e.g. __len__()).
        self._copied_poly_ = None  # Stores copied polyline to be pasted.
        self._agraphicsitem_ = None  # Stores a graphicsitem transiently (e.g. a rectangle as it is being dragged).

        self.undo_stack: SizedStack = SizedStack(PyJAMAS.undo_stack_size)
        self.slicetracker: tuple = None

        return True

    def prepare_image(self):
        if hasattr(self, 'slices') and len(self.slices.shape) == 2:
            self.slices = numpy.expand_dims(self.slices, axis=0)

        self.curslice: int = 0
        self.imagedata: numpy.ndarray = self.slices[self.curslice]
        self.n_frames: int = self.slices.shape[0]
        self.height: int = self.slices.shape[1]  # number of rows.
        self.width: int = self.slices.shape[2]  # number of columns.
        self.min_pix_percentile = 0
        self.max_pix_percentile = 100

        self.image.cbZoom(0)

    def initImage(self):
        self.prepare_image()

        self.fiducials = [[] for _ in range(self.n_frames)]
        self.polylines = [[] for _ in range(self.n_frames)]
        self.polyline_ids = [[] for _ in range(self.n_frames)]
        self.vectors = [[] for _ in range(self.n_frames)]
        self.slicetracker = None

        # Make sure to continue to store the classifier in memory.
        if self.batch_classifier is None:
            self.batch_classifier = BatchClassifier(self.n_frames)
        elif type(self.batch_classifier.image_classifier) in [rimlr.lr, rimsvm.svm]:
            self.batch_classifier = BatchClassifier(self.n_frames, self.batch_classifier.image_classifier)
        elif type(self.batch_classifier.image_classifier) is rimunet.UNet:
            self.batch_classifier = BatchNeuralNet(self.n_frames, self.batch_classifier.image_classifier)

        # Resizing the window.
        self.resize_window()

        self.timeSlider.valueChanged.disconnect()
        self.timeSlider.setMinimum(1)
        self.timeSlider.setMaximum(self.n_frames)
        self.timeSlider.setValue(1)
        self.timeSlider.valueChanged.connect(self.image.cbTimeSlider)

        self.displayData()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.menuIO.setTitle(_translate('PyJAMAS', 'IO'))
        self.menuOptions.setTitle(_translate('PyJAMAS', 'Options'))
        self.menuImage.setTitle(_translate('PyJAMAS', 'Image'))
        self.menuClassifiers.setTitle(_translate('PyJAMAS', 'Classifiers'))
        self.menuAnnotations.setTitle(_translate('PyJAMAS', 'Annotations'))
        self.menuMeasurements.setTitle(_translate('PyJAMAS', 'Measurements'))
        self.menuBatch.setTitle(_translate('PyJAMAS', 'Batch'))
        self.menuPlugins.setTitle(_translate('PyJAMAS', 'Plugins'))
        self.menuHelp.setTitle(_translate('PyJAMAS', 'Help'))

        return True

    def addMenuItem(self, themenu, thetext, thecallbackfunction):
        # Get a config name by replacing spaces with underscores and removing special characters
        thename = re.sub(r'\s+', '_', thetext.strip())
        thename = re.sub('[^A-Za-z0-9_]+', '', thename).lower()
        if thename.endswith('_'):
            thename = thename[:-1]

        theshortcut = self.config["key_bindings"].get(thename, None)
        if theshortcut is None:  # menu item that is not in the config, let's add it to the config file
            self.config["key_bindings"][thename] = ""
            theshortcut = ""

        newAction = QtGui.QAction(self.MainWindow)
        newAction.setEnabled(True)
        newAction.setText(thetext)
        newAction.setIconText(thetext)
        newAction.setToolTip(thetext)
        newAction.setObjectName(thename)
        newAction.triggered.connect(thecallbackfunction)

        newAction.setShortcut(theshortcut)

        # There are other possible values for the ShortcutContext in Qt.ShortcutContext. This is key for shortcuts to work when setNativeMenuBar(True) is used.
        newAction.setShortcutContext(QtCore.Qt.ShortcutContext.WidgetWithChildrenShortcut)
        newShortcut = QtGui.QShortcut(QtGui.QKeySequence(theshortcut), self.MainWindow)
        newShortcut.activated.connect(thecallbackfunction)
        newAction.setData({'shortcut': newShortcut, 'callback': thecallbackfunction})

        themenu.addAction(newAction)

        return newAction

    def resize_window(self) -> bool:
        self.gScene.setSceneRect(0, 0, self.width, self.height)
        self.MainWindow.resize(int(self.width * self.zoom_factors[self.zoom_index]),
                               int(self.height * self.zoom_factors[self.zoom_index] + 60))
        self.timeSlider.setGeometry(QtCore.QRect(0, self.height + 18, self.MainWindow.width(), 22))

        return True

    def displayData(self):
        # Delete annotations from the screen.
        self.eraseAnnotations()

        # Stretch the dynamic range of the image and then convert to 8 bits.
        # There is an autocontrast function in pillow, but it only works on 8 bit grayscale or color data.
        # And converting to 8 bit and then doing the stretch leads to information loss and pixelated images.
        # img_16bit_to_8bit = RImage(self.imagedata).stretch()
        # img_16bit_to_8bit = numpy.array(img_16bit_to_8bit, dtype=numpy.uint8)

        # themin = numpy.min(self.imagedata)
        # themax = numpy.max(self.imagedata)

        # Now we stretch the image for display. I tested skimage.exposure.rescale_intensity and my own stretch method
        # (implemented  following the code in dipimage). stretch took 419 us, vs 484 us for rescale_intensity.
        # img_16bit_to_8bit = exposure.rescale_intensity(self.imagedata, in_range=(themin, themax), out_range=(0, 255))
        img_16bit_to_8bit = rimutils.stretch(self.imagedata, self.min_pix_percentile, self.max_pix_percentile)
        img_16bit_to_8bit = numpy.array(img_16bit_to_8bit, dtype=numpy.uint8)

        # Display image. The fourth parameter in the QImage constructor is 1*self.width for grayscale images,
        # and 3*self.width for color images.
        qImg = QtGui.QImage(bytes(img_16bit_to_8bit), self.width, self.height, self.width,
                            QtGui.QImage.Format.Format_Grayscale8)
        pixmap = QtGui.QPixmap.fromImage(qImg)

        if self._imageItem is not None:
            self.gScene.removeItem(self._imageItem)

        self._imageItem = QtWidgets.QGraphicsPixmapItem(pixmap)
        self.gScene.addItem(self._imageItem)
        # self.gView.fitInView(self._imageItem, QtCore.Qt.KeepAspectRatio)

        if self.show_annotations:
            self.paintAnnotations()

        if self.slicetracker is not None:
            self.paintTracker()

        self.statusbar.showMessage(str(self.curslice + 1) + '/' + str(self.n_frames))

        return True

    # Perhaps create a class RAnnotations, and a PyJAMAS object has an RAnnotations property, that contains fields fiducials, polylines, etc. Does it contain the GraphicsScene as well? Yes, it is the argument to the constructor.
    # Add and remove methods take on an additional argument, the current slice. Constants are taken from class properties (PyJAMAS.fiducial_color, etc.).
    def addFiducial(self, x, y, z, paint=True, pushundo=False):
        """

        :param x:
        :param y:
        :param z:
        :param paint: when set to False, the screen will not be repainted. This helps when adding fiducials on a different thread (which is not allowed to modify the GUI - see https://doc.qt.io/qt-5/thread-basics.html#gui-thread-and-worker-thread)
        :return:
        """
        self.fiducials[z].append([x, y])
        if pushundo:
            self.undo_stack.push({'changetype': undo_modes.FIDUCIAL_ADDED, 'frame': self.curslice,
                                  'index': len(self.fiducials[self.curslice]) - 1, 'details': None})
        # print('Fiducials on frame ' + str(self.curslice) + ': ' + self.fiducials[self.curslice].__str__())

        # Add ellipse at (0,0). Then move it to the right position. This is important so that scenePos() returns the proper coordinates for the item.
        # If you add here directly in the (x, y) coordinates, scenePos() returns [0, 0].
        if paint and z == self.curslice:
            theItem = self.gScene.addEllipse(0, 0, PyJAMAS.fiducial_radius, PyJAMAS.fiducial_radius,
                                             PyJAMAS.fiducial_color,
                                             PyJAMAS.fiducial_brush_style)
            theItem.setPos(x - PyJAMAS.fiducial_radius / 2, y - PyJAMAS.fiducial_radius / 2)

            # If fiducial ids are on display, repaint them.
            if self.display_fiducial_ids:
                self.repaint()

        return True

    def findGraphicItem(self, x, y, class_type_or_tuple,
                        radius=fiducial_radius):  # Substitute in removeFiducial, removePolygon and movepolyline.

        theItems = self.gScene.items(
            QtCore.QRectF(x - radius / 4, y - radius / 4, radius / 2, radius / 2))

        # Because there are layers, if a rectangle was drawn on the ellipse, the rectangle will come first. So we look for the ellipse.
        for theClickedItem in theItems:
            if isinstance(theClickedItem, class_type_or_tuple):
                return theClickedItem

        return None

    def find_clicked_polyline(self, x: int, y: int) -> int:
        polyline_class_tuple: Tuple = (QtWidgets.QGraphicsPolygonItem, QtWidgets.QGraphicsPathItem)
        self._agraphicsitem_ = self.findGraphicItem(x, y, polyline_class_tuple)

        if isinstance(self._agraphicsitem_, QtWidgets.QGraphicsPolygonItem):
            theClickedPolygon = self._agraphicsitem_.polygon()
        elif isinstance(self._agraphicsitem_, QtWidgets.QGraphicsPathItem):
            # Extract polyline from the path using toFillPolygon. Need to remove the last point, though, as it closes the polygon so that it can be filled.
            theClickedPolygon = (self._agraphicsitem_.path().toFillPolygon())[:-1]
        else:
            return -1

        try:
            index = self.polylines[self.curslice].index(theClickedPolygon)
        except LookupError:
            return -1
        else:
            self._poly_ = self.polylines[self.curslice][index]
            return index

    def removeFiducial(self, x, y, z, pushundo=False):
        # Grab items within a small square around the click point.
        """theItems = self.gScene.items(
            QtCore.QRectF(x - PyJAMAS.fiducial_radius / 4, y - PyJAMAS.fiducial_radius / 4, PyJAMAS.fiducial_radius / 2,
                          PyJAMAS.fiducial_radius / 2))

        # Because there are layers, if a rectangle was drawn on the ellipse, the rectangle will come first. So we look for the ellipse.
        for theClickedItem in theItems:
            if type(theClickedItem) == QtWidgets.QGraphicsEllipseItem:
                break
        """

        theClickedItem = self.findGraphicItem(x, y, QtWidgets.QGraphicsEllipseItem)

        # If you found an ellipse:
        if isinstance(theClickedItem, QtWidgets.QGraphicsEllipseItem):
            # Get coordinates. Find item in fiducial list. If you can find it, delete it there and delete the item from the scene.
            pos = theClickedItem.scenePos()
            deleteCoords = [int(pos.x() + PyJAMAS.fiducial_radius / 2), int(pos.y() + PyJAMAS.fiducial_radius / 2)]

            if deleteCoords in self.fiducials[z]:
                if pushundo:
                    ind = self.fiducials[z].index(deleteCoords)
                    self.undo_stack.push(
                        {'changetype': undo_modes.FIDUCIAL_DELETED, 'frame': z, 'index': ind, 'details': deleteCoords})

                self.fiducials[z].remove(deleteCoords)
                self.gScene.removeItem(theClickedItem)
                # print('Fiducials on frame ' + str(self.curslice) + ': ' + self.fiducials[self.curslice].__str__())

                # If fiducial ids are on display, repaint them.
                if self.display_fiducial_ids:
                    self.repaint()

        return True

    def removeFiducialsPolyline(self, polyline: QtGui.QPolygonF = None, inside_flag: bool = True):
        # Go through the list of fiducials.
        polyline_list = RUtils.qpolygonf2ndarray(polyline)

        inside_poly_flags: numpy.ndarray = points_in_poly(self.fiducials[self.curslice], polyline_list)

        # To avoid deleting fiducials from the list we are checking.
        fiducial_list = self.fiducials[self.curslice].copy()

        for thefiducial, is_inside in zip(fiducial_list, inside_poly_flags):
            if (is_inside and inside_flag) or not (is_inside or inside_flag):
                self.removeFiducial(thefiducial[0], thefiducial[1], self.curslice)

        return True

    def drawRectangle(self, x0, y0, x1, y1):
        # print([x0,y0].__str__() + " " + [x1, y1].__str__())
        if x0 > x1:
            x0, x1 = x1, x0

        if y0 > y1:
            y0, y1 = y1, y0

        # print([x0,y0].__str__() + " " + [x1, y1].__str__())
        pen = QtGui.QPen()
        pen.setWidth(self.brush_size)
        pen.setColor(PyJAMAS.polyline_color)

        return self.gScene.addRect(
            x0, y0, x1 - x0, y1 - y0, pen, PyJAMAS.polyline_brush_style
        )

    def drawPath(self, coordinates):
        thepolyline = RUtils.list2qpolygonf(coordinates)

        thepath = QtGui.QPainterPath()
        thepath.addPolygon(thepolyline)

        pen = QtGui.QPen()
        pen.setWidth(self.brush_size)
        pen.setColor(PyJAMAS.polyline_color)

        theItem = self.gScene.addPath(thepath, pen, PyJAMAS.polyline_brush_style)

        return theItem, thepolyline

    def drawPolyline(self, aQPolygonF):
        pen = QtGui.QPen()
        pen.setWidth(self.brush_size)
        pen.setColor(PyJAMAS.polyline_color)

        if aQPolygonF.isClosed():
            pen.setColor(PyJAMAS.polyline_color)
            return self.gScene.addPolygon(aQPolygonF, pen, PyJAMAS.polyline_brush_style)
        else:
            aPath = QtGui.QPainterPath()
            aPath.addPolygon(aQPolygonF)
            pen.setColor(PyJAMAS.trajectory_color)
            return self.gScene.addPath(aPath, pen, PyJAMAS.polyline_brush_style)

    def drawVector(self, aVector: RVector2D):
        pen = QtGui.QPen()
        pen.setWidth(self.brush_size)
        pen.setColor(PyJAMAS.vector_color)

        # draw an ellipse at the origin.
        theItem = self.gScene.addEllipse(0, 0, PyJAMAS.fiducial_radius, PyJAMAS.fiducial_radius,
                                         PyJAMAS.fiducial_color,
                                         PyJAMAS.fiducial_brush_style)
        theItem.setPos(aVector.origin[0] - PyJAMAS.fiducial_radius / 2, aVector.origin[1] - PyJAMAS.fiducial_radius / 2)

        # and a line pointing in the appropriate direction
        aPath = QtGui.QPainterPath()
        apolygonf = QtGui.QPolygonF()
        apolygonf.append(QtCore.QPointF(aVector.origin[0], aVector.origin[1]))
        apolygonf.append(QtCore.QPointF(aVector.end[0], aVector.end[1]))

        aPath.addPolygon(apolygonf)
        return self.gScene.addPath(aPath, pen, PyJAMAS.polyline_brush_style)

    def addPolyline(self, coordinates: list, z: int, theid: int = None, paint: bool = True, pushundo=False) -> bool:
        thepolyline: QtGui.QPolygonF = RUtils.list2qpolygonf(coordinates)

        self.polylines[z].append(thepolyline)
        if theid is not None and type(theid) == int and theid > 0:
            polyline_id = theid
        else:
            polyline_id = max(self.polyline_ids[z]) + 1 if len(self.polyline_ids[z]) else 1

        self.polyline_ids[z].append(polyline_id)
        if pushundo:
            self.undo_stack.push(
                {'changetype': undo_modes.POLYLINE_ADDED, 'frame': z, 'index': len(self.polylines[z]) - 1,
                 'details': None})

        # Draw the polyline if it is being added to the right time point.
        if paint and z == self.curslice:
            self.drawPolyline(thepolyline)

            # If ids are on display, repaint them.
            if self.display_fiducial_ids:
                self.repaint()

        return True

    def replacePolyline(self, index: int, coordinates: list, z: int, paint: bool = True,
                        pushundo: bool = False) -> bool:
        thepolyline: QtGui.QPolygonF = RUtils.list2qpolygonf(coordinates)

        old_poly = self.polylines[z][index]
        self.polylines[z][index] = thepolyline

        if pushundo:
            self.undo_stack.push(
                {'changetype': undo_modes.POLYLINE_REPLACED, 'frame': z, 'index': self.polyline_ids[z][index],
                 'details': old_poly})
        # Draw the polyline if it is being added to the right time point.
        if paint and z == self.curslice:
            self.drawPolyline(thepolyline)

            # If ids are on display, repaint them.
            if self.display_fiducial_ids:
                self.repaint()

        return True

    def removePolyline(self, x, y, z, paint=True, pushundo=False) -> Optional[QtGui.QPolygonF]:
        poly: QtGui.QPolygonF = None

        index_polyline = self.find_clicked_polyline(x, y)  # stores the clicked graphic item in self._agraphicsitem_
        if index_polyline >= 0:
            poly = self.polylines[z].pop(index_polyline)
            poly_id = self.polyline_ids[z].pop(index_polyline)
            if pushundo:
                self.undo_stack.push(
                    {'changetype': undo_modes.POLYLINE_DELETED, 'frame': z, 'index': poly_id, 'details': poly})

            if paint and self.curslice == z:
                self.gScene.removeItem(self._agraphicsitem_)

                # If ids are on display, repaint them.
                if self.display_fiducial_ids:
                    self.repaint()

        return poly

    def removePolylineByIndex(self, index: int, z: int, paint: bool = True, pushundo: bool = False):

        poly = self.polylines[z].pop(index)
        poly_id = self.polyline_ids[z].pop(index)
        if pushundo:
            self.undo_stack.push(
                {'changetype': undo_modes.POLYLINE_DELETED, 'frame': z, 'index': poly_id, 'details': poly})

        if paint and self.curslice == z:
            self.repaint()

        return poly

    def eraseAnnotations(self) -> bool:
        allItems = self.gScene.items()

        for i in allItems:
            if isinstance(i,
                          (QtWidgets.QGraphicsEllipseItem, QtWidgets.QGraphicsPolygonItem, QtWidgets.QGraphicsTextItem,
                           QtWidgets.QGraphicsPathItem, QtWidgets.QGraphicsLineItem)
                          ):
                self.gScene.removeItem(i)

        self.active_element = None

        return True

    def paintAnnotations(self) -> bool:
        # pen = QtGui.QPen()
        # pen.setWidth(self.brush_size)
        # pen.setColor(PyJAMAS.polyline_color)

        # Paints temporary polylines (e.g. a livewire being drawn) when switching across slices.
        if self._poly_ and type(self._poly_) == list:
            apoly = self._poly_.copy()
            apoly.append([self.filter.x, self.filter.y])
            self._agraphicsitem_, _ = self.drawPath(apoly)

        # Paints all other polylines.
        for i, thepoly in enumerate(self.polylines[self.curslice]):
            if thepoly == [] or list(thepoly) == []:
                continue

            thePolyline = self.drawPolyline(thepoly)
            thePolyline.setData(0, None)  # will store the ID text item when IDs are shown
            # self.gScene.addPolygon(thepoly, pen, PyJAMAS.polyline_brush_style)

            if self.display_fiducial_ids:
                polygon = RUtils.qpolygonf2polygon(thepoly)
                theItem = self.gScene.addText(str(self.polyline_ids[self.curslice][i]), PyJAMAS.fiducial_font)
                theItem.setPos(polygon.centroid.x, polygon.centroid.y)
                if thepoly.isClosed():
                    theItem.setDefaultTextColor(self.polyline_color)
                else:
                    theItem.setDefaultTextColor(self.trajectory_color)
                thePolyline.setData(0, theItem)

        # Paint fiducials after polylines so that polylines are in the foreground.
        for i, thefiducial in enumerate(self.fiducials[self.curslice]):
            # Add ellipse at (0,0). Then move it to the right position. This is important so that scenePos() returns the proper coordinates for the item.
            # If you add here directly in the (x, y) coordinates, scenePos() returns [0, 0].
            theFiducial = self.gScene.addEllipse(0, 0, self.fiducial_radius, self.fiducial_radius, self.fiducial_color,
                                                 self.fiducial_brush_style)
            theFiducial.setData(0, None)  # will store the ID text item when IDs are shown

            x = thefiducial[0]
            y = thefiducial[1]
            theFiducial.setPos(x - PyJAMAS.fiducial_radius / 2, y - PyJAMAS.fiducial_radius / 2)

            if self.display_fiducial_ids:
                theItem = self.gScene.addText(str(i + 1), PyJAMAS.fiducial_font)
                theItem.setPos(x - PyJAMAS.fiducial_radius / 2, y - PyJAMAS.fiducial_radius / 2)
                theItem.setDefaultTextColor(self.fiducial_color)
                theFiducial.setData(0, theItem)

        # Re-color the active element
        if self.highlight_on_hover:
            self.paint_active_element(self.filter.x, self.filter.y)

        # Make sure focus goes back to the main window.
        self.MainWindow.activateWindow()

        return True

    def paintTracker(self):
        self.gScene.addLine(0, self.slicetracker[1], self.width, self.slicetracker[1], QtCore.Qt.GlobalColor.yellow)
        self.gScene.addLine(self.slicetracker[0], 0, self.slicetracker[0], self.height, QtCore.Qt.GlobalColor.yellow)

    def repaint(self):
        self.eraseAnnotations()
        self.paintAnnotations()
        if self.slicetracker is not None:
            self.paintTracker()

        return True

    def file_dropped(self, filename_list: List[str], kb: QtCore.Qt.KeyboardModifier) -> bool:
        pjfiles = []
        siestafiles = []

        replace_flag: bool = kb != QtCore.Qt.KeyboardModifier.AltModifier

        for file_name in filename_list:
            if not os.path.exists(file_name):
                return False

            file_name_str = str(file_name).lower()
            _, extension = os.path.splitext(file_name_str)

            if extension in PyJAMAS.image_extensions + (PyJAMAS.backgroundimage_extension,):
                self.io.cbLoadTimeSeries(file_name_str)
            elif extension == PyJAMAS.data_extension:
                pjfiles.append(file_name_str)
            elif extension == PyJAMAS.matlab_extension:
                siestafiles.append(file_name_str)
            elif extension == PyJAMAS.classifier_extension:
                self.io.cbLoadClassifier(file_name_str)
            elif extension == PyJAMAS.plugin_extension:
                self.plugins.cbInstallPlugin(file_name_str)
            elif extension == PyJAMAS.config_extension:
                self.io.cbLoadConfig(file_name_str)

        if pjfiles:
            self.io.cbLoadAnnotations(pjfiles, replace=replace_flag)
        elif len(siestafiles) > 0:
            self.io.cbImportSIESTAAnnotations(siestafiles, replace=replace_flag)

        return True

    @classmethod
    def new_pjs(cls, theimage: numpy.ndarray):
        thenewpjs: PyJAMAS = PyJAMAS()
        thenewpjs.io.cbLoadArray(theimage)

        return thenewpjs

    def __copy__(self):
        newone = type(self)()
        newone.__dict__.update(self.__dict__)
        return newone

    def __deepcopy__(self, memodict={}):
        newone = type(self)()
        memodict[id(self)] = newone

        # Deep copy methods with a __deepcopy__ magic method.
        # Otherwise, copy by reference.
        for k, v in self.__dict__.items():
            if getattr(v, "__deepcopy__", None):
                setattr(newone, k, v.__deepcopy__(memodict))
            else:
                setattr(newone, k, v)

        return newone

    def __str__(self) -> str:
        the_string: str = f"file name: {self.filename}\n" \
                          f"size (width, height, slices): ({self.width}, {self.height}, {self.n_frames})\n" \
                          f"display percentiles (min, max): ({self.min_pix_percentile}, {self.max_pix_percentile})\n" \
                          f"zoom: {self.zoom_factors[self.zoom_index]}x\n" \
                          f"brush size (pixels): {self.brush_size}\n" \
                          f"frames per second: {self.fps}\n" \
                          f"current slice: {self.curslice + 1}\n" \
                          f"\tnumber of fiducials: {len(self.fiducials[self.curslice])}\n" \
                          f"\tnumber of polylines: {len(self.polylines[self.curslice])}"

        return the_string

    def copy_annotations(self, arange: Optional[Tuple[int, int]] = None) -> Tuple:
        if not arange:
            arange = (0, self.n_frames)

        return (copy.deepcopy(self.fiducials[arange[0]:arange[1]]),
                [[QtGui.QPolygonF(apolyline) for apolyline in atimepoint]
                 for atimepoint in self.polylines[arange[0]:arange[1]]],
                copy.deepcopy(self.polyline_ids[arange[0]:arange[1]]))

    def paste_annotations(self, theannotations: Tuple, arange: Optional[Tuple[int, int]] = None) -> bool:
        if len(theannotations) == 3:
            fiducials, polylines, polyline_ids = theannotations
        else:
            return False

        if not arange:
            arange = (0, self.n_frames)

        self.fiducials[arange[0]:arange[1]] = fiducials
        self.polylines[arange[0]:arange[1]] = polylines
        self.polyline_ids[arange[0]:arange[1]] = polyline_ids

        return True

    def get_key_bindings(self):
        key_bindings = {}
        for this_menu in self.menubar.children():
            if type(this_menu) == QtWidgets.QToolButton:
                continue  # the menubar also has a tool button that is not one of the dropdown menus
            these_shortcuts = {}
            for this_action in self.get_menu_children(this_menu):
                these_shortcuts[this_action.text()] = this_action.shortcut().toString()
            key_bindings[this_menu.title()] = these_shortcuts
        return key_bindings

    def get_menu_children(self, menu: QtWidgets.QMenu) -> list:
        menu_actions = menu.actions()
        menu_children = []
        for this_action in menu_actions:
            if this_action.isSeparator():  # Separator
                continue
            elif menu.menuInAction(this_action) is not None:  # Submenu
                menu_children.extend(self.get_menu_children(menu.menuInAction(this_action)))
            else:  # Action connected to a callback function
                menu_children.append(this_action)
        return menu_children



    def paint_active_element(self, x: int, y: int) -> QtWidgets.QAbstractGraphicsShapeItem:
        if self.annotation_mode in self.fiducial_highlight_modes:
            object_types = QtWidgets.QGraphicsEllipseItem
        elif self.annotation_mode in self.polyline_highlight_modes:
            object_types = QtWidgets.QGraphicsPolygonItem
        else:
            object_types = (QtWidgets.QGraphicsPolygonItem, QtWidgets.QGraphicsEllipseItem)
        scene_element = self.findGraphicItem(x, y, object_types)

        if self.active_element is not None and self.active_element != scene_element:
            # return previous active element to normal colour
            pen = QtGui.QPen()
            if isinstance(self.active_element, QtWidgets.QGraphicsPolygonItem):
                pen.setWidth(self.brush_size)
                pen.setColor(PyJAMAS.polyline_color)
            else:
                pen.setBrush(PyJAMAS.fiducial_brush_style)
                pen.setColor(PyJAMAS.fiducial_color)
            self.active_element.setPen(pen)
            if self.active_element.data(0) is not None:  # Change ID color if present
                self.active_element.data(0).setDefaultTextColor(pen.color())
            self.active_element = None

        if scene_element is not None:
            self.active_element = scene_element  # store pointer to active element
            pen = self.active_element.pen()
            pen.setColor(PyJAMAS.highlight_color)
            self.active_element.setPen(pen)
            if self.active_element.data(0) is not None:  # Change ID color if present
                self.active_element.data(0).setDefaultTextColor(pen.color())

        return self.active_element


def main():
    aPyJAMA: PyJAMAS = PyJAMAS()
    sys.exit(aPyJAMA.app.exec())


if __name__ == '__main__':
    main()
