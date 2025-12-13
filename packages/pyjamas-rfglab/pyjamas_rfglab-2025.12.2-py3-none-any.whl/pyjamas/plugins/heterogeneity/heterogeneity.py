from typing import List

import matplotlib.pyplot as plt
import numpy
import pandas as pd

from pyjamas.rannotations.rpolyline import RPolyline
from pyjamas.rplugins.base import PJSPluginABC

class PJSPlugin(PJSPluginABC):
    def name(self) -> str:
        return 'Heterogeneity'

    def run(self, parameters: dict) -> bool:
        # Array with an index per slice in the image stack.
        slices = numpy.arange(self.pjs.n_frames, dtype=numpy.int16)

        # Find the maximum number of polylines in a slice.
        max_n_polylines = 0
        for i in slices:
            max_n_polylines = max(max_n_polylines, len(self.pjs.polylines[i]))

        # Create a pandas data frame to store the measurements.
        # The data frame will have one column per polyline, and one row per slice in the image.
        n_columns: int = max_n_polylines
        n_rows: int = slices.shape[0]

        column_names: List[str] = ['heterogeneity_' + str(i) for i in range(1, max_n_polylines+1)]

        heterogeneity_df: pd.DataFrame = pd.DataFrame(numpy.nan * numpy.zeros((n_rows, n_columns)), columns=column_names, index=slices+1)

        # For every slice ...
        for i in slices:
            theimage = self.pjs.slices[i]

            # Retrieve the polylines in this slice.
            polygon_slice = self.pjs.polylines[i]

            n_polylines = len(polygon_slice)

            # For every polyline ...
            for j in range(n_polylines):
                # We take advantage of the RPolyline class in PyJAMAS, which contains methods to measure
                # morphology and pixel values for the polyline.
                thepolyline = RPolyline(polygon_slice[j])

                intensities = thepolyline.pixel_values(theimage, self.pjs.brush_size)
                mean_poly = intensities[0]
                std_poly = intensities[2]
                heterogeneity_df.loc[i + 1, 'heterogeneity_' + str(j + 1)] = std_poly / mean_poly

        # Plot results.
        heterogeneity_df.plot()
        plt.xlabel('slice index')
        plt.ylabel('heterogeneity')
        plt.show()

        # Print full results in the terminal.
        with pd.option_context('display.max_rows', None, 'display.max_columns', None):
            print(heterogeneity_df)

        return True

