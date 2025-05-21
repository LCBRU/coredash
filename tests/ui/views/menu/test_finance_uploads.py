import re
from flask import url_for
from tests.requests import coredash_get


def _url(external=True, **kwargs):
    return url_for('ui.index', _external=external, **kwargs)


def _get(client, url, user):
    resp = coredash_get(client, url, user, False)
    return resp


def test__get__finance_uploader__finance_uploads_menu_item_exists(client, loggedin_user_finance_uploader):
    resp = _get(client, _url(), loggedin_user_finance_uploader)

    # print(loggedin_user_finance_uploader)
    # print(resp.soup)
    assert resp.soup.nav.find("a", href=url_for('ui.finance_upload_index'), string=re.compile("Finance Uploads")) is not None


def test__get__non_finance_uploader__finance_uploads_menu_item_not_exists(client, loggedin_user):
    resp = _get(client, _url(), loggedin_user)
    assert resp.soup.nav.find("a", href=url_for('ui.finance_upload_index'), string=re.compile("Finance Uploads")) is None
