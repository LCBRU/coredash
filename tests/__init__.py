from dotenv import load_dotenv

from coredash.model.finance_upload import FinanceUpload_ExternalFunding_ColumnDefinition, FinanceUpload_ProjectList_ColumnDefinition

# Load environment variables from '.env' file.
load_dotenv()


def convert_projects_to_spreadsheet_data(projects):
    result = []

    col_def = FinanceUpload_ProjectList_ColumnDefinition()

    for p in projects:
        row = {}

        for c in col_def.column_definition:
            row[c.name.lower()] = c.get_object_value(p)

        result.append(row)

    return result


def convert_external_funding_to_spreadsheet_data(external_fundings):
    result = []

    col_def = FinanceUpload_ExternalFunding_ColumnDefinition()

    for o in external_fundings:
        row = {}

        for c in col_def.column_definition:
            row[c.name.lower()] = c.get_object_value(o)

        result.append(row)

    return result
