from io import BytesIO
from typing import Optional
import pytest
from flask import url_for
from lbrc_flask.pytest.asserts import assert__requires_login, assert__input_file, assert__refresh_response, assert__requires_role
from lbrc_flask.database import db
from sqlalchemy import func, select
from coredash.model.finance_upload import WORKSHEET_NAME_PROJECT_LIST, FinanceUpload, FinanceUploadColumnDefinition, FinanceUploadErrorMessage, FinanceUploadWarningMessage
from coredash.model.project import Project
from tests import convert_projects_to_spreadsheet_data
from tests.requests import coredash_modal_get
from unittest.mock import patch


def _url(external=True, **kwargs):
    return url_for('ui.finance_upload_upload', _external=external, **kwargs)


def _get(client, url, loggedin_user, has_form):
    resp = coredash_modal_get(client, url, loggedin_user, has_form)

    assert__input_file(resp.soup, 'finance_file')

    return resp


def _post(client, url, file, filename):
    data={
        'finance_file': (
            BytesIO(file),
            filename,
        ),
    }

    return client.post(url, data=data)


def _post_upload_data(client, faker, data, expected_status, expected_projects):
    file = faker.xlsx(
        headers=FinanceUploadColumnDefinition().column_names,
        data=data,
        worksheet=WORKSHEET_NAME_PROJECT_LIST,
        headers_on_row=4,
    )
    _post_upload_file(client, expected_status, expected_projects, file)


def _post_upload_file(client, expected_status, expected_projects, file):
    resp = _post(client, _url(external=False), file.get_iostream(), file.filename)
    assert__refresh_response(resp)

    out = db.session.execute(select(FinanceUpload)).scalar()
    assert out.filename == file.filename
    assert out.status == expected_status
    assert db.session.execute(select(func.count(Project.id))).scalar() == expected_projects


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
    data = faker.finance_spreadsheet_data()

    _post_upload_data(
        client,
        faker,
        data,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        expected_projects=len(data),
        )

    actual = convert_projects_to_spreadsheet_data(db.session.execute(select(Project)).scalars())
    expected = data

    assert expected == actual


@pytest.mark.xdist_group(name="spreadsheets")
def test__post__valid_file__update(client, faker, loggedin_user_finance_uploader, standard_lookups):
    rows = 10
    existing = [faker.project().get_in_db() for _ in range(rows)]
    data = faker.finance_spreadsheet_data(rows=rows)

    _post_upload_data(
        client,
        faker,
        data,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        expected_projects=len(data),
        )

    # Remove Keys as the data has no keys, but they will be
    # given one when they are saved
    actual = convert_projects_to_spreadsheet_data(db.session.execute(select(Project)).scalars())
    expected = data

    assert expected == actual


@pytest.mark.xdist_group(name="spreadsheets")
def test__post__missing_worksheet(client, faker, loggedin_user_finance_uploader, standard_lookups):
    data = faker.finance_spreadsheet_data()

    file = faker.xlsx(
        headers=FinanceUploadColumnDefinition().column_names,
        data=data,
        worksheet='Project Not List',
        headers_on_row=4,
    )

    _post_upload_file(
        client=client,
        expected_status=FinanceUpload.STATUS__ERROR,
        expected_projects=0,
        file=file,
    )

    assert__finance_upload_error(row=None, message=f"Missing worksheet '{WORKSHEET_NAME_PROJECT_LIST}'")


@pytest.mark.parametrize(
    "missing_column_name", FinanceUploadColumnDefinition().column_names,
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__missing_column(client, faker, loggedin_user_finance_uploader, standard_lookups, missing_column_name):
    columns_to_include = set(FinanceUploadColumnDefinition().column_names) - set([missing_column_name])

    data = faker.finance_spreadsheet_data()

    file = faker.xlsx(
        headers=columns_to_include,
        data=data, worksheet=WORKSHEET_NAME_PROJECT_LIST,
        headers_on_row=4,
    )

    _post_upload_file(
        client=client,
        expected_status=FinanceUpload.STATUS__ERROR,
        expected_projects=0,
        file=file,
    )

    assert__finance_upload_error(row=None, message=f"Missing column '{missing_column_name}'")


@pytest.mark.parametrize(
    "casing", ['lower', 'upper', 'title'],
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__case_insenstive_column_names(client, faker, loggedin_user_finance_uploader, standard_lookups, casing):
    match casing:
        case 'lower':
            columns_to_include = [cn.lower() for cn in FinanceUploadColumnDefinition().column_names]
        case 'upper':
            columns_to_include = [cn.upper() for cn in FinanceUploadColumnDefinition().column_names]
        case 'title':
            columns_to_include = [cn.title() for cn in FinanceUploadColumnDefinition().column_names]

    data = faker.finance_spreadsheet_data()
    file = faker.xlsx(
        headers=columns_to_include,
        data=data,
        worksheet=WORKSHEET_NAME_PROJECT_LIST,
        headers_on_row=4,
    )

    _post_upload_file(
        client,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        expected_projects=len(data),
        file=file,
        )

    actual = convert_projects_to_spreadsheet_data(db.session.execute(select(Project)).scalars())
    expected = data
    assert expected == actual


@pytest.mark.parametrize(
    "invalid_column", [
        'Project Actual Start Date',
        'Project End Date',
        'BRC funding',
        'Total External Funding Awarded',
        'Is this project sensitive',
        'First in Human Project',
        'Link to NIHR Translational Research Collaboration',
        'CRN/RDN Portfolio study',
        'REC Approval Required',
        'Randomised Trial',
    ],
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__invalid_column_type(client, faker, loggedin_user_finance_uploader, standard_lookups, invalid_column):
    data = faker.finance_spreadsheet_data(rows=1)

    data[0][invalid_column.lower()] = faker.pystr()

    _post_upload_data(
        client=client,
        faker=faker,
        data=data,
        expected_status=FinanceUpload.STATUS__ERROR,
        expected_projects=0,
    )

    assert__finance_upload_error(row=1, message=f"{invalid_column}: Invalid value")


@pytest.mark.parametrize(
    "invalid_column", [
        'Main Funding - BRC Funding',
    ],
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__invalid_column_type__ignore_errors(client, faker, loggedin_user_finance_uploader, standard_lookups, invalid_column):
    data = faker.finance_spreadsheet_data(rows=1)

    data[0][invalid_column.lower()] = faker.pystr()

    _post_upload_data(
        client=client,
        faker=faker,
        data=data,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        expected_projects=1,
    )

    assert__finance_upload_warning(row=1, message=f"{invalid_column}: Invalid value")


@pytest.mark.parametrize(
    "boolean_column", [
        'Is this project sensitive',
        'First in Human Project',
        'Link to NIHR Translational Research Collaboration',
        'CRN/RDN Portfolio study',
        'REC Approval Required',
        'Randomised Trial',
    ],
)
@pytest.mark.parametrize(
    "value", [
        ('true', True),
        ('True', True),
        ('false', False),
        ('False', False),
        ('y', True),
        ('Y', True),
        ('n', False),
        ('N', False),
        ('yes', True),
        ('Yes', True),
        ('no', False),
        ('No', False),
    ],
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__valid_boolean_options(client, faker, loggedin_user_finance_uploader, standard_lookups, boolean_column, value):
    data = faker.finance_spreadsheet_data(rows=1)

    data[0][boolean_column.lower()] = value[0]

    _post_upload_data(
        client=client,
        faker=faker,
        data=data,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        expected_projects=1,
    )

    actual = convert_projects_to_spreadsheet_data(db.session.execute(select(Project)).scalars())
    assert actual[0][boolean_column.lower()] == value[1]


@pytest.mark.parametrize(
    "invalid_column", [
        'Project Title',
        'Local REC number',
        'IRAS Number',
        'CRN/RDN CPMS ID',
        'Main Funding Source',
    ],
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__invalid_column_length(client, faker, loggedin_user_finance_uploader, standard_lookups, invalid_column):
    max_length = FinanceUploadColumnDefinition().definition_for_column_name(invalid_column).max_length

    data = faker.finance_spreadsheet_data(rows=1)
    data[0][invalid_column.lower()] = faker.pystr(min_chars=max_length+1, max_chars=max_length*2)

    _post_upload_data(
        client=client,
        faker=faker,
        data=data,
        expected_status=FinanceUpload.STATUS__ERROR,
        expected_projects=0,
    )

    assert__finance_upload_error(row=1, message=f"{invalid_column}: Text is longer than {max_length} characters")



@pytest.mark.parametrize(
    "missing_data", [
        'Project Title',
        'BRC funding',
        'Total External Funding Awarded',
        'Is this project sensitive',
        'First in Human Project',
        'Link to NIHR Translational Research Collaboration',
        'CRN/RDN Portfolio study',
        'REC Approval Required',
        'Randomised Trial',
        'Project Status',
        'Theme',
        'UKCRC Health Category',
        'UKCRC Research Activity Code',
        'Research Type',
        'Methodology',
        'Expected Impact',
        'Main Funding Source',
        'Main Funding Category',
    ],
)
@pytest.mark.parametrize(
    "value", ['', None, ' '],
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__missing_mandatory_data(client, faker, loggedin_user_finance_uploader, standard_lookups, missing_data, value):
    data = faker.finance_spreadsheet_data(rows=1)
    data[0][missing_data.lower()] = value

    _post_upload_data(
        client,
        faker,
        data,
        expected_status=FinanceUpload.STATUS__ERROR,
        expected_projects=0,
        )

    assert__finance_upload_error(row=1, message=f"{missing_data}: Data is missing")


@pytest.mark.parametrize(
    "invalid_column", [
        'Project Status',
        'Theme',
        'UKCRC Health Category',
        'NIHR priority Areas / Fields of Research',
        'UKCRC Research Activity Code',
        'RACS sub-categories',
        'Research Type',
        'Methodology',
        'Expected Impact',
        'Trial Phase',
        'Main Funding Category',
        'Main Funding - DHSC/NIHR Funding',
        'Main Funding - Industry Collaborative or Industry Contract Funding',
    ],
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__invalid_lookup_value(client, faker, loggedin_user_finance_uploader, standard_lookups, invalid_column):
    data = faker.finance_spreadsheet_data(rows=1)
    data[0][invalid_column.lower()] = 'This doesnt exist'

    _post_upload_data(
        client=client,
        faker=faker,
        data=data,
        expected_status=FinanceUpload.STATUS__ERROR,
        expected_projects=0,
    )

    assert__finance_upload_error(row=1, message=f"{invalid_column}: Does not exist")


@pytest.mark.parametrize(
    "invalid_column", [
        'RACS sub-categories',
        'Trial Phase',
        'Main Funding - DHSC/NIHR Funding',
        'Main Funding - Industry Collaborative or Industry Contract Funding',
    ],
)
@pytest.mark.parametrize(
    "value", ['', None, ' '],
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__empty_lookup_value_for_not_mandatory(client, faker, loggedin_user_finance_uploader, standard_lookups, invalid_column, value):
    data = faker.finance_spreadsheet_data(rows=1)
    data[0][invalid_column.lower()] = value

    _post_upload_data(
        client=client,
        faker=faker,
        data=data,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        expected_projects=1,
    )


@pytest.mark.parametrize(
    "invalid_column", [
        'Project Status',
        'Theme',
        'UKCRC Health Category',
        'NIHR priority Areas / Fields of Research',
        'UKCRC Research Activity Code',
        'RACS sub-categories',
        'Research Type',
        'Methodology',
        'Expected Impact',
        'Trial Phase',
        'Main Funding Category',
        'Main Funding - DHSC/NIHR Funding',
        'Main Funding - Industry Collaborative or Industry Contract Funding',
    ],
)
@pytest.mark.parametrize(
    "punc", ',.;',
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__lookup_value_with_punctuation(client, faker, loggedin_user_finance_uploader, standard_lookups, invalid_column, punc):
    data = faker.finance_spreadsheet_data(rows=1)
    data[0][invalid_column.lower()] = punc + data[0][invalid_column.lower()] + punc

    _post_upload_data(
        client=client,
        faker=faker,
        data=data,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        expected_projects=1,
    )


@pytest.mark.parametrize(
    "invalid_column", [
        'Participants Recruited to Centre FY',
        'BRC funding',
        'Main Funding - BRC Funding',
        'Total External Funding Awarded',
    ],
)
@pytest.mark.parametrize(
    "curr", '£$€¥',
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__numbers_with_currency_indicators(client, faker, loggedin_user_finance_uploader, standard_lookups, invalid_column, curr):
    data = faker.finance_spreadsheet_data(rows=1)
    data[0][invalid_column.lower()] = curr + str(data[0][invalid_column.lower()])

    _post_upload_data(
        client=client,
        faker=faker,
        data=data,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        expected_projects=1,
    )


@pytest.mark.parametrize(
    "invalid_column", [
        'Participants Recruited to Centre FY',
        'BRC funding',
        'Main Funding - BRC Funding',
        'Total External Funding Awarded',
    ],
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__numbers_with_commas(client, faker, loggedin_user_finance_uploader, standard_lookups, invalid_column):
    data = faker.finance_spreadsheet_data(rows=1)
    data[0][invalid_column.lower()] = '3,000,000'

    _post_upload_data(
        client=client,
        faker=faker,
        data=data,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        expected_projects=1,
    )


@pytest.mark.xdist_group(name="spreadsheets")
def test__post__unexpected_error(client, faker, loggedin_user_finance_uploader, standard_lookups):
    data = faker.finance_spreadsheet_data(rows=1)

    with patch('coredash.services.finance_uploads.finance_upload_process', side_effect=Exception('Mocked Error')):
        _post_upload_data(
            client=client,
            faker=faker,
            data=data,
            expected_status=FinanceUpload.STATUS__ERROR,
            expected_projects=0,
        )

    assert__finance_upload_error(row=None, message="Unexpected error")

