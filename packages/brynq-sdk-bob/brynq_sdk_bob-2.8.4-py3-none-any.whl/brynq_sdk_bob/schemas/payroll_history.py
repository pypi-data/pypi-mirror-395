from datetime import datetime
from typing import Optional

import pandas as pd
import pandera as pa
from pandera import Bool
from pandera.typing import Series, String, Float, DateTime
import pandera.extensions as extensions
from brynq_sdk_functions import BrynQPanderaDataFrameModel



@extensions.register_check_method()
def check_list(x):
    return isinstance(x, list)


class PayrollHistorySchema(BrynQPanderaDataFrameModel):
    id: Optional[Series[String]] = pa.Field(coerce=True, description="Person ID", alias="id")
    display_name: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Display Name", alias="displayName")
    company_id: Optional[Series[String]] = pa.Field(coerce=True, description="Company ID", alias="companyId")

    class Config:
        coerce = True
