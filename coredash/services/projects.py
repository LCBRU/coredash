from lbrc_flask.database import db
from sqlalchemy import or_, select
from coredash.model.project import Project, ProjectStatus


def project_search_query(search_data=None):
    q = select(Project)

    search_data = search_data or []

    if x := search_data.get('search'):
        for word in x.split():
            q = q.where(or_(
                Project.title.like(f"%{word}%"),
                Project.summary.like(f"%{word}%"),
                Project.comments.like(f"%{word}%"),
                Project.local_rec_number.like(f"%{word}%"),
                Project.iras_number.like(f"%{word}%"),
            ))

    if search_data.get('sensitive') is not None:
        q = q.where(Project.sensitive == search_data.get('sensitive'))

    if search_data.get('first_in_human') is not None:
        q = q.where(Project.first_in_human == search_data.get('first_in_human'))

    if search_data.get('link_to_nihr_transactional_research_collaboration') is not None:
        q = q.where(Project.link_to_nihr_transactional_research_collaboration == search_data.get('link_to_nihr_transactional_research_collaboration'))

    if search_data.get('crn_rdn_portfolio_study') is not None:
        q = q.where(Project.crn_rdn_portfolio_study == search_data.get('crn_rdn_portfolio_study'))

    if search_data.get('rec_approval_required') is not None:
        q = q.where(Project.rec_approval_required == search_data.get('rec_approval_required'))

    if search_data.get('randomised_trial') is not None:
        q = q.where(Project.randomised_trial == search_data.get('randomised_trial'))

    if x := search_data.get('project_status_id'):
        q = q.where(Project.project_status_id == x)

    if x := search_data.get('theme_id'):
        q = q.where(Project.theme_id == x)

    if x := search_data.get('ukcrc_health_category_id'):
        q = q.where(Project.ukcrc_health_category_id == x)

    if x := search_data.get('nihr_priority_area_id'):
        q = q.where(Project.nihr_priority_area_id == x)

    if x := search_data.get('ukcrc_research_activity_code_id'):
        q = q.where(Project.ukcrc_research_activity_code_id == x)

    if x := search_data.get('racs_sub_category_id'):
        q = q.where(Project.racs_sub_category_id == x)

    if x := search_data.get('research_type_id'):
        q = q.where(Project.research_type_id == x)

    if x := search_data.get('methodology_id'):
        q = q.where(Project.methodology_id == x)

    if x := search_data.get('expected_impact_id'):
        q = q.where(Project.expected_impact_id == x)

    if x := search_data.get('trial_phase_id'):
        q = q.where(Project.trial_phase_id == x)

    if x := search_data.get('main_funding_source_id'):
        q = q.where(Project.main_funding_source_id == x)

    if x := search_data.get('main_funding_category_id'):
        q = q.where(Project.main_funding_category_id == x)

    if x := search_data.get('main_funding_dhsc_nihr_funding_id'):
        q = q.where(Project.main_funding_dhsc_nihr_funding_id == x)

    if x := search_data.get('main_funding_industry_id'):
        q = q.where(Project.main_funding_industry_id == x)

    return q
