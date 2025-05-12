from dotenv import load_dotenv

from coredash.model.finance_upload import FinanceUploadColumnDefinition

# Load environment variables from '.env' file.
load_dotenv()


def convert_projects_to_spreadsheet_data(projects):
    result = []

    col_def = FinanceUploadColumnDefinition()

    for p in projects:
        row = {}

        for c in col_def.column_definition:
            row[c.name.lower()] = c.get_object_value(p)

        result.append(row)

    return result
