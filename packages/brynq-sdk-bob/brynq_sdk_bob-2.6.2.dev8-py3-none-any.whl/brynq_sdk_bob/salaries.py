import pandas as pd
import requests
from typing import Optional, List
from brynq_sdk_functions import Functions
from .schemas.salary import SalarySchema, SalaryCreateSchema


class Salaries:
    def __init__(self, bob):
        self.bob = bob
        self.schema = SalarySchema

    def get(self, employee_ids: Optional[List[str]] = None) -> tuple[pd.DataFrame, pd.DataFrame]:
        params = {"limit": 100}

        # Add employeeIds filter if provided
        if employee_ids is not None:
            params["employeeIds"] = ",".join(employee_ids)

        request = requests.Request(method='GET',
                                   url=f"{self.bob.base_url}bulk/people/salaries",
                                   params=params)
        data = self.bob.get_paginated_result(request)
        df = pd.json_normalize(
            data,
            record_path='values',
            meta=['employeeId']
        )
        valid_salaries, invalid_salaries = Functions.validate_data(df=df, schema=SalarySchema, debug=True)

        return valid_salaries, invalid_salaries

    def create(self, salary_data: dict) -> requests.Response:
        nested_data = self.nmbrs.flat_dict_to_nested_dict(salary_data, SalaryCreateSchema)
        salary_data = SalaryCreateSchema(**nested_data)
        payload = salary_data.model_dump(exclude_none=True, by_alias=True)

        resp = self.bob.session.post(url=f"{self.bob.base_url}people/{salary_data.employee_id}/salaries", json=payload)
        resp.raise_for_status()
        return resp

    def delete(self, employee_id: str, salary_id: str) -> requests.Response:
        resp = self.bob.session.delete(url=f"{self.bob.base_url}people/{employee_id}/salaries/{salary_id}")
        resp.raise_for_status()
        return resp
