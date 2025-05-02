from lbrc_flask.security.model import User as BaseUser
from coredash.security import ROLENAME_FINANCE_UPLOADER, ROLENAME_PROJECT_EDITOR


class User(BaseUser):
    @property
    def is_project_editor(self):
        return self.has_role(ROLENAME_PROJECT_EDITOR)

    @property
    def is_finance_uploader(self):
        return self.has_role(ROLENAME_FINANCE_UPLOADER)
