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


def project_save(project, data):
    project.title = data['title']
    project.summary = data['summary']
    project.comments = data['comments']
    project.local_rec_number = data['local_rec_number']
    project.iras_number = data['iras_number']
    project.cpms_id = data['cpms_id']
    project.start_date = data['start_date']
    project.end_date = data['end_date']
    project.participants_recruited_to_centre_fy = data['participants_recruited_to_centre_fy']
    project.brc_funding = data['brc_funding']
    project.main_funding_brc_funding = data['main_funding_brc_funding']
    project.total_external_funding_award = data['total_external_funding_award']
    project.sensitive = data['sensitive']
    project.first_in_human = data['first_in_human']
    project.link_to_nihr_transactional_research_collaboration = data['link_to_nihr_transactional_research_collaboration']
    project.crn_rdn_portfolio_study = data['crn_rdn_portfolio_study']
    project.rec_approval_required = data['rec_approval_required']
    project.randomised_trial = data['randomised_trial']
    project.project_status_id = data['project_status_id']
    project.theme_id = data['theme_id']
    project.ukcrc_health_category_id = data['ukcrc_health_category_id']
    project.nihr_priority_area_id = data['nihr_priority_area_id']
    project.ukcrc_research_activity_code_id = data['ukcrc_research_activity_code_id']
    project.racs_sub_category_id = data['racs_sub_category_id']
    project.research_type_id = data['research_type_id']
    project.methodology_id = data['methodology_id']
    project.expected_impact_id = data['expected_impact_id']
    project.trial_phase_id = data['trial_phase_id']
    project.main_funding_source_id = data['main_funding_source_id']
    project.main_funding_category_id = data['main_funding_category_id']
    project.main_funding_dhsc_nihr_funding_id = data['main_funding_dhsc_nihr_funding_id']
    project.main_funding_industry_id = data['main_funding_industry_id']

    db.session.add(project)
