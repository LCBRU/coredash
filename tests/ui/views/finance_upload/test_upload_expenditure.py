import pytest
from coredash.model.finance_upload import WORKSHEET_NAME_EXTERNAL_FUNDING, FinanceUpload, FinanceUpload_ExternalFunding_ColumnDefinition
from tests.ui.views.finance_upload.test_upload import FakeFinanceUpload, assert__expenditure_equals_expected, assert__external_funding_equals_expected, assert__finance_upload_error, upload_post_file


@pytest.mark.usefixtures("loggedin_user_finance_uploader", "standard_lookups")
@pytest.mark.xdist_group(name="spreadsheets")
class TestUploadExternalFunding:
    def test__post__valid_file__insert(self, client, faker):
        file: FakeFinanceUpload = faker.finance_spreadsheet()

        upload_post_file(
            client,
            expected_status=FinanceUpload.STATUS__PROCESSED,
            file=file,
        )

        assert__expenditure_equals_expected(file)


    # def test__post__valid_file__update(self, client, faker):
    #     existing = faker.project().get_in_db()
    #     file: FakeFinanceUpload = faker.finance_spreadsheet()

    #     upload_post_file(
    #         client,
    #         expected_status=FinanceUpload.STATUS__PROCESSED,
    #         file=file,
    #     )

    #     assert__external_funding_equals_expected(file)


    # def test__post__missing_worksheet(self, client, faker):
    #     file: FakeFinanceUpload = faker.finance_spreadsheet()
    #     file.external_funding_name = 'External Not Funding'

    #     upload_post_file(
    #         client,
    #         expected_status=FinanceUpload.STATUS__ERROR,
    #         file=file,
    #     )

    #     assert__finance_upload_error(row=None, message=f"Missing worksheet '{WORKSHEET_NAME_EXTERNAL_FUNDING}'")


    # def test__post__missing_row(self, client, faker):
    #     file: FakeFinanceUpload = faker.finance_spreadsheet(external_funding_count=0)

    #     upload_post_file(
    #         client,
    #         expected_status=FinanceUpload.STATUS__ERROR,
    #         file=file,
    #     )

    #     assert__finance_upload_error(row=None, message=f"Expected a minimum of 1 rows, but 0 were found")


    # def test__post__multiple_rows_given__takes_only_first(self, client, faker):
    #     file: FakeFinanceUpload = faker.finance_spreadsheet(external_funding_count=2)

    #     upload_post_file(
    #         client,
    #         expected_status=FinanceUpload.STATUS__PROCESSED,
    #         file=file,
    #     )

    #     assert__external_funding_equals_expected(file)


    # @pytest.mark.parametrize(
    #     "missing_column_name", FinanceUpload_ExternalFunding_ColumnDefinition().column_names,
    # )
    # def test__post__missing_column(self, client, faker, missing_column_name):
    #     columns_to_include = set(FinanceUpload_ExternalFunding_ColumnDefinition().column_names) - set([missing_column_name])

    #     file: FakeFinanceUpload = faker.finance_spreadsheet()
    #     file.external_funding_headers = columns_to_include

    #     upload_post_file(
    #         client,
    #         expected_status=FinanceUpload.STATUS__ERROR,
    #         file=file
    #         )

    #     assert__finance_upload_error(row=None, message=f"Missing column '{missing_column_name}'")


    # @pytest.mark.parametrize(
    #     "casing", ['lower', 'upper', 'title'],
    # )
    # def test__post__case_insenstive_column_names(self, client, faker, casing):
    #     match casing:
    #         case 'lower':
    #             columns_to_include = [cn.lower() for cn in FinanceUpload_ExternalFunding_ColumnDefinition().column_names]
    #         case 'upper':
    #             columns_to_include = [cn.upper() for cn in FinanceUpload_ExternalFunding_ColumnDefinition().column_names]
    #         case 'title':
    #             columns_to_include = [cn.title() for cn in FinanceUpload_ExternalFunding_ColumnDefinition().column_names]

    #     file: FakeFinanceUpload = faker.finance_spreadsheet()
    #     file.external_funding_headers = columns_to_include

    #     upload_post_file(
    #         client,
    #         expected_status=FinanceUpload.STATUS__PROCESSED,
    #         file=file,
    #     )

    #     assert__external_funding_equals_expected(file)


    # @pytest.mark.parametrize(
    #     "invalid_column", [
    #         'Research Council',
    #         'Research Charity',
    #         'DHSC/NIHR',
    #         'Industry Collaborative',
    #         'Industry Contract',
    #         'Other non-commercial',
    #         'Total',
    #     ],
    # )
    # def test__post__invalid_column_type(self, client, faker, invalid_column):
    #     file: FakeFinanceUpload = faker.finance_spreadsheet()
    #     file.external_funding_data[0][invalid_column.lower()] = faker.pystr()

    #     upload_post_file(
    #         client,
    #         expected_status=FinanceUpload.STATUS__ERROR,
    #         file=file,
    #     )

    #     assert__finance_upload_error(row=1, message=f"{invalid_column}: Invalid value")


    # @pytest.mark.parametrize(
    #     "missing_data", [
    #         'Research Council',
    #         'Research Charity',
    #         'DHSC/NIHR',
    #         'Industry Collaborative',
    #         'Industry Contract',
    #         'Other non-commercial',
    #         'Total',
    #     ],
    # )
    # @pytest.mark.parametrize(
    #     "value", ['', None, ' '],
    # )
    # def test__post__missing_mandatory_data(self, client, faker, missing_data, value):
    #     file: FakeFinanceUpload = faker.finance_spreadsheet()
    #     file.external_funding_data[0][missing_data.lower()] = value

    #     upload_post_file(
    #         client,
    #         expected_status=FinanceUpload.STATUS__ERROR,
    #         file=file,
    #     )

    #     assert__finance_upload_error(row=1, message=f"{missing_data}: Data is missing")


    # @pytest.mark.parametrize(
    #     "invalid_column", [
    #         'Research Council',
    #         'Research Charity',
    #         'DHSC/NIHR',
    #         'Industry Collaborative',
    #         'Industry Contract',
    #         'Other non-commercial',
    #         'Total',
    #     ],
    # )
    # @pytest.mark.parametrize(
    #     "curr", '£$€¥',
    # )
    # def test__post__numbers_with_currency_indicators(self, client, faker, invalid_column, curr):
    #     file: FakeFinanceUpload = faker.finance_spreadsheet()
    #     file.external_funding_data[0][invalid_column.lower()] = curr + str(file.external_funding_data[0][invalid_column.lower()])

    #     upload_post_file(
    #         client,
    #         expected_status=FinanceUpload.STATUS__PROCESSED,
    #         file=file,
    #     )


    # @pytest.mark.parametrize(
    #     "invalid_column", [
    #         'Research Council',
    #         'Research Charity',
    #         'DHSC/NIHR',
    #         'Industry Collaborative',
    #         'Industry Contract',
    #         'Other non-commercial',
    #         'Total',
    #     ],
    # )
    # def test__post__numbers_with_commas(self, client, faker, invalid_column):
    #     file: FakeFinanceUpload = faker.finance_spreadsheet()
    #     file.external_funding_data[0][invalid_column.lower()] = '3,000,000'

    #     upload_post_file(
    #         client,
    #         expected_status=FinanceUpload.STATUS__PROCESSED,
    #         file=file,
    #     )
