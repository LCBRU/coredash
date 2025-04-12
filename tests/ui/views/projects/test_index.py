import pytest
from flask import url_for
from lbrc_flask.pytest.asserts import assert__search_html, assert__requires_login, assert__select, assert__input_date, assert__yesno_select
from coredash.model.lookups import Theme
from coredash.model.project import ExpectedImpact, MainFundingCategory, MainFundingDhscNihrFunding, MainFundingIndustry, MainFundingSource, Methodology, NihrPriorityArea, ProjectStatus, RacsSubCategory, ResearchType, TrialPhase, UkcrcHealthCategory, UkcrcResearchActivityCode
from tests.requests import coredash_get
from lbrc_flask.pytest.html_content import get_records_found, get_panel_list_row_count


def _url(external=True, **kwargs):
    return url_for('ui.index', _external=external, **kwargs)


def _get(client, url, loggedin_user, faker, has_form, expected_count):
    resp = coredash_get(client, url, loggedin_user, has_form)

    assert__search_html(resp.soup, clear_url=_url(external=False))

    assert__input_date(soup=resp.soup, id='start_date')
    assert__input_date(soup=resp.soup, id='end_date')

    assert__yesno_select(soup=resp.soup, id='sensitive')
    assert__yesno_select(soup=resp.soup, id='first_in_human')
    assert__yesno_select(soup=resp.soup, id='link_to_nihr_transactional_research_collaboration')
    assert__yesno_select(soup=resp.soup, id='crn_rdn_portfolio_study')
    assert__yesno_select(soup=resp.soup, id='rec_approval_required')
    assert__yesno_select(soup=resp.soup, id='randomised_trial')

    assert__select(soup=resp.soup, id='project_status_id', options=faker.lookup_select_choices(ProjectStatus))
    assert__select(soup=resp.soup, id='theme_id', options=faker.lookup_select_choices(Theme))
    assert__select(soup=resp.soup, id='ukcrc_health_category_id', options=faker.lookup_select_choices(UkcrcHealthCategory))
    assert__select(soup=resp.soup, id='nihr_priority_area_id', options=faker.lookup_select_choices(NihrPriorityArea))
    assert__select(soup=resp.soup, id='ukcrc_research_activity_code_id', options=faker.lookup_select_choices(UkcrcResearchActivityCode))
    assert__select(soup=resp.soup, id='racs_sub_category_id', options=faker.lookup_select_choices(RacsSubCategory))
    assert__select(soup=resp.soup, id='research_type_id', options=faker.lookup_select_choices(ResearchType))
    assert__select(soup=resp.soup, id='methodology_id', options=faker.lookup_select_choices(Methodology))
    assert__select(soup=resp.soup, id='expected_impact_id', options=faker.lookup_select_choices(ExpectedImpact))
    assert__select(soup=resp.soup, id='trial_phase_id', options=faker.lookup_select_choices(TrialPhase))
    assert__select(soup=resp.soup, id='main_funding_source_id', options=faker.lookup_select_choices(MainFundingSource))
    assert__select(soup=resp.soup, id='main_funding_category_id', options=faker.lookup_select_choices(MainFundingCategory))
    assert__select(soup=resp.soup, id='main_funding_dhsc_nihr_funding_id', options=faker.lookup_select_choices(MainFundingDhscNihrFunding))
    assert__select(soup=resp.soup, id='main_funding_industry_id', options=faker.lookup_select_choices(MainFundingIndustry))

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
        faker.project().get_in_db()
    resp = _get(client, _url(), loggedin_user, faker, has_form=False, expected_count=n)


@pytest.mark.parametrize(
    "n", [1, 2, 3],
)
@pytest.mark.parametrize(
    "field", ['title', 'summary', 'comments', 'local_rec_number', 'iras_number'],
)
def test__search__string(client, faker, loggedin_user, standard_lookups, n, field):
    for _ in range(30):
        faker.project().get_in_db()
    for i in range(n):
        params = {field: f'the fred one {i}'}
        faker.project().get_in_db(**params)

    resp = _get(client, _url(search='fred'), loggedin_user, faker, has_form=False, expected_count=n)


@pytest.mark.parametrize(
    "n", [1, 2, 3],
)
@pytest.mark.parametrize(
    "field", ['sensitive', 'first_in_human', 'link_to_nihr_transactional_research_collaboration', 'crn_rdn_portfolio_study', 'rec_approval_required', 'randomised_trial'],
)
@pytest.mark.parametrize(
    "value", ['yes', 'no'],
)
def test__search__yesno(client, faker, loggedin_user, standard_lookups, n, field, value):
    for _ in range(30):
        params = {field: value == 'no'}
        x = faker.project().get_in_db(**params)
    for i in range(n):
        params = {field: value == 'yes'}
        x = faker.project().get_in_db(**params)

    search_params = {field: value}
    resp = _get(client, _url(**search_params), loggedin_user, faker, has_form=False, expected_count=n)


@pytest.mark.parametrize(
    "n", [1, 2, 3],
)
@pytest.mark.parametrize(
    "field, cls", [
        ('project_status', ProjectStatus),
        ('theme', Theme),
        ('ukcrc_health_category', UkcrcHealthCategory),
        ('nihr_priority_area', NihrPriorityArea),
        ('ukcrc_research_activity_code', UkcrcResearchActivityCode),
        ('racs_sub_category', RacsSubCategory),
        ('research_type', ResearchType),
        ('methodology', Methodology),
        ('expected_impact', ExpectedImpact),
        ('trial_phase', TrialPhase),
        ('main_funding_source', MainFundingSource),
        ('main_funding_category', MainFundingCategory),
        ('main_funding_dhsc_nihr_funding', MainFundingDhscNihrFunding),
        ('main_funding_industry', MainFundingIndustry),
    ],
)
def test__search__string(client, faker, loggedin_user, standard_lookups, n, field, cls):
    for _ in range(30):
        faker.project().get_in_db()
    this_value = faker.lookup_creator(cls).get_in_db()
    for i in range(n):
        params = {field: this_value}
        faker.project().get_in_db(**params)

    search_params = {f"{field}_id": this_value.id}

    resp = _get(client, _url(**search_params), loggedin_user, faker, has_form=False, expected_count=n)
