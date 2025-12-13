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

import enum
from types import SimpleNamespace as NS


NAMESPACE = NS(
    cc="http://creativecommons.org/ns#",
    dc="http://purl.org/dc/elements/1.1/",
    dunnart="http://www.dunnart.org/ns/dunnart",
    inkscape="http://www.inkscape.org/namespaces/inkscape",
    rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    sodipodi="http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
    svg="http://www.w3.org/2000/svg",
    xlink="http://www.w3.org/1999/xlink",
)

# Dunnart codes

class Direction(enum.IntEnum):
    GUIDE_TYPE_VERT = 100
    GUIDE_TYPE_HORI = 101


class Handle(enum.IntFlag):
    HAN_TOP    = 1
    HAN_BOT    = 2
    HAN_LEFT   = 4
    HAN_RIGHT  = 8
    HAN_HANDLE = 16
    HAN_CONNPT = 32
    HAN_CENDPT = 64
    HAN_SRC    = 128
    HAN_DST    = 256
    HAN_CENTER = 512
    HAN_POINT  = 1024
    HAN_SEPARA = 2048


class FlowDirection(enum.IntEnum):
    FlowDown  = 0
    FlowLeft  = 1
    FlowUp    = 2
    FlowRight = 3


class LayeredAlignment(enum.IntEnum):
    ShapeMiddle = 0
    ShapeStart = 1
    ShapeEnd = 2


class LayoutMode(enum.IntEnum):
    OrganicLayout = 0
    FlowLayout    = 1
    LayeredLayout = 2


class OptimizationMethod(enum.IntEnum):
    MAJORIZATION = 0
    STEEPESTDESCENT = 1
