#!/usr/bin/env python

"""Tests for `pymagics` package."""


import unittest
from click.testing import CliRunner

from pymagics import scryfall
from pymagics import cli

class TestScryfall(unittest.TestCase):
    """Tests for `pymagics` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def testBase(self):
        self.assertIsNotNone(scryfall.get_bulk_cards())
