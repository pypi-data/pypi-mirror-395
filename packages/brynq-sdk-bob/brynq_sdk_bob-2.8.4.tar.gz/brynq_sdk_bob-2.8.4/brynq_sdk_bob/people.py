import pandas as pd
import re
from typing import Optional
from brynq_sdk_functions import Functions
from brynq_sdk_functions import BrynQPanderaDataFrameModel
from .bank import Bank
from .employment import Employment
from .salaries import Salaries
from .schemas.people import PeopleSchema
from .work import Work
from .custom_tables import CustomTables


class People:
    def __init__(self, bob):
        self.bob = bob
        self.salaries = Salaries(bob)
        self.employment = Employment(bob)
        self.bank = Bank(bob)
        self.work = Work(bob)
        self.custom_tables = CustomTables(bob)
        self.schema = PeopleSchema



        # Build API fields using column metadata if present (api_field), otherwise use the column (alias) name
    def __build_api_fields(self, schema_model: BrynQPanderaDataFrameModel) -> list[str]:
        schema = schema_model.to_schema()
        return [
            ((getattr(col, "metadata", None) or {}).get("api_field")) or col_name
            for col_name, col in schema.columns.items()
        ]

    def get(self, schema_custom_fields: Optional[BrynQPanderaDataFrameModel] = None) -> pd.DataFrame:

        core_fields = self.__build_api_fields(PeopleSchema)
        custom_fields = self.__build_api_fields(schema_custom_fields) if schema_custom_fields is not None else []
        fields = core_fields + custom_fields

        resp = self.bob.session.post(url=f"{self.bob.base_url}people/search",
                                      json={
                                          "fields": fields,
                                          "filters": []
                                          #"humanReadable": "REPLACE"
                                      },
                                      timeout=self.bob.timeout)
        resp.raise_for_status()
        df = pd.json_normalize(resp.json()['employees'])


        # Normalize separators in incoming data: convert '/' to '.' to match schema aliases
        df.columns = df.columns.str.replace('/', '.', regex=False)


        # Clean up custom .value columns; keeps only one field per custom key. the .value column actually contains the value., other column is nested key.
        custom_cols = [col for col in df.columns if "custom" in str(col) and str(col).endswith('.value')]
        for col in custom_cols:
            new_col = col.removesuffix('.value')
            # prefer non-empty clean column, otherwise upgrade .value data
            if new_col not in df.columns:
                df = df.rename(columns={col: new_col})
            elif df[new_col].isna().all() and not df[col].isna().all():
                df[new_col] = df[col]
                df = df.drop(columns=[col])
            else:
                # Drop identical/redundant .value col
                if df[new_col].equals(df[col]):
                    df = df.drop(columns=[col])
                pass


        # A lot of fields from Bob are returned with only ID's. Those fields should be mapped to names. Therefore, we need to get the mapping from the named-lists endpoint.
        resp_named_lists = self.bob.session.get(url=f"{self.bob.base_url}company/named-lists", timeout=self.bob.timeout, headers=self.bob.headers)
        named_lists = resp_named_lists.json()

        # Transform named_lists to create id-to-value mappings for each field
        named_lists = {key.split('.')[-1]: {item['id']: item['value'] for item in value['values']} for key, value in named_lists.items()}

        for field in df.columns:
            # Fields in the response and in the named-list does have different building blocks (e.g. people.payroll.entitlement. or people.entitlement.). But they both end with the same last block
            field_df = field.split('.')[-1].split('work_')[-1]
            if field_df in named_lists.keys() and field_df not in ['site']:
                mapping = named_lists[field_df]
                df[field] = df[field].apply(
                    lambda v: [mapping.get(x, x) for x in v] if isinstance(v, list) else mapping.get(v, v)
                )


        if schema_custom_fields is not None:

            valid_people, invalid_people_custom = Functions.validate_data(df=df, schema=schema_custom_fields, debug=True)


        else:
            valid_people = df
            invalid_people_custom = pd.DataFrame()


        valid_people, invalid_people = Functions.validate_data(df=valid_people, schema=PeopleSchema, debug=True)

        # For columns ending with .value.value, use fillna to fill the corresponding base column since that's not done automatically
        def _normalize_key(key: str) -> str:
            # Build mapping from custom schema alias (API path) to the real column name used after validation
            key = key.lstrip('.')
            key = key.replace('/', '.')
            key = key.replace('.', '_')
            key = re.sub(r'(?<!^)([A-Z])', r'_\1', key).lower()
            return key

        alias_to_real: dict = {}
        if schema_custom_fields is not None:
            alias_map = getattr(schema_custom_fields, "_alias_map", {})  # real_name -> alias
            alias_to_real = {_normalize_key(alias): real for real, alias in alias_map.items()}

        for col in valid_people.columns:
            if col.endswith('value.value'):
                # Compute the base alias (remove suffix), normalise, and resolve to real column name via custom schema
                base_alias = col[:-12]
                target_key = _normalize_key(base_alias)
                target_col = alias_to_real.get(target_key, target_key)
                if target_col in valid_people.columns:
                    valid_people[target_col] = valid_people[target_col].fillna(valid_people[col])

        # Remove columns that contain '.value' or '_get'
        valid_people = valid_people.loc[:, ~valid_people.columns.str.contains(r'\.value|_get')]
        return valid_people, pd.concat([invalid_people, invalid_people_custom])
