from dotenv import load_dotenv

from coredash.model.lookups import Theme
from coredash.model.project import ExpectedImpact, MainFundingCategory, MainFundingDhscNihrFunding, MainFundingIndustry, MainFundingSource, Methodology, NihrPriorityArea, ProjectStatus, RacsSubCategory, ResearchType, TrialPhase, UkcrcHealthCategory, UkcrcResearchActivityCode

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

# Create MainFundingSource
main_funding_source_repo = LookupRepository(MainFundingSource)
main_funding_sources = main_funding_source_repo.get_or_create_all([
    'Medtronic, Inc.',
    'Collaboration for Leadership in Applied Health Research and Care (CLAHRC)',
    'NHS',
    'NIHR Programme Grant',
    'Servier Affaires Medicales',
    'Eli Lilly and Company Ltd (UK)',
    'Other/Miscellaneous',
    'Health Technology Assessment Programme (UK)',
    'British Heart Foundaion',
    'BHF',
    'Industry Collaborative',
    'Bayer AG',
    'NIHR BRC',
    'University College London Hospitals NHS Foundation Trust',
    'AstraZeneca UK Limited',
    'UKRI/NIHR Rapid Response Rolling Call',
    'Boston Scientific Corporate Headquarters',
    'Medidata Solutions, Inc',
    'King’s College London/BHF',
    'SQ Innovation, Inc',
    'NIHR Grant',
    'Abbott Vascular International BVBA',
    'NIHR Newcastle Biomedical Research Unit',
    'Glenfield Hospital - Heart Link Charity',
    'Med Alliance SA',
    'Shockwave Medical Incorporated',
    'Catheter Precision. Inc.',
    'No application for external funding will be made',
    'Heart Research UK',
    'UK Research and Innovation',
    'W. L. Gore & Associates (UK) Limited',
    'Industry funded project',
    'PHD funded',
    'British Heart Foundation Research Accelerator Award',
    'The George Institute for Global Health',
    'Funding secured from one or more funders',
    'The British Society for Heart Failure',
    'Vifor Pharma',
    'Canadian Institutes of Health Research',
    'Pump-priming project, University of Leeds',
    'Abbott Medical UK Ltd',
    'The Burdett Trust for Nursing',
    'National Institute for Health and Care Research',
    'Cardiovascular Sciences',
    'Bradford Institute for Health Research, NIHR Health Technology Assessment Programme',
    'Medtronic Inc',
    'UK Research and Innovation UKRI',
    'The study is in set-up and is awaiting approval to commence recruitment.',
    'Faraday Pharmaceuticals Inc',
    'Sir Jules Thorn Charitable Trust',
    'NIHR Biomedical Research Unit',
    'The Medicines Company',
    'Saudi Arabian Cultural Bureau',
    'Portola Pharmaceuticals, Inc',
    'National Institute for Health Research',
    'Highlife SAS',
    'British Heart Foundation',
    'Novartis Pharma Arzneimittel GmbH',
    'Medpace Finland OY',
    'JP Moulton Charitable Foundation',
    'The George Institute for Global Health National Health and Medical Research Council (NHMRC), Australia',
    'Boehringer Ingelheim Pharma GmbH & Co. KG',
    'Biotronik UK Ltd,SAHMRI Heart Foundation, Heart Health',
    'NIHR Health Services and Delivery Research',
    'Hull and East Yorkshire Hospitals NHS Trust',
    'Kompetenznetz Vorhofflimmern e.V. (AFNET) [Atrial Fibrillation NETwork]',
    'British Heart Foundation (BHF), National Institute for Health Research (NIHR)',
    'The study is supported with funding from the Oxford Biomedical research Centre, The British Heart Foundation, Innovate UK, the National Consortium for Intelligent Medical Imaging and the European Commission.',
    'DEFRA',
    'Asthma & Lung UK / Victor Daladeh Foundation',
    'MRC',
    'NIHR/other',
    'Acadamy of Medical Sciences',
    'BioInvent International AB',
    'F. Hoffmann-La Roche Ltd',
    'Exelixis Inc',
    'Genentech Inc',
    'Takeda',
    'CRUK',
    'Acerta Pharma BV',
    'Gilead Sciences, Inc',
    'CellCentric Ltd',
    'Merck Sharp & Dohme Corp., a subsidiary of Merck & Co., Inc.',
    'ECMC',
    'Constellation Pharmaceuticals, Inc.',
    'Janssen-Cilag International NV',
    'CRUK/Accelerator',
    'Beigene',
    'F Hoffmann-La Roche Ltd',
    'No funding required as retrospective data analysis using existing datasets collected',
    'PFIZER LTD Dublin - charitable fund',
    'Cancer Research UK, National Institute of Health Research',
    'Innovate UK, Isogenica Limited',
    'Leicester Haematology Research Fund',
    'Gilead Sciences Ltd - Gilead giving',
    'Hope Foundation for Cancer Research',
    'Step Pharma',
    'CRUK, AstraZeneca',
    'Associazione Angela Serra per la Ricerca sul Canro',
    'Blood Cancer UK',
    'NIHR',
    'NIHR, MRC',
    'Scott-Waudby Trust',
    'Roche Glycart AG',
    'Kay Kendall Leukaemia Fund',
    'Janpix Limited',
    'Astex Pharmaceuticals,Inc',
    'Loxo Oncology, Inc.',
    'BeiGene Switzerland GmbH',
    'The British Society for Haematology',
    'UCB Biopharma SRL',
    'LifeArc',
    'Dr P Hutchinson',
    'Cancer Research UK',
    'Breast Cancer Now',
    'INSTITUT DE RECHERCHE PIERRE FABRE',
    'CRT Ltd',
    'Multi Funded; CRT Ltd',
    'Orion Corporation',
    'Innovate UK',
    'Association of Breast Surgery',
    'University of Leicester',
    'Horizon Europe/Innovate UK',
    'ERA-PerMed via FONDAZIONE IRCCS',
    'Health Research Board',
    'DNAe',
    'Samworth Foundation',
    'British Thyroid Foundation',
    'RS Oncology LLC',
    'Asthma & Lung UK',
    'Ikena Oncology, Inc',
    'AstraZeneca AB - Sweden',
    'AstraZeneca AB Sweden',
    'National Health and Medical Research Council (NHMRC) Australia',
    'Novartis Pharma Ag',
    'National Institute for Health Research (NIHR) – Health Technology Assessment (HTA)'
    'Asthma & Lung UK / Victor Daladeh Foundation',
    'Owkin France',
    'Astex Therapeutics',
    'Bayer Healthcare Pharmaceuticals Inc',
    'NIHR Health Technology Assessment Programme',
    'Lipid Charity Funds',
    'British Heart Foundation (BHF)',
    'National Institutes of Health (NIH USA)',
    'Mesothelioma UK',
    'Bristol-Myers Squibb',
    'Aldeyra Therapeutics, Inc',
    'British Lung Foundation',
    'Iovance Biotherapeutics, Inc',
    'Boehringer Ingelheim Limited',
    'The Victor Phillip Dahdaleh (VPDCF) through A-LUK',
    'BerGenBio ASA',
    'GLAXOSMITHKLINE R&D LTD',
    'Wellcome Trust',
    'Rosetrees Trust',
    'Intuitive Surgical',
    'University Hospitals of Leicester NHS Trust',
    'None',
    'Cidara Therapeutics',
    'North East London Cancer Alliance',
    'East Genomic Medicine Service AllianceUK Health & Hospitals',
    'NHS Leicester, Leicestershire and Rutland Integrated Care Board',
    'British Gynaecological Cancer Society',
    'East Midland Genome Service, LIAS',
    'Cancer Prevention Research Trust',
    'Bowel Cancer UK',
    'Novo Nordisk A/S',
    'Novo Nordisk',
    'Eli Lilly',
    'Sanofi',
    'Genentech Roche',
    'Boehringer Ingelheim',
    'Leicester Diabetes Centre, Leicester Biomedical Research Centre',
    'Investigator initiated and funded - supported by an NIHR Senior Investigators Award',
    'Diabetes UK',
    'Academy of Medical Sciences and Diabetes UK (joint grant scheme)',
    'MRC IAA (via University of Leicester, Institute for Precision Health)',
    'Novo Nordisk Research Foundation',
    'AstraZeneca UK ltd',
    'Health Education East Midlands',
    'Philanthropic Donor',
    'Medical Research Council',
    'Kidney Research UK',
    'NIHR Programme Grants for Applied Research',
    'Other non-commercial',
    'MRC CiC (via University of Leicester Institute of Precision Health)',
    'The Saudi Cultural Bureau London',
    'NIHR HTA',
    'NIHR Fellowship',
    'Royal Embassy of Saudi Arabia Cultural Bureau',
    'Academy of Medical Sciences',
    'School of Sport, Exercise and Health Sciences, Loughborough University',
    'PI core funding',
    'The Colt Foundation',
    'Industry match funding',
    'TBC',
    'JDRF (Breakthrough T1D)',
    'Abbott',
    'Imcyse',
    'Insulet',
    'Welcome',
    'Innovate UK - Horizon Europe Guarantee',
    'Horizon Europe 2020 IMI',
    'This project (project reference NIHR129910) is funded by the Efficacy and Mechanism Evaluation (EME) Programme, an MRC and NIHR partnership.',
    'AstraZeneca AB',
    'NIHR HTA Programme',
    'AZ',
    'OM Pharma SA',
    'Genentech - commercial',
    'Astra Zeneca',
    'F. Hoffmann-La Roche AG',
    'SANOFI PASTEUR',
    'Commercial',
    'Roche Products Ltd',
    'Action Medical Research,Asthma UK,NIHR Leicester Respiratory Biomedical Rsearch Unit,NIHR senior Fellowship award',
    'Asthma UK',
    'ERS',
    'Glaxo Smith Klein',
    '4D Pharma PLC',
    'AstraZeneca within RASP MRC Workstrand 4',
    'Galecto Biotech AB',
    'other - non commercial',
    'European Respiratory Society',
    'No Funder',
    'AstraZeneca',
    'UK Research & Innovation',
    'UKRI',
    'NIHR Leicester Biomedical Research Centre',
    'NIHR Invention for Innovation (NIHR203424)',
    'Janssen Pharmaceuticals Inc. & Synairgen',
    'European Commission',
    'National Asthma Campaign',
    'Regeneron Pharmaceuticals, Inc',
    'University Hospitals of leicester',
    'GSK',
    'Commercial (AstraZeneca)',
    'PBD Biotech Ltd.',
    'Moderna Biotech Manufacturing UK Ltd',
    'National Institute of Health Research',
    'Pacific Life Re Services Limited',
    '*Spire Health Technology PBC',
    'National Institute for Health Research, University of Southampton',
    'UKRI-MRC/DHSC NIHR',
    'NIHR/ UKRI',
    'ResMed',
    'NHS England and NHS Improvement, Artificial Intelligence (AI) in Health and Care',
])
db.session.add_all(main_funding_sources)
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