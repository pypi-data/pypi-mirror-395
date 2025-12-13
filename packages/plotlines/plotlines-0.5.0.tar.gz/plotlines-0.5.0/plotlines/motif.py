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


import bisect
from collections import deque
from collections.abc import Generator
from fractions import Fraction
import enum
import random
import sys

from plotlines.board import Board
from plotlines.board import Edge
from plotlines.board import Node
from plotlines.coordinates import Coordinates


class Motif:
    """
    https://heterogenoustasks.wordpress.com/2015/01/26/standard-patterns-in-choice-based-games/

    """

    class Edit(enum.Flag):
        FORK = enum.auto()
        JOIN = enum.auto()
        LINK = enum.auto()
        LOOP = enum.auto()
        STEP = enum.auto()
        COPY = enum.auto()
        FILL = enum.auto()

    def __init__(self):
        self.methods = {
            self.Edit.FORK: 10,
            self.Edit.JOIN: 10,
            self.Edit.LINK: 10,
            self.Edit.LOOP: 10,
        }
        self.edits = []

    def __call__(
        self,
        items: list[Node | Edge],
        ratio: Fraction = None,
        metric = None,
        **kwargs
    ):
        conf, params = self.configure(ratio)
        edit = random.sample(
            list(conf), k=1, counts=list(conf.values())
        )[0]
        method = getattr(self, edit.name.lower())
        kwargs = dict(kwargs, **params)
        rv = list(method(items, **kwargs))
        self.edits.append((edit, len(rv)))
        return rv

    @property
    def config(self):
        return {
            Fraction(1, 10): (
                {self.Edit.FORK: 1},
                {},
            ),
            Fraction(1, 3): (
                {
                    self.Edit.FORK: 1,
                    self.Edit.LINK: 1,
                    self.Edit.LOOP: 1,
                },
                {},
            ),
            Fraction(2, 3): (
                {
                    self.Edit.LINK: 1,
                    self.Edit.LOOP: 1,
                    self.Edit.JOIN: 1,
                },
                {},
            ),
            Fraction(9, 10): (
                {self.Edit.JOIN: 1},
                {},
            ),
            1: (
                {self.Edit.JOIN: 1},
                {},
            ),
        }

    def configure(self, ratio: Fraction):
        keys = list(self.config)
        pos = min(bisect.bisect_left(keys, ratio), len(keys) - 1)
        return self.config[keys[pos]]

    @staticmethod
    def fork(
        items: list[Node | Edge],
        limit: int = None,
        exits: int = 2,
        zone=None,
        fwd=True,
        **kwargs
    ) -> Generator[Node | Edge]:
        if fwd:
            leaves = {i: exits - c for i in items if isinstance(i, Node) and (c := len(i.connections[1])) < exits}
        else:
            leaves = {i: exits - c for i in items if isinstance(i, Node) and (c := len(i.connections[0])) < exits}

        n = 0
        limit = limit or sys.maxsize
        nodes = []
        for n, (item, m) in enumerate(leaves.items()):
            for _ in range(m):
                z = item.zone if zone is None else (fwd and item.zone + n + 1) or item.zone - n - 1
                nodes.append(Node(zone=z))
                if fwd:
                    yield item.connect(nodes[-1])
                else:
                    yield nodes[-1].connect(item)
                n += 2

            if n >= limit:
                break
        yield from nodes

    @staticmethod
    def join(
        items: list[Node | Edge],
        limit: int = None,
        exits: int = 0,
        zone=None,
        fwd=True,
        **kwargs
    ) -> Generator[Node | Edge]:
        if fwd:
            leaves = {i for i in items if isinstance(i, Node) and len(i.connections[0]) == 0}
        else:
            leaves = {i for i in items if isinstance(i, Node) and len(i.connections[1]) == 0}

        n = 0
        limit = limit or sys.maxsize
        group = leaves.copy()
        node = None
        while leaves:
            item = random.choice(list(leaves))
            z = item.zone if zone is None else (fwd and item.zone + n + 1) or item.zone - n - 1
            if not node or len(node.ports) >= (exits or sys.maxsize):
                node = Node(zone=z)
                yield node
                n += 1

            if fwd:
                yield item.connect(node)
            else:
                yield node.connect(item)

            n += 1
            leaves.discard(item)

            if n >= limit:
                break

        while node and exits and len(node.ports) < exits:
            item = random.choice(list(group))
            if fwd:
                yield item.connect(node)
            else:
                yield node.connect(item)

    @staticmethod
    def link(
        items: list[Node | Edge],
        limit: int = None,
        fwd=True,
        **kwargs
    ) -> Generator[Node | Edge]:
        if fwd:
            nodes = [i for i in items if isinstance(i, Node) and i.connections[1]]
        else:
            nodes = [i for i in items if isinstance(i, Node) and i.connections[0]]

        n = 0
        limit = len(nodes) if limit is None else min(limit, len(nodes))
        while n < limit:
            n += 1
            node = random.choice(nodes)
            other = random.choice(node.nearby)
            rv = Node(zone=node.zone)
            yield rv
            if fwd:
                yield node.connect(rv)
                yield rv.connect(other)
            else:
                yield rv.connect(node)
                yield other.connect(rv)

    @staticmethod
    def loop(
        items: list[Node | Edge],
        limit: int = 1,
        fwd=True,
        **kwargs
    ) -> Generator[Node | Edge]:
        if fwd:
            leaves = [i for i in items if isinstance(i, Node) and len(i.connections[1]) == 0]
        else:
            leaves = [i for i in items if isinstance(i, Node) and len(i.connections[0]) == 0]

        n = 0
        limit = len(leaves) if limit is None else min(limit, len(leaves))
        while n < limit:
            try:
                leaf = random.choice(leaves)
                node = random.choice(leaf.nearby)
            except IndexError:
                return

            n += 1
            if fwd:
                yield leaf.connect(node)
            else:
                yield node.connect(leaf)
