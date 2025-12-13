import pandas as pd
from brynq_sdk_functions import Functions
from .schemas.custom_tables import CustomTableSchema, CustomTableMetadataSchema


class CustomTables:
    def __init__(self, bob):
        self.bob = bob
        self.schema = CustomTableSchema

    def get(self, employee_id: str, custom_table_id: str) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Get custom table data for an employee

        Args:
            employee_id: The employee ID
            custom_table_id: The custom table ID

        Returns:
            A tuple of (valid_data, invalid_data) as pandas DataFrames
        """
        resp = self.bob.session.get(url=f"{self.bob.base_url}people/custom-tables/{employee_id}/{custom_table_id}")
        resp.raise_for_status()
        data = resp.json()

        # Normalize the nested JSON response
        df = pd.json_normalize(
            data,
            record_path=['values']
        )

        df['employee_id'] = employee_id
        valid_data, invalid_data = Functions.validate_data(df=df, schema=self.schema, debug=True)

        return valid_data, invalid_data

    def get_metadata(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Get metadata for all custom tables

        Returns:
            A tuple of (valid_data, invalid_data) as pandas DataFrames containing table and column metadata
        """
        url = f"{self.bob.base_url}people/custom-tables/metadata"
        resp = self.bob.session.get(url=url)
        resp.raise_for_status()
        data = resp.json()

        # Flatten the nested structure - create one row per column with table info repeated
        rows = []
        for table in data.get('tables', []):
            table_info = {
                'table_id': table.get('id'),
                'table_name': table.get('name'),
                'table_category': table.get('category'),
                'table_description': table.get('description')
            }

            for column in table.get('columns', []):
                row = {
                    **table_info,
                    'column_id': column.get('id'),
                    'column_name': column.get('name'),
                    'column_description': column.get('description'),
                    'column_mandatory': column.get('mandatory'),
                    'column_type': column.get('type')
                }
                rows.append(row)

        df = pd.DataFrame(rows)

        # Validate against the metadata schema
        valid_data, invalid_data = Functions.validate_data(df=df, schema=CustomTableMetadataSchema, debug=True)

        return valid_data, invalid_data
