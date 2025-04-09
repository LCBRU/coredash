#!/usr/bin/env python3

from dotenv import load_dotenv

# Load environment variables from '.env' file.
load_dotenv()

from lbrc_flask.database import db
from lbrc_flask.security import init_roles, init_users
from lbrc_flask.pytest.faker import LbrcFlaskFakerProvider
from alembic.config import Config
from alembic import command
from tests.faker import CoreDashLookupProvider, ProjectProvider
from faker import Faker
from coredash.model import *

fake = Faker("en_GB")
fake.add_provider(LbrcFlaskFakerProvider)
fake.add_provider(CoreDashLookupProvider)
fake.add_provider(ProjectProvider)

from coredash import create_app

application = create_app()
application.app_context().push()
db.create_all()
init_roles([])
init_users()

alembic_cfg = Config("alembic.ini")
command.stamp(alembic_cfg, "head")

lookups = fake.create_standard_lookups()
db.session.commit()

for _ in range(30):
    fake.project().get_in_db()
db.session.commit()

db.session.close()
