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


from collections.abc import Callable
from collections import namedtuple
from fractions import Fraction
import functools
import math

Finite = namedtuple("Finite", ["min", "max", "modulus", "type"], defaults=[None, int])


class Bezier:

    def __init__(self, *args):
        self.points = args
        self.coefficients = dict()

    @property
    def order(self) -> int:
        return len(self.points) - 1

    def bernstein(self, index: int, order=None) -> int:
        f = math.factorial
        return self.coefficients.setdefault(
            (index, order),
            Fraction(f(order), f(index) * f(order - index))
        )

    def blend(self, pos, coerce: type = float) -> list[Callable]:
        return [
            functools.partial(self.basis, pos=pos, index=n, order=self.order, coerce=coerce)
            for n, _ in enumerate(self.points)
        ]

    def basis(self, point, *, pos: float | int, index: int, order: int, coerce: type):
        coeff = self.bernstein(index, order)
        k = coeff * pos ** index * (1 - pos) ** (order - index)
        rv = coerce(k) * point
        return rv

    def __call__(self,  pos: float | int):
        coerce = type(pos)
        blend = self.blend(pos, coerce=coerce)
        vals = [fn(p) for fn, p in zip(blend, self.points)]
        try:
            return sum(vals[1:], start=vals[0])
        except IndexError:
            return (vals or None) and vals[0]
