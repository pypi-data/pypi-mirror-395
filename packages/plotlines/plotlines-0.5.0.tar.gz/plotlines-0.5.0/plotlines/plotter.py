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

from collections import Counter
from collections import defaultdict
from collections import deque
from decimal import Decimal
from fractions import Fraction
import importlib.resources
import itertools
import logging
import math
import operator
import statistics
import sys
import tkinter as tk
import turtle
from types import SimpleNamespace

from plotlines.board import Board
from plotlines.board import Edge
from plotlines.board import Node
from plotlines.board import Pin
from plotlines.coordinates import Coordinates as C
from plotlines.motif import Motif


class Plotter:

    def __init__(self, b: Board, t = None):
        self.board = b
        self.turtle = t or turtle.RawTurtle(None)
        self.stamps = dict()
        try:
            self.words = self.build_words()
        except Exception:
            self.words = dict()

    def build_shape(self, size, scale=1) -> turtle.Shape:
        key = f"sq{size:.02f}x{size:.02f}-{scale}"
        try:
            return self.board.shapes[key]
        except KeyError:
            unit = scale * size / 2
            shape = turtle.Shape(
                "polygon", (
                    (-unit, -unit),
                    (unit, -unit),
                    (unit, unit),
                    (-unit, unit))
            )
            shape.key = key
            self.board.shapes[key] = shape
            self.turtle.screen.register_shape(key, shape)
            return shape

    @staticmethod
    def build_words() -> dict[int, list[str]]:
        text = importlib.resources.read_text("plotlines", "assets/words.txt")
        words = text.splitlines()
        return words

    @staticmethod
    def build_graph(
        limit: int,
        ending: int,
        exits: int = 2,
        steps: int = sys.maxsize,
        mode: str = "rtl",
        builder: type = Motif,
        **kwargs
    ) -> Generator[Node | Edge]:

        fwd = mode == "ltr"
        trails = {} # A walk in G where no Edge is repeated
        zones = defaultdict(list)
        state = SimpleNamespace(step=0, spare=limit, zone=0 if fwd else limit, motif=builder())

        endings = [f"ending_{i + 1:02d}" for i in range(ending)]
        zones[state.zone].extend(Node(label=i, zone=state.zone) for i in endings)
        state.tally = Counter({Node: len(endings)})

        while state.step < steps:
            group = list(itertools.chain.from_iterable(zones.values()))
            if state.step == 0:
                yield from group

            state.step += 1
            state.ratio = Fraction(state.tally[Node] + state.tally[Edge], limit - exits)
            for n, item in enumerate(
                state.motif(
                    group,
                    ratio=state.ratio,
                    exits=exits,
                    zone=state.zone,
                    fwd=fwd,
                    **kwargs
                )
            ):

                try:
                    state.zone = max(state.zone, item.zone) if fwd else min(state.zone, item.zone)
                except AttributeError:
                    pass

                item.state = state
                state.tally[type(item)] += 1
                state.spare = limit - state.tally[Node] - state.tally[Edge]

                zones[state.zone].append(item)
                yield item

                if state.spare <= 0:
                    break

    @staticmethod
    def node_size(node: Node):
        connections = node.connections
        lhs_sizes = {edge: math.sqrt(edge.ports[1].area) for edge in connections[0]}
        rhs_sizes = {edge: math.sqrt(edge.ports[0].area) for edge in connections[1]}
        height = max(sum(lhs_sizes.values()), sum(rhs_sizes.values()), math.sqrt(node.area))
        return height

    @staticmethod
    def expandex(length: int):
        "Generate indexes from the middle outwards"
        mid = length // 2
        up = range(mid, length)
        dn = range(mid - 1, -1, -1)
        for i, j in itertools.zip_longest(up, dn):
            for x in (i, j):
                if x is not None:
                    yield x

    @staticmethod
    def place_items(items: list = None, boundary: tuple = None, visited=None):
        visited = set() if visited is None else visited
        work = list()
        sizes = {item: Plotter.node_size(item) for item in items if isinstance(item, Node)}
        zones = dict(
            [
                (key, list(group))
                for key, group in itertools.groupby(
                    sorted((item for item in items if isinstance(item, Node)), key=operator.attrgetter("zone")),
                    key=operator.attrgetter("zone")
                )
            ]
        )

        offset_x = 0
        width_x = 0
        for zone, nodes in zones.items():
            space_y = ((boundary[2] - boundary[0])[1] - sum(sizes[i] for i in nodes)) / (2 * len(nodes) + 1)
            for n, node in enumerate(nodes):
                lhs_edges = {edge: math.sqrt(edge.ports[1].area) for edge in node.edges if node.uid in edge.ports[1].joins}
                rhs_edges = {edge: math.sqrt(edge.ports[0].area) for edge in node.edges if node.uid in edge.ports[0].joins}
                node.height = max(sum(lhs_edges.values()), sum(rhs_edges.values()))
                node.width = max(node.height, math.sqrt(node.area))
                width_x = max(width_x, node.width)

                # Allocate coordinates from lhs of boundary
                node.pos = C(
                    boundary[0][0] + offset_x + node.width / 2,
                    boundary[0][1] + n * space_y + node.height / 2,
                )

                visited.add(node)
                visited.add(node.pos)

                for n, (edge, size) in enumerate(lhs_edges.items()):
                    if n == 0:
                        pos = node.pos - C(node.width / 2, size / 2 + sum(lhs_edges.values()) / 2)
                    pos += C(0, size)
                    edge.ports[1].pos = pos
                for n, (edge, size) in enumerate(rhs_edges.items()):
                    if n == 0:
                        pos = node.pos - C(node.width / -2, size / 2 + sum(rhs_edges.values()) / 2)
                    pos += C(0, size)
                    edge.ports[0].pos = pos
            yield zone, nodes

            edge_length = 2 * width_x
            offset_x += width_x + edge_length
            width_x = 0

    def layout_board(self, size, threshold=0.1, limit: int = None, **kwargs) -> dict:
        limit = limit or 2 * len(self.board.items)
        nodes = set(i for i in self.board.items if isinstance(i, Node))
        placed = set()

        boundary = [C(0, 0), C(0, size[0]), C(size[1], 0), C(*size)]
        zones = dict(self.place_items(self.board.items, boundary=boundary))

        step = 0
        crowding = {0: 0}
        while step < limit and statistics.median(crowding.values()) < threshold:
            step += 1
            crowding = {
                z: min([
                    val
                    for node in zone
                    for other in zone
                    for item in other.nearby + other.edges
                    for val in node.spacing(item).values()
                    if val != 0
                ] + [sys.maxsize])
                for z, zone in zones.items()
            }
            crowded = {v: k for k, v in crowding.items()}.get(min(crowding.values()))
            zone = zones[crowded]
            for n, index in enumerate(self.expandex(len(zone))):
                node = zone[index]
                if n % 2 == 0:
                    hop = node.height
                else:
                    hop = -node.height
                zone[index].translate(C(0, hop))

        return self.board.items

    def style_items(self, items: list, **kwargs) -> dict:
        screen = self.turtle.getscreen()
        screen.colormode(255)

        frame = self.board.frame(*self.board.extent(items), square=True)
        try:
            screen.setworldcoordinates(*[float(i) for c in frame for i in c])
        except ZeroDivisionError:
            frame = [C(0, 0), C(120, 120)]
            screen.setworldcoordinates(*[float(i) for c in frame for i in c])

        size = screen.screensize()
        scale = self.board.scale_factor(size, frame)

        for item in items:
            try:
                size = max(getattr(item, "width", 0), getattr(item, "height", 0)) or math.sqrt(item.area)
                item.shape = self.build_shape(size=size, scale=scale).key
            except AttributeError:
                assert isinstance(item, Edge)
        return frame, scale

    def draw_items(self, items: list[Edge], debug=False, delay: int = 10) -> RawTurtle:
        screen = self.turtle.getscreen()
        try:
            screen.title(self.board.title)
            screen.delay(delay)
        except AttributeError:
            # Test fixture
            pass

        self.turtle.shape("blank")
        self.turtle.color((0, 0, 0), (255, 255, 255))
        nodes = set()
        for edge in [i for i in items if isinstance(i, Edge)]:
            self.turtle.up()
            for port in edge.ports:
                for node_uid in port.joins:
                    if node_uid in nodes:
                        continue

                    try:
                        node = edge.store[node_uid]
                        self.turtle.shape(node.shape)
                        self.turtle.setpos(node.pos)
                    except AttributeError:
                        pass
                    except KeyError as error:
                        raise
                    except turtle.TurtleGraphicsError:
                        # TODO: Diagnose shape bug
                        pass
                    else:
                        self.stamps[self.turtle.stamp()] = node.shape
                        nodes.add(node_uid)
                        if debug:
                            self.turtle.write(self.turtle.pos())
                    finally:
                        self.turtle.shape("blank")

            if not all(i.pos for i in edge.ports):
                continue

            self.turtle.setpos(edge.ports[0].pos)
            if debug:
                self.turtle.write(self.turtle.pos())
            self.turtle.down()
            self.turtle.setpos(edge.ports[1].pos)
            if debug:
                self.turtle.write(self.turtle.pos())
        return items
