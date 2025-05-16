from decimal import Decimal
from lbrc_flask.database import db
from lbrc_flask.security import AuditMixin
from lbrc_flask.model import CommonMixin
from lbrc_flask.lookups import Lookup
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DECIMAL, ForeignKey, String, Text

from coredash.model.lookups import UkcrcHealthCategory


class JobTitle(Lookup, db.Model):
    pass


class ProfessionalBackground(Lookup, db.Model):
    pass


class ProfessionalBackgroundDetail(Lookup, db.Model):
    pass


class Person(AuditMixin, CommonMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    first_name: Mapped[str] = mapped_column(String(200), nullable=False)
    last_name: Mapped[str] = mapped_column(String(200), nullable=False)
    orcid: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    comments: Mapped[str] = mapped_column(Text, nullable=False)

    full_time_equivalent: Mapped[Decimal] = mapped_column(DECIMAL(4, 2), nullable=False)

    job_title_id: Mapped[int] = mapped_column(ForeignKey(JobTitle.id), index=True, nullable=False)
    job_title: Mapped[JobTitle] = relationship(foreign_keys=[job_title_id])
    professional_background_id: Mapped[int] = mapped_column(ForeignKey(ProfessionalBackground.id), index=True, nullable=False)
    professional_background: Mapped[ProfessionalBackground] = relationship(foreign_keys=[professional_background_id])
    ukcrc_health_category_id: Mapped[int] = mapped_column(ForeignKey(UkcrcHealthCategory.id), index=True, nullable=False)
    ukcrc_health_category: Mapped[UkcrcHealthCategory] = relationship(foreign_keys=[ukcrc_health_category_id])
    professional_background_detail_id: Mapped[int] = mapped_column(ForeignKey(ProfessionalBackgroundDetail.id), index=True, nullable=False)
    professional_background_detail: Mapped[ProfessionalBackgroundDetail] = relationship(foreign_keys=[professional_background_detail_id])

    @property
    @property
    def full_name(self):
        return " ".join(filter(None, [self.first_name, self.last_name]))
