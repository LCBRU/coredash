from lbrc_flask.database import db
from sqlalchemy import delete, select
from coredash.model.external_funding import ExternalFunding


def get_external_funding():
    return db.sessions.execute(select(ExternalFunding)).scalar()


def external_funding_save(data):
    external_fundings = [external_funding_populate(ExternalFunding(), d) for d in data]

    db.session.execute(delete(ExternalFunding))
    db.session.add_all(external_fundings)


def external_funding_populate(external_funding: ExternalFunding, data: dict):
    external_funding.research_council = data['research_council']
    external_funding.research_charity = data['research_charity']
    external_funding.dhsc_nihr = data['dhsc_nihr']
    external_funding.industry_collaborative = data['industry_collaborative']
    external_funding.industry_contract = data['industry_contract']
    external_funding.other_non_commercial = data['other_non_commercial']
    external_funding.total = data['total']

    return external_funding