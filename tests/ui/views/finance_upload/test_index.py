from flask import url_for
from lbrc_flask.pytest.asserts import assert__search_html, assert__requires_login, assert__requires_role
from lbrc_flask.pytest.html_content import get_records_found, get_table_row_count
from tests.requests import coredash_get


def _url(external=True, **kwargs):
    return url_for('ui.finance_upload_index', _external=external, **kwargs)


def _get(client, url, loggedin_user, has_form, expected_count):
    resp = coredash_get(client, url, loggedin_user, has_form)

    assert__search_html(resp.soup, clear_url=_url(external=False))

    assert expected_count == get_records_found(resp.soup)
    assert expected_count == get_table_row_count(resp.soup)

    return resp


def test__get__requires_login(client):
    assert__requires_login(client, _url(external=False))


def test__get__requires_editor_login__not(client, loggedin_user):
    assert__requires_role(client, _url(external=False))


def test__get__one(client, faker, loggedin_user_uploader, standard_lookups):
    fu = faker.finance_upload().get_in_db()
    resp = _get(client, _url(), loggedin_user_uploader, has_form=False, expected_count=1)


def test__search__one_found(client, faker, loggedin_user_uploader, standard_lookups):
    fus = [faker.finance_upload().get_in_db() for _ in range(10)]

    resp = _get(client, _url(search=fus[0].filename), loggedin_user_uploader, has_form=False, expected_count=1)


def test__search__none_found(client, faker, loggedin_user_uploader, standard_lookups):
    fu = faker.finance_upload().get_in_db(filename='not_there.xslx')

    resp = _get(client, _url(search='suttin_else.xslx'), loggedin_user_uploader, has_form=False, expected_count=0)
