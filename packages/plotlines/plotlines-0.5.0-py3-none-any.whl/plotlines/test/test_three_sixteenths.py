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


from collections import defaultdict
from collections import Counter
from fractions import Fraction
import itertools
from turtle import Vec2D as V
import unittest

from plotlines.three_sixteenths import Grid


class GridTests(unittest.TestCase):

    def test_markers(self):
        for n in range(7):
            with self.subTest(n=n):
                rv = Grid.build_markers(n)
                self.assertEqual(len(rv), n)
                self.assertEqual(len({i.value for i in rv}), n)

    def test_init(self):
        grid = Grid.build()
        self.assertEqual(len(grid.markers), 4)
        self.assertEqual(set(grid.markers), {1, 2, 3, 4})
        self.assertEqual(len(grid.cells), 16)
        self.assertIn((0, 0), grid.cells)

    def test_cell_values(self):
        grid = Grid.build()
        rows = defaultdict(list)
        for cell in grid.cells.values():
            rows[cell.spot[0]].append(cell)

        for row in rows:
            with self.subTest(row=row):
                cells = rows[row]
                if row in [0, 2]:
                    self.assertEqual([cell.value for cell in cells], [1, 7, 1, 7])
                elif row in [1, 3]:
                    self.assertEqual([cell.value for cell in cells], [3, 5, 3, 5])

    def test_makers_aligned(self):
        grid = Grid.build()
        rows = defaultdict(list)
        grid.mark(grid.Cell(V(0, 1)), grid.Cell(V(1, 0)), grid.Cell(V(2, 1)), grid.Cell(V(3, 2)))
        self.assertTrue(grid.markers[1].cell.transits(grid.markers[2].cell))
        self.assertTrue(grid.markers[2].cell.transits(grid.markers[1].cell))
        self.assertTrue(grid.markers[2].cell.transits(grid.markers[3].cell))
        self.assertTrue(grid.markers[2].cell.transits(grid.markers[4].cell))
        self.assertTrue(grid.markers[3].cell.transits(grid.markers[2].cell))
        self.assertTrue(grid.markers[3].cell.transits(grid.markers[4].cell))
        self.assertTrue(grid.markers[4].cell.transits(grid.markers[3].cell))
        self.assertTrue(grid.markers[4].cell.transits(grid.markers[2].cell))
        self.assertFalse(grid.markers[4].cell.transits(grid.markers[1].cell))
        self.assertFalse(grid.markers[3].cell.transits(grid.markers[1].cell))
        self.assertFalse(grid.markers[1].cell.transits(grid.markers[3].cell))
        self.assertFalse(grid.markers[1].cell.transits(grid.markers[4].cell))

    def test_marker_zone(self):
        grid = Grid.build()
        grid.mark(grid.Cell(V(1, 0)), grid.Cell(V(0, 2)), grid.Cell(V(2, 1)), grid.Cell(V(3, 2)))

        witness = set()
        for marker in grid.markers.values():
            with self.subTest(marker=marker):
                self.assertEqual(len(marker.zone), 4, marker.zone)
                self.assertFalse(witness.intersection(set(marker.zone)))
                witness = witness.union(set(marker.zone))

    def test_marker_results(self):
        m = Grid.Marker(0, value=Fraction(1, 9))

        self.assertEqual(sorted(m.results(0)), [Fraction(1, 9)])
        self.assertEqual(sorted(m.results(1)), [Fraction(2, 9)])
        self.assertEqual(sorted(m.results(3)), [Fraction(4, 9), Fraction(1, 2), Fraction(2, 1)])

    def test_partition(self):
        witness = Counter()
        grid = Grid.build()
        for n in range(100):
            rv = grid.partition()
            with self.subTest(n=n, rv=rv):
                self.assertEqual(len(set(rv)), 4, rv)
                for pair in itertools.product(rv, repeat=2):
                    if pair[0] == pair[1]:
                        continue

                    self.assertFalse(pair[0].transits(pair[1]), pair)
                    witness[frozenset(rv)] += 1

        self.assertLessEqual(len(witness), 56)
