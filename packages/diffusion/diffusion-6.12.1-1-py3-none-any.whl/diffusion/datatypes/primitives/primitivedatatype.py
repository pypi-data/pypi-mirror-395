#  Copyright (c) 2021 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

from __future__ import annotations

import functools
import typing
from typing_extensions import Self
import traceback

from diffusion.datatypes.exceptions import InvalidDataError
from diffusion.datatypes.foundation.abstract import A_T, ValueType, \
    ValueType_target, Converter
from diffusion.datatypes.foundation.ibytesdatatype import IBytes
from diffusion.features.topics.details.topic_specification import (
    TopicSpecification,
)
from io import BytesIO
from diffusion.handlers import LOG

T = typing.TypeVar("T", contravariant=True)
TypeTupleVar = typing.TypeVar("TypeTupleVar", bound=typing.Tuple[type, ...])


class PrimitiveDataType(
    IBytes[
        TopicSpecification["PrimitiveDataType[T]"],
        "PrimitiveDataType[T]",
        typing.Optional[T]
    ],
    typing.Generic[T],
):

    # noinspection PyTypeChecker
    @classmethod
    @functools.lru_cache(maxsize=None)
    def __class_getitem__(
        cls, item: typing.Tuple[ValueType_target]
    ) -> typing.Type[
        PrimitiveDataType[ValueType_target]
    ]:
        return typing.cast(
            typing.Type[
                "PrimitiveDataType[ValueType_target]"
            ],
            cls,
        )

    def validate(self) -> None:
        """Check the current value for correctness.

        Raises:
            `InvalidDataError`: If the value is invalid.
        """
        if not self.validate_raw_type(type(self.value)):
            raw_types = (
                t.__name__
                for t in self._get_base_type_parameters()
                if t not in (None, type(None))
            )
            raise InvalidDataError(
                "The value must be either None, or one of the following types:"
                f" {', '.join(raw_types)}; "
                f"got {type(self.value).__name__} instead."
            )

    @classmethod
    def encode(cls, value: typing.Any) -> bytes:
        return cls.encoder.dumps(value)

    @classmethod
    def decode(cls: typing.Type[A_T], data: bytes) -> typing.Any:
        try:
            with BytesIO(data) as fp:
                value = cls.encoder.load(fp)
                if len(fp.read(1)) > 0:
                    raise InvalidDataError("Excess CBOR data")
        except Exception as e:
            LOG.error(f"Got {e}: {traceback.format_exc()}")
            raise
        return value

    @classmethod
    def _converter_from(
            cls: typing.Type[ValueType],
            source_type: typing.Type[ValueType_target],
    ) -> typing.Optional[Converter[ValueType_target, ValueType]]:
        from diffusion.datatypes.foundation.abstract import AbstractDataType
        if issubclass(source_type, cls):

            def raw_type_converter(
                    value: typing.Optional[ValueType_target],
            ) -> typing.Optional[ValueType]:
                raw_value = (
                    typing.cast(typing.Type[Self], cls)(
                        typing.cast(AbstractDataType, value).value
                    )
                    if value
                    else None
                )
                return typing.cast(typing.Optional[ValueType], raw_value)

            return raw_type_converter
        return typing.cast(
            typing.Optional[Converter[ValueType_target, ValueType]],
            typing.cast(Self, cls).timeseries_converter_from(source_type),
        )

