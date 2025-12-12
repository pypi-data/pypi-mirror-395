#  Copyright (c) 2022 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

import typing

import diffusion.internal.pydantic_compat.v1 as pydantic

import diffusion
from diffusion.datatypes.timeseries import VT
from diffusion.datatypes.timeseries.types import (
    TimeSeriesValueType, TimeSeriesValueType_Diffusion, )
from diffusion.internal.serialisers.pydantic import (
    MarshalledModel,
)


class TimeSeriesAppendRequest(MarshalledModel):
    topic_path: str = pydantic.Field(alias="path")
    value_type: typing.Union[
        str, typing.Type[TimeSeriesValueType_Diffusion]
    ] = pydantic.Field(alias="data-type-name")
    value: typing.Union[TimeSeriesValueType_Diffusion, bytes]

    # noinspection PyUnusedLocal,PyNestedDecorators
    @pydantic.validator("value_type", pre=True)
    @classmethod
    def validate_dt(
        cls,
        field_value: typing.Type[VT],
        values: typing.Dict[str, typing.Any],
        field,
        config,
    ) -> str:
        return str(field_value)

    # noinspection PyUnusedLocal,PyNestedDecorators
    @pydantic.validator("value", pre=True)
    @classmethod
    def validate_value(
        cls,
        field_value: TimeSeriesValueType,
        values: typing.Dict[str, typing.Any],
        field,
        config,
    ) -> bytes:
        return bytes(field_value)

    class Config(MarshalledModel.Config):
        alias = "time-series-append-request"
        allow_population_by_field_name = True

        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {
                "time-series-append-request": {
                    "time-series-append-request.path": "topic_path",
                    "time-series-append-request.data-type-name": "value_type",
                    "time-series-append-request.value": "value",
                }
            }


class TimeSeriesTimestampAppendRequest(TimeSeriesAppendRequest):
    timestamp: int

    class Config(MarshalledModel.Config):
        alias = "time-series-timestamp-append-request"

        @classmethod
        def attr_mappings_all(cls, modelcls):
            return {
                "time-series-timestamp-append-request": {
                    "time-series-append-request.path": "topic_path",
                    "time-series-append-request.data-type-name": "value_type",
                    "time-series-append-request.value": "value",
                }
            }


class TimeSeriesEditRequest(MarshalledModel):
    """
    The time series edit request.
    Added in version 6.8.3
    """

    topic_path: str = pydantic.Field(alias="path")
    """
    The topic path.
    """

    value_type: str = pydantic.Field(alias="data-type-name")

    # noinspection PyUnusedLocal,PyNestedDecorators
    @pydantic.validator("value_type", pre=True)
    @classmethod
    def validate_dt(
        cls,
        field_value: typing.Type[VT],
        values: typing.Dict[str, typing.Any],
        field,
        config,
    ) -> str:
        return str(field_value)

    @property
    def type(self):
        return diffusion.datatypes.get(self.value_type)

    """
    The corresponding data type name of the value type.
    """
    original_sequence: int = pydantic.Field(
        alias="time-series-sequence"
    )
    """
    The original sequence number.
    """

    value: bytes = pydantic.Field(alias="value")
    """
    The value in serialised form.
    """
    # noinspection PyUnusedLocal,PyNestedDecorators
    @pydantic.validator("value", pre=True)
    @classmethod
    def validate_value(
        cls,
        field_value: TimeSeriesValueType,
        values: typing.Dict[str, typing.Any],
        field,
        config,
    ) -> bytes:
        return bytes(field_value)

    class Config(MarshalledModel.Config):
        alias = "time-series-edit-request"
