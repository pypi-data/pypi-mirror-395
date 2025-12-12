import pandas as pd
from typing import Optional, List
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

    def get(self, schema_custom_fields: Optional[BrynQPanderaDataFrameModel] = None, employee_ids: Optional[List[str]] = None, show_inactive: bool = False) -> pd.DataFrame:
        core_fields = self.__build_api_fields(PeopleSchema)
        custom_fields = self.__build_api_fields(schema_custom_fields) if schema_custom_fields is not None else []
        fields = core_fields + custom_fields

        # Build filters based on employee_ids if provided
        filters = []
        if employee_ids is not None:
            filters = [
                {
                    "fieldPath": "root.id",
                    "operator": "equals",
                    "values": employee_ids
                }
            ]

        resp = self.bob.session.post(url=f"{self.bob.base_url}people/search",
                                      json={
                                          "fields": fields,
                                          "filters": filters,
                                          "showInactive": show_inactive,
                                          #"humanReadable": "REPLACE"
                                      },
                                      timeout=self.bob.timeout)
        resp.raise_for_status()
        df = pd.json_normalize(resp.json()['employees'])
        if df.empty and employee_ids is not None and resp.status_code == 200:
            raise Exception(f"No employees found in HiBob for employee_ids: {employee_ids}")

        df = df.loc[:, ~df.columns.str.contains('value')]

        # Normalize separators in incoming data: convert '/' to '.' to match schema aliases
        df.columns = df.columns.str.replace('/', '.', regex=False)

        # A lot of fields from Bob are returned with only ID's. Those fields should be mapped to names. Therefore, we need to get the mapping from the named-lists endpoint.
        resp_named_lists = self.bob.session.get(url=f"{self.bob.base_url}company/named-lists", timeout=self.bob.timeout, headers=self.bob.headers)
        named_lists = resp_named_lists.json()
        # save json to file
        # import json
        # with open('named_lists.json', 'w') as f:
        #     json.dump(named_lists, f, indent=4)

        # Transform named_lists to create id-to-value mappings for each field
        named_lists = {key.split('.')[-1]: {item['id']: item['value'] for item in value['values']} for key, value in named_lists.items()}

        deviating_named_list_cols_mapping = {
            'payroll.employment.type': 'payrollEmploymentType',
            'home.familyStatus': 'familystatus',
            'personal.nationality': 'nationalities',
            'internal.terminationReason': 'terminationreason',
        }

        for field in df.columns:
            # Fields in the response and in the named-list does have different building blocks (e.g. people.payroll.entitlement. or people.entitlement.). But they both end with the same last block
            field_df = field.split('.')[-1].split('work_')[-1]

            # Check if this field has a deviating mapping
            named_list_key = deviating_named_list_cols_mapping.get(field, field_df)

            if named_list_key in named_lists.keys() and named_list_key not in ['site']:
                mapping = named_lists[named_list_key]
                df[field] = df[field].apply(
                    lambda v: [mapping.get(x, x) for x in v] if isinstance(v, list) else mapping.get(v, v)
                )

        if schema_custom_fields is not None:
            valid_people, invalid_people_custom = Functions.validate_data(df=df, schema=schema_custom_fields, debug=True)
        else:
            valid_people = df
            invalid_people_custom = pd.DataFrame()

        valid_people, invalid_people = Functions.validate_data(df=valid_people, schema=PeopleSchema, debug=True)

        return valid_people, pd.concat([invalid_people, invalid_people_custom])
