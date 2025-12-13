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
import sys
from typing import Optional

import numpy
import pandas as pd
from PyQt6 import QtWidgets
import skimage.filters as skif

from pyjamas.rimage.rimutils import rimutils
from pyjamas.rutils import RUtils
import pyjamas.dialogs.measurepoly as measurepoly
import pyjamas.rannotations.rpolyline as rpolyline
from pyjamas.rcallbacks.rcallback import RCallback


class RCBMeasure(RCallback):
    GAUSSIAN_SIGMA: float = 10.0

    def cbMeasurePoly(self, firstSlice: Optional[int] = None, lastSlice: Optional[int] = None,
                      measurements: Optional[dict] = None, filename: Optional[str] = None) -> dict:
        """
        Measure polylines.

        A dialog will be opened if any parameters are set to None.

        :param firstSlice: slice number for the first slice to use (minimum is 1).
        :param lastSlice: slice number for the last slice to use.
        :param measurements: dictionary with the following keys:

            ``area``:
                True|False
            ``perimeter``:
                True|False
            ``pixels``:
                True|False
            ``image``:
                True|False
            ``sample``:
                True|False
        :param filename: path and file name where the measurement results will be saved; results are saved in .csv format. If filename=='', no results are saved.
        :return: dictionary with measurement results.
        """

        theresults = {}

        # Create and open dialog for measuring polygons.
        if filename is False or filename is None or \
                firstSlice is False or firstSlice is None or lastSlice is False or lastSlice is None:
            # Create a measurement dialog that allows input of all this at once (unless all the parameters are given as arguments).
            dialog = QtWidgets.QDialog()
            ui = measurepoly.MeasurePolyDialog()

            firstSlice = self.pjs.curslice + 1
            lastSlice = 1 if self.pjs.n_frames == 1 else self.pjs.slices.shape[0]
            ui.setupUi(dialog, savepath=self.pjs.cwd, firstslice=firstSlice, lastslice=lastSlice)
            dialog.exec()
            dialog.show()
            # If the dialog was closed by pressing OK, then run the measurements.
            continue_flag = dialog.result() == QtWidgets.QDialog.DialogCode.Accepted
            themeasurements = ui.measurements()
            dialog.close()

        else:
            if firstSlice > lastSlice:
                firstSlice, lastSlice = lastSlice, firstSlice

            if filename not in ('', -1):
                filename = RUtils.set_extension(filename, '.csv')

            if measurements is False or measurements is None:
                themeasurements = {
                    'path': filename,
                    'first': firstSlice,
                    'last': lastSlice,
                    'area': True,
                    'perimeter': True,
                    'pixels': True,
                    'image': True,
                    'sample': False
                }

            else:
                themeasurements = {
                    'path': filename,
                    'first': firstSlice,
                    'last': lastSlice,
                    'area': measurements.get('area', False),
                    'perimeter': measurements.get('perimeter', False),
                    'pixels': measurements.get('pixels', False),
                    'image': measurements.get('image', False),
                    'sample': measurements.get('sample', False)
                }

            continue_flag = True

        if continue_flag:
            theslicenumbers = numpy.arange(themeasurements['first'] - 1, themeasurements['last'])

            theresults = self.measurePolygons(themeasurements, theslicenumbers)

            # If a file name was entered, save the data.
            if themeasurements["path"] not in ('', -1):
                # RUtils.write_dict_csv(filename, theresults)
                # results_df = pd.DataFrame(theresults)
                theresults.to_csv(themeasurements['path'])
                self.pjs.statusbar.showMessage(f'Saved measurements to {themeasurements.get("path")}.')

            elif themeasurements["path"] == '':
                with pd.option_context('display.max_columns', sys.maxsize):
                    print(theresults)
                self.pjs.statusbar.showMessage(f'Measurement results displayed in terminal.')

            elif themeasurements["path"] == -1:
                self.pjs.statusbar.showMessage(f'Measurements completed.')

        return theresults

    def measurePolygons(self, measurements: dict, slices: numpy.ndarray) -> pd.DataFrame:
        # todo: add other measurements: heterogeneity, shape factor, edge-to-centre distance profile, etc.
        # todo: change lists from dictionary into numpy.ndarrays.

        # Returns a pandas DataFrame in which columns represent time points and rows correspond to image statistics or polylines.
        # :param measurements:
        # :param slices: slice indexes -start at 0-, not numbers -start at 1-.
        # :return:

        # Create dictionary with results.
        n_image_metrics: int = 3
        n_polyline_metrics: int = 6
        # Find the maximum polyline id.
        max_n_polylines = max(max(self.pjs.polyline_ids))

        row_names = ['slice_number', 'image_mean', 'image_mode']
        row_names.extend(['area_' + str(i) for i in range(1, max_n_polylines + 1)])
        row_names.extend(['perimeter_' + str(i) for i in range(1, max_n_polylines + 1)])
        row_names.extend(['pixel_values_perimeter_' + str(i) for i in range(1, max_n_polylines + 1)])
        row_names.extend(['pixel_values_interior_' + str(i) for i in range(1, max_n_polylines + 1)])
        row_names.extend(['std_perimeter_' + str(i) for i in range(1, max_n_polylines + 1)])
        row_names.extend(['std_interior_' + str(i) for i in range(1, max_n_polylines + 1)])

        rows: int = n_image_metrics + n_polyline_metrics * max_n_polylines
        columns: int = slices.shape[0]

        measurement_df: pd.DataFrame = pd.DataFrame(numpy.nan * numpy.zeros((rows, columns)), columns=slices + 1,
                                                    index=row_names)

        # If supposed to use a background file, load it ...
        if measurements.get('pixels') and not measurements.get('image') and not measurements.get('sample'):
            bgfilepath = RUtils.set_extension(self.pjs.filename, self.pjs.backgroundimage_extension)
            if os.path.exists(bgfilepath):
                bgstack = rimutils.read_stack(bgfilepath)
            else:
                self.pjs.statusbar.showMessage("Background file not found, reverting to image mean and mode.")
                measurements['image'] = True

        # For every slice ...
        for i in slices:
            # When indexing a DataFrame, the i+1 is the name of the column, not an index.
            measurement_df.loc['slice_number', i + 1] = i + 1

            theimage = self.pjs.slices[i]

            # Find the polylines in this slice.
            polygon_slice = self.pjs.polylines[i]

            # For every polyline ...
            for thepolyid in range(1, max_n_polylines + 1):
                try:
                    thepolyindex = self.pjs.polyline_ids[i].index(thepolyid)
                except ValueError:
                    continue

                # Create a polyline and measure it:
                thepolyline = rpolyline.RPolyline(polygon_slice[thepolyindex])

                # Areas.
                if measurements.get('area'):
                    # Create a polyline and calculate the area.
                    measurement_df.loc['area_' + str(thepolyid), i + 1] = thepolyline.area()

                # Perimeters.
                if measurements.get('perimeter'):
                    measurement_df.loc['perimeter_' + str(thepolyid), i + 1] = thepolyline.perimeter()

                # Pixel values.
                if measurements.get('pixels'):
                    intensities = thepolyline.pixel_values(theimage, self.pjs.brush_size)
                    measurement_df.loc['pixel_values_perimeter_' + str(thepolyid), i + 1] = intensities[0]
                    measurement_df.loc['pixel_values_interior_' + str(thepolyid), i + 1] = intensities[1]
                    measurement_df.loc['std_perimeter_' + str(thepolyid), i + 1] = intensities[2]
                    measurement_df.loc['std_interior_' + str(thepolyid), i + 1] = intensities[3]

            # Image statistics.
            if measurements.get('image'):
                measurement_df.loc['image_mean', i + 1] = numpy.mean(theimage)

                themode = rimutils.mode(theimage)
                measurement_df.loc['image_mode', i + 1] = themode

            if measurements.get('sample'):
                mask = skif.gaussian(numpy.asarray(theimage, dtype=float), RCBMeasure.GAUSSIAN_SIGMA) > numpy.median(
                    theimage)  # also tested the mode here, but the results are very noisy.
                measurement_df.loc['image_mean', i + 1] = numpy.mean(theimage[mask])

                themode = rimutils.mode(theimage[mask])
                measurement_df.loc['image_mode', i + 1] = themode

            # If file-based background subtraction ...
            if measurements.get('pixels') and not measurements.get('image') and not measurements.get('sample'):
                # if the background files has as many slices as the image, use the corresponding slice
                if bgstack.ndim == 3 and bgstack.shape[0] == self.pjs.slices.shape[0]:
                    measurement_df.loc['image_mean', i + 1] = numpy.mean(bgstack[i])

                    themode = rimutils.mode(bgstack[i])
                    measurement_df.loc['image_mode', i + 1] = themode

                # if the number of slices does not match, use the first slice for the background file
                elif bgstack.ndim == 3:
                    measurement_df.loc['image_mean', i + 1] = numpy.mean(bgstack[0])

                    themode = rimutils.mode(bgstack[0])
                    measurement_df.loc['image_mode', i + 1] = themode

                # if the background file has a single slice, use that
                elif bgstack.ndim == 2:
                    measurement_df.loc['image_mean', i + 1] = numpy.mean(bgstack)

                    themode = rimutils.mode(bgstack)
                    measurement_df.loc['image_mode', i + 1] = themode

        return measurement_df
