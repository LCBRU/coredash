import pytest
from flask import url_for
from lbrc_flask.pytest.asserts import assert__search_html, assert__requires_login, assert__select
from coredash.model.people import JobTitle, ProfessionalBackground, ProfessionalBackgroundDetail
from coredash.model.project import UkcrcHealthCategory
from tests.requests import coredash_get
from lbrc_flask.pytest.html_content import get_records_found, get_panel_list_row_count


def _url(external=True, **kwargs):
    return url_for('ui.people_index', _external=external, **kwargs)


def _get(client, url, loggedin_user, faker, has_form, expected_count):
    resp = coredash_get(client, url, loggedin_user, has_form)

    assert__search_html(resp.soup, clear_url=_url(external=False))

    assert__select(soup=resp.soup, id='job_title_id', options=faker.lookup_select_choices(JobTitle))
    assert__select(soup=resp.soup, id='ukcrc_health_category_id', options=faker.lookup_select_choices(UkcrcHealthCategory))
    assert__select(soup=resp.soup, id='professional_background_id', options=faker.lookup_select_choices(ProfessionalBackground))
    assert__select(soup=resp.soup, id='professional_background_detail_id', options=faker.lookup_select_choices(ProfessionalBackgroundDetail))

    assert expected_count == get_records_found(resp.soup)
    assert expected_count == get_panel_list_row_count(resp.soup)

    return resp


def test__get__requires_login(client):
    assert__requires_login(client, _url(external=False))


@pytest.mark.parametrize(
    "n", [1, 2, 3],
)
def test__get__n(client, faker, loggedin_user, standard_lookups, n):
    for _ in range(n):
        faker.person().get_in_db()
    resp = _get(client, _url(), loggedin_user, faker, has_form=False, expected_count=n)


@pytest.mark.parametrize(
    "n", [1, 2, 3],
)
@pytest.mark.parametrize(
    "field", ['first_name', 'last_name', 'comments', 'orcid'],
)
def test__search__string(client, faker, loggedin_user, standard_lookups, n, field):
    for i in range(30):
        params = {field: f"Y'ha-nthlei {i}"}
        faker.person().get_in_db(**params)
    for i in range(n):
        params = {field: f'Cthulhu {i}'}
        faker.person().get_in_db(**params)

    resp = _get(client, _url(search='Cthulhu'), loggedin_user, faker, has_form=False, expected_count=n)


@pytest.mark.parametrize(
    "n", [1, 2, 3],
)
@pytest.mark.parametrize(
    "field, cls", [
        ('job_title', JobTitle),
        ('ukcrc_health_category', UkcrcHealthCategory),
        ('professional_background', ProfessionalBackground),
        ('professional_background_detail', ProfessionalBackgroundDetail),
    ],
)
def test__search__lookup(client, faker, loggedin_user, standard_lookups, n, field, cls):
    for _ in range(30):
        faker.person().get_in_db()
    this_value = faker.lookup_creator(cls).get_in_db()
    for i in range(n):
        params = {field: this_value}
        faker.person().get_in_db(**params)

    search_params = {f"{field}_id": this_value.id}

    resp = _get(client, _url(**search_params), loggedin_user, faker, has_form=False, expected_count=n)
