from dotenv import load_dotenv

from coredash.model.finance_upload import FinanceUploadColumnDefinition
from lbrc_flask.column_data import ColumnDefinition

# Load environment variables from '.env' file.
load_dotenv()


def convert_projects_to_spreadsheet_data(projects):
    result = []

    col_def = FinanceUploadColumnDefinition()

    for p in projects:
        row = {}

        for c in col_def.column_definition:
            field = getattr(p, c.translated_name)
            if c.type == ColumnDefinition.COLUMN_TYPE_LOOKUP:
                row[c.name.lower()] = field.name
            else:
                row[c.name.lower()] = field

        result.append(row)

    return result
