#!/usr/bin/env python

"""Tests for `agilizedmc` package."""

import pytest
from agilizedmc import (
    Config,
    DatabaseConfig,
    BackupService,
    GoogleDriveService,
    NotificationService,
    DB
)

from click.testing import CliRunner

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


def test_mysql_exists():
    db = DB
    assert db is not None


def test_db():
    """Test DB class creation"""
    db = DB('localhost', 'root', None, '3306', 'test')
    assert db.host == 'localhost'
    assert db.user == 'root'
    assert db.password is None
    assert db.port == '3306'
    assert db.database == 'test'


def test_version():
    """Test version is string."""
    from agilizedmc import __version__
    assert isinstance(__version__, str)


def test_config():
    """Test config creation."""
    db_config = DatabaseConfig(
        host="localhost",
        port=3306,
        user="test",
        password="test",
        database="test"
    )
    config = Config(
        database=db_config,
        google_drive_folder_id="test_folder",
        backup_dir="/tmp/backup",
        ssh_config={},
        telegram_bot_token="test_token",
        telegram_chat_id="test_chat",
        service_account_file="test.json"
    )
    assert config.database.host == "localhost"