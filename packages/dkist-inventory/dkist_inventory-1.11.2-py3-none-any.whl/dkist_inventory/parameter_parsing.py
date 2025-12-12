from datetime import datetime
from typing import Any
from typing import Mapping
from typing import TypeAlias

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator
from pydantic import model_validator

ParameterType: TypeAlias = list[dict] | str | None


class ParameterValue(BaseModel):
    parameter_value_start_date: datetime | None = Field(
        default_factory=lambda: datetime(1, 1, 1),
        alias="parameterValueStartDate",
    )
    parameter_value_id: int = Field(alias="parameterValueId")
    parameter_value: str = Field(alias="parameterValue")

    @field_validator("parameter_value_start_date", mode="before")
    def set_default_start_date(cls, v):
        if v is None:
            return datetime(1, 1, 1)
        return v


class Parameter(BaseModel):
    parameter_name: str = Field(alias="parameterName")
    parameter_values: list[ParameterValue] = Field(alias="parameterValues")


class ParameterParser(BaseModel):
    parameters: list[Parameter]
    dataset_date: datetime
    filtered_parameters: list[Mapping[str, Any]] = Field(default_factory=list)

    @model_validator(mode="after")
    def filter_latest_parameters(self) -> "ParameterParser":
        """
        Filters the parameter values to keep only the most recent value for each parameter name,
        based on the dataset date. The result is stored in `filtered_parameters`.

        Returns:
            ParameterParser: The model instance with `filtered_parameters` populated.
        """
        if not self.parameters:
            return self

        # make dataset_date naive to match inputs
        ds_date = (
            self.dataset_date.replace(tzinfo=None)
            if self.dataset_date.tzinfo
            else self.dataset_date
        )

        filtered_data = []
        for parameter in self.parameters:
            parameter_values = parameter.parameter_values or []

            # filter to <= ds_date
            valid_values = [
                value for value in parameter_values if value.parameter_value_start_date <= ds_date
            ]

            # if none, drop this parameter
            if not valid_values:
                continue

            # pick latest from valid only
            latest_value = valid_values[0]
            for v in valid_values[1:]:
                if v.parameter_value_start_date > latest_value.parameter_value_start_date:
                    latest_value = v

            filtered_data.append(
                {
                    "parameterName": parameter.parameter_name,
                    "parameterValues": [
                        {
                            "parameterValue": latest_value.parameter_value,
                            "parameterValueId": latest_value.parameter_value_id,
                            "parameterValueStartDate": latest_value.parameter_value_start_date.isoformat(),
                        }
                    ],
                }
            )

        self.filtered_parameters = filtered_data
        return self
