#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Type aliases for various arrays."""

from numpy import float64, int_
from numpy.typing import NDArray

#: Array of geometrical points.
#: Coordinates of points are in the last dimension so shape should be
#: (*shape, 2) and this coordinates are float
type PointArray = NDArray[float64]

#: Array of indices.
type IndexArray = NDArray[int_]

#: Array for values taken after evaluation of something. Shape can be
#: anything.
type ValueArray = NDArray[float64]
