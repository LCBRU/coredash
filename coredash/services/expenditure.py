from lbrc_flask.database import db
from sqlalchemy import delete, select
from coredash.model.expenditure import Expenditure


def get_expenditure():
    return db.sessions.execute(select(Expenditure)).scalar()


def expenditure_save(data):
    expenditures = [expenditure_populate(Expenditure(), d) for d in data]

    db.session.execute(delete(Expenditure))
    db.session.add_all(expenditures)


def expenditure_populate(expenditure: Expenditure, data: dict):
    print(data)
    expenditure.blood = data['blood']
    expenditure.cancer_and_neoplasms = data['cancer_and_neoplasms']
    expenditure.cardiovascular = data['cardiovascular']
    expenditure.congenital_disorders = data['congenital_disorders']
    expenditure.ear = data['ear']
    expenditure.eye = data['eye']
    expenditure.infection = data['infection']
    expenditure.inflammatory_and_immune_system = data['inflammatory_and_immune_system']
    expenditure.injuries_and_accidents = data['injuries_and_accidents']
    expenditure.mental_health = data['mental_health']
    expenditure.metabolic_and_endocrine = data['metabolic_and_endocrine']
    expenditure.musculoskeletal = data['musculoskeletal']
    expenditure.oral_and_gastrointestinal = data['oral_and_gastrointestinal']
    expenditure.renal_and_urogenital = data['renal_and_urogenital']
    expenditure.reproductive_health_and_childbirth = data['reproductive_health_and_childbirth']
    expenditure.respiratory = data['respiratory']
    expenditure.skin = data['skin']
    expenditure.stroke = data['stroke']
    expenditure.generic_health_revelance = data['generic_health_revelance']
    expenditure.disputed_aetiology_and_other = data['disputed_aetiology_and_other']
    expenditure.total = data['total']

    return expenditure
