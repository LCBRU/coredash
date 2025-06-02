from dotenv import load_dotenv

from coredash.model.finance_upload import FinanceUpload_Expenditure_ColumnDefinition, FinanceUpload_ExternalFunding_ColumnDefinition, FinanceUpload_ProjectList_ColumnDefinition

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


def convert_expenditure_to_spreadsheet_data(expenditure):
    result = []

    for hc in FinanceUpload_Expenditure_ColumnDefinition.HEALTH_CATEGORIES:
        row = {}
        row[FinanceUpload_Expenditure_ColumnDefinition.COLUMN_NAME__HEALTH_CATEGORY.lower()] = hc
        field_name = FinanceUpload_Expenditure_ColumnDefinition.field_name_from_column_name(hc)
        row[FinanceUpload_Expenditure_ColumnDefinition.COLUMN_NAME__EXPENDITURE.lower()] = getattr(expenditure, field_name)

        result.append(row)

    return result
