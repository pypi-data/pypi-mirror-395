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

import datetime
import importlib.resources
import itertools
import pathlib
import sys
import textwrap

import plotlines
from plotlines.board import Board
from plotlines.board import Edge
from plotlines.board import Node


class Tree:
    "Generates a tree of files suitable for Spiki processing"

    @staticmethod
    def index_comment(ts):
        return f"# Generated {ts} by Plotlines {plotlines.__version__}"

    @staticmethod
    def base_head():
        return importlib.resources.read_text("plotlines.assets", "head.toml")

    @staticmethod
    def base_link(path: pathlib.Path):
        return textwrap.dedent(f"""
        [[base.html.head.link]]
        config = {{tag_mode = "void"}}
        attrib = {{rel= "stylesheet", href="{path.name}"}}
        """).lstrip()

    @staticmethod
    def index_nav(board: Board):
        yield textwrap.dedent("""
        [base.html.body.header]
        attrib = {accesskey = "m", popovertarget = "nav-upper"}
        button = "≡"  # "IDENTICAL TO" (U+2261)

        [base.html.body.header.nav]
        attrib = {id="nav-upper", popover = "auto"}
        """).lstrip()

        for item in board.items:
            yield textwrap.dedent(f"""
            [[base.html.body.header.nav.ul.li]]
            attrib = {{class = "card"}}

            [base.html.body.header.nav.ul.li.div.span]
            attrib = {{href = "{item.name}.html"}}
            a = "{item.name}"

            [base.html.body.header.nav.ul.li.div]
            p = "{item.label}"
            """).lstrip()

        yield textwrap.dedent("""
        [base.html.body.main]
        config = {tag_mode = "pair", block_wrap = "div"}
        """).lstrip()

        yield textwrap.dedent("""
        [[base.html.body.footer.nav.ul.li]]
        attrib = {class = "spiki home", href = "index.html"}
        a = "Home"
        """).lstrip()

        for node in board.initial:
            yield textwrap.dedent(f"""
            [[doc.html.body.footer.nav.ul.li]]
            attrib = {{class = "spiki next", href = "{node.name}.html"}}
            a = "{node.label or 'Start'}"
            """).lstrip()

    @staticmethod
    def edge_comment(edge: Edge):
        return f"# Edge '{edge.label}'\n"

    @staticmethod
    def edge_nav(edge: Edge):
        node = edge.joins[1]
        return textwrap.dedent(f"""
        [[doc.html.body.footer.nav.ul.li]]
        attrib = {{class = "spiki next", href = "{node.name}.html"}}
        a = "{node.label or 'Next'}"
        """).lstrip()

    @staticmethod
    def edge_blocks(edge: Edge):
        if isinstance(edge.contents, list):
            contents = "\n".join(i for i in edge.contents if isinstance(i, str))
        else:
            contents = edge.contents
        return textwrap.dedent(f'''
        [doc.html.body.main]
        blocks = """
        {contents}
        """
        ''').lstrip()

    @staticmethod
    def node_comment(node: Node):
        return f"# Node '{node.label}'\n"

    @staticmethod
    def node_nav(node: Node):
        for edge in node.connections[1]:
            trail = edge.trail or "next"
            yield textwrap.dedent(f"""
            [[doc.html.body.footer.nav.ul.li]]
            attrib = {{class = "spiki {trail}", href = "{edge.name}.html"}}
            a = "{edge.label or 'Next'}"
            """).lstrip()

    @staticmethod
    def node_blocks(node: Node):
        if isinstance(node.contents, list):
            contents = "\n".join(i for i in node.contents if isinstance(i, str))
        else:
            contents = node.contents
        return textwrap.dedent(f'''
        [doc.html.body.main]
        blocks = """
        {contents}
        """
        ''').lstrip()

    def __init__(self, board: Board):
        self.board = board

    def __call__(self, parent: pathlib.Path, ts: datetime.datetime = None):
        ts = ts or datetime.datetime.now(tz=datetime.timezone.utc)
        chunks = [self.index_comment(ts), self.base_head()]
        for path in importlib.resources.files("plotlines.assets").iterdir():
            if path.suffix == ".css":
                yield path.read_text(), parent.joinpath(path.name)
                chunks.append(self.base_link(path))

        chunks.extend(self.index_nav(self.board))
        yield "\n".join(chunks), parent.joinpath("index.toml")

        nodes = [i for i in self.board.items if isinstance(i, Node)]
        for node in nodes:
            path = parent.joinpath(node.name).with_suffix(".toml")
            text = "\n".join(itertools.chain(
                [self.node_comment(node)], self.node_nav(node), [self.node_blocks(node)]
            ))
            yield text, path

        edges = [i for i in self.board.items if isinstance(i, Edge)]
        for edge in edges:
            path = parent.joinpath(edge.name).with_suffix(".toml")
            text = "\n".join((self.edge_comment(edge), self.edge_nav(edge), self.edge_blocks(edge)))
            yield text, path
