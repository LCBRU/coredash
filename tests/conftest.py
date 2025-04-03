import pytest
from faker import Faker
from lbrc_flask.pytest.fixtures import *
from coredash.config import TestConfig
from coredash import create_app
from lbrc_flask.pytest.faker import LbrcFlaskFakerProvider, LbrcFileProvider
from lbrc_flask.pytest.helpers import login
from coredash.security import init_authorization


@pytest.fixture(scope="function")
def standard_lookups(client, faker):
    return faker.create_standard_lookups()


@pytest.fixture(scope="function")
def loggedin_user(client, faker):
    init_authorization()
    return login(client, faker)


@pytest.fixture(scope="function")
def app():
    yield create_app(TestConfig)

    # shutil.rmtree(TestConfig().FILE_UPLOAD_DIRECTORY, ignore_errors=True)


@pytest.fixture(scope="function")
def faker():
    result = Faker("en_GB")
    result.add_provider(LbrcFlaskFakerProvider)
    result.add_provider(LbrcFileProvider)

    yield result
