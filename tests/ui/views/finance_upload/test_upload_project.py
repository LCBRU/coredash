import pytest
from lbrc_flask.database import db
from sqlalchemy import select
from coredash.model.finance_upload import WORKSHEET_NAME_PROJECT_LIST, FinanceUpload, FinanceUpload_ProjectList_ColumnDefinition
from coredash.model.project import Project
from tests import convert_projects_to_spreadsheet_data
from tests.ui.views.finance_upload.test_upload import FakeFinanceUpload, assert__finance_upload_error, assert__finance_upload_warning, upload_post_file


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
def test__post__missing_worksheet(client, faker, loggedin_user_finance_uploader, standard_lookups):
    data = faker.finance_spreadsheet_data()

    file = FakeFinanceUpload()
    file.project_list_data = data
    file.project_list_name = 'Project Not List'

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__ERROR,
        file=file,
    )

    assert__finance_upload_error(row=None, message=f"Missing worksheet '{WORKSHEET_NAME_PROJECT_LIST}'")


@pytest.mark.parametrize(
    "missing_column_name", FinanceUpload_ProjectList_ColumnDefinition().column_names,
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__missing_column(client, faker, loggedin_user_finance_uploader, standard_lookups, missing_column_name):
    columns_to_include = set(FinanceUpload_ProjectList_ColumnDefinition().column_names) - set([missing_column_name])

    data = faker.finance_spreadsheet_data()
    file = FakeFinanceUpload()
    file.project_list_data = data
    file.project_list_headers = columns_to_include

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__ERROR,
        file=file
        )

    assert__finance_upload_error(row=None, message=f"Missing column '{missing_column_name}'")


@pytest.mark.parametrize(
    "casing", ['lower', 'upper', 'title'],
)
@pytest.mark.xdist_group(name="spreadsheets")
def test__post__case_insenstive_column_names(client, faker, loggedin_user_finance_uploader, standard_lookups, casing):
    match casing:
        case 'lower':
            columns_to_include = [cn.lower() for cn in FinanceUpload_ProjectList_ColumnDefinition().column_names]
        case 'upper':
            columns_to_include = [cn.upper() for cn in FinanceUpload_ProjectList_ColumnDefinition().column_names]
        case 'title':
            columns_to_include = [cn.title() for cn in FinanceUpload_ProjectList_ColumnDefinition().column_names]

    data = faker.finance_spreadsheet_data()

    file = FakeFinanceUpload()
    file.project_list_data = data
    file.project_list_headers = columns_to_include

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__PROCESSED,
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

    file = FakeFinanceUpload()
    file.project_list_data = data

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__ERROR,
        file=file,
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

    file = FakeFinanceUpload()
    file.project_list_data = data

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        file=file,
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

    file = FakeFinanceUpload()
    file.project_list_data = data

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        file=file,
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
    max_length = FinanceUpload_ProjectList_ColumnDefinition().definition_for_column_name(invalid_column).max_length

    data = faker.finance_spreadsheet_data(rows=1)
    data[0][invalid_column.lower()] = faker.pystr(min_chars=max_length+1, max_chars=max_length*2)

    file = FakeFinanceUpload()
    file.project_list_data = data

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__ERROR,
        file=file,
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

    file = FakeFinanceUpload()
    file.project_list_data = data

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__ERROR,
        file=file,
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

    file = FakeFinanceUpload()
    file.project_list_data = data

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__ERROR,
        file=file,
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

    file = FakeFinanceUpload()
    file.project_list_data = data

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        file=file,
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

    file = FakeFinanceUpload()
    file.project_list_data = data

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        file=file,
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

    file = FakeFinanceUpload()
    file.project_list_data = data

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        file=file,
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

    file = FakeFinanceUpload()
    file.project_list_data = data

    upload_post_file(
        client,
        expected_status=FinanceUpload.STATUS__PROCESSED,
        file=file,
    )
