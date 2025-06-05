from pathlib import Path
import pytest
from faker import Faker
from lbrc_flask.pytest.fixtures import *
from coredash.config import TestConfig
from coredash import create_app
from lbrc_flask.pytest.faker import LbrcFlaskFakerProvider, LbrcFileProvider
from lbrc_flask.pytest.helpers import login
from coredash.security import ROLENAME_FINANCE_UPLOADER, ROLENAME_PROJECT_EDITOR, init_authorization
from coredash.model.security import User
from tests.faker import CoreDashLookupProvider, CoreDashProvider, FinanceUploadProvider


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
def loggedin_user_finance_uploader(client, faker):
    init_authorization()

    user = faker.get_test_user(rolename=ROLENAME_FINANCE_UPLOADER)
    return login(client, faker, user)


@pytest.fixture(scope="function")
def app(tmp_path):
    class LocalTestConfig(TestConfig):
        # FILE_UPLOAD_DIRECTORY = tmp_path
        FILE_UPLOAD_DIRECTORY = Path('/home/richard/projects/coredash/upload/test/')

    yield create_app(LocalTestConfig)


@pytest.fixture(scope="function")
def faker():
    result = Faker("en_GB")
    result.add_provider(LbrcFlaskFakerProvider)
    result.add_provider(LbrcFileProvider)
    result.add_provider(CoreDashLookupProvider)
    result.add_provider(CoreDashProvider)
    result.add_provider(FinanceUploadProvider)

    result.provider('LbrcFlaskFakerProvider').set_userclass(User)

    yield result
