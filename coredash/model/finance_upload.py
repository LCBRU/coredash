from flask import current_app
from lbrc_flask.database import db
from lbrc_flask.security import AuditMixin
from lbrc_flask.model import CommonMixin
from lbrc_flask.column_data import ColumnDefinition, ColumnsDefinition, ExcelData
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text
from werkzeug.utils import secure_filename


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
    filename: Mapped[str] = mapped_column(String(500))
    status: Mapped[str] = mapped_column(String(50), default='')
    errors: Mapped[str] = mapped_column(Text, default='')

    @property
    def local_filepath(self):
        return current_app.config["FILE_UPLOAD_DIRECTORY"] / secure_filename(f"{self.id}_{self.filename}")

    def validate(self):
        spreadsheet = ExcelData(self.local_filepath)
        definition = FinanceUploadColumnDefinition()

        errors = definition.validation_errors(spreadsheet)

        if errors:
            self.errors = "\n".join(errors)
            self.status = FinanceUpload.STATUS__ERROR

    @property
    def is_error(self):
        return self.status == FinanceUpload.STATUS__ERROR

    def data(self):
        definition = FinanceUploadColumnDefinition()

        return definition.translated_data(ExcelData(self.local_filepath))


class FinanceUploadColumnDefinition(ColumnsDefinition):
    @property
    def column_definition(self):
        return [
            ColumnDefinition(
                name='title',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=500,
                allow_null=False,
            ),
            ColumnDefinition(
                name='summary',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                allow_null=True,
            ),
            ColumnDefinition(
                name='comments',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                allow_null=True,
            ),
            ColumnDefinition(
                name='local_rec_number',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=50,
                allow_null=False,
            ),
            ColumnDefinition(
                name='iras_number',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=50,
                allow_null=False,
            ),
            ColumnDefinition(
                name='cpms_id',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=50,
                allow_null=False,
            ),
            ColumnDefinition(
                name='start_date',
                type=ColumnDefinition.COLUMN_TYPE_DATE,
                allow_null=False,
            ),
            ColumnDefinition(
                name='end_date',
                type=ColumnDefinition.COLUMN_TYPE_DATE,
                allow_null=False,
            ),
            ColumnDefinition(
                name='brc_funding',
                type=ColumnDefinition.COLUMN_TYPE_INTEGER,
                allow_null=False,
            ),
            ColumnDefinition(
                name='main_funding_brc_funding',
                type=ColumnDefinition.COLUMN_TYPE_INTEGER,
                allow_null=True,
            ),
            ColumnDefinition(
                name='total_external_funding_award',
                type=ColumnDefinition.COLUMN_TYPE_INTEGER,
                allow_null=False,
            ),
            ColumnDefinition(
                name='sensitive',
                type=ColumnDefinition.COLUMN_TYPE_BOOLEAN,
                allow_null=False,
            ),
            ColumnDefinition(
                name='first_in_human',
                type=ColumnDefinition.COLUMN_TYPE_BOOLEAN,
                allow_null=False,
            ),
            ColumnDefinition(
                name='link_to_nihr_transactional_research_collaboration',
                type=ColumnDefinition.COLUMN_TYPE_BOOLEAN,
                allow_null=False,
            ),
            ColumnDefinition(
                name='crn_rdn_portfolio_study',
                type=ColumnDefinition.COLUMN_TYPE_BOOLEAN,
                allow_null=False,
            ),
            ColumnDefinition(
                name='rec_approval_required',
                type=ColumnDefinition.COLUMN_TYPE_BOOLEAN,
                allow_null=False,
            ),
            ColumnDefinition(
                name='randomised_trial',
                type=ColumnDefinition.COLUMN_TYPE_BOOLEAN,
                allow_null=False,
            ),
            ColumnDefinition(
                name='project_status',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
            ColumnDefinition(
                name='theme',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
            ColumnDefinition(
                name='ukcrc_health_category',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
            ColumnDefinition(
                name='nihr_priority_area',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
            ColumnDefinition(
                name='ukcrc_research_activity_code',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
            ColumnDefinition(
                name='racs_sub_category',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
            ColumnDefinition(
                name='research_type',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
            ColumnDefinition(
                name='methodology',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
            ColumnDefinition(
                name='expected_impact',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
            ColumnDefinition(
                name='trial_phase',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
            ColumnDefinition(
                name='main_funding_source',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
            ColumnDefinition(
                name='main_funding_category',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
            ColumnDefinition(
                name='main_funding_dhsc_nihr_funding',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
            ColumnDefinition(
                name='main_funding_industry',
                type=ColumnDefinition.COLUMN_TYPE_STRING,
                max_length=100,
                allow_null=False,
            ),
        ]
