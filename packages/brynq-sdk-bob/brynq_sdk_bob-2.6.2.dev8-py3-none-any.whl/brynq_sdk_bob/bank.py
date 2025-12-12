import pandas as pd
from brynq_sdk_functions import Functions
from .schemas.bank import BankSchema

import time
from tqdm import tqdm
from tenacity import retry, stop_after_delay, wait_exponential

class Bank:
    def __init__(self, bob):
        self.bob = bob
        self.schema = BankSchema

    @retry(stop=stop_after_delay(120), wait=wait_exponential(multiplier=1, min=1, max=10))
    def _get_bank_accounts(self, person_id: str):
        """Fetch bank accounts for a person with retry logic (max 2 minutes)."""
        resp = self.bob.session.get(url=f"{self.bob.base_url}people/{person_id}/bank-accounts", timeout=self.bob.timeout)
        resp.raise_for_status()
        return resp

    def get(self, person_ids: pd.Series, field_selection: list[str] = []) -> (pd.DataFrame, pd.DataFrame):
        data = []
        for person_id in tqdm(person_ids, desc="Fetching bank accounts"):
            resp = self._get_bank_accounts(person_id)
            temp_data = resp.json()['values']
            # when an employee has one or more bank accounts, the response is a list of dictionaries.
            for account in temp_data:
                account['employee_id'] = person_id
            data += temp_data

            # rate limit is 50 per minute
            time.sleep(1.3)

        df = pd.DataFrame(data)

        valid_banks, invalid_banks = Functions.validate_data(df=df, schema=BankSchema, debug=True)

        return valid_banks, invalid_banks
