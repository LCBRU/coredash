from flask import url_for
from lbrc_flask.pytest.asserts import assert__requires_login
from tests.requests import coredash_get


def _url(external=True, **kwargs):
    return url_for('ui.dashboard_frontpage', _external=external, **kwargs)


def _get(client, url, loggedin_user):
    return coredash_get(client, url, loggedin_user, has_form=False)


def test__get__requires_login(client):
    assert__requires_login(client, _url(external=False))
