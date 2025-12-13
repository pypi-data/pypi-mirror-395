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


import math
import pickle
import unittest

from plotlines.coordinates import Coordinates


class CoordinatesTests(unittest.TestCase):

    def test_cardinality(self):
        for n in range(5):
            args = list(range(n))
            with self.subTest(n=n, args=args):
                rv = Coordinates(*args)
                self.assertEqual(len(rv), n)
                self.assertTrue(all(isinstance(i, int) for i in rv))

    def test_coerce(self):
        for n in range(5):
            args = list(range(n))
            with self.subTest(n=n, args=args):
                rv = Coordinates(*args, coerce=complex)
                self.assertEqual(len(rv), n)
                self.assertTrue(all(isinstance(i, complex) for i in rv))

    def test_abs(self):
        c = Coordinates(3, 4)
        rv = abs(c)
        self.assertEqual(rv, 5)

    def test_pickle(self):
        c = Coordinates(3, 4)
        b = pickle.dumps(c)
        d = pickle.loads(b)
        self.assertIsInstance(d, Coordinates)
        self.assertEqual(d, c)

    def test_subtract(self):
        x = Coordinates(1.1, 2.2, 3.3)
        y = Coordinates(0.5, 0.6, 0.7)
        z = x - y
        self.assertIsInstance(z, Coordinates)
        for a, b in zip(z, (0.6, 1.6, 2.6)):
            self.assertAlmostEqual(a, b)

    def test_addition(self):
        x = Coordinates(1.1, 2.2, 3.3)
        y = Coordinates(0.5, 0.6, 0.7)
        z = x + y
        self.assertIsInstance(z, Coordinates)
        for a, b in zip(z, (1.6, 2.8, 4.0, 0.0)):
            self.assertAlmostEqual(a, b)

    def test_multiply_by_int(self):
        z = Coordinates(1.1, 2.2, 3.3) * 3
        self.assertIsInstance(z, Coordinates)
        for a, b in zip(z, (3.3, 6.6, 9.9)):
            self.assertAlmostEqual(a, b)

    def test_multiply_by_float(self):
        z = 3.3 * Coordinates(1, 2, 3)
        self.assertIsInstance(z, Coordinates)
        for a, b in zip(z, (3.3, 6.6, 9.9)):
            self.assertAlmostEqual(a, b)

    def test_scalar_division(self):
        z = Coordinates(3.3, 6.6, 9.9) / 3
        self.assertIsInstance(z, Coordinates)
        for a, b in zip(z, (1.1, 2.2, 3.3)):
            self.assertAlmostEqual(a, b)

    def test_floor_division(self):
        z = Coordinates(3.3, 6.6, 9.9) // 3
        self.assertIsInstance(z, Coordinates)
        for a, b in zip(z, (1, 2, 3)):
            self.assertAlmostEqual(a, b)

    def test_magnitude(self):
        self.assertAlmostEqual(abs(Coordinates(1, 1)), math.sqrt(2))
        self.assertAlmostEqual(abs(Coordinates(1, math.sqrt(3))), 2)
        self.assertAlmostEqual(abs(Coordinates(3, 4)), 5)

    def test_normalised(self):
        self.assertAlmostEqual(abs(Coordinates(1, 1)), math.sqrt(2))
        self.assertAlmostEqual(abs(Coordinates(1, math.sqrt(3)).unity), 1)
        self.assertAlmostEqual(abs(Coordinates(3, 4).unity), 1)

    def test_unity(self):
        pos = Coordinates(0, 0)
        self.assertEqual(pos.unity, pos)

    def test_gt(self):
        self.assertTrue(Coordinates(1, 0, 0) > Coordinates(0, 0, 0))
        self.assertTrue(Coordinates(0, 1, 0) > Coordinates(0, 0, 0))
        self.assertTrue(Coordinates(0, 0, 1) > Coordinates(0, 0, 0))
        self.assertTrue(Coordinates(0, 0, 0) > Coordinates(-1, 0, 0))
        self.assertTrue(Coordinates(0, 0, 0) > Coordinates(0, -1, 0))
        self.assertTrue(Coordinates(0, 0, 0) > Coordinates(0, 0, -1))

    def test_lt(self):
        self.assertTrue(Coordinates(0, 0, 0) < Coordinates(1, 0, 0))
        self.assertTrue(Coordinates(0, 0, 0) < Coordinates(0, 1, 0))
        self.assertTrue(Coordinates(0, 0, 0) < Coordinates(0, 0, 1))
        self.assertTrue(Coordinates(-1, 0, 0) < Coordinates(0, 0, 0))
        self.assertTrue(Coordinates(0, -1, 0) < Coordinates(0, 0, 0))
        self.assertTrue(Coordinates(0, 0, -1) < Coordinates(0, 0, 0))

    def test_max(self):
        self.assertEqual(
            max(Coordinates(1, 0, 0), Coordinates(0, 0, 0)),
            Coordinates(1, 0, 0)
        )
        self.assertEqual(
            max(Coordinates(0, -1, 0), Coordinates(0, 0, 0)),
            Coordinates(0, 0, 0)
        )

    def test_min(self):
        self.assertEqual(
            min(Coordinates(0, 0, 0), Coordinates(1, 0, 0)),
            Coordinates(0, 0, 0)
        )
        self.assertEqual(
            min(Coordinates(0, -1, 0), Coordinates(0, 0, 0)),
            Coordinates(0, -1, 0)
        )

    def test_dot_int(self):
        self.assertEqual(
            Coordinates(2, 3, 1).dot(Coordinates(0, 4, -1)),
            11
        )
        self.assertEqual(
            Coordinates(22, 2, 7).dot(Coordinates(12, -9, 11)),
            323
        )

    def test_dot_float(self):
        self.assertEqual(
            Coordinates(2, 2, 2, 2).dot(Coordinates(4, 1, 2, 1.1)),
            16.2
        )
        self.assertEqual(
            Coordinates(169, 0, 43).dot(Coordinates(0, -375.3, 0)),
            0
        )

    def test_intercept_steps(self):
        # Drop a normal on to a line and measure distance
        a = Coordinates(1, 3)
        b = Coordinates(19, 12)
        c = Coordinates(13, 4)

        shadow = (c - b).unity.dot((a - b).unity) * abs(b - c)
        self.assertAlmostEqual(shadow, 8.9, places=1)

        d = b - (b - a) * shadow / abs(b - a)

        self.assertIsInstance(d, Coordinates)
        self.assertEqual(d, Coordinates(11, 8))

    def test_intercept_steps(self):
        # Drop a normal on to a line and measure distance
        a = Coordinates(1, 3)
        b = Coordinates(19, 12)
        c = Coordinates(13, 4)

        rv = Coordinates.intercept(a, b, c)
        self.assertIsInstance(rv, Coordinates)
        self.assertAlmostEqual(rv[0], 11)
        self.assertAlmostEqual(rv[1], 8)
