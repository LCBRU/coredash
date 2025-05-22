from lbrc_flask.database import db
from sqlalchemy import case, func, literal_column, select

from coredash.model.project import MainFundingCategory, Project


def get_frontpage():
    q_industrial_funding_categories = select(MainFundingCategory.id).where(MainFundingCategory.name.in_(['Industry contract', 'Industry collaborative']))

    q = select(
        func.count(Project.id).label('projects_supported'),
        func.sum(case(
            (
                Project.main_funding_category_id.in_(q_industrial_funding_categories),
                literal_column('1'),
            ),
            else_=literal_column('0'),
        )).label('commercial_projects_supported'),
        func.sum(Project.participants_recruited_to_centre_fy).label('recruitment_count'),
    )

    return next(db.session.execute(q).mappings())
