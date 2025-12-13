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

from pyjamas import pjscore, pjseventfilter, pjsthreads, rutils, dragdropmainwindow
from .version import __version__

name = "pyjamas"

# Re-export names at top-level namespace
PyJAMAS = pjscore.PyJAMAS
PJSEventFilter = pjseventfilter.PJSEventFilter
ThreadSignals = pjsthreads.ThreadSignals
Thread = pjsthreads.Thread
RUtils = rutils.RUtils
SizedStack = rutils.SizedStack
DragDropMainWindow = dragdropmainwindow.DragDropMainWindow

__all__ = [
    "PyJAMAS",
    "PJSEventFilter",
    "ThreadSignals",
    "Thread",
    "RUtils",
    "SizedStack",
    "DragDropMainWindow",
    "__version__",
]

