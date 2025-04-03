from lbrc_flask.security import init_roles, init_users

ROLENAMES = []

def init_authorization():
    init_roles(ROLENAMES)
    init_users()
