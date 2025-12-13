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

import dataclasses
from decimal import Decimal
from fractions import Fraction
import functools
import importlib.resources
import textwrap
import tkinter as tk
import tomllib
import turtle
from types import SimpleNamespace as NS
import unittest.mock
import uuid
import xml.etree.ElementTree as ET

from plotlines.board import Board
from plotlines.board import Edge
from plotlines.board import Node
from plotlines.board import Pin
from plotlines.board import Port
from plotlines.board import RGB
from plotlines.board import Style
from plotlines.coordinates import Coordinates as C
from plotlines.schema import NAMESPACE


class EdgeTests(unittest.TestCase):

    def test_uid_int(self):
        edge = Edge(uid=1)
        self.assertTrue(edge)
        self.assertEqual(edge.uid, 1)

    def test_init_from_toml_full(self):
        toml = textwrap.dedent("""
        uid = "e7ed29c8-f718-488c-9b3b-adf1f881f6a2"
        trail = "main"

        [style]
        stroke = [127, 127, 127]
        fill = [32, 32, 32]
        weight = 6

        [[ports]]
        pos = [0, 1]
        joins = []

        [[ports]]
        pos = [2, 3]
        joins = [77096613620228011470678743578062052921, "NODE_1"]

        [[contents]]
        """)
        data = tomllib.loads(toml)
        edge = Edge.build(**data)
        self.assertTrue(edge)
        self.assertIsInstance(edge.uid, uuid.UUID)
        self.assertIsInstance(edge.ports[0].joins, set)
        self.assertIsInstance(edge.ports[0].pos, C)
        self.assertIsInstance(edge.ports[1].joins, set)
        self.assertIsInstance(edge.ports[1].pos, C)

        self.assertEqual(len(edge.ports[0].joins), 1, edge.ports[0].joins)
        self.assertEqual(len(edge.ports[1].joins), 3, edge.ports[1].joins)
        self.assertIn(uuid.UUID(int=list(data["ports"][1]["joins"])[0]), edge.ports[1].joins)
        self.assertNotIn(list(data["ports"][1]["joins"])[0], edge.ports[1].joins)
        self.assertIn("NODE_1", edge.ports[1].joins)

        self.assertIsInstance(edge.style, Style)


class NodeTests(unittest.TestCase):

    def test_uid_int(self):
        node = Node(uid=1)
        self.assertTrue(node)
        self.assertEqual(node.uid, 1)
        self.assertEqual(node.handle(), "00")

    def test_init_from_toml_full(self):
        toml = textwrap.dedent("""
        uid = "e7ed29c8-f718-488c-9b3b-adf1f881f6a2"
        pos = [0, 0]

        [style]
        stroke = [127, 127, 127]
        fill = [32, 32, 32]
        weight = 6

        [ports.E]
        pos = [0, 1]
        joins = []

        [ports.W]
        pos = [0, -1]
        joins = [77096613620228011470678743578062052921, "EDGE_1"]

        [[contents]]
        """)
        data = tomllib.loads(toml)
        node = Node.build(**data)
        self.assertTrue(node)

        self.assertIsInstance(node.uid, uuid.UUID)
        self.assertIsInstance(node.ports["E"].joins, set)
        self.assertIsInstance(node.ports["E"].pos, C)
        self.assertIsInstance(node.ports["W"].joins, set)
        self.assertIsInstance(node.ports["W"].pos, C)

        self.assertEqual(len(node.ports["E"].joins), 0, node.ports["E"].joins)
        self.assertEqual(len(node.ports["W"].joins), 2, node.ports["W"].joins)
        self.assertTrue(any(isinstance(i, uuid.UUID) for i in node.ports["W"].joins), node.ports["W"].joins)
        self.assertFalse(any(isinstance(i, int) for i in node.ports["W"].joins), node.ports["W"].joins)
        self.assertIn("EDGE_1", node.ports["W"].joins)

        self.assertIsInstance(node.style, Style)


class BoardTests(unittest.TestCase):

    @staticmethod
    def build_3_nodes():
        nodes = [
            Node((20, 20), area=1600, label="a"),
            Node(
                (70, 20), area=1600,
                label="b", style=Style(stroke=RGB(127, 127, 127),
                fill=RGB(32, 32, 32), weight=10)
            ),
            Node((120, 20), area=1600, label="c")
        ]
        edges = [
            nodes[0].connect(nodes[1], C(30, 20), C(60, 20), label="d"),
            nodes[1].connect(nodes[2], C(80, 20), C(110, 20), label="e"),
        ]
        return nodes, edges

    def test_edge_init(self):
        edge = Edge((1, 3), (19, 12))
        self.assertEqual(len(edge.ports), 2)
        self.assertTrue(all(isinstance(p.pos, C) for p in edge.ports), edge.ports)
        self.assertEqual(edge.ports[0].pos, (1, 3))
        self.assertEqual(edge.ports[1].pos, (19, 12))

    def test_node_init(self):
        node = Node((13, 14))
        self.assertIsInstance(node.pos, C)
        self.assertEqual(node.pos, (13, 14))

    def test_node_connect(self):
        nodes = [Node(), Node()]
        edge = nodes[0].connect(nodes[1])
        self.assertIsInstance(edge, Edge)
        self.assertEqual(edge.ports[0].joins, {edge.uid, nodes[0].uid})
        self.assertEqual(edge.ports[1].joins, {edge.uid, nodes[1].uid})
        self.assertEqual(nodes[0].ports["00"].joins, {edge.uid, nodes[0].uid})
        self.assertEqual(nodes[1].ports["00"].joins, {edge.uid, nodes[1].uid})

    def test_node_nearby(self):
        Node.store.clear()
        nodes = [Node(), Node()]
        edge = nodes[0].connect(nodes[1])
        self.assertIn(nodes[1], nodes[0].nearby)
        self.assertNotIn(nodes[0], nodes[0].nearby)
        self.assertIn(nodes[0], nodes[1].nearby)
        self.assertNotIn(nodes[1], nodes[1].nearby)

    def test_node_edges(self):
        nodes = [Node(), Node()]
        edge = nodes[0].connect(nodes[1])

        for node in nodes:
            with self.subTest(node=node):
                self.assertIsInstance(node.edges, list)
                self.assertIn(edge, node.edges)
                self.assertEqual(len(node.edges), 1)

    def test_node_spacing_node_self(self):
        node = Node((1, 3))

        spacing = node.spacing(node)
        self.assertEqual(len(spacing), 1)
        space = min(spacing.values())
        self.assertEqual(space, 0)

    def test_node_spacing_node_other(self):
        nodes = [Node((1, 3)), Node((19, 12))]

        spacing = nodes[0].spacing(nodes[1])
        self.assertEqual(len(spacing), 1)
        space = min(spacing.values())
        self.assertAlmostEqual(space, 20, places=0)

    def test_node_spacing_edge(self):
        edge = Edge((1, 3), (19, 12))
        node = Node((13, 4))

        spacing = node.spacing(edge)
        self.assertEqual(len(spacing), 3, spacing)
        space = min(spacing.values())
        self.assertAlmostEqual(space, 4.5, places=1)

    def test_frame(self):
        points = (C(0, 0), C(10, 10))
        check = (C(-0.5, -0.5), C(10.5, 10.5))
        self.assertEqual(Board.frame(*points), check)

        points = (C(0, 0), C(0, 10))
        check = (C(-0.5, -0.5), C(0.5, 10.5))
        self.assertEqual(Board.frame(*points), check)

    def test_scale_factor(self):
        geom = (400, 300)
        frame = (C(1.50, 1.50, coerce=Decimal), C(12.50, 2.50, coerce=Decimal))
        scale = Board.scale_factor(geom, frame)
        check = Fraction(909, 25)
        self.assertEqual(scale, check)

    def test_3_nodes_initial(self):
        nodes, edges = self.build_3_nodes()
        board = Board(items=nodes + edges)
        self.assertEqual(len(board.initial), 1, board.initial)
        self.assertIs(board.initial[0], nodes[0])

    def test_3_nodes_terminal(self):
        nodes, edges = self.build_3_nodes()
        board = Board(items=nodes + edges)
        self.assertEqual(len(board.terminal), 1, board.terminal)
        self.assertIs(board.terminal[0], nodes[-1])

    def test_3_nodes_toml(self):
        nodes, edges = self.build_3_nodes()
        for node in nodes:
            toml = "\n".join(node.toml(scope=""))
            try:
                data = tomllib.loads(toml)
                check = Node.build(**data)
            except Exception:
                self.fail("\n" + toml)
                raise

            self.assertEqual(node.uid, check.uid)
            for field in dataclasses.fields(Node):
                with self.subTest(field=field):
                    try:
                        self.assertEqual(sorted(getattr(node, field.name)), sorted(getattr(check, field.name)), "\n" + toml)
                    except TypeError:
                        self.assertEqual(format(getattr(node, field.name)), format(getattr(check, field.name)), "\n" + toml)

            self.assertEqual(node, check)

    def test_2_edges_toml(self):
        nodes, edges = self.build_3_nodes()
        for edge in edges:
            toml = "\n".join(edge.toml(scope=""))
            try:
                data = tomllib.loads(toml)
                check = Edge.build(**data)
            except Exception:
                self.fail("\n" + toml)

            self.assertEqual(edge.uid, check.uid)
            for field in dataclasses.fields(Edge):
                with self.subTest(field=field):
                    self.assertEqual(getattr(edge, field.name), getattr(check, field.name), "\n" + toml)

            self.assertEqual(edge, check)

    def test_3_nodes_svg(self):
        screen_size = (400, 300)
        nodes, edges = self.build_3_nodes()

        board = Board(title="Test", items=nodes + edges)
        svg = "\n".join(board.svg(*screen_size))
        root = ET.fromstring(svg)

        ns = NS(svg="http://www.w3.org/2000/svg", xlink="http://www.w3.org/1999/xlink")
        self.assertEqual(root.tag, ET.QName(ns.svg, "svg"))
        self.assertIn('xmlns:xlink="http://www.w3.org/1999/xlink"', svg)
        self.assertEqual(root.attrib.get("width"), str(screen_size[0]), root.attrib)
        self.assertEqual(root.attrib.get("height"), str(screen_size[1]), root.attrib)

        self.assertIn("viewBox", root.attrib)
        self.assertIn("preserveAspectRatio", root.attrib)

        title = root.find(f"svg:title", vars(ns))
        self.assertEqual(title.text, "Test")

    def test_3_nodes_xml(self):
        screen_size = (400, 300)
        nodes, edges = self.build_3_nodes()

        board = Board(title="Test", items=nodes + edges)
        xml = "\n".join(board.xml(*screen_size))
        try:
            root = ET.fromstring(xml)
        except ET.ParseError:
            print(xml)
            raise

        self.assertEqual(root.tag, ET.QName(NAMESPACE.svg, "svg"))
        self.assertIn('xmlns:xlink="http://www.w3.org/1999/xlink"', xml)
        self.assertIn('xmlns:dunnart="http://www.dunnart.org/ns/dunnart"', xml)

        self.assertNotIn("viewBox", root.attrib)
        self.assertNotIn("preserveAspectRatio", root.attrib)

        title = root.find(f"svg:title", vars(NAMESPACE))
        self.assertEqual(title.text, "Test")

        options = root.find("dunnart:options", namespaces=vars(NAMESPACE))
        self.assertIsNotNone(options, xml)
        self.assertEqual(options.tag, ET.QName(NAMESPACE.dunnart, "options"))

        nodes = root.findall("dunnart:node[@type!='connector']", namespaces=vars(NAMESPACE))
        for n, node in enumerate(nodes):
            with self.subTest(n=n, node=node):
                self.assertTrue(node.attrib["id"], node)
                self.assertEqual(node.attrib["type"], "org.dunnart.shapes.rect")
        self.assertEqual(len(nodes), 3, nodes)

        edges = root.findall("dunnart:node[@type='connector']", namespaces=vars(NAMESPACE))
        for e, edge in enumerate(edges):
            with self.subTest(e=e, edge=edge):
                self.assertTrue(edge.attrib["id"], edge)
                self.assertTrue(edge.attrib["srcID"], edge)
                self.assertTrue(edge.attrib["dstID"], edge)
        self.assertEqual(len(edges), 2, edges)

    def test_51_nodes_merge_xml(self):
        text = importlib.resources.read_text("plotlines.test.data", "spiki-demo_n51.svg")
        root = ET.fromstring(text)
        board = Board()
        rv = board.merge(root)
        self.assertEqual(len(rv), 151)
        nodes = {i.uid: i for i in board.items if isinstance(i, Node)}
        edges = {i.uid: i for i in board.items if isinstance(i, Edge)}
        self.assertEqual(len(nodes), 51)
        self.assertTrue(all(isinstance(i.pos, C) for i in nodes.values()))

        self.assertEqual(len(edges), 100)
        for edge in edges.values():
            with self.subTest(edge=edge):
                self.assertEqual(len(edge.joins), 2)
                self.assertTrue(all(i.uid in nodes) for i in edge.joins)

    def test_inkscape_properties_merge_xml(self):
        text = importlib.resources.read_text("plotlines.test.data", "inkscape_properties_n03e02.svg")
        root = ET.fromstring(text)
        board = Board()
        rv = board.merge(root)
        self.assertEqual(len(rv), 5, text)
        self.assertEqual(len(board.items), 5)
        self.assertEqual(len(board.initial), 1)
        self.assertEqual(len(board.initial[0].nearby), 2)

        node = next(i for i in board.terminal if i.id == 825)
        self.assertEqual(node.name, "825")
        self.assertEqual(node.label, "Win")
        self.assertEqual(node.edges[0].label, "A arc")
        self.assertEqual(node.contents, ["Good ending.\n\n<NARRATOR>\tOr is it?"], rv)
        self.assertEqual(node.edges[0].contents, ["This is what happens if you go left."])
