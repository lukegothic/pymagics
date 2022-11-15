#!/usr/bin/env python

"""Tests for `pymagics` package."""


import unittest
from click.testing import CliRunner

from pymagics import mpc
from pymagics import cli
from pyluke import venn

class TestDecklist(unittest.TestCase):
    """Tests for `pymagics` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_simple3(self):
        a = ["papas", "verdura"]
        b = ["loto", "verdura", "perr", "alcachofa"]
        c = ["papas", "backend", "verdura"]
        mpc_order = mpc.MCPOrder(lists=[a, b, c])
        g = mpc_order.generate()
        self.assertIsNotNone(g)