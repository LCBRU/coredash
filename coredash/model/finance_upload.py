from dataclasses import dataclass
from itertools import islice
from pathlib import Path
from typing import List, Optional
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
WORKSHEET_NAME_EXTERNAL_FUNDING = 'External Funding'
WORKSHEET_NAME_EXPENDITURE = 'Expenditure by Health Category'


@dataclass
class Worksheet:
    filepath: Path
    name: str
    definition: ColumnsDefinition
    column_header_row: Optional[int] = 1
    header_rows: Optional[int] = 1

    def get_worksheet(self):
        return ExcelData(
            filepath=self.filepath,
            worksheet=self.name,
            column_header_row=self.column_header_row,
            header_rows=self.header_rows,
        )

    @property
    def worksheet_missing(self):
        return not self.get_worksheet().has_worksheet()

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

        self.local_filepath = current_app.config["FILE_UPLOAD_DIRECTORY"] / secure_filename(f"{self.guid}_{self.filename}")

        self.project_list_worksheet = Worksheet(
            filepath=self.local_filepath,
            name=WORKSHEET_NAME_PROJECT_LIST,
            definition=FinanceUpload_ProjectList_ColumnDefinition(),
            column_header_row=4,
            header_rows=4,
        )
        self.external_funding_worksheet = Worksheet(
            filepath=self.local_filepath,
            name=WORKSHEET_NAME_EXTERNAL_FUNDING,
            definition=FinanceUpload_ExternalFunding_ColumnDefinition(),
            column_header_row=3,
            header_rows=3,
        )
        self.expenditure_worksheet = Worksheet(
            filepath=self.local_filepath,
            name=WORKSHEET_NAME_EXPENDITURE,
            definition=FinanceUpload_Expenditure_ColumnDefinition(),
            column_header_row=4,
            header_rows=4,
        )

        self.worksheets = [
            self.project_list_worksheet,
            self.external_funding_worksheet,
            self.expenditure_worksheet,
        ]

    def validate(self):
        messages = []

        for w in self.worksheets:
            messages.extend(self.validate_worksheet(w))

        db.session.add_all([FinanceUploadMessage(
            finance_upload=self,
            type=m.type,
            row=m.row,
            message=m.message,
        ) for m in messages])

        if any(m.is_error for m in messages):
            self.status = FinanceUpload.STATUS__ERROR

    def validate_worksheet(self, worksheet: Worksheet):
        messages = []

        if worksheet.worksheet_missing:
            message = f"Missing worksheet '{worksheet.name}'"
            messages.append(ColumnsDefinitionValidationMessage(
                type=ColumnsDefinitionValidationMessage.TYPE__ERROR,
                message=message,
            ))
        else:
            messages.extend(worksheet.definition.validation_errors(worksheet.get_worksheet()))

        return messages

    @property
    def is_error(self):
        return self.status == FinanceUpload.STATUS__ERROR

    def project_data(self):
        definition = FinanceUpload_ProjectList_ColumnDefinition()

        return definition.translated_data(self.project_list_worksheet.get_worksheet())

    def external_funding_data(self):
        definition = FinanceUpload_ExternalFunding_ColumnDefinition()

        return definition.translated_data(self.external_funding_worksheet.get_worksheet())

    def expenditure_data(self):
        definition = FinanceUpload_Expenditure_ColumnDefinition()

        return definition.translated_data(self.expenditure_worksheet.get_worksheet())


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


class FinanceUpload_ProjectList_ColumnDefinition(ColumnsDefinition):
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


class FinanceUpload_ExternalFunding_ColumnDefinition(ColumnsDefinition):
    @property
    def minimum_row_count(self):
        return 1
    
    def row_filter(self, spreadsheet):
        return [True] + [False for _ in spreadsheet.iter_rows()]

    @property
    def column_definition(self):
        return [
            NumericColumnDefinition(
                name='Research Council',
                translated_name='research_council',
                allow_null=False,
            ),
            NumericColumnDefinition(
                name='Research Charity',
                translated_name='research_charity',
                allow_null=False,
            ),
            NumericColumnDefinition(
                name='DHSC/NIHR',
                translated_name='dhsc_nihr',
                allow_null=False,
            ),
            NumericColumnDefinition(
                name='Industry Collaborative',
                translated_name='industry_collaborative',
                allow_null=False,
            ),
            NumericColumnDefinition(
                name='Industry Contract',
                translated_name='industry_contract',
                allow_null=False,
            ),
            NumericColumnDefinition(
                name='Other non-commercial',
                translated_name='other_non_commercial',
                allow_null=False,
            ),
            NumericColumnDefinition(
                name='Total',
                translated_name='total',
                allow_null=False,
            ),
        ]


class FinanceUpload_Expenditure_ColumnDefinition(ColumnsDefinition):

    HEALTH_CATEGORY__BLOOD = 'blood'
    HEALTH_CATEGORY__CANCER = 'cancer and neoplasms'
    HEALTH_CATEGORY__CARDIOVASCULAR = 'cardiovascular'
    HEALTH_CATEGORY__CONGENITAL = 'congenital disorders'
    HEALTH_CATEGORY__EAR = 'ear'
    HEALTH_CATEGORY__EYE = 'eye'
    HEALTH_CATEGORY__INFECTION = 'infection'
    HEALTH_CATEGORY__INFLAMMATORY = 'inflammatory and immune system'
    HEALTH_CATEGORY__INJURIES = 'injuries and accidents'
    HEALTH_CATEGORY__MENTAL = 'mental health'
    HEALTH_CATEGORY__METABOLIC = 'metabolic and endocrine'
    HEALTH_CATEGORY__MUSCULOSKELETAL = 'musculoskeletal'
    HEALTH_CATEGORY__GASTOINTESTINAL = 'oral and gastrointestinal'
    HEALTH_CATEGORY__RENAL = 'renal and urogenital'
    HEALTH_CATEGORY__REPRODUCTIVE = 'reproductive health and childbirth'
    HEALTH_CATEGORY__RESPIRATORY = 'respiratory'
    HEALTH_CATEGORY__SKIN = 'skin'
    HEALTH_CATEGORY__STROKE = 'stroke'
    HEALTH_CATEGORY__GENETIC = 'generic health revelance'
    HEALTH_CATEGORY__OTHER = 'disputed aetiology and other'
    HEALTH_CATEGORY__TOTAL = 'total'

    HEALTH_CATEGORIES = [
        HEALTH_CATEGORY__BLOOD,
        HEALTH_CATEGORY__CANCER,
        HEALTH_CATEGORY__CARDIOVASCULAR,
        HEALTH_CATEGORY__CONGENITAL,
        HEALTH_CATEGORY__EAR,
        HEALTH_CATEGORY__EYE,
        HEALTH_CATEGORY__INFECTION,
        HEALTH_CATEGORY__INFLAMMATORY,
        HEALTH_CATEGORY__INJURIES,
        HEALTH_CATEGORY__MENTAL,
        HEALTH_CATEGORY__METABOLIC,
        HEALTH_CATEGORY__MUSCULOSKELETAL,
        HEALTH_CATEGORY__GASTOINTESTINAL,
        HEALTH_CATEGORY__RENAL,
        HEALTH_CATEGORY__REPRODUCTIVE,
        HEALTH_CATEGORY__RESPIRATORY,
        HEALTH_CATEGORY__SKIN,
        HEALTH_CATEGORY__STROKE,
        HEALTH_CATEGORY__GENETIC,
        HEALTH_CATEGORY__OTHER,
        HEALTH_CATEGORY__TOTAL,
    ]

    COLUMN_NAME__HEALTH_CATEGORY = 'UKCRC Health Category'
    COLUMN_NAME__EXPENDITURE = 'Expenditure'

    @property
    def health_category_column_definition(self):
        return StringColumnDefinition(
            name=self.COLUMN_NAME__HEALTH_CATEGORY,
            translated_name=self.field_name_from_column_name(self.COLUMN_NAME__HEALTH_CATEGORY),
            allow_null=False,
        )

    @property
    def expenditure_column_definition(self):
        return NumericColumnDefinition(
            name=self.COLUMN_NAME__EXPENDITURE,
            translated_name=self.field_name_from_column_name(self.COLUMN_NAME__EXPENDITURE),
            allow_null=False,
        )

    @property
    def column_definition(self):
        return [
            self.health_category_column_definition,
            self.expenditure_column_definition,
        ]

    def translated_data(self, spreadsheet):
        result = {}

        for row in self.iter_filtered_data(spreadsheet):
            health_category = self.health_category_column_definition.get_translated_value(row)
            column_name = self.field_name_from_column_name(health_category)
            expenditure = self.expenditure_column_definition.get_translated_value(row)

            result[column_name] = expenditure

        return [result]
