#  __author__ = 'Alexey Buchkin'

import pytest
import json
import os.path
import ftputil

from fixture.application import Application
from fixture.db import DbFixture

fixture = None
target = None


def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target


@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    if fixture is None or not fixture.is_valid():
        fixture = Application(browser=browser, config = config)
    fixture.session.login(username=config['webadmin']["username"], password=config['webadmin']["password"])
    return fixture


@pytest.fixture(scope="session")
def db(request, config):
    db = DbFixture(host=config['db']['host'], name=config['db']['name'],
                          user=config['db']['user'], password=config['db']['password'])
    return db


@pytest.fixture(scope="session")
def config(request):
    return load_config(request.config.getoption("--target"))


@pytest.fixture(scope="session", autouse=True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()

    request.addfinalizer(fin)
    return fixture


def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_defaults_inc.bak"):
            remote.remove("config_defaults_inc.bak")
        if remote.path.isfile("config_defaults_inc.php"):
            remote.rename("config_defaults_inc.php", "config_defaults_inc.bak")
        remote.upload(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                   "resources/config_defaults_inc.php"), "config_defaults_inc.php")


def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_defaults_inc.bak"):
            if remote.path.isfile("config_defaults_inc.php"):
                remote.remove("config_defaults_inc.php")
            if remote.path.isfile("config_defaults_inc.php"):
                remote.rename("config_defaults_inc.bak", "config_defaults_inc.php")


@pytest.fixture(scope="session", autouse=True)
def configure_server(request, config):
    install_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    def fin():
        restore_server_configuration(config['ftp']['host'], config['ftp']['username'], config['ftp']['password'])
    request.addfinalizer(fin)


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="firefox")
    parser.addoption("--target", action="store", default="target.json")
