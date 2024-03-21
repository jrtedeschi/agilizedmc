#!/usr/bin/env python

"""Tests for `agilizedmc` package."""

import pytest

from click.testing import CliRunner

from agilizedmc import agilizedmc
from agilizedmc import cli
from agilizedmc.db import DB

@pytest.fixture
def response():
    """Sample pytest fixture.

    See more at: http://doc.pytest.org/en/latest/fixture.html
    """
    # import requests
    # return requests.get('https://github.com/audreyr/cookiecutter-pypackage')


def test_content(response):
    """Sample pytest test function with the pytest fixture as an argument."""
    # from bs4 import BeautifulSoup
    # assert 'GitHub' in BeautifulSoup(response.content).title.string


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(cli.main)
    assert result.exit_code == 0
    assert 'agilizedmc.cli.main' in result.output
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert '--help  Show this message and exit.' in help_result.output


def test_mysql_exists():
    db = DB
    assert db is not None


def test_db():
    db = DB('localhost', 'root', None, '3306', 'test')

    assert db.host == 'localhost'
    assert db.user == 'root'
    assert db.password == None
    assert db.port == '3306'
    assert db.database == 'test'

    db.connection.execute('CREATE TABLE IF NOT EXISTS test_table (id INT, name VARCHAR(255))')
    tables = db.get_tables()

    ## assert that the table was created and is in the list of tables
    assert ('test_table',) in tables