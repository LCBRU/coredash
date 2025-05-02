import uuid
from flask import current_app
from lbrc_flask.database import db
from lbrc_flask.security import AuditMixin
from lbrc_flask.model import CommonMixin
from lbrc_flask.column_data import ColumnDefinition, ColumnsDefinition, ExcelData, StringColumnDefinition, IntegerColumnDefinition, DateColumnDefinition, BooleanColumnDefinition, LookupColumnDefinition
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from werkzeug.utils import secure_filename

from coredash.model.lookups import Theme
from coredash.model.project import ExpectedImpact, MainFundingCategory, MainFundingDhscNihrFunding, MainFundingIndustry, MainFundingSource, Methodology, NihrPriorityArea, ProjectStatus, RacsSubCategory, ResearchType, TrialPhase, UkcrcHealthCategory, UkcrcResearchActivityCode


WORKSHEET_NAME_PROJECT_LIST = 'Project List'

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
    errors: Mapped[str] = mapped_column(Text, default='')

    def __init__(self, **kwargs):
        if 'guid' not in kwargs:
            kwargs['guid'] = str(uuid.uuid4())
        super().__init__(**kwargs)

    @property
    def local_filepath(self):
        return current_app.config["FILE_UPLOAD_DIRECTORY"] / secure_filename(f"{self.guid}_{self.filename}")

    def get_spreadsheet(self):
        return ExcelData(filepath=self.local_filepath, worksheet=WORKSHEET_NAME_PROJECT_LIST)

    def validate(self):
        definition = FinanceUploadColumnDefinition()

        spreadsheet = self.get_spreadsheet()

        errors = []

        if not spreadsheet.has_worksheet():
            errors.append(f"Missing worksheet '{WORKSHEET_NAME_PROJECT_LIST}'")
        else:
            errors.extend(definition.validation_errors(spreadsheet))

        if errors:
            self.errors = "\n".join(errors)
            self.status = FinanceUpload.STATUS__ERROR

    @property
    def is_error(self):
        return self.status == FinanceUpload.STATUS__ERROR

    def data(self):
        definition = FinanceUploadColumnDefinition()

        return definition.translated_data(self.get_spreadsheet())


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
                allow_null=False,
            ),
            StringColumnDefinition(
                name='IRAS Number',
                translated_name='iras_number',
                max_length=50,
                allow_null=False,
            ),
            StringColumnDefinition(
                name='CRN/RDN CPMS ID',
                translated_name='cpms_id',
                max_length=50,
                allow_null=False,
            ),
            DateColumnDefinition(
                name='Project Actual Start Date',
                translated_name='start_date',
                allow_null=False,
            ),
            DateColumnDefinition(
                name='Project End Date',
                translated_name='end_date',
                allow_null=True,
            ),
            IntegerColumnDefinition(
                name='Participants Recruited to Centre FY',
                translated_name='participants_recruited_to_centre_fy',
                allow_null=False,
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
            ),
            IntegerColumnDefinition(
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
                allow_null=False,
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
                allow_null=False,
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
                allow_null=False,
            ),
            LookupColumnDefinition(
                name='Main Funding Source',
                translated_name='main_funding_source',
                lookup_class=MainFundingSource,
                max_length=100,
                allow_null=False,
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
                allow_null=False,
            ),
            LookupColumnDefinition(
                name='Main Funding - Industry Collaborative or Industry Contract Funding',
                translated_name='main_funding_industry',
                lookup_class=MainFundingIndustry,
                max_length=100,
                allow_null=False,
            ),
        ]
