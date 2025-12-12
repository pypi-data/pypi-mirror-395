import pandera as pa
from typing import Optional
from pandera.typing import Series, String
import pandas as pd
from brynq_sdk_functions import BrynQPanderaDataFrameModel


class BankSchema(BrynQPanderaDataFrameModel):
    id: Series[pd.Int64Dtype] = pa.Field(coerce=True, description="Bank ID", alias="id")
    employee_id: Series[String] = pa.Field(coerce=True, description="Employee ID", alias="employee_id")
    amount: Optional[Series[pd.Int64Dtype]] = pa.Field(coerce=True, description="Amount", alias="amount")
    allocation: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Allocation", alias="allocation")
    branch_address: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Branch Address", alias="branchAddress")
    bank_name: Series[String] = pa.Field(coerce=True, nullable=True, description="Bank Name", alias="bankName")
    account_number: Series[String] = pa.Field(coerce=True, nullable=True, description="Account Number", alias="accountNumber")
    routing_number: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="Routing Number", alias="routingNumber")
    bank_account_type: Series[String] = pa.Field(coerce=True, nullable=True, description="Bank Account Type", alias="bankAccountType")
    bic_or_swift: Optional[Series[String]] = pa.Field(coerce=True, nullable=True, description="BIC or SWIFT", alias="bicOrSwift")
    changed_by: Series[String] = pa.Field(coerce=True, nullable=True, description="Changed By", alias="changedBy")
    iban: Series[String] = pa.Field(coerce=True, description="IBAN", alias="iban")
    account_nickname: Series[String] = pa.Field(coerce=True, nullable=True, description="Account Nickname", alias="accountNickname")
    use_for_bonus: Optional[Series[pd.BooleanDtype]] = pa.Field(coerce=True, nullable=True, description="Use for Bonus", alias="useForBonus")

    class Config:
        coerce = True
