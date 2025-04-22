from lbrc_flask.security import init_roles, init_users

ROLENAME_PROJECT_EDITOR='project_editor'

ROLENAMES = [ROLENAME_PROJECT_EDITOR]

def init_authorization():
    init_roles(ROLENAMES)
    init_users()
