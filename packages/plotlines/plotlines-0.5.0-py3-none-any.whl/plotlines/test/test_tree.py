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

import importlib.resources
import pathlib
import shutil
import tempfile
import tomllib
import unittest
import xml.etree.ElementTree as ET

from plotlines.board import Board
from plotlines.board import Edge
from plotlines.board import Node
from plotlines.tree import Tree


class TreeTests(unittest.TestCase):
    def setUp(self):
        self.parent = pathlib.Path(tempfile.mkdtemp(prefix="plotlines-", suffix="-test"))

    def tearDown(self):
        shutil.rmtree(self.parent)
        self.assertFalse(self.parent.exists())

    def test_n03e02_index(self):
        text = importlib.resources.read_text("plotlines.test.data", "inkscape_properties_n03e02.svg")
        root = ET.fromstring(text)
        board = Board()
        rv = board.merge(root)
        tree = Tree(board)
        for text, path in tree(self.parent):
            path.write_text(text)

        path = self.parent.joinpath("index.toml")
        self.assertTrue(path.exists())

        text = path.read_text()
        index = tomllib.loads(text)

        links = {i.get("attrib", {}).get("href") for i in index["base"]["html"]["head"]["link"]}
        self.assertIn("basics.css", links)

        self.assertEqual(index["base"]["html"]["body"]["header"]["nav"].get("attrib", []).get("popover"), "auto")

        nav_list = index["base"]["html"]["body"]["header"]["nav"]["ul"]["li"]
        self.assertEqual(len(nav_list), 5)

    def test_n03e02_edge(self):
        text = importlib.resources.read_text("plotlines.test.data", "inkscape_properties_n03e02.svg")
        root = ET.fromstring(text)
        board = Board()
        board.merge(root)
        tree = Tree(board)
        for text, path in tree(self.parent):
            path.write_text(text)

        path = self.parent.joinpath("831.toml")
        self.assertTrue(path.exists())

        text = path.read_text()
        self.assertIn("A arc", text)
        node = tomllib.loads(text)

        nav_list = node["doc"]["html"]["body"]["footer"]["nav"]["ul"]["li"]
        self.assertEqual({i.get("attrib", {}).get("href") for i in nav_list}, {"825.html"})
        self.assertEqual({i.get("a") for i in nav_list}, {"Win"})

        self.assertEqual(
            node["doc"]["html"]["body"]["main"].get("blocks", "").strip(),
            "This is what happens if you go left."
        )

    def test_n03e02_node(self):
        text = importlib.resources.read_text("plotlines.test.data", "inkscape_properties_n03e02.svg")
        root = ET.fromstring(text)
        board = Board()
        board.merge(root)
        tree = Tree(board)
        for text, path in tree(self.parent):
            path.write_text(text)

        path = self.parent.joinpath("815.toml")
        self.assertTrue(path.exists())

        text = path.read_text()
        self.assertIn("Start", text)
        node = tomllib.loads(text)

        nav_list = node["doc"]["html"]["body"]["footer"]["nav"]["ul"]["li"]
        self.assertEqual({i.get("attrib", {}).get("href") for i in nav_list}, {"831.html", "833.html"})
        self.assertEqual({i.get("a") for i in nav_list}, {"A arc", "B arc"})

        self.assertEqual(node["doc"]["html"]["body"]["main"].get("blocks", "").strip(), "First node.")
