import re
from flask import url_for
from lbrc_flask.pytest.asserts import get_and_assert_standards, get_and_assert_standards_modal


def coredash_get(client, url, user, has_form=False):
    resp = get_and_assert_standards(client, url, user, has_form)

    assert resp.soup.nav is not None
    assert resp.soup.nav.find("a", href=url_for('ui.index'), string=re.compile("Projects")) is not None

    return resp


def coredash_modal_get(client, url, user, has_form=False):
    resp = get_and_assert_standards_modal(client, url, user, has_form)

    return resp
