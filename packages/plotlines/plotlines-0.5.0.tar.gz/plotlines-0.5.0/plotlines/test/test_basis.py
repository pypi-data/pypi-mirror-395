#! /usr/bin/env python3
# encoding: UTF-8

# This file is part of Plotlines.

# Plotlines is free software: You can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.

# Plotlines is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.

# You should have received a copy of the
# GNU General Public License along with Plotlines.
# If not, see <https://www.gnu.org/licenses/>.


import unittest

from plotlines.basis import Bezier
from plotlines.coordinates import Coordinates


class BernsteinTests(unittest.TestCase):

    def test_empty(self):
        poly = Bezier()
        for i in range(2):
            with self.subTest(i=i):
                self.assertEqual(poly.bernstein(i, order=1), 1)

    def test_n_2(self):
        points = [
            Coordinates(0, 0),
            Coordinates(3, 4),
            Coordinates(5, 0),
        ]
        poly = Bezier(*points)
        self.assertEqual(poly.order, 2)
        self.assertEqual(poly(0), points[0])
        self.assertEqual(poly(1), points[2])

        rv = poly(0.5)
        self.assertIsInstance(rv, Coordinates)
        self.assertEqual(rv, (2.75, 2))
