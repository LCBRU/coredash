from io import BytesIO
from typing import Optional
import pytest
from flask import url_for
from lbrc_flask.pytest.asserts import assert__requires_login, assert__input_file, assert__refresh_response, assert__requires_role
from lbrc_flask.database import db
from lbrc_flask.pytest.faker import FakeXlsxWorksheet, FakeXlsxFile
from sqlalchemy import func, select
from coredash.model.finance_upload import WORKSHEET_NAME_PROJECT_LIST, FinanceUpload, FinanceUpload_ProjectList_ColumnDefinition, FinanceUploadErrorMessage, FinanceUploadWarningMessage
from coredash.model.project import Project
from tests import convert_projects_to_spreadsheet_data
from tests.requests import coredash_modal_get
from unittest.mock import patch


class FakeFinanceUpload():
    def __init__(self, filename: Optional[str] = None):
        self.filename: str = filename or 'test.xlsx'

        self.project_list_name: str = WORKSHEET_NAME_PROJECT_LIST
        self.project_list_headers: list[str] = FinanceUpload_ProjectList_ColumnDefinition().column_names
        self.project_list_header_row: int = 4
        self.project_list_data: list = []

    def get_project_list_worksheet(self):
        return FakeXlsxWorksheet(
            name=self.project_list_name,
            headers=self.project_list_headers,
            data=self.project_list_data,
            headers_on_row=self.project_list_header_row,
        )

    def get_worksheets(self):
        return [
            self.get_project_list_worksheet(),
        ]

    def get_workbook(self):
        return FakeXlsxFile(
            filename=self.filename,
            worksheets=self.get_worksheets(),
        )


def _url(external=True, **kwargs):
    return url_for('ui.finance_upload_upload', _external=external, **kwargs)


def _get(client, url, loggedin_user, has_form):
    resp = coredash_modal_get(client, url, loggedin_user, has_form)

    assert__input_file(resp.soup, 'finance_file')

    return resp


def upload_post(client, url, file, filename):
    data={
        'finance_file': (
            BytesIO(file),
            filename,
        ),
    }

    return client.post(url, data=data)


def upload_post_file(client, file: FakeFinanceUpload, expected_status: str):
    wb = file.get_workbook()

    resp = upload_post(client, _url(external=False), wb.get_iostream(), file.filename)
    assert__refresh_response(resp)

    out = db.session.execute(select(FinanceUpload)).scalar()

    assert out.filename == wb.filename
    assert out.status == expected_status

    if expected_status == FinanceUpload.STATUS__PROCESSED:
        expected_project_count = len(file.project_list_data)
    else:
        expected_project_count = 0

    assert db.session.execute(select(func.count(Project.id))).scalar() == expected_project_count


def test__get__requires_login(client):
    assert__requires_login(client, _url(external=False))


def test__get__requires_editor_login__not(client, loggedin_user):
    assert__requires_role(client, _url(external=False))


def assert__finance_upload_error(row: Optional[int], message: str):
    assert db.session.execute(
        select(FinanceUploadErrorMessage)
        .where(FinanceUploadErrorMessage.row == row)
        .where(FinanceUploadErrorMessage.message.like(f"{message}%"))
    ).scalar_one_or_none() is not None


def assert__finance_upload_warning(row: Optional[int], message: str):
    assert db.session.execute(
        select(FinanceUploadWarningMessage)
        .where(FinanceUploadWarningMessage.row == row)
        .where(FinanceUploadWarningMessage.message.like(f"{message}%"))
    ).scalar_one_or_none() is not None


@pytest.mark.app_crsf(True)
def test__get__has_form(client, loggedin_user_finance_uploader):
    _get(client, _url(external=False), loggedin_user_finance_uploader, has_form=True)


@pytest.mark.xdist_group(name="spreadsheets")
def test__post__valid_file__insert(client, faker, loggedin_user_finance_uploader, standard_lookups):
    file = FakeFinanceUpload()
    file.project_list_data = faker.finance_spreadsheet_data()

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        file=file,
    )

    actual = convert_projects_to_spreadsheet_data(db.session.execute(select(Project)).scalars())
    expected = file.project_list_data

    assert expected == actual


@pytest.mark.xdist_group(name="spreadsheets")
def test__post__valid_file__update(client, faker, loggedin_user_finance_uploader, standard_lookups):
    rows = 10
    existing = [faker.project().get_in_db() for _ in range(rows)]
    data = faker.finance_spreadsheet_data(rows=rows)

    file = FakeFinanceUpload()
    file.project_list_data = data

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        file=file,
    )

    actual = convert_projects_to_spreadsheet_data(db.session.execute(select(Project)).scalars())
    expected = data

    assert expected == actual


@pytest.mark.xdist_group(name="spreadsheets")
def test__post__unexpected_error(client, faker, loggedin_user_finance_uploader, standard_lookups):
    data = faker.finance_spreadsheet_data(rows=1)
    file = FakeFinanceUpload()
    file.project_list_data = data


    with patch('coredash.services.finance_uploads.finance_upload_process', side_effect=Exception('Mocked Error')):
        upload_post_file(
            client,
            expected_status=FinanceUpload.STATUS__ERROR,
            file=file,
        )
    assert__finance_upload_error(row=None, message="Unexpected error")
