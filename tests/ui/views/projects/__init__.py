from lbrc_flask.pytest.asserts import assert__input_date, assert__select, assert__input_checkbox
from coredash.model.lookups import Theme
from coredash.model.project import ExpectedImpact, MainFundingCategory, MainFundingDhscNihrFunding, MainFundingIndustry, MainFundingSource, Methodology, NihrPriorityArea, ProjectStatus, RacsSubCategory, ResearchType, TrialPhase, UkcrcHealthCategory, UkcrcResearchActivityCode


def assert_project_form(resp, faker):
    assert__input_date(resp.soup, 'start_date')
    assert__input_date(resp.soup, 'end_date')
    assert__input_checkbox(resp.soup, 'sensitive')
    assert__input_checkbox(resp.soup, 'first_in_human')
    assert__input_checkbox(resp.soup, 'link_to_nihr_transactional_research_collaboration')
    assert__input_checkbox(resp.soup, 'crn_rdn_portfolio_study')
    assert__input_checkbox(resp.soup, 'rec_approval_required')
    assert__input_checkbox(resp.soup, 'randomised_trial')
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


def assert_actual_equals_expected_project(expected, actual):
    assert actual is not None
    assert actual.title == expected.title
    assert actual.summary == expected.summary
    assert actual.comments == expected.comments
    assert actual.local_rec_number == expected.local_rec_number
    assert actual.iras_number == expected.iras_number
    assert actual.start_date == expected.start_date
    assert actual.end_date == expected.end_date
    assert actual.participants_recruited_to_centre_fy == expected.participants_recruited_to_centre_fy
    assert actual.brc_funding == expected.brc_funding
    assert actual.main_funding_brc_funding == expected.main_funding_brc_funding
    assert actual.total_external_funding_award == expected.total_external_funding_award
    assert actual.sensitive == expected.sensitive
    assert actual.first_in_human == expected.first_in_human
    assert actual.link_to_nihr_transactional_research_collaboration == expected.link_to_nihr_transactional_research_collaboration
    assert actual.crn_rdn_portfolio_study == expected.crn_rdn_portfolio_study
    assert actual.rec_approval_required == expected.rec_approval_required
    assert actual.randomised_trial == expected.randomised_trial
    assert actual.project_status_id == expected.project_status.id
    assert actual.theme_id == expected.theme.id
    assert actual.ukcrc_health_category_id == expected.ukcrc_health_category.id
    assert actual.nihr_priority_area_id == expected.nihr_priority_area.id
    assert actual.ukcrc_research_activity_code_id == expected.ukcrc_research_activity_code.id
    assert actual.racs_sub_category_id == expected.racs_sub_category.id
    assert actual.research_type_id == expected.research_type.id
    assert actual.methodology_id == expected.methodology.id
    assert actual.expected_impact_id == expected.expected_impact.id
    assert actual.trial_phase_id == expected.trial_phase.id
    assert actual.main_funding_source_id == expected.main_funding_source.id
    assert actual.main_funding_category_id == expected.main_funding_category.id
    assert actual.main_funding_dhsc_nihr_funding_id == expected.main_funding_dhsc_nihr_funding.id
    assert actual.main_funding_industry_id == expected.main_funding_industry.id


def convert_project_to_form_data(project):
    result = {
        "title": project.title,
        "summary": project.summary,
        "comments": project.comments,
        "local_rec_number": project.local_rec_number,
        "iras_number": project.iras_number,
        "cpms_id": project.cpms_id,
        "start_date": project.start_date,
        "end_date": project.end_date,
        "participants_recruited_to_centre_fy": project.participants_recruited_to_centre_fy,
        "brc_funding": project.brc_funding,
        "main_funding_brc_funding": project.main_funding_brc_funding,
        "total_external_funding_award": project.total_external_funding_award,

        "sensitive": True if project.sensitive else None,
        "first_in_human": True if project.first_in_human else None,
        "link_to_nihr_transactional_research_collaboration": True if project.link_to_nihr_transactional_research_collaboration else None,
        "crn_rdn_portfolio_study": True if project.crn_rdn_portfolio_study else None,
        "rec_approval_required": True if project.rec_approval_required else None,
        "randomised_trial": True if project.randomised_trial else None,

        "project_status_id": project.project_status.id,
        "theme_id": project.theme.id,
        "ukcrc_health_category_id": project.ukcrc_health_category.id,
        "nihr_priority_area_id": project.nihr_priority_area.id,
        "ukcrc_research_activity_code_id": project.ukcrc_research_activity_code.id,
        "racs_sub_category_id": project.racs_sub_category.id,
        "research_type_id": project.research_type.id,
        "methodology_id": project.methodology.id,
        "expected_impact_id": project.expected_impact.id,
        "trial_phase_id": project.trial_phase.id,
        "main_funding_source_id": project.main_funding_source.id,
        "main_funding_category_id": project.main_funding_category.id,
        "main_funding_dhsc_nihr_funding_id": project.main_funding_dhsc_nihr_funding.id,
        "main_funding_industry_id": project.main_funding_industry.id,
    }

    return result


def project_form_lookup_names():
    return [
        'project_status_id',
        'theme_id',
        'ukcrc_health_category_id',
        'nihr_priority_area_id',
        'ukcrc_research_activity_code_id',
        'racs_sub_category_id',
        'research_type_id',
        'methodology_id',
        'expected_impact_id',
        'trial_phase_id',
        'main_funding_source_id',
        'main_funding_category_id',
        'main_funding_dhsc_nihr_funding_id',
        'main_funding_industry_id',
    ]
