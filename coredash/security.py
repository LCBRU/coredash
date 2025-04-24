from lbrc_flask.security import init_roles, init_users

ROLENAME_PROJECT_EDITOR='project_editor'
ROLENAME_FINANCE_UPLOADER='finance_uploader'

ROLENAMES = [ROLENAME_PROJECT_EDITOR, ROLENAME_FINANCE_UPLOADER]

def init_authorization():
    init_roles(ROLENAMES)
    init_users()
