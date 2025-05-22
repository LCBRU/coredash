from io import BytesIO
from typing import Optional
import pytest
from flask import url_for
from lbrc_flask.pytest.asserts import assert__requires_login, assert__input_file, assert__refresh_response, assert__requires_role
from lbrc_flask.database import db
from sqlalchemy import func, select
from coredash.model.external_funding import ExternalFunding
from coredash.model.finance_upload import FinanceUpload, FinanceUploadErrorMessage, FinanceUploadWarningMessage
from coredash.model.project import Project
from tests import convert_external_funding_to_spreadsheet_data, convert_projects_to_spreadsheet_data
from tests.faker import FakeFinanceUpload
from tests.requests import coredash_modal_get
from unittest.mock import patch


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

    print(out.messages)

    assert out.filename == wb.filename
    assert out.status == expected_status

    if expected_status == FinanceUpload.STATUS__PROCESSED:
        expected_project_count = len(file.project_list_data)
        expected_external_funding_count = 1
    else:
        expected_project_count = 0
        expected_external_funding_count = 0

    assert db.session.execute(select(func.count(Project.id))).scalar() == expected_project_count
    assert db.session.execute(select(func.count(ExternalFunding.id))).scalar() == expected_external_funding_count


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


def assert__projects_equals_expected(spreadsheet: FakeFinanceUpload):
    actual = convert_projects_to_spreadsheet_data(db.session.execute(select(Project)).scalars())

    assert spreadsheet.project_list_data == actual


def assert__external_funding_equals_expected(spreadsheet: FakeFinanceUpload):
    actual = convert_external_funding_to_spreadsheet_data(db.session.execute(select(ExternalFunding)).scalars())

    assert spreadsheet.external_funding_data[0:1] == actual


@pytest.mark.app_crsf(True)
def test__get__has_form(client, loggedin_user_finance_uploader):
    _get(client, _url(external=False), loggedin_user_finance_uploader, has_form=True)


@pytest.mark.xdist_group(name="spreadsheets")
def test__post__unexpected_error(client, faker, loggedin_user_finance_uploader, standard_lookups):
    file: FakeFinanceUpload = faker.finance_spreadsheet()

    with patch('coredash.services.finance_uploads.finance_upload_process', side_effect=Exception('Mocked Error')):
        upload_post_file(
            client,
            expected_status=FinanceUpload.STATUS__ERROR,
            file=file,
        )

    assert__finance_upload_error(row=None, message="Unexpected error")
