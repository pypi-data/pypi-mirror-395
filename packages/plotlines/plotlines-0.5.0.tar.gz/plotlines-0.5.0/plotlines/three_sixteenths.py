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
"""
Three-sixteenths is a game for four players.

It takes place on a board of sixteen squares.
Each quadrant of the board is guarded by the marker of one player.
The squares of each quadrant are labelled with the numbers 1, 3, 7, and 5
going clockwise from the bottom left corner.

The markers are knitting counters, which have two rotating registers labelled 0 to 9.
The value of each counter is calculatred as a fraction, ie: the top digit divided by the bottom.

At the beginning of the game each player selects a unique value for his counter.
The lower digit must be 9. The upper digit may be any which preserves the value as a ninth, eg: 1, 2, 4, 5, 7 or 8.

Each player places his counter on a square within his quadrant. It must be placed so that it does not
lie on a diagonal with any other.

Play proceeds clockwise, sequentially. On each turn, a player moves his counter to a new square in his quadrant.
He then adjusts the value of his counter by indexing either or both of the registers, by one digit at a time,
in total as many times as indicated by the number of the square.

The following rules apply to values of a counter:
* The divisor may not finish on zero (ie: infinity is not allowed).
* A value may be factored down, eg: 3/6 may be redialled as 1/2.

Following a move and an update of the counter, a player may 'attack' another if their markers lie on a diagonal.
An attack allows a player to multiply the value of his counter with the value of the counter he attacks.

A player wins the round if the result of his attack equals 3/16.

"""

import argparse
from collections import Counter
from collections import namedtuple
import dataclasses
import datetime
from decimal import Decimal
from fractions import Fraction
import itertools
import json
import logging
import pprint
import random
import statistics
import sys
import turtle


class Grid:

    Option = namedtuple("Option", ["marker", "cell", "result", "transit", "total"], defaults=[None, None])

    @dataclasses.dataclass(frozen=True)
    class Cell:
        spot: turtle.Vec2D

        @property
        def value(self) -> int:
            return {
                0: {0: 1, 1: 7},
                1: {0: 3, 1: 5},
            }[int(self.spot[0]) % 2][int(self.spot[1]) % 2]

        def transits(self, cell: "Cell") -> bool:
            vector = cell.spot - self.spot
            return abs(vector[0]) == abs(vector[1])

    @dataclasses.dataclass
    class Marker:
        id: int
        value: Fraction = None
        grid: "Grid" = None
        cell: "Cell" = None

        @property
        def zone(self):
            try:
                quadrant = tuple(i // 2 for i in self.cell.spot)
                return [spot for spot in self.grid.cells if tuple(i // 2 for i in spot) == quadrant]
            except AttributeError:
                return []

        def results(self, cardinal: int):
            for n, d in zip(range(0, cardinal + 1), range(cardinal, -1, -1)):
                try:
                    yield Fraction(
                        (self.value.numerator + n) % 10,
                        (self.value.denominator + d) % 10,
                    )
                except ZeroDivisionError:
                    pass

        def options(self, cell: "Cell"):
            transits = [m for m in self.grid.markers.values() if m is not self and m.cell.transits(cell)]
            for r in self.results(cell.value):
                yield self.grid.Option(self, cell, r)
                for t in transits:
                    val = r * t.value
                    yield self.grid.Option(self, cell, r, t, val)

    @classmethod
    def build_markers(cls, k=4):
        return [
            cls.Marker(id=n+1, value=v)
            for n, v in enumerate(random.sample(
                [Fraction(n, 9) for n in [1, 2, 4, 5, 7, 8]],
                k
            ))
        ]

    @classmethod
    def build(cls, n_sectors=4, n_regions=4):
        rv = cls(markers=cls.build_markers(k=n_sectors))
        size = int(Decimal(n_sectors).sqrt() * Decimal(n_regions).sqrt())
        rv.cells = {
            pos: cls.Cell(turtle.Vec2D(*pos))
            for pos in itertools.product(range(size), repeat=2)
        }
        return rv

    def __init__(self, markers: list = None, cells: dict = None):
        self.markers = {i.id: i for i in markers}
        for mark in self.markers.values():
            mark.grid = self

        self.cells = cells or dict()

    def partition(self) -> list["Cell"]:
        markers = []
        pool = set(self.cells.values())
        while len(markers) < len(self.markers):
            cell = random.choice(list(pool))
            if not any(cell in m.zone for m in markers):
                m = self.Marker(len(markers), grid=self, cell=cell)
                if not any(m.cell.transits(i.cell) for i in markers):
                    markers.append(m)
                    zone = [self.Cell(spot=spot) for spot in m.zone]
                    pool = pool - set(zone)
        return [m.cell for m in markers]

    def mark(self, *args: tuple["Cell"]):
        for cell, marker in zip(args, self.markers.values()):
            marker.cell = self.cells[cell.spot]
        return self


def game(grid, limit=sys.maxsize, goal = Fraction(3, 16)):
    logger = logging.getLogger()

    moves = []
    n = 0
    while n < limit:
        for marker in grid.markers.values():
            options = list()
            for spot in marker.zone:
                cell = grid.cells[spot]
                if cell != marker.cell:
                    options.extend(marker.options(cell))

            chosen = next((i for i in options if i.total == goal), random.choice(options))
            marker.cell = chosen.cell
            marker.value = chosen.result
            logger.info(
                f"Player {marker.id} moves to {marker.cell.spot}[{marker.cell.value}]. "
                f"Takes value {marker.value}."
            )
            moves.append(chosen)
            if chosen.total == goal:
                logger.info(
                    f"Player {marker.id} wins against player {chosen.transit.id}. "
                    f"({marker.value} * {chosen.transit.value} = {goal})."
                )
                return moves

        n += 1
    return moves


def run():
    ts = datetime.datetime.now(tz=datetime.timezone.utc)
    parser = argparse.ArgumentParser(usage=__doc__)
    parser.add_argument("-n", dest="rounds", type=int, default=1, help="Set the number of rounds to play [1]")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.info("Three-sixteenths by D E Haynes.")

    score = Counter()
    turns = []
    for n in range(args.rounds):
        grid = Grid.build()
        grid.mark(*grid.partition())
        for marker in grid.markers.values():
            logger.info(
                f"Player {marker.id} first at {marker.cell.spot}[{marker.cell.value}]. "
                f"Takes value {marker.value}."
            )

        moves = game(grid, limit=100000)
        logger.info(f"Round ends after {len(moves)} moves.")

        score[moves[-1].marker.id] += 1
        turns.append(len(moves))

    record = dict(
        turns=Counter(sorted(turns)),
        ts=ts.isoformat(),
        rounds=args.rounds,
        min=min(turns),
        max=max(turns),
        mode=statistics.mode(turns),
        score=score,
    )
    logger.info(f"Moves: min {record['min']}, max {record['max']}, mode {record['mode']}")
    print(json.dumps(record, indent=0), "\n", file=sys.stdout)


if __name__ == "__main__":
    run()
