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

from collections import defaultdict
from collections.abc import Generator
import dataclasses
from decimal import Decimal
from fractions import Fraction
import functools
import html
import itertools
import logging
import math
from numbers import Number
import sys
import textwrap
import typing
import uuid
import weakref
import xml.etree.ElementTree as ET

from plotlines.coordinates import Coordinates
from plotlines.schema import LayoutMode
from plotlines.schema import OptimizationMethod
from plotlines.schema import NAMESPACE

RGB = functools.partial(Coordinates, coerce=int)


@dataclasses.dataclass(unsafe_hash=True)
class Style:
    stroke:     RGB = dataclasses.field(default=RGB(0, 0, 0), kw_only=True)
    fill:       RGB = dataclasses.field(default=RGB(255, 255, 255), kw_only=True)
    weight:     int = dataclasses.field(default=1, kw_only=True)


@dataclasses.dataclass(unsafe_hash=True)
class Item:
    store: typing.ClassVar[dict] = defaultdict(weakref.WeakValueDictionary)

    id:         int = dataclasses.field(default=0, kw_only=True)
    uid:        uuid.UUID = dataclasses.field(default_factory=uuid.uuid4, kw_only=True)
    style:      Style = dataclasses.field(default_factory=Style, kw_only=True)
    label:      str = dataclasses.field(default="", kw_only=True)
    contents:   list = dataclasses.field(default_factory=list, compare=False, kw_only=True)

    @staticmethod
    def key(val):
        try:
            if isinstance(val, int):
                return uuid.UUID(int=val)
            else:
                return uuid.UUID(val)
        except (AttributeError, ValueError):
            return val

    def __post_init__(self, *args):
        try:
            self.uid = uuid.UUID(self.uid)
        except AttributeError:
            # Already a UUID
            pass

        try:
            self.style = Style(**self.style)
        except TypeError:
            # Already a Style
            pass

        self.__class__.store[self.uid] = self

    @property
    def name(self):
        if self.id:
            max_id = max(i.id for i in self.store.values())
            digits = math.ceil(math.log10(max_id))
            return f"{{0:0{digits}d}}".format(self.id)
        return format(self.uid)


@dataclasses.dataclass(unsafe_hash=True)
class Link:
    joins:  set[Item] = dataclasses.field(default_factory=weakref.WeakSet, compare=False, kw_only=True)


@dataclasses.dataclass(unsafe_hash=True)
class Pin(Item):
    pos:        Coordinates = None
    area:       int = dataclasses.field(default=4, kw_only=True)
    shape:      str = dataclasses.field(default="", kw_only=True)
    zone:       int = dataclasses.field(default=0, kw_only=True)


@dataclasses.dataclass(unsafe_hash=True)
class Port(Pin, Link):
    pass


@dataclasses.dataclass(unsafe_hash=True)
class Edge(Item):
    pos_0: dataclasses.InitVar[Coordinates | None] = None
    pos_1: dataclasses.InitVar[Coordinates | None] = None
    trail: str = ""
    ports: list[Port] = dataclasses.field(default_factory=list, compare=False)

    @classmethod
    def build(cls, **kwargs):
        ports = kwargs.pop("ports", [])
        args = [port.get("pos") for port in ports]
        rv = cls(*args, **kwargs)

        for n, port in enumerate(ports):
            rv.ports[n].uid = cls.key(port.get("uid", rv.ports[n].uid))
            for val in port.get("joins", []):
                rv.ports[n].joins.discard(val)
                rv.ports[n].joins.add(cls.key(val))
        return rv

    def __post_init__(self, pos_0: tuple, pos_1: tuple, *args):
        super().__post_init__(*args)
        coords = [Coordinates(*c) for c in (pos_0, pos_1) if c is not None]
        if coords:
            self.ports = [
                Port(joins={self.uid}, pos=coords[0]),
                Port(joins={self.uid}, pos=coords[-1]),
            ]
        else:
            self.ports = [Port(joins={self.uid}), Port(joins={self.uid})]

        self.style.stroke = RGB(*self.style.stroke)
        self.style.fill = RGB(*self.style.fill)

    @property
    def joins(self):
        return [
            n
            for p in self.ports
            for uid in p.joins
            if isinstance(n := self.store.get(uid), Node) and uid != self.uid
        ]

    def toml(self, scope="board.edges."):
        yield f'id      = {self.id}'
        yield f'uid     = "{self.uid}"'
        yield f'label   = "{self.label}"'
        yield f"[{scope}style]"
        yield f'stroke  = {list(self.style.stroke)}'
        yield f'fill    = {list(self.style.fill)}'
        yield f'weight  = {self.style.weight}'
        for port in self.ports:
            yield f"[[{scope}ports]]"
            yield f'uid     = "{port.uid}"'
            yield f'pos     = {list(port.pos or [])}'
            yield f'joins   = {[str(i) for i in port.joins]}'


@dataclasses.dataclass(unsafe_hash=True)
class Node(Pin):
    ports:  dict[int, Port] = dataclasses.field(default_factory=dict, compare=False)

    @classmethod
    def build(cls, **kwargs):
        ports = {
            k: Port(joins={cls.key(i) for i in v.pop("joins", [])}, **v)
            for k, v in kwargs.pop("ports", {}).items()
        }
        rv = cls(ports=ports, **kwargs)
        return rv

    def __post_init__(self, *args):
        super().__post_init__(*args)
        if self.pos:
            self.pos = Coordinates(*self.pos)
        for port in self.ports.values():
            port.pos = Coordinates(*port.pos)

        self.style.stroke = RGB(*self.style.stroke)
        self.style.fill = RGB(*self.style.fill)

    @property
    def nearby(self):
        return [
            n
            for edge in self.edges
            for p in edge.ports
            for uid in p.joins
            if isinstance(n := self.store.get(uid), Node) and uid != self.uid
        ]

    @property
    def density(self):
        "Degree of node divided by number of neighbours"
        raise NotImplementedError

    @property
    def edges(self):
        return [e for p in self.ports.values() for uid in p.joins if isinstance(e := self.store.get(uid), Edge)]

    @property
    def connections(self):
        edges = self.edges
        i_edges = [edge for edge in edges if self.uid in edge.ports[1].joins]
        x_edges = [edge for edge in edges if self.uid in edge.ports[0].joins]
        return (i_edges, x_edges)

    def handle(self, fmt="{0:02d}"):
        return next(n for n in (fmt.format(n) for n in itertools.count(len(self.ports))) if n not in self.ports)

    def connect(self, other: Pin, *pos, edge=None, **kwargs):
        rv = edge or Edge(**kwargs)
        rv.ports[0].joins.add(self.uid)
        self.ports[self.handle()] = rv.ports[0]

        rv.ports[1].joins.add(other.uid)
        other.ports[other.handle()] = rv.ports[1]

        try:
            rv.ports[0].pos = pos[0]
            rv.ports[1].pos = pos[-1]
        except IndexError:
            pass

        return rv

    @functools.singledispatchmethod
    def spacing(self, other: Node) -> dict[tuple[Pin, Pin], Number]:
        mine = {i: i.pos for i in self.ports.values()} | {self: self.pos}
        others = {i: i.pos for i in other.ports.values()} | {other: other.pos}
        rv = {
            (mk, ok): abs(ov - mv)
            for (mk, mv), (ok, ov) in itertools.product(mine.items(), others.items())
            if None not in (ov, mv)
        }
        return rv

    @spacing.register
    def _(self, other: Edge) -> dict[tuple[Pin, Pin], Number]:
        mine = {i: i.pos for i in self.ports.values()} | {self: self.pos}
        others = {i: i.pos for i in other.ports}
        others.update({
            i: i.pos for i in (
                Pin(Coordinates.intercept(other.ports[0].pos, other.ports[1].pos, pos))
                for pos in mine.values()
            )
        })
        rv = {
            (mk, ok): abs(ov - mv)
            for (mk, mv), (ok, ov) in itertools.product(mine.items(), others.items())
            if None not in (ov, mv)
        }
        return rv

    def translate(self, vec: Coordinates):
        self.pos += vec
        for port in self.ports.values():
            port.pos += vec

    def toml(self, scope="board.nodes."):
        yield f'id      = {self.id}'
        yield f'uid     = "{self.uid}"'
        yield f'label   = "{self.label}"'
        yield f'zone    = {self.zone}'
        yield f'pos     = {list(self.pos or [])}'
        yield f'area    = {self.area}'
        yield f"[{scope}style]"
        yield f'stroke  = {list(self.style.stroke)}'
        yield f'fill    = {list(self.style.fill)}'
        yield f'weight  = {self.style.weight}'
        for handle, port in self.ports.items():
            yield f"[{scope}ports.{handle}]"
            yield f'uid     = "{port.uid}"'
            yield f'pos     = {list(port.pos or [])}'
            yield f'joins   = {[str(i) for i in port.joins]}'


class Board:

    xml_options = dict(
        layoutMode=LayoutMode.OrganicLayout,
        layoutMethod=OptimizationMethod.MAJORIZATION,
        defaultIdealConnectorLength=2,
    )

    @classmethod
    def build(cls, data: dict) -> Board:
        body = data.get("board", {})
        nodes = [Node.build(**item) for item in body.get("nodes", [])]
        edges = [Edge.build(**item) for item in body.get("edges", [])]
        return cls(items=nodes + edges, **body)

    def __init__(self, title: str = "", items: list = None, **kwargs):
        self.title = title
        self.shapes = dict()
        self.items = items or list()

    @staticmethod
    def extent(items: list) -> tuple[Coordinates]:
        nodes = [i for i in items if isinstance(i, Node)]
        x_vals = sorted([p.pos[0] for node in nodes for p in [node] + list(node.ports.values()) if p.pos]) or [0]
        y_vals = sorted([p.pos[1] for node in nodes for p in [node] + list(node.ports.values()) if p.pos]) or [0]

        min_pos = Coordinates(x_vals[0], y_vals[0])
        max_pos = Coordinates(x_vals[-1], y_vals[-1])
        return min_pos, max_pos

    @staticmethod
    def frame(*points: tuple[Coordinates], margin: Decimal = Decimal("0.05"), square=False):
        x_vals = sorted([Decimal(point[0]) for point in points])
        y_vals = sorted([Decimal(point[1]) for point in points])

        span_x = x_vals[-1] - x_vals[0] or y_vals[-1] - y_vals[0]
        span_y = y_vals[-1] - y_vals[0] or x_vals[-1] - x_vals[0]

        min_x = x_vals[0] - margin * span_x
        max_x = x_vals[1] + margin * span_x
        min_y = y_vals[0] - margin * span_y
        max_y = y_vals[1] + margin * span_y

        if square:
            min_pos = Coordinates(min(min_x, min_y), min(min_x, min_y))
            max_pos = Coordinates(max(max_x, max_y), max(max_x, max_y))
        else:
            min_pos = Coordinates(min_x, min_y)
            max_pos = Coordinates(max_x, max_y)
        return (min_pos, max_pos)

    @staticmethod
    def scale_factor(geom: tuple[Number], frame: tuple[Coordinates, Coordinates], quant: str = ".01"):
        try:
            return Fraction(*min(
                Decimal(geom[0]) / (frame[1][0] - frame[0][0]),
                Decimal(geom[1]) / (frame[1][1] - frame[0][1])
            ).quantize(Decimal(quant)).as_integer_ratio())
        except Exception:
            return Fraction(1, 1)

    @property
    def initial(self) -> list[Node]:
        survey = defaultdict(set)
        for item in self.items:
            for n, port in enumerate(item.ports):
                try:
                    survey[n].update({node for uid in port.joins if isinstance(node := item.store.get(uid), Node)})
                except AttributeError:
                    assert isinstance(item, Node)

        return list(survey.get(0, set()).difference(survey.get(1, set())))

    @property
    def terminal(self) -> list[Node]:
        survey = defaultdict(set)
        for item in self.items:
            for n, port in enumerate(item.ports):
                try:
                    survey[n].update({node for uid in port.joins if isinstance(node := item.store.get(uid), Node)})
                except AttributeError:
                    assert isinstance(item, Node)

        return list(survey.get(1, set()).difference(survey.get(0, set())))

    def merge_svg(self, root: ET) -> dict:
        "Merge from Inkscape format."
        edges = []
        nodes = {}
        for edge_elem in root.findall(".//*[@inkscape:connector-type]", namespaces=vars(NAMESPACE)):
            node_id_start = edge_elem.attrib[ET.QName(NAMESPACE.inkscape, "connection-start")].lstrip("#")
            node_id_end = edge_elem.attrib[ET.QName(NAMESPACE.inkscape, "connection-end")].lstrip("#")
            joins = [
                nodes.setdefault(id_, Node(
                    id=int(''.join(i for i in attrib.get("id") if i.isdigit())),
                    area=Decimal(attrib.get("width")) * Decimal(attrib.get("height")),
                    pos=(attrib.get("x"), attrib.get("y")),
                    label=elem.findtext("{*}title"),
                    contents=[elem.findtext("{*}desc")],
                ))
                for id_ in (node_id_start, node_id_end)
                if (elem := root.find(f".//*[@id='{id_}']")) is not None
                and (attrib := elem.attrib)
            ]
            edges.append(joins[0].connect(
                joins[1],
                id=int(''.join(i for i in edge_elem.attrib.get("id") if i.isdigit())),
                label=edge_elem.findtext("{*}title"),
                contents=[edge_elem.findtext("{*}desc")],
            ))
        rv = list(nodes.values()) + edges
        self.items.extend(rv)
        return rv

    def merge_xml(self, root: ET) -> dict:
        "Merge from Dunnart format."
        items = [i.attrib for i in root.findall("dunnart:node[@type!='guideline']", namespaces=vars(NAMESPACE))]
        nodes = {
            int(n["id"]): Node(
                id=int(n.pop("id")),
                area=n.pop("width") * n.pop("height"),
                pos=(n.pop("cx"), n.pop("cy")),
                **n
            )
            for n in (
                dict(
                    (a, i.get(a) if a in ("id", "label") else Decimal(i[a]))
                    for a in ("id", "width", "height", "label", "cx", "cy")
                )
                for i in items if i.get("type") != "connector"
            )
        }
        edges = [
            nodes[e.pop("srcID")].connect(nodes[e.pop("dstID")], **e)
            for e in (
                dict((a, int(i[a])) for a in ("id", "srcID", "dstID"))
                for i in items if i.get("type") == "connector"
            )
        ]
        rv = list(nodes.values()) + edges
        self.items.extend(rv)
        return rv

    def merge(self, root: ET) -> dict:
        svg_like = bool(root.attrib.get(ET.QName(NAMESPACE.sodipodi, "docname")))
        if svg_like:
            return self.merge_svg(root)
        else:
            return self.merge_xml(root)

    def toml(self) -> Generator[str]:
        yield "[board]"
        yield "[board.shapes]"
        yield from (f'"{key}" = {[list(pos) for pos in val._data]}' for key, val in self.shapes.items())
        yield ""
        for item in self.items:
            if isinstance(item, Node):
                yield "[[board.nodes]]"
                yield from item.toml()
                yield ""
        yield ""
        for item in self.items:
            if isinstance(item, Edge):
                yield "[[board.edges]]"
                yield from item.toml()
                yield ""

    def svg(self, width=None, height=None) -> Generator[str]:
        # TODO: Switch tou connectors.
        height = height or 480
        width = width or 640
        frame = self.frame(*self.extent(self.items), square=width==height)
        size = (width, height)
        scale = self.scale_factor(size, frame)

        defs = [
            '<polygon id="{0}" points="{1}" />'.format(
                id_, " ".join(f"{pos[0]},{pos[1]}" for pos in shape._data)
            )
            for id_, shape in self.shapes.items()
        ]
        shrink = scale.denominator / scale.numerator
        polygons = [
            (f'<use href="#{item.shape}" '
             f'transform="translate({item.pos[0]}, {item.pos[-1]}) scale({shrink:.4f})" '
             f'fill="none" stroke="black" '
             '/>')
            for item in self.items
            if isinstance(item, Node)
        ]
        lines = [
            (f'<line x1="{item.ports[0].pos[0]}" y1="{item.ports[0].pos[1]}" '
             f'x2="{item.ports[1].pos[0]}" y2="{item.ports[1].pos[1]}" '
             f'stroke="black" '
             '/>')
            for item in self.items
            if isinstance(item, Edge)
        ]
        yield textwrap.dedent(f"""
        <svg xmlns="http://www.w3.org/2000/svg"
             xmlns:xlink="http://www.w3.org/1999/xlink"
        width="{width}" height="{height}"
        viewBox="{frame[0][0]} {frame[0][1]} {frame[1][0]} {frame[1][1]}"
        preserveAspectRatio="xMidYMid slice"
        >
        """)
        yield "<title>{0}</title>".format(html.escape(self.title)) if self.title else ""
        yield "<defs>"
        yield from defs
        yield "</defs>"
        yield from polygons
        yield from lines
        yield "</svg>"

    def xml(self, width=None, height=None) -> Generator[str]:
        frame = self.frame(*self.extent(self.items), square=width==height)
        yield textwrap.dedent(f"""
        <svg xmlns="http://www.w3.org/2000/svg"
             xmlns:xlink="http://www.w3.org/1999/xlink"
             xmlns:dunnart="http://www.dunnart.org/ns/dunnart"
        >
        """)
        yield "<title>{0}</title>".format(html.escape(self.title)) if self.title else ""
        options = [f'{k}="{v}"' for k, v in self.xml_options.items()]
        yield '<dunnart:options {0}/>'.format(" ".join(options))
        nodes = [i for i in self.items if isinstance(i, Node)]
        for node in nodes:
            size = math.sqrt(node.area)
            yield (
                f'<dunnart:node id="{node.uid}" '
                f'type="org.dunnart.shapes.rect" '
                f'label="{node.label}" '
                f'cx="{node.pos[0]}" cy="{node.pos[1]}" '
                f'width="{size:.2f}" height="{size:.2f}" '
                '/>'
            )
        edges = [i for i in self.items if isinstance(i, Edge)]
        for edge in edges:
            j = edge.joins
            yield (
                f'<dunnart:node id="{edge.uid}" type="connector" '
                f'label="{edge.label}" '
                f'srcID="{j[0].uid}" dstID="{j[1].uid}" '
                'directed="1" '
                '/>'
            )
        yield "</svg>"
