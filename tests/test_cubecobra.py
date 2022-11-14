#!/usr/bin/env python

"""Tests for `pymagics` package."""


import unittest
from click.testing import CliRunner

from pymagics import cubecobra, decklist
from pymagics import cli


class TestCubeCobra(unittest.TestCase):
    """Tests for `pymagics` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_get_list_noparam(self):
        with self.assertRaises(cubecobra.ParamException):
            cubecobra.get_list()

    def test_get_list_ok(self):
        res = cubecobra.get_list(cube_name="modovintage")
        self.assertTrue(isinstance(res, decklist.Decklist))

    def test_get_list_error(self):
        with self.assertRaises(cubecobra.NotFoundException):
            cubecobra.get_list(cube_name="modovintagexxxxxxx")
