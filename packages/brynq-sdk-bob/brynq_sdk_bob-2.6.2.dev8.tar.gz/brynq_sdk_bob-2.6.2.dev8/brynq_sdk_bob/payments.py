import time
from typing import List, Optional

import pandas as pd
from tqdm import tqdm

from brynq_sdk_functions import Functions

from .schemas.payments import ActualPaymentsSchema, VariablePaymentSchema


class Payments:
    def __init__(self, bob):
        self.bob = bob
        self.schema = VariablePaymentSchema

    def _apply_named_list_mappings(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply named list ID-to-value mappings to dataframe columns."""
        if df.empty:
            return df

        # Fetch named lists from Bob API
        resp_named_lists = self.bob.session.get(
            url=f"{self.bob.base_url}company/named-lists",
            timeout=self.bob.timeout,
            headers=self.bob.headers
        )
        named_lists = resp_named_lists.json()

        # Transform named_lists to create id-to-value mappings for each field
        named_lists = {
            key.split('.')[-1]: {item['id']: item['value'] for item in value['values']}
            for key, value in named_lists.items()
        }

        # rename payrollVariableType to variableType in named lists
        named_lists['variableType'] = named_lists['payrollVariableType']

        for field in df.columns:
            # Fields in the response and in the named-list have different building blocks
            # but they both end with the same last block
            field_df = field.split('.')[-1].split('work_')[-1]
            if field_df in named_lists.keys() and field_df not in ['site']:
                mapping = named_lists[field_df]
                df[field] = df[field].apply(
                    lambda v: [mapping.get(x, x) for x in v] if isinstance(v, list) else mapping.get(v, v)
                )

        return df

    def get(self, person_ids: List[str]) -> (pd.DataFrame, pd.DataFrame):
        df = pd.DataFrame()
        for person_id in tqdm(person_ids, desc="Fetching variable payments"):
            resp = self.bob.session.get(url=f"{self.bob.base_url}people/{person_id}/variable", timeout=self.bob.timeout)
            resp.raise_for_status()
            data = resp.json()
            df = pd.concat([df, pd.json_normalize(
                data,
                record_path='values'
            )])
            df['employee_id'] = person_id

            # Rate limit is 50 per minute
            time.sleep(1.3)

        df = df.reset_index(drop=True)

        # Apply named list mappings
        df = self._apply_named_list_mappings(df)

        valid_payments, invalid_payments = Functions.validate_data(df=df, schema=self.schema, debug=True)
        return valid_payments, invalid_payments

    def get_actual_payments(
        self,
        limit: int = 200,
        employee_ids: Optional[List[str]] = None,
        pay_date_from: Optional[str] = None,
        pay_date_to: Optional[str] = None
    ) -> (pd.DataFrame, pd.DataFrame):
        """
        Search for actual payments with optional employee and pay date filters.
        This method auto-paginates until all results are fetched.

        See Bob API: https://apidocs.hibob.com/reference/post_people-actual-payments-search
        See Pagination: https://apidocs.hibob.com/docs/pagination

        Args:
            limit (int): Number of records per page (default: 50, max: 200).
            employee_ids (Optional[List[str]]): Filter by employee IDs.
            pay_date_from (Optional[str]): Inclusive start date filter (YYYY-MM-DD).
            pay_date_to (Optional[str]): Inclusive end date filter (YYYY-MM-DD).

        Returns:
            tuple: (valid_payments DataFrame, invalid_payments DataFrame)
        """
        base_payload = {
            "pagination": {
                "limit": limit
            }
        }

        filters = []
        if employee_ids:
            filters.append({
                "fieldPath": "employeeId",
                "operator": "equals",
                "values": employee_ids
            })
        if pay_date_from:
            filters.append({
                "fieldPath": "payDate",
                "operator": "greaterThanOrEquals",
                "value": pay_date_from
            })
        if pay_date_to:
            filters.append({
                "fieldPath": "payDate",
                "operator": "lessThanOrEquals",
                "value": pay_date_to
            })

        if filters:
            base_payload["filters"] = filters

        all_results = []
        next_cursor = None

        while True:
            payload = dict(base_payload)
            payload["pagination"] = dict(base_payload["pagination"])
            if next_cursor:
                payload["pagination"]["cursor"] = next_cursor

            resp = self.bob.session.post(
                url=f"{self.bob.base_url}people/actual-payments/search",
                json=payload,
                timeout=self.bob.timeout
            )
            resp.raise_for_status()
            data = resp.json()

            page_results = data.get('results') or []
            if page_results:
                all_results.extend(page_results)

            next_cursor = (data.get('response_metadata') or {}).get('next_cursor')
            if not next_cursor:
                break

        if not all_results:
            empty_df = pd.DataFrame()
            return empty_df, empty_df

        df = pd.json_normalize(all_results)

        # Apply named list mappings
        df = self._apply_named_list_mappings(df)

        valid_payments, invalid_payments = Functions.validate_data(
            df=df,
            schema=ActualPaymentsSchema,
            debug=True
        )

        return valid_payments, invalid_payments
