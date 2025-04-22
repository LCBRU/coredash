from datetime import date
import pytest
from flask import url_for
from lbrc_flask.pytest.asserts import assert__requires_login, assert__refresh_response, assert__requires_role
from lbrc_flask.database import db
from sqlalchemy import func, select
from coredash.model.project import Project
from tests.requests import coredash_modal_get
from tests.ui.views.projects import assert_actual_equals_expected_project, assert_project_form, convert_project_to_form_data, project_form_lookup_names


def updater_out(faker, standard_lookups):
    result: Project = faker.project().get(
        title='Title A',
        summary='Summary A',
        comments='Comments A',

        local_rec_number='LR_A',
        iras_number='I_A',
        cpms_id='CPMS_A',

        start_date=date(2025, 1, 1),
        end_date=date(2025, 6, 1),

        participants_recruited_to_centre_fy=1001,
        brc_funding=2001,
        main_funding_brc_funding=3001,
        total_external_funding_award=4001,

        sensitive=True,
        first_in_human=True,
        link_to_nihr_transactional_research_collaboration=True,
        crn_rdn_portfolio_study=True,
        rec_approval_required=True,
        randomised_trial=True,

        project_status=standard_lookups['project status'][0],
        theme=standard_lookups['theme'][0],
        ukcrc_health_category=standard_lookups['ukcrc health category'][0],
        nihr_priority_area=standard_lookups['nihr priority area'][0],
        ukcrc_research_activity_code=standard_lookups['ukcrc research activity code'][0],
        racs_sub_category=standard_lookups['racs sub category'][0],
        research_type=standard_lookups['research type'][0],
        methodology=standard_lookups['methodology'][0],
        expected_impact=standard_lookups['expected impact'][0],
        trial_phase=standard_lookups['trial phase'][0],
        main_funding_source=standard_lookups['main funding source'][0],
        main_funding_category=standard_lookups['main funding category'][0],
        main_funding_dhsc_nihr_funding=standard_lookups['main funding dhsc nihr funding'][0],
        main_funding_industry=standard_lookups['main funding industry'][0],
    )
    
    return result


def original_out(faker, standard_lookups):
    result: Project = faker.project().get(
        title='Title B',
        summary='Summary B',
        comments='Comments B',

        local_rec_number='LR_B',
        iras_number='I_B',
        cpms_id='CPMS_B',

        start_date=date(2025, 1, 2),
        end_date=date(2025, 6, 2),

        participants_recruited_to_centre_fy=1002,
        brc_funding=2002,
        main_funding_brc_funding=3002,
        total_external_funding_award=4002,

        sensitive=False,
        first_in_human=False,
        link_to_nihr_transactional_research_collaboration=False,
        crn_rdn_portfolio_study=False,
        rec_approval_required=False,
        randomised_trial=False,

        project_status=standard_lookups['project status'][1],
        theme=standard_lookups['theme'][1],
        ukcrc_health_category=standard_lookups['ukcrc health category'][1],
        nihr_priority_area=standard_lookups['nihr priority area'][1],
        ukcrc_research_activity_code=standard_lookups['ukcrc research activity code'][1],
        racs_sub_category=standard_lookups['racs sub category'][1],
        research_type=standard_lookups['research type'][1],
        methodology=standard_lookups['methodology'][1],
        expected_impact=standard_lookups['expected impact'][1],
        trial_phase=standard_lookups['trial phase'][1],
        main_funding_source=standard_lookups['main funding source'][1],
        main_funding_category=standard_lookups['main funding category'][1],
        main_funding_dhsc_nihr_funding=standard_lookups['main funding dhsc nihr funding'][1],
        main_funding_industry=standard_lookups['main funding industry'][1],
    )

    db.session.add(result)
    db.session.commit()
    
    return result


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


def test__post__valid(client, faker, loggedin_user_project_editor, standard_lookups):
    original = original_out(faker, standard_lookups)
    expected = updater_out(faker, standard_lookups)
    
    resp = _post(
        client=client,
        url=_url(id=original.id),
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
    original = original_out(faker, standard_lookups)
    expected = updater_out(faker, standard_lookups)
    data = convert_project_to_form_data(expected)
    data[missing_column_name] = ''

    resp = _post(
        client=client,
        url=_url(id=original.id),
        data=data,
    )
    assert_project_form(resp, faker)

    assert db.session.execute(select(func.count(Project.id))).scalar() == 1


@pytest.mark.parametrize(
    "invalid_column_name", ['participants_recruited_to_centre_fy', 'brc_funding', 'main_funding_brc_funding', 'total_external_funding_award'],
)
def test__post__invalid_column__integer(client, faker, loggedin_user_project_editor, standard_lookups, invalid_column_name):
    original = original_out(faker, standard_lookups)
    expected = updater_out(faker, standard_lookups)
    data = convert_project_to_form_data(expected)
    data[invalid_column_name] = 'Blob'

    resp = _post(
        client=client,
        url=_url(id=original.id),
        data=data,
    )
    assert_project_form(resp, faker)

    assert db.session.execute(select(func.count(Project.id))).scalar() == 1


@pytest.mark.parametrize(
    "invalid_column_name", ['start_date', 'end_date'],
)
def test__post__invalid_column__date(client, faker, loggedin_user_project_editor, standard_lookups, invalid_column_name):
    original = original_out(faker, standard_lookups)
    expected = updater_out(faker, standard_lookups)
    data = convert_project_to_form_data(expected)
    data[invalid_column_name] = 'Blob'

    resp = _post(
        client=client,
        url=_url(id=original.id),
        data=data,
    )
    assert_project_form(resp, faker)

    assert db.session.execute(select(func.count(Project.id))).scalar() == 1


@pytest.mark.parametrize(
    "invalid_column_name", project_form_lookup_names(),
)
def test__post__invalid_column__select_value(client, faker, loggedin_user_project_editor, standard_lookups, invalid_column_name):
    original = original_out(faker, standard_lookups)
    expected = updater_out(faker, standard_lookups)
    data = convert_project_to_form_data(expected)
    data[invalid_column_name] = 'Blob'

    resp = _post(
        client=client,
        url=_url(id=original.id),
        data=data,
    )
    assert_project_form(resp, faker)

    assert db.session.execute(select(func.count(Project.id))).scalar() == 1


@pytest.mark.parametrize(
    "invalid_column_name", project_form_lookup_names(),
)
def test__post__invalid_column__select_non_existent(client, faker, loggedin_user_project_editor, standard_lookups, invalid_column_name):
    original = original_out(faker, standard_lookups)
    expected = updater_out(faker, standard_lookups)
    data = convert_project_to_form_data(expected)
    data[invalid_column_name] = 1000

    resp = _post(
        client=client,
        url=_url(id=original.id),
        data=data,
    )
    assert_project_form(resp, faker)

    assert db.session.execute(select(func.count(Project.id))).scalar() == 1


@pytest.mark.parametrize(
    "invalid_column_name", ['title', 'local_rec_number', 'iras_number', 'cpms_id'],
)
def test__post__invalid_column__string_length(client, faker, loggedin_user_project_editor, standard_lookups, invalid_column_name):
    original = original_out(faker, standard_lookups)
    expected = updater_out(faker, standard_lookups)
    data = convert_project_to_form_data(expected)
    data[invalid_column_name] = 'A'*1000

    resp = _post(
        client=client,
        url=_url(id=original.id),
        data=data,
    )
    assert_project_form(resp, faker)

    assert db.session.execute(select(func.count(Project.id))).scalar() == 1
