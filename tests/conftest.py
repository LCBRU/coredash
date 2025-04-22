import shutil
import pytest
from faker import Faker
from lbrc_flask.pytest.fixtures import *
from coredash.config import TestConfig
from coredash import create_app
from lbrc_flask.pytest.faker import LbrcFlaskFakerProvider, LbrcFileProvider
from lbrc_flask.pytest.helpers import login
from coredash.security import ROLENAME_PROJECT_EDITOR, init_authorization
from tests.faker import CoreDashLookupProvider, ProjectProvider


@pytest.fixture(scope="function")
def standard_lookups(client, faker):
    return faker.create_standard_lookups()


@pytest.fixture(scope="function")
def loggedin_user(client, faker):
    init_authorization()
    return login(client, faker)


@pytest.fixture(scope="function")
def loggedin_user_project_editor(client, faker):
    init_authorization()

    user = faker.get_test_user(rolename=ROLENAME_PROJECT_EDITOR)
    return login(client, faker, user)


@pytest.fixture(scope="function")
def app():
    yield create_app(TestConfig)

    shutil.rmtree(TestConfig().FILE_UPLOAD_DIRECTORY, ignore_errors=True)


@pytest.fixture(scope="function")
def faker():
    result = Faker("en_GB")
    result.add_provider(LbrcFlaskFakerProvider)
    result.add_provider(LbrcFileProvider)
    result.add_provider(CoreDashLookupProvider)
    result.add_provider(ProjectProvider)

    yield result
