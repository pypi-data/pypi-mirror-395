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

from __future__ import annotations  # Until Python 3.14 is everywhere

import math


class Coordinates(tuple):

    def __new__(cls, *args, coerce=None):
        if coerce:
            args = [coerce(i) for i in args]
        return tuple.__new__(cls, args)

    def __abs__(self):
        return math.hypot(*self)

    def __getnewargs__(self):
        return self

    def __add__(self, other):
        return self.__class__(*[a + b for a, b in zip(self, other)])

    def __sub__(self, other):
        return self.__class__(*[a - b for a, b in zip(self, other)])

    def __mul__(self, other):
        return self.__class__(*[other * i for i in self])

    def __rmul__(self, other):
        return self.__mul__(other)

    def __floordiv__(self, other):
        return self.__class__(*[i // other for i in self])

    def __truediv__(self, other):
        return self.__class__(*[i / other for i in self])

    def __repr__(self):
        return "< {0} >".format(", ".join(f"{i}" for i in self))

    @staticmethod
    def intercept(origin: Component, transit: Component, point: Component) -> Component:
        "Find the normal intercept from a point to a line between origin and transit"
        try:
            shadow = (point - origin).unity.dot((transit - origin).unity) * abs(point - origin)
            return origin + (transit - origin) * shadow / abs(transit - origin)
        except TypeError:
            return None

    @property
    def unity(self):
        try:
            return self / abs(self)
        except ZeroDivisionError:
            return self

    def dot(self, other):
        return math.sumprod(self, other)
