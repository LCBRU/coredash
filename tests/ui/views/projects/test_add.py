import pytest
from flask import url_for
from lbrc_flask.pytest.asserts import assert__requires_login, assert__refresh_response, assert__requires_role
from lbrc_flask.database import db
from sqlalchemy import func, select
from coredash.model.project import Project
from tests.requests import coredash_modal_get
from tests.ui.views.projects import assert_actual_equals_expected_project, assert_project_form, convert_project_to_form_data, project_form_lookup_names


def _url(external=True, **kwargs):
    return url_for('ui.project_add', _external=external, **kwargs)


def _get(client, url, loggedin_user, has_form, faker):
    resp = coredash_modal_get(client, url, loggedin_user, has_form)

    assert_project_form(resp, faker)

    return resp


def _post(client, url, data):
    return client.post(
        url,
        data=data,
    )


def test__get__requires_login(client):
    assert__requires_login(client, _url(external=False))


def test__get__requires_editor_login__not(client, loggedin_user):
    assert__requires_role(client, _url(external=False))


@pytest.mark.app_crsf(True)
def test__get__has_form(client, loggedin_user_project_editor, standard_lookups, faker):
    _get(client, _url(external=False), loggedin_user_project_editor, has_form=True, faker=faker)


def test__post__valid_project(client, faker, loggedin_user_project_editor, standard_lookups):
    expected: Project = faker.project().get()

    print(convert_project_to_form_data(expected))

    resp = _post(
        client=client,
        url=_url(),
        data=convert_project_to_form_data(expected),
    )

    assert__refresh_response(resp)

    assert db.session.execute(select(func.count(Project.id))).scalar() == 1
    actual = db.session.execute(select(Project)).scalar()

    assert_actual_equals_expected_project(expected, actual)


@pytest.mark.parametrize(
    "missing_column_name", project_form_lookup_names() + [
        'title',
        'summary',
        'local_rec_number',
        'iras_number',
        'cpms_id',
        'start_date',
        'end_date',
        'participants_recruited_to_centre_fy',
        'brc_funding',
        'main_funding_brc_funding',
        'total_external_funding_award',
    ],
)
def test__post__missing_column(client, faker, loggedin_user_project_editor, standard_lookups, missing_column_name):
    expected: Project = faker.project().get()
    data = convert_project_to_form_data(expected)
    data[missing_column_name] = ''

    resp = _post(
        client=client,
        url=_url(),
        data=data,
    )
    assert_project_form(resp, faker)

    assert db.session.execute(select(func.count(Project.id))).scalar() == 0


@pytest.mark.parametrize(
    "invalid_column_name", ['participants_recruited_to_centre_fy', 'brc_funding', 'main_funding_brc_funding', 'total_external_funding_award'],
)
def test__post__invalid_column__integer(client, faker, loggedin_user_project_editor, standard_lookups, invalid_column_name):
    expected: Project = faker.project().get()
    data = convert_project_to_form_data(expected)
    data[invalid_column_name] = 'Blob'

    resp = _post(
        client=client,
        url=_url(),
        data=data,
    )
    assert_project_form(resp, faker)

    assert db.session.execute(select(func.count(Project.id))).scalar() == 0


@pytest.mark.parametrize(
    "invalid_column_name", ['start_date', 'end_date'],
)
def test__post__invalid_column__date(client, faker, loggedin_user_project_editor, standard_lookups, invalid_column_name):
    expected: Project = faker.project().get()
    data = convert_project_to_form_data(expected)
    data[invalid_column_name] = 'Blob'

    resp = _post(
        client=client,
        url=_url(),
        data=data,
    )
    assert_project_form(resp, faker)

    assert db.session.execute(select(func.count(Project.id))).scalar() == 0


@pytest.mark.parametrize(
    "invalid_column_name", project_form_lookup_names(),
)
def test__post__invalid_column__select_value(client, faker, loggedin_user_project_editor, standard_lookups, invalid_column_name):
    expected: Project = faker.project().get()
    data = convert_project_to_form_data(expected)
    data[invalid_column_name] = 'Blob'

    resp = _post(
        client=client,
        url=_url(),
        data=data,
    )
    assert_project_form(resp, faker)

    assert db.session.execute(select(func.count(Project.id))).scalar() == 0


@pytest.mark.parametrize(
    "invalid_column_name", project_form_lookup_names(),
)
def test__post__invalid_column__select_non_existent(client, faker, loggedin_user_project_editor, standard_lookups, invalid_column_name):
    expected: Project = faker.project().get()
    data = convert_project_to_form_data(expected)
    data[invalid_column_name] = 1000

    resp = _post(
        client=client,
        url=_url(),
        data=data,
    )
    assert_project_form(resp, faker)

    assert db.session.execute(select(func.count(Project.id))).scalar() == 0


@pytest.mark.parametrize(
    "invalid_column_name", ['title', 'local_rec_number', 'iras_number', 'cpms_id'],
)
def test__post__invalid_column__string_length(client, faker, loggedin_user_project_editor, standard_lookups, invalid_column_name):
    expected: Project = faker.project().get()
    data = convert_project_to_form_data(expected)
    data[invalid_column_name] = 'A'*1000

    resp = _post(
        client=client,
        url=_url(),
        data=data,
    )
    assert_project_form(resp, faker)

    assert db.session.execute(select(func.count(Project.id))).scalar() == 0
