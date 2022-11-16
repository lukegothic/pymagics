#!/usr/bin/env python

"""Tests for `pymagics` package."""


import unittest
from click.testing import CliRunner

from pymagics import mappers
from pymagics import scryfall
from pymagics import cli

class TestMappers(unittest.TestCase):
    """Tests for `pymagics` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def testBase(self):
        print(mappers.cardname_to_filename("Dandân"))
        print(mappers.cardname_to_filename("Junún Efreet"))

    def testAll(self):
        scryfall_db = scryfall.get_bulk_cards(t="oracle")
        scryfall_db_names = [c["name"] for c in scryfall_db]
        for name in scryfall_db_names:
            print(name, mappers.cardname_to_filename(name))