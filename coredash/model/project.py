from datetime import date
from coredash.model.lookups import Lookup, Theme
from lbrc_flask.database import db
from lbrc_flask.security import AuditMixin
from lbrc_flask.model import CommonMixin
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text


class ProjectStatus(Lookup, db.Model):
    pass

class UkcrcHealthCategory(Lookup, db.Model):
    pass

class NihrPriorityArea(Lookup, db.Model):
    pass

class UkcrcResearchActivityCode(Lookup, db.Model):
    pass

class RacsSubCategory(Lookup, db.Model):
    pass

class ResearchType(Lookup, db.Model):
    pass

class Methodology(Lookup, db.Model):
    pass

class ExpectedImpact(Lookup, db.Model):
    pass

class TrialPhase(Lookup, db.Model):
    pass

class MainFundingSource(Lookup, db.Model):
    pass

class MainFundingCategory(Lookup, db.Model):
    pass

class MainFundingDhscNihrFunding(Lookup, db.Model):
    pass

class MainFundingIndustry(Lookup, db.Model):
    pass


class Project(AuditMixin, CommonMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    comments: Mapped[str] = mapped_column(Text, nullable=False)

    local_rec_number: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)
    iras_number: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)
    cpms_id: Mapped[str] = mapped_column(String(50), nullable=True, unique=True)

    start_date: Mapped[date] = mapped_column(nullable=False, index=True)
    end_date: Mapped[date] = mapped_column(index=True)
    participants_recruited_to_centre_fy: Mapped[int] = mapped_column()

    brc_funding: Mapped[int] = mapped_column()
    main_funding_brc_funding: Mapped[int] = mapped_column(nullable=True)
    total_external_funding_award: Mapped[int] = mapped_column()

    sensitive: Mapped[bool] = mapped_column(nullable=False)
    first_in_human: Mapped[bool] = mapped_column(nullable=False)
    link_to_nihr_transactional_research_collaboration: Mapped[bool] = mapped_column(nullable=False)
    crn_rdn_portfolio_study: Mapped[bool] = mapped_column(nullable=False)
    rec_approval_required: Mapped[bool] = mapped_column(nullable=False)
    randomised_trial: Mapped[bool] = mapped_column(nullable=False)

    project_status_id: Mapped[int] = mapped_column(ForeignKey(ProjectStatus.id), index=True, nullable=False)
    project_status: Mapped[ProjectStatus] = relationship(foreign_keys=[project_status_id])
    theme_id: Mapped[int] = mapped_column(ForeignKey(Theme.id), index=True, nullable=False)
    theme: Mapped[Theme] = relationship(foreign_keys=[theme_id])
    ukcrc_health_category_id: Mapped[int] = mapped_column(ForeignKey(UkcrcHealthCategory.id), index=True, nullable=False)
    ukcrc_health_category: Mapped[UkcrcHealthCategory] = relationship(foreign_keys=[ukcrc_health_category_id])
    nihr_priority_area_id: Mapped[int] = mapped_column(ForeignKey(NihrPriorityArea.id), index=True, nullable=False)
    nihr_priority_area: Mapped[NihrPriorityArea] = relationship(foreign_keys=[nihr_priority_area_id])
    ukcrc_research_activity_code_id: Mapped[int] = mapped_column(ForeignKey(UkcrcResearchActivityCode.id), index=True, nullable=False)
    ukcrc_research_activity_code: Mapped[UkcrcResearchActivityCode] = relationship(foreign_keys=[ukcrc_research_activity_code_id])
    racs_sub_category_id: Mapped[int] = mapped_column(ForeignKey(RacsSubCategory.id), index=True, nullable=True)
    racs_sub_category: Mapped[RacsSubCategory] = relationship(foreign_keys=[racs_sub_category_id])
    research_type_id: Mapped[int] = mapped_column(ForeignKey(ResearchType.id), index=True, nullable=False)
    research_type: Mapped[ResearchType] = relationship(foreign_keys=[research_type_id])
    methodology_id: Mapped[int] = mapped_column(ForeignKey(Methodology.id), index=True, nullable=False)
    methodology: Mapped[Methodology] = relationship(foreign_keys=[methodology_id])
    expected_impact_id: Mapped[int] = mapped_column(ForeignKey(ExpectedImpact.id), index=True, nullable=False)
    expected_impact: Mapped[ExpectedImpact] = relationship(foreign_keys=[expected_impact_id])
    trial_phase_id: Mapped[int] = mapped_column(ForeignKey(TrialPhase.id), index=True, nullable=True)
    trial_phase: Mapped[TrialPhase] = relationship(foreign_keys=[trial_phase_id])
    main_funding_source_id: Mapped[int] = mapped_column(ForeignKey(MainFundingSource.id), index=True, nullable=False)
    main_funding_source: Mapped[MainFundingSource] = relationship(foreign_keys=[main_funding_source_id])
    main_funding_category_id: Mapped[int] = mapped_column(ForeignKey(MainFundingCategory.id), index=True, nullable=False)
    main_funding_category: Mapped[MainFundingCategory] = relationship(foreign_keys=[main_funding_category_id])
    main_funding_dhsc_nihr_funding_id: Mapped[int] = mapped_column(ForeignKey(MainFundingDhscNihrFunding.id), index=True, nullable=True)
    main_funding_dhsc_nihr_funding: Mapped[MainFundingDhscNihrFunding] = relationship(foreign_keys=[main_funding_dhsc_nihr_funding_id])
    main_funding_industry_id: Mapped[int] = mapped_column(ForeignKey(MainFundingIndustry.id), index=True, nullable=True)
    main_funding_industry: Mapped[MainFundingIndustry] = relationship(foreign_keys=[main_funding_industry_id])
