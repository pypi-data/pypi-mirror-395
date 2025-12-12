#  Copyright (c) 2024 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from __future__ import annotations

import traceback
import typing
from typing import Any

from typing_extensions import Self

from diffusion.datatypes.foundation.abstract import (
    ValueType,
    ValueType_target,
    Converter,
    ValueTypeProtocol,
    ValueType_target_non_co, TS_T, RealValue,
)
from .abstract import AbstractDataType, A_T
from diffusion.handlers import LOG

if typing.TYPE_CHECKING:
    from ..timeseries.types import TimeSeriesValueType
    from ..timeseries.time_series_event import Event


class IBytes(
    AbstractDataType[TS_T, ValueType, RealValue],
    typing.Generic[TS_T, ValueType, RealValue],
):
    """Base type for Diffusion data types allowing conversion to and from [bytes][bytes]."""

    @classmethod
    def encode(cls, value: Any) -> bytes:
        raise NotImplementedError()

    @classmethod
    def decode(cls: typing.Type[A_T], data: bytes) -> Any:
        raise NotImplementedError()

    type_name = "IBytes"

    @classmethod
    def _converter_from(
            cls: typing.Type[ValueType],
            source_type: typing.Type[ValueType_target],
    ) -> typing.Optional[Converter[ValueType_target, ValueType]]:
        if issubclass(source_type, cls):
            def convert_from(
                    source_value: ValueTypeProtocol
            ) -> typing.Optional[
                ValueType
            ]:
                try:
                    if source_value and source_value.value is not None:
                        return typing.cast(
                            ValueType,
                            typing.cast(typing.Type[Self], cls).from_bytes(
                                source_value.to_bytes()
                            ),
                        )
                    return None
                except Exception as e:  # pragma: no cover
                    LOG.error(f"Got {e}: {traceback.format_exc()}")
                    raise

            return typing.cast(
                Converter[
                    ValueType_target,
                    ValueType
                ],
                convert_from,
            )
        return typing.cast(
            typing.Optional[Converter[ValueType_target, ValueType]],
            typing.cast(Self, cls).timeseries_converter_from(source_type),
        )

    @classmethod
    def timeseries_converter_from(
            cls: typing.Type[ValueType],
            source_type: typing.Type[ValueType_target_non_co],
    ) -> typing.Optional[Converter[ValueType_target_non_co, ValueType]]:
        from diffusion.datatypes import TimeSeriesEventDataType
        from ..timeseries import Event

        if issubclass(source_type, TimeSeriesEventDataType):
            def converter_from_event_data_type():
                inner_type_converter = typing.cast(
                    typing.Type[Self], cls
                ).converter_from(source_type.real_value_type())

                if inner_type_converter is not None:
                    inner_type_converter_final = typing.cast(Converter, inner_type_converter)

                    def converter(
                            input_event: typing.Optional[ValueType_target_non_co],
                    ) -> typing.Optional[ValueType]:
                        source_ts_event_data_value = typing.cast(
                            typing.Optional[TimeSeriesEventDataType], input_event)
                        return typing.cast(
                            typing.Optional[ValueType],
                            inner_type_converter_final(source_ts_event_data_value.value)
                            if source_ts_event_data_value and source_ts_event_data_value.value
                            else None,
                        )

                    return typing.cast(Converter[ValueType_target_non_co, ValueType], converter)
            return converter_from_event_data_type()
        elif issubclass(source_type, Event):
            return typing.cast(
                typing.Optional[Converter[ValueType_target_non_co, ValueType]],
                typing.cast(typing.Type[Self], cls).converter_from_event(source_type),
            )
        return None

    @classmethod
    def converter_from_event(
        cls: typing.Type[ValueType],
        source_type: typing.Type[Event[TimeSeriesValueType]],
    ) -> typing.Optional[Converter[Event[TimeSeriesValueType], ValueType]]:
        from ..timeseries.types import TimeSeriesValueType
        from ..timeseries import Event

        inner_type_converter = typing.cast(typing.Optional[
            Converter[TimeSeriesValueType, ValueType]
        ], typing.cast(typing.Type[Self], cls).converter_from(
            source_type.held_value_type(),
        ))
        if inner_type_converter is not None:
            assert inner_type_converter is not None

            def converter(
                input_event: Event[TimeSeriesValueType],
            ) -> typing.Optional[ValueType]:
                source_ts_event = typing.cast(typing.Optional[Event], input_event)
                return typing.cast(
                    typing.Optional[ValueType],
                    inner_type_converter(source_ts_event.value)
                    if source_ts_event and source_ts_event.value
                    else None,
                )

            return typing.cast(
                Converter[Event[TimeSeriesValueType], ValueType],
                converter,
            )
        return None


