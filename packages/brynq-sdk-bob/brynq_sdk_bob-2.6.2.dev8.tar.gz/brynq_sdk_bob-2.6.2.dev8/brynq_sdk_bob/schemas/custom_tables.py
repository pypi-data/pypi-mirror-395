import pandera as pa
from pandera.typing import Series
import pandas as pd
from brynq_sdk_functions import BrynQPanderaDataFrameModel

class CustomTableSchema(BrynQPanderaDataFrameModel):
    id: Series[pd.Int64Dtype] = pa.Field(coerce=True, description="Custom Table ID", alias="id")
    employee_id: Series[str] = pa.Field(coerce=True, description="Employee ID", alias="employee_id")

    class Config:
        coerce = True
class CustomTableMetadataSchema(BrynQPanderaDataFrameModel):
    # Table information
    table_id: Series[str] = pa.Field(coerce=True, description="Table ID", alias="table_id")
    table_name: Series[str] = pa.Field(coerce=True, description="Table Name", alias="table_name")
    table_category: Series[str] = pa.Field(coerce=True, description="Table Category", alias="table_category")
    table_description: Series[str] = pa.Field(coerce=True, nullable=True, description="Table Description", alias="table_description")

    # Column information
    column_id: Series[str] = pa.Field(coerce=True, description="Column ID", alias="column_id")
    column_name: Series[str] = pa.Field(coerce=True, description="Column Name", alias="column_name")
    column_description: Series[str] = pa.Field(coerce=True, nullable=True, description="Column Description", alias="column_description")
    column_mandatory: Series[bool] = pa.Field(coerce=True, description="Is Column Mandatory", alias="column_mandatory")
    column_type: Series[str] = pa.Field(coerce=True, description="Column Type", alias="column_type")

    class Config:
        coerce = True
