from datetime import datetime
from io import BytesIO
from typing import Optional, TYPE_CHECKING

import pandas as pd
from brynq_sdk_functions import Functions
if TYPE_CHECKING:
    from brynq_sdk_bob import Bob


class Reports:
    def __init__(self, bob):
        self.bob: Bob = bob

    def get(self) -> pd.DataFrame:
        resp = self.bob.session.get(url=f"{self.bob.base_url}company/reports", timeout=self.bob.timeout)
        resp.raise_for_status()
        data = resp.json()
        df = pd.json_normalize(
            data,
            record_path='views'
        )
        # df = self.bob.rename_camel_columns_to_snake_case(df)
        # valid_documents, invalid_documents = Functions.validate_data(df=df, schema=DocumentsSchema, debug=True)

        return df

    def download(self, report_id: int | str = None, report_format: str = "csv") -> bytes:
        if report_id:
            url = f"{self.bob.base_url}company/reports/{report_id}/download"
        else:
            raise ValueError("Either report_id or report_name must be provided")

        resp = self.bob.session.get(url=url, timeout=self.bob.timeout, params={"format": report_format})
        resp.raise_for_status()
        data = resp.content

        return data
