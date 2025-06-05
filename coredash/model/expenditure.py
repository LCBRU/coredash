from lbrc_flask.database import db
from lbrc_flask.security import AuditMixin
from lbrc_flask.model import CommonMixin
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DECIMAL


class Expenditure(AuditMixin, CommonMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    blood: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    cancer_and_neoplasms: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    cardiovascular: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    congenital_disorders: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    ear: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    eye: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    infection: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    inflammatory_and_immune_system: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    injuries_and_accidents: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    mental_health: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    metabolic_and_endocrine: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    musculoskeletal: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    oral_and_gastrointestinal: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    renal_and_urogenital: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    reproductive_health_and_childbirth: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    respiratory: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    skin: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    stroke: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    generic_health_relevance: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
    disputed_aetiology_and_other: Mapped[DECIMAL] = mapped_column(DECIMAL(10,2), nullable=False)
