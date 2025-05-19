from typing import List
import uuid
from flask import current_app
from lbrc_flask.database import db
from lbrc_flask.security import AuditMixin
from lbrc_flask.model import CommonMixin
from lbrc_flask.column_data import NumericColumnDefinition, ColumnsDefinition, ExcelData, StringColumnDefinition, IntegerColumnDefinition, DateColumnDefinition, BooleanColumnDefinition, LookupColumnDefinition, ColumnsDefinitionValidationMessage
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, String, Text
from werkzeug.utils import secure_filename

from coredash.model.lookups import Theme
from coredash.model.project import ExpectedImpact, MainFundingCategory, MainFundingDhscNihrFunding, MainFundingIndustry, Methodology, NihrPriorityArea, ProjectStatus, RacsSubCategory, ResearchType, TrialPhase, UkcrcHealthCategory, UkcrcResearchActivityCode


WORKSHEET_NAME_PROJECT_LIST = 'Project List'
WORKSHEET_NAME_INVESTIGATORS = 'NIHR Investigators'


class FinanceUpload(AuditMixin, CommonMixin, db.Model):
    STATUS__AWAITING_PROCESSING = 'Awaiting Processing'
    STATUS__PROCESSED = 'Processed'
    STATUS__ERROR = 'Error'

    STATUS_NAMES = [
        STATUS__AWAITING_PROCESSING,
        STATUS__PROCESSED,
        STATUS__ERROR,
    ]

    id: Mapped[int] = mapped_column(primary_key=True)
    guid: Mapped[str] = mapped_column(String(50))
    filename: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(50), default='')
    messages: Mapped[List["FinanceUploadMessage"]] = relationship(back_populates="finance_upload")

    def __init__(self, **kwargs):
        if 'guid' not in kwargs:
            kwargs['guid'] = str(uuid.uuid4())
        super().__init__(**kwargs)

    @property
    def local_filepath(self):
        return current_app.config["FILE_UPLOAD_DIRECTORY"] / secure_filename(f"{self.guid}_{self.filename}")

    def get_spreadsheet(self, worksheet):
        return ExcelData(filepath=self.local_filepath, worksheet=worksheet, column_header_row=4, header_rows=4)

    def validate(self):
        self.validate_project_list()
        self.validate_investigators()

    def validate_project_list(self):
        definition = FinanceUploadColumnDefinition()

        spreadsheet = self.get_spreadsheet(WORKSHEET_NAME_PROJECT_LIST)

        messages = []

        if not spreadsheet.has_worksheet():
            messages.append(ColumnsDefinitionValidationMessage(type=ColumnsDefinitionValidationMessage.TYPE__ERROR, message=f"Missing worksheet '{WORKSHEET_NAME_PROJECT_LIST}'"))
        else:
            messages.extend(definition.validation_errors(spreadsheet))

        db.session.add_all([FinanceUploadMessage(
            finance_upload=self,
            type=m.type,
            row=m.row,
            message=m.message,
        ) for m in messages])

        if any(m.is_error for m in messages):
            self.status = FinanceUpload.STATUS__ERROR


    def validate_investigators(self):
        spreadsheet = self.get_spreadsheet(WORKSHEET_NAME_INVESTIGATORS)

        messages = []

        if not spreadsheet.has_worksheet():
            messages.append(ColumnsDefinitionValidationMessage(type=ColumnsDefinitionValidationMessage.TYPE__ERROR, message=f"Missing worksheet '{WORKSHEET_NAME_INVESTIGATORS}'"))

        db.session.add_all([FinanceUploadMessage(
            finance_upload=self,
            type=m.type,
            row=m.row,
            message=m.message,
        ) for m in messages])

        if any(m.is_error for m in messages):
            self.status = FinanceUpload.STATUS__ERROR

    @property
    def is_error(self):
        return self.status == FinanceUpload.STATUS__ERROR

    def data(self):
        definition = FinanceUploadColumnDefinition()

        return definition.translated_data(self.get_spreadsheet(WORKSHEET_NAME_PROJECT_LIST))


class FinanceUploadMessage(AuditMixin, CommonMixin, db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    finance_upload_id: Mapped[int] = mapped_column(ForeignKey(FinanceUpload.id), index=True, nullable=False)
    finance_upload: Mapped["FinanceUpload"] = relationship(back_populates="messages")
    type: Mapped[str] = mapped_column(String(20), index=True)

    __mapper_args__ = {
        "polymorphic_on": type,
    }

    row: Mapped[int] = mapped_column(Integer, nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)

    @property
    def display_text(self):
        if self.row:
            return f"{self.type}: {self.message} on row {self.row}"
        else:
            return f"{self.type}: {self.message}"


class FinanceUploadErrorMessage(FinanceUploadMessage):
    __mapper_args__ = {
        "polymorphic_identity": 'Error',
    }

    @property
    def is_error(self):
        return True


class FinanceUploadWarningMessage(FinanceUploadMessage):
    __mapper_args__ = {
        "polymorphic_identity": 'Warning',
    }

    @property
    def is_error(self):
        return False


class FinanceUploadColumnDefinition(ColumnsDefinition):
    @property
    def column_definition(self):
        return [
            StringColumnDefinition(
                name='Project Title',
                translated_name='title',
                max_length=500,
                allow_null=False,
            ),
            StringColumnDefinition(
                name='Project summary',
                translated_name='summary',
                allow_null=True,
            ),
            StringColumnDefinition(
                name='Comments',
                translated_name='comments',
                allow_null=True,
            ),
            StringColumnDefinition(
                name='Local REC number',
                translated_name='local_rec_number',
                max_length=50,
                allow_null=True,
            ),
            StringColumnDefinition(
                name='IRAS Number',
                translated_name='iras_number',
                max_length=50,
                allow_null=True,
            ),
            StringColumnDefinition(
                name='CRN/RDN CPMS ID',
                translated_name='cpms_id',
                max_length=50,
                allow_null=True,
            ),
            StringColumnDefinition(
                name='Main Funding Source',
                translated_name='main_funding_source',
                max_length=500,
                allow_null=False,
            ),
            DateColumnDefinition(
                name='Project Actual Start Date',
                translated_name='start_date',
                allow_null=True,
            ),
            DateColumnDefinition(
                name='Project End Date',
                translated_name='end_date',
                allow_null=True,
            ),
            IntegerColumnDefinition(
                name='Participants Recruited to Centre FY',
                translated_name='participants_recruited_to_centre_fy',
                allow_null=True,
            ),
            IntegerColumnDefinition(
                name='BRC funding',
                translated_name='brc_funding',
                allow_null=False,
            ),
            IntegerColumnDefinition(
                name='Main Funding - BRC Funding',
                translated_name='main_funding_brc_funding',
                allow_null=True,
                skip_errors=True,
            ),
            NumericColumnDefinition(
                name='Total External Funding Awarded',
                translated_name='total_external_funding_award',
                allow_null=False,
            ),
            BooleanColumnDefinition(
                name='Is this project sensitive',
                translated_name='sensitive',
                allow_null=False,
            ),
            BooleanColumnDefinition(
                name='First in Human Project',
                translated_name='first_in_human',
                allow_null=False,
            ),
            BooleanColumnDefinition(
                name='Link to NIHR Translational Research Collaboration',
                translated_name='link_to_nihr_transactional_research_collaboration',
                allow_null=False,
            ),
            BooleanColumnDefinition(
                name='CRN/RDN Portfolio study',
                translated_name='crn_rdn_portfolio_study',
                allow_null=False,
            ),
            BooleanColumnDefinition(
                name='REC Approval Required',
                translated_name='rec_approval_required',
                allow_null=False,
            ),
            BooleanColumnDefinition(
                name='Randomised Trial',
                translated_name='randomised_trial',
                allow_null=False,
            ),
            LookupColumnDefinition(
                name='Project Status',
                translated_name='project_status',
                lookup_class=ProjectStatus,
                max_length=100,
                allow_null=False,
            ),
            LookupColumnDefinition(
                name='Theme',
                translated_name='theme',
                lookup_class=Theme,
                max_length=100,
                allow_null=False,
            ),
            LookupColumnDefinition(
                name='UKCRC Health Category',
                translated_name='ukcrc_health_category',
                lookup_class=UkcrcHealthCategory,
                max_length=100,
                allow_null=False,
            ),
            LookupColumnDefinition(
                name='NIHR priority Areas / Fields of Research',
                translated_name='nihr_priority_area',
                lookup_class=NihrPriorityArea,
                max_length=100,
                allow_null=True,
            ),
            LookupColumnDefinition(
                name='UKCRC Research Activity Code',
                translated_name='ukcrc_research_activity_code',
                lookup_class=UkcrcResearchActivityCode,
                max_length=100,
                allow_null=False,
            ),
            LookupColumnDefinition(
                name='RACS sub-categories',
                translated_name='racs_sub_category',
                lookup_class=RacsSubCategory,
                max_length=100,
                allow_null=True,
            ),
            LookupColumnDefinition(
                name='Research Type',
                translated_name='research_type',
                lookup_class=ResearchType,
                max_length=100,
                allow_null=False,
            ),
            LookupColumnDefinition(
                name='Methodology',
                translated_name='methodology',
                lookup_class=Methodology,
                max_length=100,
                allow_null=False,
            ),
            LookupColumnDefinition(
                name='Expected Impact',
                translated_name='expected_impact',
                lookup_class=ExpectedImpact,
                max_length=100,
                allow_null=False,
            ),
            LookupColumnDefinition(
                name='Trial Phase',
                translated_name='trial_phase',
                lookup_class=TrialPhase,
                max_length=100,
                allow_null=True,
            ),
            LookupColumnDefinition(
                name='Main Funding Category',
                translated_name='main_funding_category',
                lookup_class=MainFundingCategory,
                max_length=100,
                allow_null=False,
            ),
            LookupColumnDefinition(
                name='Main Funding - DHSC/NIHR Funding',
                translated_name='main_funding_dhsc_nihr_funding',
                lookup_class=MainFundingDhscNihrFunding,
                max_length=100,
                allow_null=True,
            ),
            LookupColumnDefinition(
                name='Main Funding - Industry Collaborative or Industry Contract Funding',
                translated_name='main_funding_industry',
                lookup_class=MainFundingIndustry,
                max_length=100,
                allow_null=True,
            ),
        ]
