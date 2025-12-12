#  Copyright (c) 2022 - 2025 DiffusionData Ltd., All Rights Reserved.
#
#  Use is subject to licence terms.
#
#  NOTICE: All information contained herein is, and remains the
#  property of DiffusionData. The intellectual and technical
#  concepts contained herein are proprietary to DiffusionData and
#  may be covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law.

"""Stream handlers for topics."""
from __future__ import annotations

import typing_extensions

import typing
import warnings

from typing_extensions import Annotated, Doc, Unpack

from typing import Type

import structlog

if typing.TYPE_CHECKING:
    from diffusion.datatypes import DataType, AbstractDataType
    from diffusion.datatypes.foundation.abstract import Converter, A_T, A_T_Target
from diffusion.handlers import EventStreamHandler, SubHandlerProtocol, \
    UnsubscribeProtocol, UpdateProtocol, AT_T_contra, AT_T_co, Callback_RT

LOG = structlog.get_logger()

"""
[diffusion.handlers.SubHandlerProtocol][] or subclass.
"""

class SubHandlerValues(
    typing_extensions.TypedDict, typing.Generic[AT_T_contra, Callback_RT],
    total=False
):
    """
    Handlers that can be passed into the
    [ValueStreamHandler][diffusion.features.topics.streams.ValueStreamHandler]
    """

    unsubscribe: Annotated[
        typing.Optional[UnsubscribeProtocol[AT_T_contra, Callback_RT]],
        Doc("An unsubscribe handler."),
    ]
    subscribe: Annotated[
        typing.Optional[SubHandlerProtocol[AT_T_contra, Callback_RT]],
        Doc("A subscribe handler."),
    ]
    update: Annotated[
        typing.Optional[UpdateProtocol[AT_T_contra, Callback_RT]], Doc("An update handler.")
    ]
    close: Annotated[
        typing.Optional[SubHandlerProtocol[AT_T_contra, Callback_RT]],
        Doc("A close handler." ""),
    ]


class ValueStreamHandler(EventStreamHandler[AT_T_co, Callback_RT]):
    """Stream handler implementation for the value streams of the given type."""

    def __init__(
        self,
        data_type: Annotated[
            Type[AT_T_co],
            Doc("the data type associated with this handler"),
        ],
        **kwargs: Unpack[SubHandlerValues[AT_T_co, Callback_RT]],
    ) -> None:
        """
        Initialise the
        [ValueStreamHandler][diffusion.features.topics.streams.ValueStreamHandler]

        Args:
            data_type: the data type associated with this handler
            **kwargs: as documented in "Other Parameters."
        """

        unexpected = set(kwargs) - set(SubHandlerValues.__annotations__)
        if unexpected:
            warnings.warn(f"Unexpected keyword arguments: {unexpected}")
        self.type: typing.Type[AT_T_co] = data_type
        self.converter_map = {
            typing.cast(typing.Type["DataType"], self.type): typing.cast(
                ValueStreamHandler["AbstractDataType", typing.Any], self
            )
        }
        super().__init__(**kwargs)  # type: ignore[arg-type]

    def __str__(self):
        return f"{super().__str__()} with type {self.type}"

    converter_map: typing.Dict[
        typing.Type[DataType], "ValueStreamHandler[AbstractDataType, typing.Any]"
    ]


    def get_converter(self, source_type: typing.Type[A_T]):
        existing_converter = self.converter_map.get(source_type)
        if existing_converter:
            return existing_converter
        converter: typing.Optional[Converter[A_T, typing.Any]] = (
            source_type.converter_to(self.type)
        )
        if converter:
            existing_converter = ConversionHandler(source_type, converter, self)
            self.converter_map[source_type] = existing_converter
            return existing_converter
        return None


class ConversionHandler(ValueStreamHandler):
    def __init__(
        self,
        public_type: typing.Type[AbstractDataType],
        converter: Converter[A_T, A_T_Target],
        delegate: ValueStreamHandler[A_T_Target, typing.Any],
    ):
        self.converter = converter
        self.delegate = delegate
        super().__init__(public_type)

    async def handle(self, event: str, **kwargs) -> typing.Any:
        converted_kwargs = {**kwargs}
        for k in {"topic_value", "old_value"} & kwargs.keys():
            try:
                converted = self.converter(kwargs[k])
                LOG.debug(f"Converted {k}:{kwargs[k]}->{self.converter}->{converted}")
                converted_kwargs.update({k: converted})
            except Exception as e:
                LOG.error(e)
                raise
        try:
            return await self.delegate.handle(event, **converted_kwargs)
        except Exception as e:
            LOG.exception(f"Failed processing ConversionHandler event {self}", exc_info=e)
            raise e

    def __str__(self):
        return f"ConversionHandler: {self.type}->{self.type}->{self.converter}->{self.delegate}"
