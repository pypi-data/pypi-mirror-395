import pandas as pd
import requests
from typing import Optional, List
from brynq_sdk_functions import Functions
from .schemas.work import WorkSchema


class Work:
    def __init__(self, bob):
        self.bob = bob
        self.schema = WorkSchema

    def get(self, employee_ids: Optional[List[str]] = None) ->(pd.DataFrame, pd.DataFrame):
        params = {"limit": 100}

        # Add employeeIds filter if provided
        if employee_ids is not None:
            params["employeeIds"] = ",".join(employee_ids)

        request = requests.Request(method='GET',
                                   url=f"{self.bob.base_url}bulk/people/work",
                                   params=params)
        data = self.bob.get_paginated_result(request)
        df = pd.json_normalize(
            data,
            record_path='values',
            meta=['employeeId']
        )
        valid_work, invalid_work = Functions.validate_data(df=df, schema=self.schema, debug=True)

        return valid_work, invalid_work
