from dotenv import load_dotenv

from coredash.model.lookups import Theme
from coredash.model.project import ExpectedImpact, MainFundingCategory, MainFundingDhscNihrFunding, MainFundingIndustry, Methodology, NihrPriorityArea, ProjectStatus, RacsSubCategory, ResearchType, TrialPhase, UkcrcHealthCategory, UkcrcResearchActivityCode

# Load environment variables from '.env' file.
load_dotenv()

import alembic.config

from lbrc_flask.security import get_admin_user, add_user_to_role
from coredash import create_app
from lbrc_flask.database import db
from lbrc_flask.lookups import LookupRepository
from coredash.security import init_authorization, ROLENAMES
from coredash.model import *

alembicArgs = [
    '--raiseerr',
    'upgrade', 'head',
]
alembic.config.main(argv=alembicArgs)

application = create_app()
application.app_context().push()

init_authorization()

admin_user = get_admin_user()
for r in ROLENAMES:
    add_user_to_role(admin_user, r)

# Create Project Statuses
project_status_repo = LookupRepository(ProjectStatus)
project_statuses = project_status_repo.get_or_create_all([
    'Closed Follow Up Complete',
    'Closed in Follow up',
    'Closed, No Follow Up',
    'In Setup NHS Permission Received',
    'In Setup Pending NHS Permission',
    'In Setup, Approval Received',
    'Open to Recruitment',
    'Open, with Recruitment',
    'Pre-Setup',
    'Suspended',
    'The study is in set-up and is awaiting approval to commence recruitment',
])
db.session.add_all(project_statuses)
db.session.commit()

# Create Themes
theme_repo = LookupRepository(Theme)
themes = theme_repo.get_or_create_all([
    'Cancer',
    'Lifestyle',
    'Respiratory',
    'Environment',
    'Cardiovascular',
    'Data',
])
db.session.add_all(themes)
db.session.commit()

# Create UkcrcHealthCategory
health_cat_repo = LookupRepository(UkcrcHealthCategory)
health_cats = health_cat_repo.get_or_create_all([
    'Cancer',
    'Lifestyle',
    'Respiratory',
    'Environment',
    'Cardiovascular',
    'Data',
    'Cancer and neoplasms',
    'Metabolic and Endocrine',
    'Renal and Urogenital',
    'Musculoskeletal',
    'Infection',
    'Generic health relevance',
    'Inflammatory and immune system',
])
db.session.add_all(health_cats)
db.session.commit()

# Create NihrPriorityArea
priority_area_repo = LookupRepository(NihrPriorityArea)
priority_areas = priority_area_repo.get_or_create_all([
    'Innovative clinical trials',
    'Equality, Diversity, & Inclusion',
    'Multiple long-term conditions;Covid-19',
    'Health information technology/ digital transformation',
    'Artificial Intelligence',
    'Multiple long-term conditions: Health ageing',
    'Prevention agenda',
    'Patient & Public Involvement (PPI)',
    'Obesity/ healthy weight',
    'Research addressing health inequalities',
    'Multiple long-term conditions',
    'Diabetes',
    'Covid-19',
    'Healthy ageing',
    'Public health',
    'Antimicrobial resistance',
    'Med-tech',
    'Social care',
    'Leveling up (research following burden of patient need)',
])
db.session.add_all(priority_areas)
db.session.commit()

# Create UkcrcResearchActivityCode
research_activity_repo = LookupRepository(UkcrcResearchActivityCode)
research_activities = research_activity_repo.get_or_create_all([
    'Evaluation of treatments and therapeutic interventions',
    'Underpinning research',
    'Health and social care services research',
    'Development of treatments and therapeutic interventions',
    'Detection, screening and diagnosis',
    'Aetiology',
    'Prevention of disease and conditions, and promotion of well-being',
    'Management of diseases and conditions',
])
db.session.add_all(research_activities)
db.session.commit()

# Create RacsSubCategory
racs_subcategory_repo = LookupRepository(RacsSubCategory)
racs_subcategories = racs_subcategory_repo.get_or_create_all([
    'Drug',
    'Cellular/Cells',
    'Vaccine',
    'Device',
    'Gene Therapy',
])
db.session.add_all(racs_subcategories)
db.session.commit()

# Create ResearchType
research_type_repo = LookupRepository(ResearchType)
research_types = research_type_repo.get_or_create_all([
    'Clinical trial or investigation',
    'Proof of concept or feasability',
    'Methodology development',
    'Basic science',
    'Epidemiological',
    'Evaluation',
    'Implementation',
])
db.session.add_all(research_types)
db.session.commit()

# Create Methodology
methodology_repo = LookupRepository(Methodology)
methodologies = methodology_repo.get_or_create_all([
    'Mixed methods',
    'Human tissue/Tissuebank use',
    'Research database',
    'Cohort based',
    'Quantitative',
    'Qualitative',
    'Modelling',
    'Survey/Questionnaire',
    'Cross-sectional',
    'Literature review',
    'Meta analysis',
])
db.session.add_all(methodologies)
db.session.commit()

# Create ExpectedImpact
expected_impact_repo = LookupRepository(ExpectedImpact)
expected_impacts = expected_impact_repo.get_or_create_all([
    'Improved patient/service user outcomes',
    'Changes in service delivery',
    'Policy influence',
    'Developing and delivering operational excellence',
    'Systems influence',
    'Capacity, skills or workforce development',
])
db.session.add_all(expected_impacts)
db.session.commit()

# Create TrialPhase
trial_phase_repo = LookupRepository(TrialPhase)
trial_phases = trial_phase_repo.get_or_create_all([
    'Phase II',
    'Phase I',
    'Phase III',
    'Phase IV',
])
db.session.add_all(trial_phases)
db.session.commit()

# Create MainFundingCategory
main_funding_category_repo = LookupRepository(MainFundingCategory)
main_funding_categories = main_funding_category_repo.get_or_create_all([
    'Industry contract',
    'Research charity',
    'DHSC/NIHR',
    'BRC funded',
    'Research council',
    'Industry collaborative',
    'Other non-commercial',
])
db.session.add_all(main_funding_categories)
db.session.commit()

# Create MainFundingDhscNihrFunding
main_funding_dhsc_nihr_repo = LookupRepository(MainFundingDhscNihrFunding)
main_funding_dhsc_nihrs = main_funding_dhsc_nihr_repo.get_or_create_all([
    'Other NIHR funding',
    'EME',
    'HTA',
    'PGfAR',
    'Other Infrastructure',
    'HS&DR',
    'RfPB',
    'i4i',
])
db.session.add_all(main_funding_dhsc_nihrs)
db.session.commit()

# Create MainFundingIndustry
main_funding_industry_repo = LookupRepository(MainFundingIndustry)
main_funding_industries = main_funding_industry_repo.get_or_create_all([
    'Pharma',
    'Biotech',
    'Medtech/device',
])
db.session.add_all(main_funding_industries)
db.session.commit()

db.session.close()