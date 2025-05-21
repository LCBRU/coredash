from lbrc_flask.database import db
from lbrc_flask.security import AuditMixin
from lbrc_flask.model import CommonMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DECIMAL


class ExternalFunding(AuditMixin, CommonMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    research_council: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    research_charity: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    dhsc_nihr: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    industry_collaborative: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    industry_contract: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    other_non_commercial: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    total: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
