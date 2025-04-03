import alembic.config

from coredash import create_app
from coredash.security import init_authorization
alembicArgs = [
    '--raiseerr',
    'upgrade', 'head',
]
alembic.config.main(argv=alembicArgs)

application = create_app()
application.app_context().push()

init_authorization()
