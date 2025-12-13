import pandas as pd
import pandera as pa
from pandera import Bool
from pandera.typing import Series, String, Float, DateTime
import pandera.extensions as extensions
from brynq_sdk_functions import BrynQPanderaDataFrameModel
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, Dict, Any


class SalarySchema(BrynQPanderaDataFrameModel):
    id: Series[pd.Int64Dtype] = pa.Field(coerce=True, description="Salary ID", alias="id")
    employee_id: Series[String] = pa.Field(coerce=True, description="Employee ID", alias="employeeId")
    pay_frequency: Series[String] = pa.Field(coerce=True, nullable=True, description="Pay Frequency", alias="payFrequency") # has a list of possible values , isin=['Monthly']
    creation_date: Series[DateTime] = pa.Field(coerce=True, nullable=True, description="Creation Date", alias="creationDate")
    is_current: Series[Bool] = pa.Field(coerce=True, description="Is Current", alias="isCurrent")
    modification_date: Series[DateTime] = pa.Field(coerce=True, nullable=True, description="Modification Date", alias="modificationDate")
    effective_date: Series[DateTime] = pa.Field(coerce=True, description="Effective Date", alias="effectiveDate")
    end_effective_date: Series[DateTime] = pa.Field(coerce=True, nullable=True, description="End Effective Date", alias="endEffectiveDate")
    change_reason: Series[str] = pa.Field(coerce=True, nullable=True, description="Change Reason", alias="change.reason")
    pay_period: Series[String] = pa.Field(coerce=True, nullable=True, description="Pay Period", alias="payPeriod")
    base_value: Series[Float] = pa.Field(coerce=True, nullable=True, description="Base Value", alias="base.value") #needs to become base.value?
    base_currency: Series[String] = pa.Field(coerce=True, nullable=True, description="Base Currency", alias="base.currency")
    active_effective_date: Series[DateTime] = pa.Field(coerce=True, nullable=True, description="Active Effective Date", alias="activeEffectiveDate")


class SalaryCreateSchema(BaseModel):
    can_be_deleted: Optional[bool] = Field(None, description="internal flag", alias="canBeDeleted")
    work_change_type: Optional[str] = Field(None, description="The type of the change that was performed for this work entry. This will contain the ID of the value from the Change Type list.", alias="workChangeType")
    salary_change_reason: Optional[str] = Field(None, description="Reason for the change", alias="change.reason")
    salary_change_changed_by: Optional[str] = Field(None, description="Name of the user who changed the entry", alias="change.changedBy")
    salary_change_changed_by_id: Optional[str] = Field(None, description="ID of the user who changed the entry", alias="change.changedById")
    pay_frequency: Optional[str] = Field(None, description="Represents the frequency the salary is paid. This can be one of: Monthly, Semi Monthly, Weekly, or Bi-Weekly.", alias="payFrequency")
    creation_date: Optional[date] = Field(None, description="The date this entry was created.", alias="creationDate")
    is_current: Optional[bool] = Field(None, description="Is 'true' when this is the effective entry which is currently active.", alias="isCurrent")
    modification_date: Optional[date] = Field(None, description="The date this entry was modified.", alias="modificationDate")
    id: Optional[int] = Field(None, description="The id of the entry.", alias="id")
    end_effective_date: Optional[date] = Field(None, description="For entries that are not active - this it the date this entry became not effective.", alias="endEffectiveDate")
    active_effective_date: Optional[date] = Field(None, description="The active effective date for this entry.", alias="activeEffectiveDate")
    custom_columns: Optional[Dict[str, Any]] = Field(None, description="If the table has custom columns, they will appear here.", alias="customColumns")
    base_value: float = Field(..., description="Base amount value", alias="base.value")
    base_currency: str = Field(..., description="Three-letter currency code.", alias="base.currency")
    pay_period: str = Field(..., description="Represents the period for this salary entry. This can be one of: Annual, Hourly, Daily, Weekly, Monthly.", alias="payPeriod")
    effective_date: Optional[date] = Field(None, description="The date this entry becomes effective. This is a mandatory field for a work entry.", alias="effectiveDate")

    class Config:
        allow_population_by_field_name = True
        coerce = True
