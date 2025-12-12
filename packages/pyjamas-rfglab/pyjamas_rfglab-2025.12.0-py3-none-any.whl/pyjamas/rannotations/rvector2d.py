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

import numpy

from pyjamas.rannotations import *


class RVector2D(rannotation.RAnnotation):
    '''
    Represents a vector by providing an origin (list, tuple, ndarray, etc),
    and the vector coordinates as a function of that origin.
    '''

    # Define static variables here.

    def __init__(self, origin: object, end: object):
        """
        Creates a 2D vector.

        :param origin: list, tuple, ndarray, ... Internally, a numpy.ndarray. (x, y) coordinates of the origin point.
        :param end: list, tuple, ndarray, ... Internally, a numpy.ndarray. (x, y) coordinates of the vector components).
        """

        super().__init__()

        # Define object variables here.
        self.origin = numpy.asarray(origin)  # origin
        self.end = numpy.asarray(end)  # vector coordinates
        self._magnitude = RVector2D.calculate_magnitude(self.origin, self.end)
        self._orientation = RVector2D.calculate_orientation(self.origin, self.end)

    def magnitude(self) -> float:
        return self._magnitude

    def orientation(self) -> float:
        return self._orientation

    @classmethod
    def calculate_magnitude(cls, origin: numpy.ndarray, end: numpy.ndarray) -> float:
        return numpy.linalg.norm(end - origin)

    @classmethod
    def calculate_orientation(cls, origin: numpy.ndarray, end: numpy.ndarray) -> float:
        thevectorcoords = end - origin
        return numpy.rad2deg(numpy.arctan2(thevectorcoords[1], thevectorcoords[0]))
